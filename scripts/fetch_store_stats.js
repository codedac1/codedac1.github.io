// =====================================================================
//  Google Play 스토어 지표 수집 → scripts/store_stats.json 캐시
//  - apps_base.json 의 store 링크가 있는 앱만 조회
//  - 평점(score)·평점수(ratings)·설치수(minInstalls)를 저장
//  - 결과는 정적 데이터로 커밋되며, gen_site.js 가 빌드 시 읽어 렌더한다.
//  사용: node scripts/fetch_store_stats.js
//  ※ google-play-scraper 는 devDependency (사이트 배포물에는 포함되지 않음)
// =====================================================================
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const APPS = require('./apps_base.json');
const OUT = path.join(__dirname, 'store_stats.json');

// 지표 기준 스토어(집계 일관성). 필요시 변경.
const LANG = 'en';
const COUNTRY = 'us';

const appIdOf = (store) => (store && store.includes('id=')) ? store.split('id=')[1].split('&')[0] : null;

(async () => {
  const gplayMod = await import('google-play-scraper');
  const gplay = gplayMod.default || gplayMod;

  const apps = {};
  for (const app of APPS) {
    const id = appIdOf(app.store);
    if (!id) continue;
    try {
      const d = await gplay.app({ appId: id, lang: LANG, country: COUNTRY });
      apps[app.slug] = {
        appId: id,
        score: d.score != null ? +d.score.toFixed(2) : null,
        ratings: d.ratings || 0,
        installs: d.installs || null,
        minInstalls: d.minInstalls || 0,
      };
      console.log(`✓ ${app.slug}  ★${apps[app.slug].score ?? '-'}  (${apps[app.slug].ratings} ratings)  ${apps[app.slug].installs}`);
    } catch (e) {
      console.warn(`✗ ${app.slug} (${id}): ${e.message}`);
    }
  }

  const list = Object.values(apps);
  const rated = list.filter((a) => a.score != null && a.ratings > 0);
  const totalMinInstalls = list.reduce((s, a) => s + (a.minInstalls || 0), 0);
  const totalRatings = rated.reduce((s, a) => s + a.ratings, 0);
  const avgScore = totalRatings ? +(rated.reduce((s, a) => s + a.score * a.ratings, 0) / totalRatings).toFixed(2) : null;

  // 날짜는 스크립트 실행 환경 기준으로 스탬프(생성기에서는 Date 사용 안 함)
  const out = {
    generatedAt: new Date().toISOString().slice(0, 10),
    source: { lang: LANG, country: COUNTRY },
    aggregate: { publishedApps: list.length, totalMinInstalls, totalRatings, avgScore },
    apps,
  };
  fs.writeFileSync(OUT, JSON.stringify(out, null, 2) + '\n');
  console.log(`\n저장: scripts/store_stats.json  | 앱 ${list.length}개 · 최소설치 합계 ${totalMinInstalls.toLocaleString('en-US')} · 총 평점 ${totalRatings} · 평균 ★${avgScore}`);
})();
