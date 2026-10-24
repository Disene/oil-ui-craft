/* Local memory game: explicit lifecycle, keyboard access, pause/resume and no persistence. */
(() => {
  'use strict';const $=id=>document.getElementById(id);
  const plants=[['○','月桂'],['△','松枝'],['◇','银杏'],['□','竹叶'],['✳','蕨叶'],['✦','苔花']];
  let deck=[],matched=new Set(),flips=[],moves=0,limit=18,state='ready',timer=0,due=0,remaining=600,opener=null;
  function shuffled(){const d=[0,0,1,1,2,2,3,3,4,4,5,5];for(let i=d.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[d[i],d[j]]=[d[j],d[i]];}return d;}
  function clearTimer(){clearTimeout(timer);timer=0;}
  function finish(){if(matched.size===12){state='won';$('outcome').textContent='六组植物全部找到，你完成了这一局。';}else if(moves>=limit){state='lost';$('outcome').textContent='步数已用完。可以重新开始，试着记住更多位置。';}if(state==='won'||state==='lost'){clearTimer();render();$('outcome').focus({preventScroll:true});}}
  function settle(){clearTimer();flips=[];remaining=600;if(state==='playing'){finish();render();}}
  function schedule(ms){remaining=ms;due=performance.now()+ms;timer=setTimeout(settle,ms);}
  function render(){
    document.body.dataset.state=state;$('moves').textContent=moves+' / '+limit;$('pairs').textContent=(matched.size/2)+' / 6';
    const cover=state==='ready'||state==='paused';$('cover').hidden=!cover;$('board').inert=cover;
    $('coverTitle').textContent=state==='paused'?'庭院已暂停':'准备进入庭院';$('coverText').textContent=state==='paused'?'点击“继续”回到刚才的位置。':'选择挑战步数，然后开始。';
    $('pause').disabled=!['playing','paused'].includes(state);$('pause').textContent=state==='paused'?'继续':'暂停';$('restart').disabled=state==='ready';$('difficulty').disabled=state==='playing'||state==='paused';$('start').disabled=state==='playing'||state==='paused';
    $('start').hidden=state!=='ready';$('restart').hidden=state==='ready';$('restart').classList.toggle('primary',state==='won'||state==='lost');
    [...$('board').children].forEach((b,i)=>{const face=matched.has(i)||flips.includes(i),value=plants[deck[i]];b.dataset.matched=String(matched.has(i));b.setAttribute('aria-pressed',String(face));b.setAttribute('aria-label','第 '+(i+1)+' 张：'+(face?value[1]:'未翻开'));b.disabled=state!=='playing'||matched.has(i)||flips.includes(i)||flips.length===2;b.querySelector('.symbol').textContent=face?value[0]:'·';b.querySelector('small').textContent=face?value[1]:String(i+1).padStart(2,'0');});
  }
  function build(){const fragment=document.createDocumentFragment();deck.forEach((value,i)=>{const b=document.createElement('button');b.type='button';b.className='tile';b.dataset.index=i;b.dataset.pair=value;b.innerHTML='<span class="symbol" aria-hidden="true">·</span><small aria-hidden="true"></small>';b.addEventListener('click',()=>flip(i));fragment.append(b);});$('board').replaceChildren(fragment);}
  function start(){clearTimer();deck=shuffled();matched=new Set();flips=[];moves=0;limit=Number($('difficulty').value);remaining=600;state='playing';build();$('outcome').textContent='游戏进行中：找出六组相同植物。';render();$('board').querySelector('button').focus({preventScroll:true});}
  function flip(i){if(state!=='playing'||matched.has(i)||flips.includes(i)||flips.length>=2)return;flips.push(i);if(flips.length===2){moves++;if(deck[flips[0]]===deck[flips[1]]){flips.forEach(x=>matched.add(x));flips=[];finish();}else schedule(600);}render();}
  function pause(){if(state!=='playing')return;if(timer){remaining=Math.max(0,due-performance.now());clearTimer();}state='paused';$('outcome').textContent='已暂停，原局保留。';render();}
  function resume(){if(state!=='paused')return;state='playing';$('outcome').textContent='已继续当前一局。';render();if(flips.length===2)schedule(remaining);}
  $('start').addEventListener('click',start);$('restart').addEventListener('click',start);$('pause').addEventListener('click',()=>state==='paused'?resume():pause());
  $('difficulty').addEventListener('change',()=>{if(state==='ready'){limit=Number($('difficulty').value);render();}});
  $('board').addEventListener('keydown',e=>{const change={ArrowRight:1,ArrowLeft:-1,ArrowDown:4,ArrowUp:-4}[e.key];if(!change||state!=='playing')return;e.preventDefault();const buttons=[...$('board').children];let i=buttons.indexOf(document.activeElement);for(let n=0;n<buttons.length;n++){i=(i+change+buttons.length)%buttons.length;if(!buttons[i].disabled){buttons[i].focus();break;}}});
  $('help').addEventListener('click',e=>{opener=e.currentTarget;pause();$('rules').showModal();$('closeRules').focus();});$('closeRules').addEventListener('click',()=>$('rules').close());$('rules').addEventListener('close',()=>opener?.focus());
  document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});window.addEventListener('pagehide',clearTimer);
  deck=shuffled();build();render();
})();
