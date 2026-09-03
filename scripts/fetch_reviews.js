// =====================================================================
//  Google Play 4★↑ 리뷰 후보 풀 수집 → scripts/_reviews_pool.json
//  - apps_base.json 의 store 링크가 있는 앱에서 평점 4점 이상·본문 있는 리뷰를 모은다.
//    (4★ 리뷰도 대개 '이것만 되면 5점' 형태라 쓸 만한 문장을 담고 있다. 별 개수는
//     score 로 그대로 넘어가 카드에 4개로 찍히므로, 5★ 인 척하지 않는다.)
//  - 이 파일은 "후보 풀"이며(.gitignore: scripts/_* 로 커밋 제외),
//    실제 노출 리뷰는 여기서 골라 scripts/reviews.json 에 손으로 큐레이션한다.
//    (후기는 편집 요소이므로 자동 선택하지 않고 사람이 고른다.)
//  사용: node scripts/fetch_reviews.js
// =====================================================================
const fs = require('fs');
const path = require('path');

const APPS = require('./apps_base.json');
const OUT = path.join(__dirname, '_reviews_pool.json');
const appIdOf = (store) => (store && store.includes('id=')) ? store.split('id=')[1].split('&')[0] : null;

// 리뷰는 국가별로 나뉘어 있어, 주요 마켓을 돌며 모아 중복 제거한다.
const MARKETS = [
  ['en', 'us'], ['en', 'gb'], ['en', 'ca'], ['en', 'au'], ['en', 'in'],
  ['ko', 'kr'], ['ja', 'jp'], ['de', 'de'], ['fr', 'fr'], ['es', 'es'],
  ['es', 'mx'], ['pt', 'br'], ['id', 'id'], ['vi', 'vn'], ['hi', 'in'],
  ['ru', 'ru'], ['tr', 'tr'],
];
const MIN_LEN = 60; // 너무 짧은 한 줄 리뷰 배제(최소 60자). 상한은 두지 않고 큐레이션에서 조정.

(async () => {
  const gplayMod = await import('google-play-scraper');
  const gplay = gplayMod.default || gplayMod;

  const pool = {};
  for (const app of APPS) {
    const id = appIdOf(app.store);
    if (!id) continue;
    const byId = new Map();
    for (const [lang, country] of MARKETS) {
      try {
        const r = await gplay.reviews({ appId: id, sort: gplay.sort.NEWEST, num: 100, lang, country });
        for (const x of (r.data || [])) {
          if (!(x.score >= 4)) continue;
          const text = (x.text || '').replace(/\s+/g, ' ').trim();
          if (text.length < MIN_LEN) continue;
          const key = x.id || (x.userName + '|' + text.slice(0, 40));
          if (byId.has(key)) continue;
          byId.set(key, { slug: app.slug, name: x.userName || '', score: x.score, len: text.length, market: country, text });
        }
      } catch { /* 해당 마켓 조회 실패는 건너뜀 */ }
    }
    const list = [...byId.values()].sort((a, b) => (b.score - a.score) || (b.len - a.len));
    if (list.length) pool[app.slug] = list;
    console.log(`✓ ${app.slug}: ${list.length} unique 4★↑ reviews (>=${MIN_LEN} chars)`);
  }
  fs.writeFileSync(OUT, JSON.stringify(pool, null, 2) + '\n');
  console.log(`\n저장(후보 풀): scripts/_reviews_pool.json — 여기서 골라 scripts/reviews.json 로 큐레이션하세요.`);
})();
