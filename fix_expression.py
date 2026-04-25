#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
index.html 표현 변경 + 경기팀 순서 변경
- "부산본사·경기지점에서 시공팀을 운영합니다" → "부산·경기 본사에서 시공팀을 운영합니다"
- 경기팀 순서: "경기·인천·서울" → "서울·경기·인천"

화면 FAQ + JSON-LD 스키마 둘 다 수정
"""

import os
import shutil
import json
import re
from datetime import datetime

INDEX_FILE = os.path.expanduser("~/homepage/index.html")
BACKUP_FILE = f"{INDEX_FILE}.backup_expression_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

print("=" * 60)
print("📝 index.html 표현 + 순서 수정")
print("=" * 60)

# 1. 백업 생성
print(f"\n📋 백업 생성: {BACKUP_FILE}")
shutil.copy2(INDEX_FILE, BACKUP_FILE)
print("✅ 백업 완료")

# 2. 파일 읽기
with open(INDEX_FILE, "r", encoding="utf-8") as f:
    content = f.read()

original_content = content
changes = []

# ============================================
# 변경 1: 화면 FAQ 표현 변경
# ============================================
print("\n" + "=" * 60)
print("🎯 변경 1: 화면 FAQ 표현")
print("=" * 60)

# "부산본사·경기지점에서" → "부산·경기 본사에서"
old_phrase_1 = "부산본사·경기지점에서"
new_phrase_1 = "부산·경기 본사에서"

count_1 = content.count(old_phrase_1)
print(f"   '{old_phrase_1}' 발견: {count_1}회")

if count_1 > 0:
    content = content.replace(old_phrase_1, new_phrase_1)
    changes.append(f"화면 표현: '{old_phrase_1}' → '{new_phrase_1}' ({count_1}회)")
    print(f"✅ 변경 완료")
else:
    print(f"⚠️  찾지 못함")

# ============================================
# 변경 2: 경기팀 순서 변경
# ============================================
print("\n" + "=" * 60)
print("🎯 변경 2: 경기팀 순서 - 서울을 맨 앞으로")
print("=" * 60)

# 화면 FAQ + JSON-LD 둘 다 잡기 위해 여러 패턴 시도

# 패턴 A: 화면 FAQ 형식 "경기·인천·서울·충청남도·충청북도"
old_order_1 = "경기·인천·서울·충청남도·충청북도"
new_order_1 = "서울·경기·인천·충청남도·충청북도"

count_2a = content.count(old_order_1)
print(f"   '{old_order_1}' 발견: {count_2a}회")

if count_2a > 0:
    content = content.replace(old_order_1, new_order_1)
    changes.append(f"순서 변경 (가운뎃점): '{old_order_1}' → '{new_order_1}' ({count_2a}회)")
    print(f"✅ 변경 완료")

# 패턴 B: JSON-LD acceptedAnswer 안에 들어간 같은 표현
# (보통 같은 문자열이라 위에서 같이 처리됨)

# 패턴 C: areaServed 배열 순서 확인 (참고용 출력만)
print("\n📌 참고: areaServed 배열은 그대로 둡니다 (검색엔진은 순서 신경 안 씀)")

# ============================================
# 결과 저장
# ============================================
print("\n" + "=" * 60)
print("💾 파일 저장")
print("=" * 60)

if content == original_content:
    print("⚠️  변경 사항 없음. 파일을 저장하지 않습니다.")
else:
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 저장 완료: {INDEX_FILE}")

# ============================================
# JSON-LD 스키마 유효성 검증
# ============================================
print("\n" + "=" * 60)
print("🔍 JSON-LD 스키마 유효성 검증")
print("=" * 60)

schema_pattern = r'<script type="application/ld\+json">(.*?)</script>'
schemas = re.findall(schema_pattern, content, re.DOTALL)

print(f"\n   스키마 개수: {len(schemas)}개")

all_valid = True
for i, schema_text in enumerate(schemas, 1):
    try:
        json.loads(schema_text.strip())
        print(f"   ✅ 스키마 {i}: JSON 유효")
    except json.JSONDecodeError as e:
        print(f"   ❌ 스키마 {i}: JSON 오류! → {e}")
        all_valid = False

if not all_valid:
    print("\n🚨 스키마 오류 발견! 백업으로 복구하세요:")
    print(f"   cp {BACKUP_FILE} {INDEX_FILE}")
else:
    print("\n✅ 모든 스키마 정상")

# ============================================
# 최종 요약
# ============================================
print("\n" + "=" * 60)
print("📊 최종 요약")
print("=" * 60)

if changes:
    print("\n✅ 적용된 변경:")
    for change in changes:
        print(f"   • {change}")
else:
    print("\n⚠️  적용된 변경 없음")

print(f"\n📦 백업 파일: {BACKUP_FILE}")
print("\n🎯 다음 단계:")
print("   1) 시크릿 모드(Cmd+Shift+N)로 https://www.dolbommat.com 접속")
print("   2) Cmd+Shift+R로 하드 리프레시 (2~5분 후 GitHub Pages 배포 완료)")
print("   3) FAQ '시공 가능한 지역' 클릭하여 새 답변 확인")
print("   4) 정상이면 git push로 배포")
print("\n🎉 완료!\n")
