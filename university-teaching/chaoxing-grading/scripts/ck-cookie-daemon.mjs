#!/usr/bin/env node
// ck-cookie-daemon.mjs — 超星批改用 cookie 常驻服务（属于 chaoxing-grading，不碰 web-access）
//
// 背景：新版 Chrome 对每条新建的 CDP 调试 WebSocket 连接都会弹一次「远程调试授权」窗。
// cdp-proxy（web-access）只建一条长连接所以只弹一次；但 fetch-images.mjs 原先每次运行
// 都直连浏览器新建连接，并行批改时每名学生弹一次窗。本守护进程持有唯一一条长连接，
// 授权窗只在它首次启动（或浏览器重启后重连）时弹一次，之后所有取 cookie 的调用零弹窗。
//
// 接口：
//   GET http://127.0.0.1:39217/health              → {ok, service:"ck-cookie-daemon", connected}
//   GET http://127.0.0.1:39217/cookies?domain=x.y  → {cookies:[{name,value,domain,...}]}
//
// 生命周期：由 fetch-images.mjs 检测到未运行时自动 detached 拉起；常驻后台。
// 手动停止：pkill -f ck-cookie-daemon（或任务管理器结束 node 进程）。
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import net from 'node:net';

const SERVICE = 'ck-cookie-daemon';
const PORT = parseInt(process.env.CHAOXING_COOKIE_PORT || '39217');

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

let ws = null;
let wsKey = ''; // "port|wsPath"，用于浏览器重启后换端口重连
let connecting = null;
let id = 0;
const pending = new Map(); // id -> {res, rej}

async function connect() {
  if (ws && ws.readyState === 1) return;
  if (connecting) return connecting;

  let target = null;
  for (const t of devToolsPorts()) {
    const key = `${t.port}|${t.wsPath}`;
    if (!wsKey || key === wsKey) { target = { ...t, key }; break; }
  }
  if (!target) target = { ...devToolsPorts()[0], key: null }; // 记住的端口失效则取第一个
  if (!target) throw new Error('未找到浏览器 CDP 调试端口（DevToolsActivePort）');

  connecting = new Promise((resolve, reject) => {
    const sock = new WebSocket(`ws://127.0.0.1:${target.port}${target.wsPath}`);
    const onOpen = () => {
      ws = sock; wsKey = target.key;
      connecting = null;
      console.log(`[ck-cookie-daemon] 已连接 ${target.label} 调试端口 ${target.port}（授权窗此时弹出一次）`);
      resolve();
    };
    const onErr = () => { connecting = null; reject(new Error(`连接 ${target.label}:${target.port} 失败`)); };
    const onClose = () => { ws = null; console.log('[ck-cookie-daemon] 连接断开，下次请求时重连'); };
    const onMsg = (e) => {
      const m = JSON.parse(typeof e.data === 'string' ? e.data : e.data.toString());
      if (m.id && pending.has(m.id)) {
        const p = pending.get(m.id); pending.delete(m.id);
        m.error ? p.rej(new Error(m.error.message)) : p.res(m.result);
      }
    };
    if (sock.on) { sock.on('open', onOpen); sock.on('error', onErr); sock.on('close', onClose); sock.on('message', onMsg); }
    else { sock.addEventListener('open', onOpen); sock.addEventListener('error', onErr); sock.addEventListener('close', onClose); sock.addEventListener('message', onMsg); }
  });
  return connecting;
}

function sendCDP(method, params = {}) {
  return new Promise((res, rej) => {
    const i = ++id; pending.set(i, { res, rej });
    ws.send(JSON.stringify({ id: i, method, params }));
  });
}

async function getCookies(domain) {
  await connect();
  const { cookies } = await sendCDP('Storage.getCookies', {});
  if (!domain) return cookies;
  const d = domain.replace(/^\./, '');
  return cookies.filter(c => c.domain === d || c.domain === '.' + d || c.domain.endsWith('.' + d));
}

function checkPortAvailable(port) {
  return new Promise((resolve) => {
    const s = net.createServer();
    s.once('error', () => resolve(false));
    s.once('listening', () => { s.close(); resolve(true); });
    s.listen(port, '127.0.0.1');
  });
}

async function main() {
  // 已有本服务实例在跑则直接退出（fetch-images 并发拉起时只有一个存活）。
  // 必须匹配 service 标识——端口被无关服务占用时不可误认为已有实例。
  if (!(await checkPortAvailable(PORT))) {
    try {
      const ok = await new Promise((resolve) => {
        http.get(`http://127.0.0.1:${PORT}/health`, { timeout: 2000 }, r => {
          let d = ''; r.on('data', c => d += c); r.on('end', () => resolve(d.includes(SERVICE)));
        }).on('error', () => resolve(false));
      });
      if (ok) { console.log('[ck-cookie-daemon] 已有实例，退出'); return; }
    } catch {}
    console.error(`[ck-cookie-daemon] 端口 ${PORT} 被其他程序占用，可用环境变量 CHAOXING_COOKIE_PORT 换端口`); process.exit(1);
  }

  http.createServer(async (req, res) => {
    const q = Object.fromEntries(new URL(req.url, 'http://x').searchParams);
    try {
      if (req.url.startsWith('/health')) {
        res.end(JSON.stringify({ ok: true, service: SERVICE, connected: !!(ws && ws.readyState === 1) }));
        return;
      }
      if (req.url.startsWith('/cookies')) {
        const cookies = await getCookies(q.domain);
        res.end(JSON.stringify({ cookies }));
        return;
      }
      res.statusCode = 404; res.end(JSON.stringify({ error: '未知端点' }));
    } catch (e) {
      res.statusCode = 500; res.end(JSON.stringify({ error: e.message }));
    }
  }).listen(PORT, '127.0.0.1', () => {
    console.log(`[ck-cookie-daemon] 运行在 http://127.0.0.1:${PORT}`);
    connect().catch(e => console.error('[ck-cookie-daemon] 初始连接失败（将在首次请求时重试）:', e.message));
  });
}

process.on('uncaughtException', e => console.error('[ck-cookie-daemon] 未捕获异常:', e.message));
process.on('unhandledRejection', e => console.error('[ck-cookie-daemon] 未处理拒绝:', e?.message || e));
main();
