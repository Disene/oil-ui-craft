/* Independently authored effects. No request, tracking, model or shader-library dependency. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id), reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const dots = $('dots'), shader = $('shader'), button = $('motionToggle');
  const ctx = dots.getContext('2d'); let gl = null, program = null, buffer = null, raf = 0, time = 0, last = 0, paused = false, lost = false;
  const visible = new Map([...document.querySelectorAll('[data-effect]')].map(e => [e, true]));
  function dimensions(canvas) { const r = canvas.getBoundingClientRect(), d = Math.min(devicePixelRatio || 1, 2); const w = Math.max(1, Math.round(r.width*d)), h = Math.max(1, Math.round(r.height*d)); if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; } return [w,h]; }
  function destroyGL() { if (gl && !lost) { if (buffer) gl.deleteBuffer(buffer); if (program) gl.deleteProgram(program); } buffer = null; program = null; }
  function setupGL() {
    try {
      gl = shader.getContext('webgl', { alpha:false, antialias:false, preserveDrawingBuffer:true });
      if (!gl) throw Error('unavailable');
      const compile = (type, source) => { const s=gl.createShader(type); gl.shaderSource(s,source); gl.compileShader(s); if (!gl.getShaderParameter(s,gl.COMPILE_STATUS)) { gl.deleteShader(s); throw Error('compile'); } return s; };
      const vs=compile(gl.VERTEX_SHADER,'attribute vec2 position;void main(){gl_Position=vec4(position,0.,1.);}');
      const fs=compile(gl.FRAGMENT_SHADER,`precision mediump float;uniform vec2 resolution;uniform float time;void main(){vec2 p=gl_FragCoord.xy/resolution;float a=sin(p.x*4.8+time*.27+sin(p.y*4.0-time*.19));float b=cos(p.y*5.1-time*.21+p.x*2.);float m=.5+.5*sin(a+b+time*.12);vec3 dark=vec3(.07,.18,.23);vec3 teal=vec3(.20,.47,.43);vec3 violet=vec3(.42,.31,.55);vec3 c=mix(dark,teal,smoothstep(-1.,1.,a));c=mix(c,violet,m*.7);gl_FragColor=vec4(c,1.);}`);
      program=gl.createProgram();gl.attachShader(program,vs);gl.attachShader(program,fs);gl.linkProgram(program);gl.deleteShader(vs);gl.deleteShader(fs);
      if(!gl.getProgramParameter(program,gl.LINK_STATUS)) throw Error('link');
      gl.useProgram(program);buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]),gl.STATIC_DRAW);
      const attr=gl.getAttribLocation(program,'position');gl.enableVertexAttribArray(attr);gl.vertexAttribPointer(attr,2,gl.FLOAT,false,0,0);
      shader.hidden=false;shader.dataset.renderer='webgl';$('shaderStatus').textContent='WebGL 片元着色器已启用';lost=false;
    } catch (_) { destroyGL(); gl=null;shader.hidden=true;shader.dataset.renderer='css-fallback';$('shaderStatus').textContent='WebGL 不可用，已显示静态 CSS 渐变'; }
  }
  function draw() {
    if(ctx && visible.get(dots.parentElement)) {
      const [w,h]=dimensions(dots);ctx.clearRect(0,0,w,h);const gap=28*Math.min(devicePixelRatio||1,2);
      for(let y=gap;y<h;y+=gap) for(let x=gap;x<w;x+=gap){ const wave=.5+.5*Math.sin(x/w*9+y/h*6-time*.9);ctx.beginPath();ctx.fillStyle=`rgba(143,211,203,${.18+wave*.65})`;ctx.arc(x,y,1.4+wave*2.3,0,Math.PI*2);ctx.fill(); }
    }
    if(gl && program && !lost && visible.get(shader.parentElement)) {const [w,h]=dimensions(shader);gl.viewport(0,0,w,h);gl.useProgram(program);gl.uniform2f(gl.getUniformLocation(program,'resolution'),w,h);gl.uniform1f(gl.getUniformLocation(program,'time'),time);gl.drawArrays(gl.TRIANGLES,0,6);}
  }
  function shouldRun(){return !paused&&!reduce.matches&&!document.hidden&&[...visible.values()].some(Boolean);}
  function tick(now){raf=0;if(!shouldRun())return;time+=last?Math.min((now-last)/1000,.05):0;last=now;draw();raf=requestAnimationFrame(tick);}
  function sync(){cancelAnimationFrame(raf);raf=0;last=0;const running=shouldRun();document.body.dataset.paused=String(!running);document.body.dataset.running=String(running);button.disabled=reduce.matches;button.setAttribute('aria-pressed',String(paused));button.textContent=paused?'继续动效':'暂停动效';$('motionStatus').textContent=reduce.matches?'系统已启用减少动态效果，显示静态画面。':paused?'动效已暂停。':document.hidden?'页面不可见，绘制已暂停。':'动效运行中；离开视野后自动暂停。';draw();if(running)raf=requestAnimationFrame(tick);}
  button.addEventListener('click',()=>{paused=!paused;sync();});reduce.addEventListener('change',sync);document.addEventListener('visibilitychange',sync);
  shader.addEventListener('webglcontextlost',e=>{e.preventDefault();lost=true;program=null;buffer=null;shader.hidden=true;shader.dataset.renderer='css-fallback';$('shaderStatus').textContent='WebGL 上下文丢失，已切换为静态背景';});
  shader.addEventListener('webglcontextrestored',()=>{setupGL();sync();});
  if(typeof IntersectionObserver==='function')new IntersectionObserver(entries=>{for(const e of entries){visible.set(e.target,e.isIntersecting);e.target.dataset.offscreen=String(!e.isIntersecting);}sync();},{threshold:0}).observe(document.querySelector('[data-effect="beam"]'));
  // Observe canvases separately; no frames are rendered when all effects leave the viewport.
  if(typeof IntersectionObserver==='function'){const observer=new IntersectionObserver(entries=>{for(const e of entries)visible.set(e.target,e.isIntersecting);sync();});observer.observe(dots.parentElement);observer.observe(shader.parentElement);}
  new ResizeObserver(()=>{draw();}).observe(document.querySelector('.effects'));
  window.addEventListener('pagehide',()=>{cancelAnimationFrame(raf);raf=0;});
  setupGL();sync();
})();
