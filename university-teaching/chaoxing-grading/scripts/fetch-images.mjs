#!/usr/bin/env node
// 用法: node fetch-images.mjs <url1> [url2 ...] [--out <dir>]
// 并行直下超星作业截图（绕过 tab navigate + screenshot，快约 50 倍且为原图分辨率）。
// 认证策略（2026-09-12 实测）:
//   - *.chaoxing.com 图床(ananas): 需浏览器 cookie（经 CDP Storage.getCookies 获取，含 HttpOnly）+ 浏览器 UA，302 跟随
//   - p.cldisk.com 图床: 浏览器无该域 cookie，带 UA + Referer 即可
// 输出: JSON 数组 [{url, file, bytes}]；失败项带 error。任一失败退出码 1。
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36';
const args = process.argv.slice(2);
const outIdx = args.indexOf('--out');
const outDir = outIdx >= 0 ? args[outIdx + 1] : path.join(os.tmpdir(), 'chaoxing_imgs');
const urls = args.filter((a, i) => a && !a.startsWith('--') && (outIdx < 0 || i !== outIdx + 1));
if (!urls.length) { console.error('用法: node fetch-images.mjs <url...> [--out <dir>]'); process.exit(2); }
fs.mkdirSync(outDir, { recursive: true });

// --- 端口发现: 复用 web-access 的浏览器发现逻辑（Chrome 优先，Edge 兜底） ---
function devToolsPorts() {
  const local = process.env.LOCALAPPDATA;
  const candidates = [
    [path.join(local, 'Google/Chrome/User Data/DevToolsActivePort'), 'chrome'],
    [path.join(local, 'Microsoft Edge/DevToolsActivePort'), 'edge'],
  ];
  const ports = [];
  for (const [f, label] of candidates) {
    try {
      const [port, wsPath] = fs.readFileSync(f, 'utf8').split('\n').map(s => s.trim());
      if (port && wsPath) ports.push({ port: +port, wsPath, label });
    } catch {}
  }
  return ports;
}

async function getCookieHeader() {
  for (const { port, wsPath } of devToolsPorts()) {
    try {
      const ws = new WebSocket(`ws://127.0.0.1:${port}${wsPath}`);
      let id = 0; const pending = new Map();
      ws.onmessage = e => {
        const m = JSON.parse(e.data);
        if (m.id && pending.has(m.id)) {
          const p = pending.get(m.id); pending.delete(m.id);
          m.error ? p.rej(new Error(m.error.message)) : p.res(m.result);
        }
      };
      await new Promise((r, j) => { ws.onopen = r; ws.onerror = () => j(new Error('ws connect fail')); });
      const send = (method, params = {}) => new Promise((res, rej) => {
        const i = ++id; pending.set(i, { res, rej });
        ws.send(JSON.stringify({ id: i, method, params }));
      });
      const { cookies } = await send('Storage.getCookies', {});
      ws.close();
      return cookies
        .filter(c => c.domain === 'chaoxing.com' || c.domain === '.chaoxing.com' || c.domain.endsWith('.chaoxing.com'))
        .map(c => `${c.name}=${c.value}`).join('; ');
    } catch {}
  }
  throw new Error('未找到浏览器 CDP 调试端口（DevToolsActivePort），请确认浏览器已开启远程调试');
}

async function download(url, file, headers) {
  const r = await fetch(url, { headers, redirect: 'follow' });
  if (!r.ok) throw new Error(`HTTP ${r.status}`);
  const buf = Buffer.from(await r.arrayBuffer());
  fs.writeFileSync(file, buf);
  return buf.length;
}

const chaoxingCookie = await getCookieHeader().catch(e => { console.error(e.message); process.exit(1); });
fs.rmSync(path.join(outDir, '.keep'), { force: true }); // no-op, keep dir fresh-friendly

const results = await Promise.all(urls.map(async (url, i) => {
  const host = new URL(url).hostname;
  const headers = { 'User-Agent': UA, 'Referer': 'https://mooc2-ans.chaoxing.com/' };
  if (host.endsWith('chaoxing.com')) headers['Cookie'] = chaoxingCookie;
  const base = path.basename(new URL(url).pathname) || `img${i + 1}.png`;
  const name = /^img\d+\./.test(base) ? base : `img${i + 1}_${base}`;
  const file = path.join(outDir, name.replace(/[?&=]/g, '_'));
  try {
    const bytes = await download(url, file, headers);
    return { url, file, bytes };
  } catch (e) {
    return { url, file, error: e.message };
  }
}));
console.log(JSON.stringify(results, null, 1));
process.exit(results.some(r => r.error) ? 1 : 0);
