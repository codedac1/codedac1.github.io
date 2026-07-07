// =====================================================================
//  Google Play 5★ 리뷰 후보 풀 수집 → scripts/_reviews_pool.json
//  - apps_base.json 의 store 링크가 있는 앱에서 평점 5점·본문 있는 리뷰를 모은다.
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

(async () => {
  const gplayMod = await import('google-play-scraper');
  const gplay = gplayMod.default || gplayMod;

  const pool = {};
  for (const app of APPS) {
    const id = appIdOf(app.store);
    if (!id) continue;
    try {
      const r = await gplay.reviews({ appId: id, sort: gplay.sort.RATING, num: 100, lang: 'en', country: 'us' });
      const MIN_LEN = 60;  // 너무 짧은 한 줄 리뷰 배제(최소 60자)
      const MAX_LEN = 300;
      const five = (r.data || [])
        .map((x) => ({ slug: app.slug, name: x.userName || '', score: x.score, text: (x.text || '').replace(/\s+/g, ' ').trim() }))
        .filter((x) => x.score === 5 && x.text.length >= MIN_LEN && x.text.length <= MAX_LEN);
      if (five.length) pool[app.slug] = five;
      console.log(`✓ ${app.slug}: ${five.length} five-star reviews with text`);
    } catch (e) {
      console.warn(`✗ ${app.slug}: ${e.message}`);
    }
  }
  fs.writeFileSync(OUT, JSON.stringify(pool, null, 2) + '\n');
  console.log(`\n저장(후보 풀): scripts/_reviews_pool.json — 여기서 골라 scripts/reviews.json 로 큐레이션하세요.`);
})();
