// =====================================================================
//  스토어 지표 수집 → scripts/store_stats.json 캐시
//  - apps_base.json 의 store 링크가 있는 앱만 조회 (Google Play + Microsoft Store)
//  - 평점(score)·평점수(ratings)·설치수(minInstalls)를 저장
//  - 결과는 정적 데이터로 커밋되며, gen_site.js 가 빌드 시 읽어 렌더한다.
//  사용: node scripts/fetch_store_stats.js
//  ※ google-play-scraper 는 devDependency (사이트 배포물에는 포함되지 않음)
//
//  스토어별 설치수 출처가 다르다:
//   · Google Play  — 스크레이퍼가 '10,000+' 구간을 주므로 하한값(minInstalls)을 쓴다.
//   · Microsoft Store — 공개 API(DisplayCatalog)가 평점만 주고 획득 수는 노출하지 않아,
//     ms_installs.json 에 손으로 적어 둔 Partner Center 실수치를 읽어 쓴다.
// =====================================================================
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const APPS = require('./apps_base.json');
const OUT = path.join(__dirname, 'store_stats.json');

// 지표 기준 스토어(집계 일관성). 필요시 변경.
const LANG = 'en';
const COUNTRY = 'us';

// Microsoft Store 설치수 수동 입력값 (없으면 0으로 간주 — 평점만 수집)
let MS_INSTALLS = {};
let MS_UPDATED_AT = '';
try {
  const ms = require('./ms_installs.json');
  MS_INSTALLS = ms.installs || {};
  MS_UPDATED_AT = ms.updatedAt || '';
} catch {
  console.warn('(경고) scripts/ms_installs.json 없음 — Microsoft Store 설치수 0으로 집계.');
}

const playIdOf = (store) => (store && store.includes('id=')) ? store.split('id=')[1].split('&')[0] : null;
// https://apps.microsoft.com/detail/9N9SRKQV1R6D?hl=ko-kr → 9N9SRKQV1R6D
const msIdOf = (store) => {
  const m = /apps\.microsoft\.com\/detail\/([A-Za-z0-9]+)/.exec(store || '');
  return m ? m[1] : null;
};

// Microsoft Store 공개 카탈로그. 평점/평점수만 신뢰할 수 있고 설치수는 제공되지 않는다.
async function fetchMsProduct(productId) {
  const url = `https://displaycatalog.mp.microsoft.com/v7.0/products/${productId}`
    + `?market=${COUNTRY.toUpperCase()}&languages=${LANG}-${COUNTRY}`;
  const res = await fetch(url, { headers: { 'MS-CV': 'codedac.stats.1' } });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const data = await res.json();
  const usage = ((data.Product || {}).MarketProperties || [])[0] || {};
  const all = (usage.UsageData || []).find((u) => u.AggregateTimeSpan === 'AllTime') || {};
  const ratings = all.RatingCount || 0;
  const score = ratings > 0 && all.AverageRating ? +Number(all.AverageRating).toFixed(2) : null;
  return { score, ratings };
}

(async () => {
  const gplayMod = await import('google-play-scraper');
  const gplay = gplayMod.default || gplayMod;

  const apps = {};
  for (const app of APPS) {
    const playId = playIdOf(app.store);
    const msId = playId ? null : msIdOf(app.store);

    if (playId) {
      try {
        const d = await gplay.app({ appId: playId, lang: LANG, country: COUNTRY });
        apps[app.slug] = {
          store: 'play',
          appId: playId,
          score: d.score != null ? +d.score.toFixed(2) : null,
          ratings: d.ratings || 0,
          installs: d.installs || null,
          minInstalls: d.minInstalls || 0,
        };
        console.log(`✓ ${app.slug}  ★${apps[app.slug].score ?? '-'}  (${apps[app.slug].ratings} ratings)  ${apps[app.slug].installs}`);
      } catch (e) {
        console.warn(`✗ ${app.slug} (${playId}): ${e.message}`);
      }
    } else if (msId) {
      try {
        const { score, ratings } = await fetchMsProduct(msId);
        // Partner Center 실수치. 구간이 아니라 정확한 값이므로 installs 표기도 동일한 수를 쓴다.
        const installs = MS_INSTALLS[app.slug] || 0;
        apps[app.slug] = {
          store: 'msstore',
          appId: msId,
          score,
          ratings,
          installs: installs ? installs.toLocaleString('en-US') : null,
          minInstalls: installs,
        };
        console.log(`✓ ${app.slug}  ★${score ?? '-'}  (${ratings} ratings)  ${installs ? installs.toLocaleString('en-US') : '설치수 미입력'}`);
      } catch (e) {
        console.warn(`✗ ${app.slug} (${msId}): ${e.message}`);
      }
    }
  }

  const list = Object.values(apps);
  const rated = list.filter((a) => a.score != null && a.ratings > 0);
  const totalMinInstalls = list.reduce((s, a) => s + (a.minInstalls || 0), 0);
  const totalRatings = rated.reduce((s, a) => s + a.ratings, 0);
  const avgScore = totalRatings ? +(rated.reduce((s, a) => s + a.score * a.ratings, 0) / totalRatings).toFixed(2) : null;
  const msList = list.filter((a) => a.store === 'msstore');
  const msInstalls = msList.reduce((s, a) => s + (a.minInstalls || 0), 0);

  // 날짜는 스크립트 실행 환경 기준으로 스탬프(생성기에서는 Date 사용 안 함)
  const out = {
    generatedAt: new Date().toISOString().slice(0, 10),
    source: { lang: LANG, country: COUNTRY },
    aggregate: {
      publishedApps: list.length,
      totalMinInstalls,
      totalRatings,
      avgScore,
      // 스토어별 내역 — 합계가 어디서 왔는지 추적용
      byStore: {
        play: totalMinInstalls - msInstalls,
        msstore: msInstalls,
      },
    },
    // Microsoft Store 설치수는 수동 입력이라, 언제 적은 값인지 함께 남긴다.
    msInstallsUpdatedAt: MS_UPDATED_AT || null,
    apps,
  };
  fs.writeFileSync(OUT, JSON.stringify(out, null, 2) + '\n');
  console.log(`\n저장: scripts/store_stats.json  | 앱 ${list.length}개 · 설치 합계 ${totalMinInstalls.toLocaleString('en-US')}`
    + ` (Play ${(totalMinInstalls - msInstalls).toLocaleString('en-US')} + MS Store ${msInstalls.toLocaleString('en-US')})`
    + ` · 총 평점 ${totalRatings} · 평균 ★${avgScore}`);
  if (msList.length && !msInstalls) {
    console.warn('(주의) Microsoft Store 설치수가 모두 0 — scripts/ms_installs.json 에 Partner Center 수치를 적어야 합계에 반영됩니다.');
  }
})();
