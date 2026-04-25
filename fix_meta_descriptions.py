#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
메타 태그 description 강화 스크립트
- 5개 파일의 description, og:description, twitter:description에
  "부산·경기 본사 직영" 키워드 자연스럽게 추가
- title, og:title, twitter:title은 그대로 (이미 적절한 길이)
- 기존 핵심 키워드(TPU, 층간소음 62%, 6,700가정) 모두 유지
"""

import os
import shutil
from datetime import datetime

HOMEPAGE_DIR = os.path.expanduser("~/homepage")
TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')

# 파일별 변경 매핑: (파일명, [(찾을 문자열, 바꿀 문자열), ...])
CHANGES = {
    "index.html": [
        # description
        (
            '<meta name="description" content="층간소음 62% 저감, 미끄럼 방지, 공기순환 케어 시스템. 6,700가정이 선택한 프리미엄 TPU 매트 돌봄매트. 무료 시공, 무료 샘플 제공.">',
            '<meta name="description" content="부산·경기 본사 직영 시공팀 운영. 층간소음 62% 저감, 미끄럼 방지, 공기순환 케어 시스템. 6,700가정이 선택한 프리미엄 TPU 매트 돌봄매트. 무료 시공, 무료 샘플 제공.">'
        ),
        # og:description
        (
            '<meta property="og:description" content="6,700가정이 선택한 프리미엄 매트. 층간소음 62% 저감, 미끄럼 방지, 공기순환. 무료 샘플 배송.">',
            '<meta property="og:description" content="부산·경기 본사 직영 6,700가정이 선택한 프리미엄 매트. 층간소음 62% 저감, 미끄럼 방지, 공기순환. 무료 샘플 배송.">'
        ),
        # twitter:description
        (
            '<meta name="twitter:description" content="6,700가정이 선택한 프리미엄 매트. 층간소음 62% 저감, 미끄럼 방지, 공기순환. 무료 샘플 배송.">',
            '<meta name="twitter:description" content="부산·경기 본사 직영 6,700가정이 선택한 프리미엄 매트. 층간소음 62% 저감, 미끄럼 방지, 공기순환. 무료 샘플 배송.">'
        ),
    ],
    "baby-mat.html": [
        # description
        (
            '<meta name="description" content="아이 안전을 위한 프리미엄 유아매트. 층간소음 62% 저감, 충격흡수 67%, TPU 젖병 소재. KCL 국가 인증, 전국 6,700가정 시공 완료. 무료 샘플 제공.">',
            '<meta name="description" content="아이 안전을 위한 프리미엄 유아매트. 층간소음 62% 저감, 충격흡수 67%, TPU 젖병 소재. KCL 국가 인증, 부산·경기 본사 직영 6,700가정 시공. 무료 샘플 제공.">'
        ),
        # og:description
        (
            '<meta property="og:description" content="층간소음 62% 저감, 충격흡수 67%, TPU 젖병 소재. 아이 안전을 위한 최고의 선택. 6,700가정이 선택한 돌봄매트.">',
            '<meta property="og:description" content="층간소음 62% 저감, 충격흡수 67%, TPU 젖병 소재. 아이 안전을 위한 최고의 선택. 부산·경기 본사 직영 6,700가정이 선택한 돌봄매트.">'
        ),
        # twitter:description
        (
            '<meta name="twitter:description" content="층간소음 62% 저감, 충격흡수 67%, TPU 젖병 소재. 6,700가정이 선택한 돌봄매트.">',
            '<meta name="twitter:description" content="층간소음 62% 저감, 충격흡수 67%, TPU 젖병 소재. 부산·경기 본사 직영 6,700가정 시공.">'
        ),
    ],
    "dog-mat.html": [
        # description
        (
            '<meta name="description" content="반려동물 슬개골 탈구 예방, 3중 논슬립 코팅, 스크래치 방지 프리미엄 애견매트. TPU 소재 안전, 층간소음 62% 저감. 전국 시공.">',
            '<meta name="description" content="반려동물 슬개골 탈구 예방, 3중 논슬립 코팅, 스크래치 방지 프리미엄 애견매트. TPU 소재 안전, 층간소음 62% 저감. 부산·경기 본사 직영 시공.">'
        ),
        # og:description
        (
            '<meta property="og:description" content="슬개골 탈구 예방, 3중 논슬립 코팅, 스크래치 방지. 우리 댕댕이 관절 건강을 지키는 프리미엄 애견매트.">',
            '<meta property="og:description" content="슬개골 탈구 예방, 3중 논슬립 코팅, 스크래치 방지. 부산·경기 본사 직영, 우리 댕댕이 관절 건강을 지키는 프리미엄 애견매트.">'
        ),
        # twitter:description
        (
            '<meta name="twitter:description" content="슬개골 탈구 예방, 3중 논슬립 코팅, 스크래치 방지. 반려동물 전용 프리미엄 매트.">',
            '<meta name="twitter:description" content="슬개골 탈구 예방, 3중 논슬립 코팅, 스크래치 방지. 부산·경기 본사 직영 반려동물 전용 프리미엄 매트.">'
        ),
    ],
    "cases.html": [
        # description
        (
            '<meta name="description" content="돌봄매트 시공사례 6,700곳. 부산 파라다이스호텔 키즈라운지 450장, 국공립 어린이집 80곳, 경찰서 어린이보호구역 5곳 등 검증된 시공 후기와 사례 모음.">',
            '<meta name="description" content="돌봄매트 시공사례 6,700곳. 부산·경기 본사 직영 시공팀 검증 - 파라다이스호텔 키즈라운지 450장, 국공립 어린이집 80곳, 경찰서 어린이보호구역 5곳 등.">'
        ),
        # og:description
        (
            '<meta property="og:description" content="부산 파라다이스호텔 450장, 국공립 어린이집 80곳, 경찰서 어린이보호구역 5곳 등. 전국 6,700곳의 검증된 시공 사례.">',
            '<meta property="og:description" content="파라다이스호텔 450장, 국공립 어린이집 80곳, 경찰서 어린이보호구역 5곳 등. 부산·경기 본사 직영 6,700곳 검증된 시공 사례.">'
        ),
        # twitter:description
        (
            '<meta name="twitter:description" content="파라다이스호텔·국공립 어린이집·경찰서 어린이보호구역 등 전국 6,700곳 시공 완료.">',
            '<meta name="twitter:description" content="파라다이스호텔·국공립 어린이집·경찰서 어린이보호구역 등. 부산·경기 본사 직영 6,700곳 시공 완료.">'
        ),
    ],
    "event.html": [
        # description
        (
            '<meta name="description" content="돌봄매트 진행 중인 이벤트 총정리. 디지털온누리상품권 7% 할인, 무료 샘플 배송, 무료 실측 방문. 상시 진행 중인 혜택을 확인하세요.">',
            '<meta name="description" content="부산·경기 본사 직영 돌봄매트 이벤트 총정리. 디지털온누리상품권 7% 할인, 무료 샘플 배송, 무료 실측 방문. 상시 진행 중인 혜택을 확인하세요.">'
        ),
        # og:description
        (
            '<meta property="og:description" content="디지털온누리상품권 7% 할인, 무료 샘플 배송, 무료 실측 방문. 상시 진행 중인 모든 혜택.">',
            '<meta property="og:description" content="부산·경기 본사 직영 돌봄매트 - 디지털온누리상품권 7% 할인, 무료 샘플 배송, 무료 실측 방문.">'
        ),
        # twitter:description
        (
            '<meta name="twitter:description" content="디지털온누리상품권 7% 할인, 무료 샘플, 무료 실측. 상시 진행.">',
            '<meta name="twitter:description" content="부산·경기 본사 직영. 디지털온누리상품권 7% 할인, 무료 샘플, 무료 실측.">'
        ),
    ],
}


def process_file(filename, changes):
    """단일 파일 처리"""
    file_path = os.path.join(HOMEPAGE_DIR, filename)
    backup_path = f"{file_path}.backup_meta_{TIMESTAMP}"

    print(f"\n{'='*60}")
    print(f"📄 {filename}")
    print(f"{'='*60}")

    if not os.path.exists(file_path):
        print(f"❌ 파일 없음: {file_path}")
        return False

    # 백업
    shutil.copy2(file_path, backup_path)
    print(f"✅ 백업: {os.path.basename(backup_path)}")

    # 읽기
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    success_count = 0
    fail_count = 0

    # 각 변경 적용
    for i, (old_str, new_str) in enumerate(changes, 1):
        if old_str in content:
            content = content.replace(old_str, new_str)
            success_count += 1
            # 어떤 메타 태그인지 표시
            if 'name="description"' in old_str:
                tag_name = "description"
            elif 'og:description' in old_str:
                tag_name = "og:description"
            elif 'twitter:description' in old_str:
                tag_name = "twitter:description"
            else:
                tag_name = f"태그 {i}"
            print(f"   ✅ {tag_name} 변경 완료")
        else:
            fail_count += 1
            if 'name="description"' in old_str:
                tag_name = "description"
            elif 'og:description' in old_str:
                tag_name = "og:description"
            elif 'twitter:description' in old_str:
                tag_name = "twitter:description"
            else:
                tag_name = f"태그 {i}"
            print(f"   ⚠️  {tag_name} 찾지 못함 (이미 변경되었거나 다른 형식)")

    # 저장
    if content != original:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"💾 저장 완료 (성공 {success_count}/{len(changes)})")
        return True
    else:
        print(f"⚠️  변경 사항 없음 (이미 적용된 것 같습니다)")
        # 백업 삭제 (변경 안 됐으니 불필요)
        os.remove(backup_path)
        return False


def main():
    print("=" * 60)
    print("🚀 메타 태그 description 강화 스크립트")
    print("=" * 60)
    print(f"📂 작업 폴더: {HOMEPAGE_DIR}")
    print(f"⏰ 타임스탬프: {TIMESTAMP}")

    if not os.path.exists(HOMEPAGE_DIR):
        print(f"❌ 폴더 없음: {HOMEPAGE_DIR}")
        return

    success_files = []
    skip_files = []

    for filename, changes in CHANGES.items():
        result = process_file(filename, changes)
        if result:
            success_files.append(filename)
        else:
            skip_files.append(filename)

    # 최종 요약
    print("\n" + "=" * 60)
    print("📊 최종 결과")
    print("=" * 60)

    if success_files:
        print("\n✅ 성공한 파일:")
        for f in success_files:
            print(f"   • {f}")

    if skip_files:
        print("\n⚠️  건너뛴 파일 (이미 변경되었을 가능성):")
        for f in skip_files:
            print(f"   • {f}")

    print(f"\n📦 백업 파일들은 *.backup_meta_{TIMESTAMP} 형식으로 저장됨")
    print("\n🎯 핵심 변경 내용:")
    print("   • description, og:description, twitter:description 모두에")
    print("     '부산·경기 본사 직영' 키워드 자연스럽게 추가")
    print("   • 기존 핵심 키워드(TPU, 층간소음 62%, 6,700가정) 모두 유지")
    print("   • title은 그대로 (이미 적절한 길이)")

    print("\n🚀 다음 단계:")
    print("   1) git add . && git commit -m \"메타 description에 '부산·경기 본사 직영' 키워드 추가\"")
    print("   2) git push")
    print("   3) 시크릿 모드로 https://www.dolbommat.com 접속해서 확인")
    print("\n🎉 완료!\n")


if __name__ == "__main__":
    main()
