// =====================================================================
//  앱별 지원 언어 수 스캔 → scripts/app_langs.json 캐시
//  - 각 안드로이드 프로젝트(C:\CodeDAC\<Project>)의 res/values-<locale>/ 폴더에서
//    지원 언어를 도출한다. 기본 res/values/ 는 영어(en)로 간주.
//  - 지역 변형(pt-rBR, zh-rCN…)은 기본 언어로 정규화해 중복 제거.
//  - 결과는 정적 데이터로 커밋되며 gen_site.js 가 빌드 시 읽는다.
//  사용: node scripts/scan_app_langs.js
//  ※ 앱 소스는 이 저장소 밖(형제 폴더)이라, 스캔은 개발 PC에서만 수행하고
//    산출물(app_langs.json)만 저장/커밋한다.
// =====================================================================
const fs = require('fs');
const path = require('path');

const APPS_ROOT = path.join('C:', 'CodeDAC');
const OUT = path.join(__dirname, 'app_langs.json');

// slug → 안드로이드 프로젝트 폴더명 (Windows 앱 등 로케일 없는 앱은 제외)
const PROJECT = {
  clipboard: 'Clipboard', autostart: 'AutoStart', floatcalc: 'FloatCalc',
  floatcrypto: 'FloatCrypto', floattimer: 'FloatTimer', volumebooster: 'VolumeBooster',
  photocleaner: 'PhotoCleaner', secretalbum: 'SecretAlbum', readfocus: 'ReadFocus',
  colorcards: 'ColorCards', wordcards: 'WordCards',
};

// 구식/변형 코드 → 표준 2글자 언어 코드
const ALIAS = { in: 'id', iw: 'he', ji: 'yi', tl: 'fil' };
const normLang = (code) => {
  let c = code.toLowerCase().replace(/-r[a-z]+$/i, '').replace(/-[a-z]{2,}$/i, '');
  c = c.split('-')[0];
  return ALIAS[c] || c;
};

// 프로젝트 폴더 하위에서 res/values-<locale> 디렉터리를 모두 찾는다.
function findLocaleDirs(dir, acc) {
  let entries;
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return acc; }
  for (const e of entries) {
    if (!e.isDirectory()) continue;
    const full = path.join(dir, e.name);
    if (e.name === 'build' || e.name === 'node_modules' || e.name === '.git') continue;
    if (e.name.startsWith('values-') && path.basename(dir) === 'res') {
      acc.push(e.name.slice('values-'.length));
    } else {
      findLocaleDirs(full, acc);
    }
  }
  return acc;
}

const out = {};
for (const [slug, proj] of Object.entries(PROJECT)) {
  const root = path.join(APPS_ROOT, proj);
  if (!fs.existsSync(root)) { console.warn(`✗ ${slug}: ${root} 없음 — 건너뜀`); continue; }
  const raw = findLocaleDirs(root, []);
  const set = new Set(['en']); // 기본 values/ = 영어
  for (const code of raw) {
    if (!/^[a-z]{2,3}(-r?[a-z]+)?$/i.test(code)) continue; // 언어 자원 폴더만 (night, v23 등 제외)
    set.add(normLang(code));
  }
  const codes = [...set].sort();
  out[slug] = { count: codes.length, codes };
  console.log(`✓ ${slug}: ${codes.length} langs`);
}

fs.writeFileSync(OUT, JSON.stringify(out, null, 2) + '\n');
console.log(`\n저장: scripts/app_langs.json (${Object.keys(out).length}개 앱)`);
