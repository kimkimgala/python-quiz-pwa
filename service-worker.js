const CACHE_NAME='python-quiz-pwa-v1-11-icon2';
const APP_FILES=['./','./index.html','./course-builder.html','./manifest.json','./catalog.json','./questions.json','./courses/cassette-demo.json','./app-icon-card-check-192-v2.png','./app-icon-card-check-512-v2.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE_NAME).then(c=>c.addAll(APP_FILES)));self.skipWaiting();});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE_NAME).map(k=>caches.delete(k)))));self.clients.claim();});
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  if(e.request.mode==='navigate'){
    e.respondWith(fetch(e.request).then(r=>{if(r.ok){const copy=r.clone();caches.open(CACHE_NAME).then(c=>c.put(e.request,copy));}return r;}).catch(()=>caches.match(e.request).then(x=>x||caches.match('./index.html'))));
    return;
  }
  const u=new URL(e.request.url);
  if(e.request.mode==='navigate'||(u.origin===location.origin&&u.pathname.endsWith('.html'))){e.respondWith(fetch(e.request).then(r=>{if(r.ok){const copy=r.clone();caches.open(CACHE_NAME).then(c=>c.put(e.request,copy));}return r}).catch(()=>caches.match(e.request).then(x=>x||caches.match('./index.html'))));return;}
  if(u.origin===location.origin&&u.pathname.endsWith('.json')){
    e.respondWith(fetch(e.request).then(r=>{
      if(r.ok){const copy=r.clone();caches.open(CACHE_NAME).then(c=>c.put(e.request,copy));}
      return r;
    }).catch(()=>caches.match(e.request)));
    return;
  }
  e.respondWith(caches.match(e.request).then(cached=>cached||fetch(e.request).then(r=>{
    if(r.ok){const copy=r.clone();caches.open(CACHE_NAME).then(c=>c.put(e.request,copy));}
    return r;
  }).catch(()=>caches.match('./index.html'))));
});
