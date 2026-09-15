// =====================================================================
//  앱별 최소 OS 버전 스캔 → scripts/app_reqs.json 캐시
//  - Android: 앱 모듈(com.android.application)의 build.gradle(.kts) 에서 minSdk 를 읽어
//    'Android 12+' 처럼 사용자가 아는 버전 이름으로 바꾼다.
//  - Windows(.NET): *.csproj 의 <SupportedOSPlatformVersion>(예: 10.0.17763.0)을 읽어
//    빌드 번호로 Windows 10 / 11 을 가른다(22000 이상이 Windows 11).
//  - 결과는 앱 상세 페이지 상단의 요구 사항 칩에 쓰인다. 고유명사+숫자라 번역하지 않는다.
//  사용: node scripts/scan_app_reqs.js
//  ※ scan_app_langs.js 와 마찬가지로 앱 소스는 이 저장소 밖(형제 폴더)이라,
//    스캔은 개발 PC에서만 하고 산출물(app_reqs.json)만 커밋한다.
// =====================================================================
const fs = require('fs');
const path = require('path');

const APPS_ROOT = process.env.CODEDAC_ROOT || path.resolve(__dirname, '..', '..');
const OUT = path.join(__dirname, 'app_reqs.json');

// slug → 프로젝트 폴더명 (scan_app_langs.js 의 PROJECT · RESX_PROJECT 와 같은 표)
const ANDROID_PROJECT = {
  clipboard: 'Clipboard', autostart: 'AutoStart', floatcalc: 'FloatCalc',
  floatcrypto: 'FloatCrypto', floattimer: 'FloatTimer', volumebooster: 'VolumeBooster',
  photocleaner: 'PhotoCleaner', readfocus: 'ReadFocus', floatnote: 'FloatNote',
};
const WINDOWS_PROJECT = {
  clipboardwin: 'ClipboardWin', readfocuswin: 'ReadFocusWin',
  floatnotewin: 'FloatNoteWin', floattimerwin: 'FloatTimerWin',
};

// API 레벨 → 사용자에게 보이는 Android 버전
const ANDROID_VERSION = {
  21: '5.0', 22: '5.1', 23: '6.0', 24: '7.0', 25: '7.1', 26: '8.0', 27: '8.1', 28: '9',
  29: '10', 30: '11', 31: '12', 32: '12L', 33: '13', 34: '14', 35: '15', 36: '16',
};

function walk(dir, test, acc = []) {
  let entries;
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return acc; }
  for (const e of entries) {
    if (['build', 'bin', 'obj', 'node_modules', '.git', '.gradle', '.idea'].includes(e.name)) continue;
    const full = path.join(dir, e.name);
    if (e.isDirectory()) walk(full, test, acc);
    else if (test(e.name)) acc.push(full);
  }
  return acc;
}

function androidMinSdk(project) {
  const files = walk(path.join(APPS_ROOT, project), (n) => n === 'build.gradle' || n === 'build.gradle.kts');
  let appValue = null;
  let maxValue = null;
  for (const f of files) {
    const src = fs.readFileSync(f, 'utf8');
    const m = /minSdk(?:Version)?\s*[=(]?\s*(\d+)/.exec(src);
    if (!m) continue;
    const v = Number(m[1]);
    maxValue = Math.max(maxValue || 0, v);
    // 앱 모듈의 값이 실제 설치 조건이다. 라이브러리 모듈 값은 그보다 낮거나 같다.
    if (/com\.android\.application|android\.application/.test(src)) appValue = v;
  }
  return appValue || maxValue;
}

function windowsMinBuild(project) {
  const files = walk(path.join(APPS_ROOT, project), (n) => n.endsWith('.csproj'));
  let build = null;
  for (const f of files) {
    const m = /<SupportedOSPlatformVersion>\s*10\.0\.(\d+)/.exec(fs.readFileSync(f, 'utf8'));
    if (m) build = Math.max(build || 0, Number(m[1]));
  }
  return build;
}

const out = {};
for (const [slug, project] of Object.entries(ANDROID_PROJECT)) {
  const api = androidMinSdk(project);
  if (!api) { console.warn(`✗ ${slug}: minSdk 를 찾지 못함 (${project})`); continue; }
  const ver = ANDROID_VERSION[api];
  if (!ver) { console.warn(`✗ ${slug}: API ${api} 에 대응하는 버전 이름이 없음 — ANDROID_VERSION 에 추가`); continue; }
  out[slug] = { os: 'Android', api, min: ver, label: `Android ${ver}+` };
  console.log(`✓ ${slug}  API ${api} → ${out[slug].label}`);
}
for (const [slug, project] of Object.entries(WINDOWS_PROJECT)) {
  const build = windowsMinBuild(project);
  if (!build) { console.warn(`✗ ${slug}: SupportedOSPlatformVersion 을 찾지 못함 (${project})`); continue; }
  const min = build >= 22000 ? '11' : '10';
  out[slug] = { os: 'Windows', build, min, label: `Windows ${min}+` };
  console.log(`✓ ${slug}  build ${build} → ${out[slug].label}`);
}

fs.writeFileSync(OUT, JSON.stringify(out, null, 2) + '\n');
console.log(`\n저장: scripts/app_reqs.json (${Object.keys(out).length}개 앱)`);
