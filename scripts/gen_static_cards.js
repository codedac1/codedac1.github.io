// js/main.js의 APPS 배열에서 앱 소개 "정적 카드" HTML을 생성한다.
// 크롤러(특히 JS 미실행 봇)가 앱 목록을 읽을 수 있도록 index.html #appGrid 안에 넣는 용도.
// 사용: node scripts/gen_static_cards.js  → 출력된 HTML을 index.html #appGrid 내부에 교체.
const fs = require('fs');
const src = fs.readFileSync('js/main.js', 'utf8');
const start = src.indexOf('const APPS = [');
const end = src.indexOf('\n];', start) + 3;
const APPS = eval(src.slice(start + 'const APPS = '.length, end - 1));
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const cards = APPS.map((a) => {
  const store = a.store
    ? `\n            <a class="app-link" href="${a.store}" target="_blank" rel="noopener">Google Play에서 보기 →</a>`
    : '';
  return `        <article class="app-card">
          <div class="app-head">
            <img class="app-icon" src="images/icons/${a.slug}.png" alt="${esc(a.name)} 아이콘" loading="lazy" width="56" height="56" />
            <div class="app-meta"><h3>${esc(a.name)}</h3><span class="app-tag">${esc(a.tag.ko)}</span></div>
          </div>
          <p class="app-desc">${esc(a.desc.ko)}</p>${store}
        </article>`;
}).join('\n');
process.stdout.write(cards + '\n');
