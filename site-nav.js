(()=>{
 const here=location.pathname.split('/').slice(-2,-1)[0], prefix=here==='mchtml'?'../':'';
 const current=decodeURIComponent(location.pathname.split('/').pop())||'index.html';
 const people=[["James Pinckney McNabb", "1814–1893"], ["Walter Scott McNabb", "1874–1936"], ["Warren Gilbert McNabb", "1898–1975"], ["Ruth Pauline Prutsman", "1906–1997"], ["Beverly Nan McNabb", "1932–2025"], ["Warren Neil McNabb", "1934–2025"]];
 const menu=people.map(([name,dates])=>`<a href="${prefix}mchtml/${encodeURIComponent(name)}.html"><span class="person-name">${name}</span><small>${dates}</small></a>`).join('');
 const nav=`<nav aria-label="Main navigation"><div class="site-nav-inner"><a href="${prefix}index.html" ${current==='index.html'?'aria-current="page"':''}>Home</a><a href="${prefix}mchtml/McNabb%20Tree.html" ${current==='McNabb Tree.html'?'aria-current="page"':''}>Family Tree</a><details class="bio-dropdown"><summary>Biographies</summary><div class="bio-menu">${menu}</div></details><a href="${prefix}research.html">Craig’s Research</a><a href="${prefix}about-archive.html">About</a><a href="${prefix}McNabb_Family_Archive_Complete.pdf">Download Book</a></div></nav>`;
 const mount=document.getElementById('site-nav');if(mount){mount.innerHTML=nav;const syncNav=()=>document.documentElement.style.setProperty('--archive-nav-height',mount.getBoundingClientRect().height+'px');syncNav();window.addEventListener('resize',syncNav);}
 document.addEventListener('click',e=>{for(const item of document.querySelectorAll('#site-nav details[open]')){if(!item.contains(e.target))item.open=false}});
 document.addEventListener('keydown',e=>{if(e.key==='Escape')document.querySelectorAll('#site-nav details[open]').forEach(el=>el.open=false)});
})();