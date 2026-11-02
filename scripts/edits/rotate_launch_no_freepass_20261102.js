// Rotate+ 출시(2026-11-02) 사이트 반영: 10-01 에 준비한 문구의 "광고 한 번으로 24시간 Free Pass" 를 뺀다.
// 10-24 원칙(사이트에 시간 제한·광고 패스 문구 금지, 무료/Pro 는 기능 차이로만)에 맞춘다 — 그 정리
// (no_time_limits_site_20261024.py)는 rotate 가 아직 main 에 없을 때라 빠졌다.
// long 끝 · features[5] 끝 · faq[2].a 끝을 언어별 표지에서 잘라 내고 끝맺음을 붙인다.
//     node scripts/edits/rotate_launch_no_freepass_20261102.js
const fs = require('fs');
const path = require('path');
const I18N = path.join(__dirname, '..', '..', 'i18n');

// [표지, 붙일 끝맺음]
const CUT = {
  ar: { L: ['، أو شاهد', '.'], F: [' — أو', ''], Q: [' تريد التجربة', ''] },
  de: { L: [' — oder du siehst', '.'], F: [' — oder eine Werbung', ''], Q: [' Erst ausprobieren?', ''] },
  en: { L: [' — or watch', '.'], F: [' — or one ad', ''], Q: [' Not ready to buy?', ''] },
  es: { L: [', o mira', '.'], F: [' — o un anuncio', ''], Q: [' ¿Quieres probar', ''] },
  fil: { L: [' — o manood', '.'], F: [' — o isang ad', ''], Q: [' Gusto mo munang', ''] },
  fr: { L: [' — ou regardez', '.'], F: [' — ou une publicité', ''], Q: [' Envie d', ''] },
  hi: { L: [' — या एक', '।'], F: [' — या एक', ''], Q: [' पहले आज़माना', ''] },
  id: { L: [' — atau tonton', '.'], F: [' — atau satu iklan', ''], Q: [' Ingin coba dulu', ''] },
  it: { L: [', oppure guarda', '.'], F: [' — oppure un annuncio', ''], Q: [' Vuoi provare', ''] },
  ja: { L: ['し、広告 1 本で', 'します。'], F: [' — 広告 1 本で', ''], Q: ['まず試したいなら', ''] },
  ko: { L: [' 광고 한 번으로', ''], F: [' — 광고 한 번으로', ''], Q: [' 먼저 써 보고', ''] },
  ms: { L: [' — atau tonton', '.'], F: [' — atau satu iklan', ''], Q: [' Mahu cuba', ''] },
  nl: { L: [' — of bekijk', '.'], F: [' — of één advertentie', ''], Q: [' Eerst proberen', ''] },
  pl: { L: [' — albo obejrzyj', '.'], F: [' — albo reklama', ''], Q: [' Chcesz najpierw', ''] },
  pt: { L: [' — ou assista', '.'], F: [' — ou um anúncio', ''], Q: [' Quer testar', ''] },
  ru: { L: [' — или посмотрите', '.'], F: ['; одна реклама', ''], Q: [' Хотите сначала', ''] },
  th: { L: [' หรือดูโฆษณา', ''], F: [' หรือดูโฆษณา', ''], Q: [' อยากลองก่อน', ''] },
  tr: { L: [' — ya da bir reklam', '.'], F: [' — ya da bir reklamla', ''], Q: [' Önce denemek', ''] },
  uk: { L: [' — або перегляньте', '.'], F: ['; одна реклама', ''], Q: [' Хочете спершу', ''] },
  vi: { L: [' — hoặc xem', '.'], F: [' — hoặc một quảng cáo', ''], Q: [' Muốn thử trước', ''] },
  zh: { L: ['，也可以看一个广告', '。'], F: [' —— 或看一个广告', ''], Q: ['想先试试', ''] },
};

function cut(s, [mark, end], where) {
  const i = s.lastIndexOf(mark);
  if (i < 0) throw new Error(`${where}: 표지 없음 "${mark}"`);
  const out = s.slice(0, i) + end;
  if (/Free Pass|24/.test(out.slice(-120))) throw new Error(`${where}: 아직 남음`);
  return out;
}

function swap(raw, oldV, newV, where) {
  const a = JSON.stringify(oldV), b = JSON.stringify(newV);
  if (raw.split(a).length !== 2) throw new Error(`${where}: 원문 위치가 하나가 아님`);
  return raw.replace(a, () => b);
}

for (const [l, c] of Object.entries(CUT)) {
  const p = path.join(I18N, `${l}.json`);
  let raw = fs.readFileSync(p, 'utf8');
  const r = JSON.parse(raw).apps.rotate;
  raw = swap(raw, r.long, cut(r.long, c.L, `${l}.long`), `${l}.long`);
  raw = swap(raw, r.features[5], cut(r.features[5], c.F, `${l}.f5`), `${l}.f5`);
  raw = swap(raw, r.faq[2].a, cut(r.faq[2].a, c.Q, `${l}.faq2`), `${l}.faq2`);
  JSON.parse(raw);
  if (/Free Pass/.test(JSON.stringify(JSON.parse(raw).apps.rotate))) throw new Error(`${l}: Free Pass 남음`);
  fs.writeFileSync(p, raw);
}
console.log(`${Object.keys(CUT).length}개 언어 × 3개 항목 반영`);
