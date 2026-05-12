#!/usr/bin/env python3
"""
돌봄매트 홈페이지 - 네이버 애널리틱스 추적 스크립트 일괄 설치
2026-05-12

작동:
1. 기존 4개 파일 (index, quote, baby-mat, dog-mat): 광고 추적 블록 뒤에 애널리틱스 블록 추가
2. 새 4개 파일 (cases, cs-hub, event, map): </head> 앞에 라이브러리 + 추적 블록 추가
3. 모든 원본 파일은 .backup으로 자동 백업
"""
import os
import shutil
from pathlib import Path

NEW_ID = "c938c8295771a0"
HOMEPAGE_DIR = Path.home() / "homepage"

# ===== 추가할 코드 =====

# 기존 4개 파일에 추가할 블록 (라이브러리 이미 있으므로 추적 블록만)
APPEND_TRACKING_ONLY = """
<!-- ═══ 네이버 애널리틱스 (사이트 분석) - 2026-05-12 추가 ═══ -->
<script type="text/javascript">
wcs_add["wa"] = \"""" + NEW_ID + """\";
if(window.wcs){
  wcs_do();
}
</script>
"""

# 새 4개 파일에 추가할 블록 (라이브러리 + 추적 모두)
APPEND_FULL_BLOCK = """
<!-- ═══ 네이버 애널리틱스 (사이트 분석) - 2026-05-12 추가 ═══ -->
<script type="text/javascript" src="//wcs.naver.net/wcslog.js"></script>
<script type="text/javascript">
if (!wcs_add) var wcs_add={};
wcs_add["wa"] = \"""" + NEW_ID + """\";
if(window.wcs){
  wcs_do();
}
</script>
"""

# ===== 파일 그룹 =====
FILES_WITH_AD = ['index.html', 'quote.html', 'baby-mat.html', 'dog-mat.html']
FILES_WITHOUT_AD = ['cases.html', 'cs-hub.html', 'event.html', 'map.html']

# ===== 작업 카운터 =====
success_count = 0
skip_count = 0
error_count = 0


def backup_file(filepath):
    """원본 파일을 .backup으로 백업"""
    backup_path = filepath.with_suffix(filepath.suffix + '.backup')
    if not backup_path.exists():
        shutil.copy2(filepath, backup_path)
        print(f"   📦 백업 생성: {backup_path.name}")


def process_existing_file(filename):
    """기존 광고 추적이 있는 파일 — 그 뒤에 애널리틱스 블록 추가"""
    global success_count, skip_count, error_count
    
    filepath = HOMEPAGE_DIR / filename
    print(f"\n🔵 처리 중: {filename}")
    
    if not filepath.exists():
        print(f"   ❌ 파일이 없음 — 건너뜀")
        error_count += 1
        return
    
    content = filepath.read_text(encoding='utf-8')
    
    # 이미 새 ID가 들어있는지 확인 (중복 방지)
    if NEW_ID in content:
        print(f"   ⏭ 이미 새 ID({NEW_ID})가 설치됨 — 건너뜀")
        skip_count += 1
        return
    
    # 광고 추적 블록 뒤에 추가
    # 패턴: wcs_add["wa"] = "s_520031fef386"; ... wcs_do(); } </script>
    target = 'wcs_add["wa"] = "s_520031fef386";'
    if target not in content:
        print(f"   ❌ 광고 추적 코드를 찾지 못함 — 건너뜀")
        error_count += 1
        return
    
    # 광고 블록 뒤의 첫 번째 </script> 찾기
    ad_block_pos = content.find(target)
    script_close_pos = content.find('</script>', ad_block_pos)
    
    if script_close_pos == -1:
        print(f"   ❌ </script> 종료 태그를 찾지 못함 — 건너뜀")
        error_count += 1
        return
    
    # 백업 생성
    backup_file(filepath)
    
    # </script> 닫는 부분 뒤에 새 블록 삽입
    insert_pos = script_close_pos + len('</script>')
    new_content = content[:insert_pos] + APPEND_TRACKING_ONLY + content[insert_pos:]
    
    filepath.write_text(new_content, encoding='utf-8')
    print(f"   ✅ 애널리틱스 블록 추가 완료")
    success_count += 1


def process_new_file(filename):
    """광고 추적이 없는 파일 — </head> 앞에 라이브러리 + 추적 블록 추가"""
    global success_count, skip_count, error_count
    
    filepath = HOMEPAGE_DIR / filename
    print(f"\n🟢 처리 중: {filename}")
    
    if not filepath.exists():
        print(f"   ❌ 파일이 없음 — 건너뜀")
        error_count += 1
        return
    
    content = filepath.read_text(encoding='utf-8')
    
    # 이미 설치되어 있는지 확인
    if NEW_ID in content:
        print(f"   ⏭ 이미 새 ID가 설치됨 — 건너뜀")
        skip_count += 1
        return
    
    # </head> 찾기
    head_close_pos = content.find('</head>')
    if head_close_pos == -1:
        print(f"   ❌ </head> 태그를 찾지 못함 — 건너뜀")
        error_count += 1
        return
    
    # 백업 생성
    backup_file(filepath)
    
    # </head> 앞에 삽입
    new_content = content[:head_close_pos] + APPEND_FULL_BLOCK + '\n' + content[head_close_pos:]
    
    filepath.write_text(new_content, encoding='utf-8')
    print(f"   ✅ 라이브러리 + 애널리틱스 블록 추가 완료")
    success_count += 1


# ===== 메인 실행 =====
print("=" * 60)
print("🚀 네이버 애널리틱스 추적 스크립트 일괄 설치")
print(f"📁 대상 폴더: {HOMEPAGE_DIR}")
print(f"🆔 새 발급ID: {NEW_ID}")
print("=" * 60)

if not HOMEPAGE_DIR.exists():
    print(f"\n❌ 폴더가 없어요: {HOMEPAGE_DIR}")
    print("   터미널에서 'cd ~/homepage' 이후 실행해주세요.")
    exit(1)

print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("📌 1그룹: 광고 추적이 이미 있는 파일 (추적 블록만 추가)")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
for filename in FILES_WITH_AD:
    process_existing_file(filename)

print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("📌 2그룹: 광고 추적이 없는 파일 (라이브러리 + 추적 모두 추가)")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
for filename in FILES_WITHOUT_AD:
    process_new_file(filename)

print("\n" + "=" * 60)
print("📊 작업 완료 요약")
print("=" * 60)
print(f"✅ 성공: {success_count}개 파일")
print(f"⏭ 건너뜀 (이미 설치됨): {skip_count}개")
print(f"❌ 오류: {error_count}개")
print(f"📦 백업 파일: *.backup (원복하려면 mv로 복원 가능)")
print("\n다음 단계:")
print("  1. git status — 변경 사항 확인")
print("  2. git add . — 모든 변경 추가")
print("  3. git commit -m '네이버 애널리틱스 추적 스크립트 추가'")
print("  4. git push origin main — 배포")
