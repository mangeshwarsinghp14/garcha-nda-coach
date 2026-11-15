/* Garcha NDA Coach service worker. Bump VERSION when index.html changes. */
const VERSION="v1";const SHELL="nda-shell-"+VERSION,DATA="nda-data";
const FILES=["./","index.html","manifest.webmanifest","icons/icon-192.png","icons/icon-512.png"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(SHELL).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting()))});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k.startsWith("nda-shell-")&&k!==SHELL).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener("fetch",e=>{const r=e.request;if(r.method!=="GET")return;const u=new URL(r.url);if(u.origin!==location.origin)return;
 if(u.pathname.includes("/data/")){e.respondWith(fetch(r).then(x=>{const cp=x.clone();caches.open(DATA).then(c=>c.put(r,cp));return x}).catch(()=>caches.match(r)));return}
 e.respondWith(caches.match(r).then(m=>{const net=fetch(r).then(x=>{if(x.ok){const cp=x.clone();caches.open(SHELL).then(c=>c.put(r,cp))}return x}).catch(()=>m);return m||net}))});
