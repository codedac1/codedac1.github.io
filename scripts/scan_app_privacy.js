// =====================================================================
//  앱별 개인정보 처리 현황 스캔 → scripts/app_privacy.json 캐시
//  개인정보처리방침의 '앱별 정보 처리 현황' 표가 이 파일로 만들어진다. 방침 문장을 손으로
//  고치다 보면 실제 앱과 어긋나기 쉬워서(예전 방침은 어느 앱에도 없는 마이크 권한을 예로 들었다),
//  표만큼은 앱 코드에서 직접 뽑는다.
//
//  - data (외부 연결): 광고 SDK · 결제 · Google Drive 범위 · 외부 API 호스트 · ML Kit · Microsoft Store
//    · CodeDAC 구매 기록 서버(msstore-report, Windows 앱이 PRO 구매 완료 시 보고 — 방침 6항)
//  - perms (주요 권한): 소스 AndroidManifest 에 앱이 직접 선언한 권한(사용자에게 의미 있는 것만)
//    + 광고 ID 는 라이브러리가 붙이므로 빌드된 merged manifest 에서 확인한다.
//    (merged manifest 의 다른 권한은 WorkManager 등 라이브러리가 붙인 것이라 표에는 싣지 않는다.)
//  - 모르는 외부 호스트가 새로 보이면 경고한다 — 방침 4항에 적어야 할지 확인하라는 신호다.
//  사용: node scripts/scan_app_privacy.js     (앱 소스가 있는 개발 PC 에서만)
// =====================================================================
const fs = require('fs');
const path = require('path');

const APPS_ROOT = process.env.CODEDAC_ROOT || path.resolve(__dirname, '..', '..');
const OUT = path.join(__dirname, 'app_privacy.json');

const ANDROID_PROJECT = {
  clipboard: 'Clipboard', autostart: 'AutoStart', floatcalc: 'FloatCalc',
  floatcrypto: 'FloatCrypto', floattimer: 'FloatTimer', volumebooster: 'VolumeBooster',
  photocleaner: 'PhotoCleaner', readfocus: 'ReadFocus', floatnote: 'FloatNote',
};
const WINDOWS_PROJECT = {
  clipboardwin: 'ClipboardWin', readfocuswin: 'ReadFocusWin',
  floatnotewin: 'FloatNoteWin', floattimerwin: 'FloatTimerWin',
  photocleanerwin: 'PhotoCleanerWin',
};

// 표에 싣는 권한 → 코드 (i18n/privacy/<lang>.json 의 perms 키)
const PERM_CODE = {
  'android.permission.SYSTEM_ALERT_WINDOW': 'overlay',
  'android.permission.POST_NOTIFICATIONS': 'notifications',
  'android.permission.FOREGROUND_SERVICE': 'foreground',
  'android.permission.RECEIVE_BOOT_COMPLETED': 'boot',
  'android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS': 'battery',
  'android.permission.MODIFY_AUDIO_SETTINGS': 'audio',
};
const PERM_ORDER = ['overlay', 'notifications', 'foreground', 'boot', 'battery', 'audio', 'adId'];
const DATA_ORDER = ['ads', 'billing', 'store', 'purchaseReport', 'driveSync', 'driveBackup', 'fx', 'crypto', 'mlkit'];

// 소스에 나오는 외부 호스트 → 코드. 문서·정책 링크처럼 앱이 데이터를 주고받지 않는 주소는 IGNORE.
const HOST_CODE = {
  'api.frankfurter.app': 'fx',
  'api.coingecko.com': 'crypto',
  'api.binance.com': 'crypto', 'api1.binance.com': 'crypto', 'api2.binance.com': 'crypto',
  'api3.binance.com': 'crypto', 'api4.binance.com': 'crypto',
  'www.googleapis.com': null, // Google Drive — 범위(scope)로 따로 판정
  // 자사 구매 기록 서버(Data/notify, Cloud Run). **방침 1·6항이 이 전송을 예외로 적고 있다** — 다른 앱에 붙이면 방침도 고칠 것.
  'msstore-report-847105046915.asia-northeast3.run.app': 'purchaseReport',
};
const HOST_IGNORE = /(^|\.)(android\.com|google\.com|googleusercontent\.com|microsoft\.com|codedac\.com|github\.com|apache\.org|w3\.org|schemas\.|example\.|play\.google\.com)$/;

function walk(dir, test, acc = []) {
  let entries;
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return acc; }
  for (const e of entries) {
    if (['.git', '.gradle', '.idea', 'node_modules', 'bin', 'obj'].includes(e.name)) continue;
    const full = path.join(dir, e.name);
    if (e.isDirectory()) walk(full, test, acc);
    else if (test(full, e.name)) acc.push(full);
  }
  return acc;
}
const read = (f) => fs.readFileSync(f, 'utf8');
// 빌드 산출물과 테스트 코드는 앱이 실제로 하는 일이 아니므로 뺀다(테스트의 example.com 같은 주소가 섞인다).
const notBuild = (f) => !/[\\/](build|test|androidTest)[\\/]/.test(f);
const sortBy = (list, order) => [...new Set(list)].sort((a, b) => order.indexOf(a) - order.indexOf(b));

function scanAndroid(project) {
  const root = path.join(APPS_ROOT, project);
  const data = [];
  const perms = [];
  const warnings = [];

  for (const f of walk(root, (p, n) => n === 'AndroidManifest.xml' && notBuild(p) && /[\\/]src[\\/]main[\\/]/.test(p))) {
    for (const m of read(f).matchAll(/<uses-permission[^>]*android:name="([^"]+)"/g)) {
      if (PERM_CODE[m[1]]) perms.push(PERM_CODE[m[1]]);
    }
  }
  const merged = walk(root, (p, n) => n === 'AndroidManifest.xml' && /merged_manifest/.test(p));
  const mergedRelease = merged.filter((p) => /release/i.test(p));
  const mergedFile = (mergedRelease[0] || merged[0]) || null;
  if (mergedFile) {
    const src = read(mergedFile);
    if (/com\.google\.android\.gms\.permission\.AD_ID/.test(src) && !/AD_ID"[^>]*tools:node="remove"/.test(src)) perms.push('adId');
  }

  const gradle = walk(root, (p, n) => notBuild(p) && /^(build\.gradle(\.kts)?|libs\.versions\.toml)$/.test(n)).map(read).join('\n');
  if (/play-services-ads/.test(gradle)) {
    data.push('ads');
    if (!mergedFile) { perms.push('adId'); warnings.push('merged manifest 없음 — 광고 SDK 가 있으므로 광고 ID 를 있다고 간주'); }
  }
  if (/com\.android\.billingclient|[:"']billing(-ktx)?[:"']/.test(gradle)) data.push('billing');
  if (/com\.google\.mlkit/.test(gradle)) data.push('mlkit');

  for (const f of walk(root, (p, n) => notBuild(p) && /\.(kt|java)$/.test(n))) {
    const src = read(f);
    if (/drive\.appdata|DRIVE_APPDATA/.test(src)) data.push('driveSync');
    if (/auth\/drive\.file|DRIVE_FILE/.test(src)) data.push('driveBackup');
    for (const m of src.matchAll(/https?:\/\/([a-zA-Z0-9.-]+\.[a-z]{2,})/g)) {
      const host = m[1].toLowerCase();
      if (host in HOST_CODE) { if (HOST_CODE[host]) data.push(HOST_CODE[host]); }
      else if (!HOST_IGNORE.test(host)) warnings.push(`모르는 외부 호스트 ${host} (${path.basename(f)}) — HOST_CODE 에 분류하고 방침 4항 확인`);
    }
  }
  return { platform: 'android', data: sortBy(data, DATA_ORDER), perms: sortBy(perms, PERM_ORDER), mergedManifest: mergedFile ? fs.statSync(mergedFile).mtime.toISOString().slice(0, 10) : null, warnings: [...new Set(warnings)] };
}

function scanWindows(project) {
  const root = path.join(APPS_ROOT, project);
  const data = [];
  const warnings = [];
  const csproj = walk(root, (p, n) => n.endsWith('.csproj')).map(read).join('\n');
  if (/PackageReference\s+Include="Google\.Apis\.Drive/.test(csproj)) data.push('driveSync');
  for (const f of walk(root, (p, n) => n.endsWith('.cs'))) {
    const src = read(f);
    if (/\bStoreContext\b/.test(src)) data.push('store');
    for (const m of src.matchAll(/https?:\/\/([a-zA-Z0-9.-]+\.[a-z]{2,})/g)) {
      const host = m[1].toLowerCase();
      if (host in HOST_CODE) { if (HOST_CODE[host]) data.push(HOST_CODE[host]); }
      else if (!HOST_IGNORE.test(host)) warnings.push(`모르는 외부 호스트 ${host} (${path.basename(f)})`);
    }
  }
  return { platform: 'windows', data: sortBy(data, DATA_ORDER), perms: [], warnings: [...new Set(warnings)] };
}

const out = {};
for (const [slug, project] of Object.entries(ANDROID_PROJECT)) out[slug] = scanAndroid(project);
for (const [slug, project] of Object.entries(WINDOWS_PROJECT)) out[slug] = scanWindows(project);

for (const [slug, r] of Object.entries(out)) {
  console.log(`${slug.padEnd(14)} data: ${r.data.join(', ') || '-'} | perms: ${r.perms.join(', ') || '-'}${r.mergedManifest ? ` | merged ${r.mergedManifest}` : ''}`);
  for (const w of r.warnings) console.warn(`   ! ${w}`);
  delete r.warnings;
}
fs.writeFileSync(OUT, JSON.stringify(out, null, 2) + '\n');
console.log(`\n저장: scripts/app_privacy.json (${Object.keys(out).length}개 앱)`);
