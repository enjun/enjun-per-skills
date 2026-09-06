#!/usr/bin/env node
/**
 * 通过 CDP proxy 在已打开的文献页面上下文内 fetch PDF 并分块提取到本地。
 * 用法: node extract_pdf.js <targetId> <pdfUrl> <outputPath>
 * 要求: targetId 对应的 tab 已打开同域名的正常 HTML 页面（非 PDF 查看器），
 *       且该页面已有机构登录态。
 */
'use strict';

const PROXY = 'http://localhost:3456';
const CHUNK = 786432; // 768KB raw -> ~1MB base64 per request
const POLL_INTERVAL_MS = 2000;
const POLL_TIMEOUT_MS = 90000;
const EVAL_TIMEOUT_MS = 60000;

async function main() {
  const [targetId, pdfUrl, outputPath] = process.argv.slice(2);
  if (!targetId || !pdfUrl || !outputPath) {
    console.error('用法: node extract_pdf.js <targetId> <pdfUrl> <outputPath>');
    process.exit(2);
  }

  const evalUrl = `${PROXY}/eval?target=${targetId}`;

  async function evalJs(script) {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), EVAL_TIMEOUT_MS);
    let res;
    try {
      res = await fetch(evalUrl, {
        method: 'POST',
        body: script,
        signal: ctrl.signal,
      });
    } catch (e) {
      clearTimeout(timer);
      throw new Error(`proxy 请求失败: ${e.message}`);
    }
    clearTimeout(timer);
    const body = await res.text();
    let outer;
    try {
      outer = JSON.parse(body.slice(body.indexOf('{')));
    } catch {
      throw new Error(`proxy 响应非 JSON: ${body.slice(0, 200)}`);
    }
    if (outer.error) throw new Error(`eval 出错: ${outer.error}`);
    // proxy 返回 {"value":"<JS返回值>"}，JS 侧返回的是 JSON.stringify 的字符串
    return JSON.parse(outer.value);
  }

  // 1. 非阻塞启动 fetch（大文件同步等待会导致 CDP Runtime.evaluate 超时）
  await evalJs(`(function(){
    window.__pdfErr = null; window.__pdfBuf = null;
    window.__pdfP = fetch(${JSON.stringify(pdfUrl)}, {credentials: "include"})
      .then(r => {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.arrayBuffer();
      })
      .then(b => { window.__pdfBuf = b; return b.byteLength; })
      .catch(e => { window.__pdfErr = e.message; });
    return JSON.stringify({started: true});
  })()`);

  // 2. 轮询缓存就绪
  const deadline = Date.now() + POLL_TIMEOUT_MS;
  let size = 0;
  while (true) {
    await new Promise(r => setTimeout(r, POLL_INTERVAL_MS));
    const st = await evalJs(`JSON.stringify({
      buf: !!window.__pdfBuf,
      size: window.__pdfBuf ? window.__pdfBuf.byteLength : 0,
      err: window.__pdfErr || null
    })`);
    if (st.err) throw new Error(`页面内 fetch 失败: ${st.err}（检查是否登录态有效、URL 是否同域）`);
    if (st.buf) { size = st.size; break; }
    if (Date.now() > deadline) throw new Error('等待 PDF 缓存超时');
  }
  if (size < 10000) throw new Error(`响应过小(${size}B)，可能不是 PDF 正文（登录态失效或被拦截）`);

  // 3. 分块提取 base64
  const b64Parts = [];
  for (let start = 0; ; start += CHUNK) {
    const r = await evalJs(`(function(){
      const u8 = new Uint8Array(window.__pdfBuf);
      const CH = ${CHUNK};
      const start = ${start};
      if (start >= u8.length) return JSON.stringify({done: true, total: u8.length});
      const end = Math.min(start + CH, u8.length);
      const slice = u8.subarray(start, end);
      let bin = "";
      for (let i = 0; i < slice.length; i += 8192) {
        bin += String.fromCharCode.apply(null, slice.subarray(i, Math.min(i + 8192, slice.length)));
      }
      return JSON.stringify({start: start, end: end, b64: btoa(bin)});
    })()`);
    if (r.done) break;
    if (!r.b64) throw new Error(`分块 ${start} 未返回数据`);
    b64Parts.push(r.b64);
    process.stderr.write(`  提取进度: ${r.end}/${size}\n`);
  }

  // 4. 解码落盘
  const buf = Buffer.from(b64Parts.join(''), 'base64');
  const fs = require('fs');
  const path = require('path');
  fs.mkdirSync(path.dirname(path.resolve(outputPath)), { recursive: true });
  fs.writeFileSync(outputPath, buf);

  // 5. 完整性校验
  const magic = buf.subarray(0, 5).toString('latin1');
  const tail = buf.subarray(Math.max(0, buf.length - 1024)).toString('latin1');
  const okMagic = magic === '%PDF-';
  const okEof = tail.includes('%%EOF');
  if (!okMagic) throw new Error(`文件校验失败: 魔数为 ${magic}，不是 PDF`);

  // 6. 释放页面内存
  await evalJs(`(function(){ delete window.__pdfBuf; delete window.__pdfP; delete window.__pdfErr; return "{}"; })()`);

  console.log(JSON.stringify({
    ok: true,
    path: path.resolve(outputPath),
    bytes: buf.length,
    magicOk: okMagic,
    eofOk: okEof,
  }));
}

main().catch(e => {
  console.error(JSON.stringify({ ok: false, error: e.message }));
  process.exit(1);
});
