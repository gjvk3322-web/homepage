#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rich Results 오류 수정: Service 스키마에서 aggregateRating 제거
- 구글 규칙: Service 타입은 리뷰 스니펫의 부모 노드로 허용 안 됨
- Product와 LocalBusiness에는 이미 aggregateRating이 있어서 별점 표시는 정상 작동
"""

import os
import shutil
import json
import re
from datetime import datetime

INDEX_FILE = os.path.expanduser("~/homepage/index.html")
BACKUP_FILE = f"{INDEX_FILE}.backup_richresults_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

print("=" * 60)
print("🔧 Rich Results 오류 수정 - Service 스키마")
print("=" * 60)

# 1. 백업
print(f"\n📋 백업 생성: {os.path.basename(BACKUP_FILE)}")
shutil.copy2(INDEX_FILE, BACKUP_FILE)
print("✅ 백업 완료")

# 2. 파일 읽기
with open(INDEX_FILE, "r", encoding="utf-8") as f:
    content = f.read()

original_content = content

# ============================================
# Service 스키마에서 aggregateRating 블록 제거
# ============================================
print("\n🎯 Service 스키마의 aggregateRating 제거")

# 정확한 매칭 (들여쓰기 포함)
old_block = '''  "offers": {
    "@type": "Offer",
    "priceCurrency": "KRW",
    "price": "0",
    "description": "무료 샘플 제공 + 무료 시공 견적",
    "availability": "https://schema.org/InStock"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "6700",
    "bestRating": "5"
  }
}'''

new_block = '''  "offers": {
    "@type": "Offer",
    "priceCurrency": "KRW",
    "price": "0",
    "description": "무료 샘플 제공 + 무료 시공 견적",
    "availability": "https://schema.org/InStock"
  }
}'''

if old_block in content:
    content = content.replace(old_block, new_block)
    print("   ✅ Service의 aggregateRating 제거 완료")
else:
    print("   ⚠️  정확한 블록을 찾지 못함")
    print("       (이미 수정되었거나 형식이 다를 수 있음)")

# ============================================
# 결과 저장
# ============================================
print("\n" + "=" * 60)
print("💾 파일 저장")
print("=" * 60)

if content == original_content:
    print("⚠️  변경 사항 없음. 백업 파일 삭제합니다.")
    os.remove(BACKUP_FILE)
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
schema_types = []
for i, schema_text in enumerate(schemas, 1):
    try:
        data = json.loads(schema_text.strip())
        schema_type = data.get('@type', 'Unknown')
        schema_types.append(schema_type)
        print(f"   ✅ 스키마 {i}: {schema_type} - JSON 유효")
    except json.JSONDecodeError as e:
        print(f"   ❌ 스키마 {i}: JSON 오류! → {e}")
        all_valid = False

if not all_valid:
    print("\n🚨 스키마 오류 발견! 백업으로 복구하세요:")
    print(f"   cp {BACKUP_FILE} {INDEX_FILE}")
else:
    print("\n✅ 모든 스키마 정상")

# ============================================
# Service 스키마에 aggregateRating이 없는지 최종 확인
# ============================================
print("\n" + "=" * 60)
print("🔬 최종 검증: Service에 aggregateRating 없는지 확인")
print("=" * 60)

service_found = False
for schema_text in schemas:
    try:
        data = json.loads(schema_text.strip())
        if data.get('@type') == 'Service':
            service_found = True
            if 'aggregateRating' in data:
                print("   ❌ 아직 Service에 aggregateRating이 있습니다!")
            else:
                print("   ✅ Service 스키마에 aggregateRating 없음 (정상)")
    except:
        pass

if not service_found:
    print("   ⚠️  Service 스키마를 찾지 못함")

# ============================================
# 최종 요약
# ============================================
print("\n" + "=" * 60)
print("📊 최종 요약")
print("=" * 60)

print("\n🎯 수정 내용:")
print("   • Service 스키마에서 aggregateRating 제거")
print("   • 별점 표시는 Product와 LocalBusiness에서 정상 작동")

print("\n🚀 다음 단계:")
print("   1) git add index.html")
print("   2) git commit -m \"Rich Results 오류 수정: Service에서 aggregateRating 제거\"")
print("   3) git push")
print("   4) 2~5분 후 다시 Rich Results Test 실행")
print("   5) 모든 스키마 ✅ 통과 확인")

print("\n🎉 완료!\n")
