#!/usr/bin/env python3
"""
돌봄매트 4개 페이지 스키마 완벽 수정 스크립트
실행: cd ~/homepage && python3 fix_other_schemas.py

수정 내용:
1. baby-mat.html: Product에 areaServed, manufacturer, Organization 참조 추가
2. dog-mat.html: 동일
3. cases.html: ItemList에 provider 참조 추가
4. event.html: 무료 실측 Service의 areaServed를 정확한 가능 지역으로 수정
"""

import re
import json
import os
from datetime import datetime

# ============================================
# 공통: 시공 가능 지역
# ============================================
BUSAN_AREAS = [
    {"@type": "City", "name": "부산광역시"},
    {"@type": "City", "name": "울산광역시"},
    {"@type": "City", "name": "대구광역시"},
    {"@type": "AdministrativeArea", "name": "경상남도"},
    {"@type": "City", "name": "포항시"},
    {"@type": "City", "name": "경주시"},
    {"@type": "City", "name": "김천시"},
    {"@type": "City", "name": "구미시"},
    {"@type": "City", "name": "경산시"},
    {"@type": "City", "name": "영천시"}
]

GYEONGGI_AREAS = [
    {"@type": "AdministrativeArea", "name": "경기도"},
    {"@type": "City", "name": "인천광역시"},
    {"@type": "City", "name": "서울특별시"},
    {"@type": "AdministrativeArea", "name": "충청남도"},
    {"@type": "AdministrativeArea", "name": "충청북도"}
]

ALL_AREAS = BUSAN_AREAS + GYEONGGI_AREAS

# 공통 Organization (manufacturer/provider)
ORGANIZATION_REF = {
    "@type": "Organization",
    "@id": "https://www.dolbommat.com/#organization",
    "name": "돌봄매트",
    "alternateName": ["DOLBOMMAT", "돌봄"],
    "url": "https://www.dolbommat.com/",
    "logo": "https://www.dolbommat.com/logo.png",
    "telephone": "+82-507-1345-4146",
    "email": "dolbommat@naver.com",
    "foundingDate": "2020-11-23",
    "founder": {"@type": "Person", "name": "허민석"},
    "sameAs": [
        "https://www.instagram.com/dolbomstore",
        "https://blog.naver.com/dolbommatt1004",
        "https://pf.kakao.com/_UMyBK"
    ]
}

def make_backup(filename):
    backup_name = f"{filename}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(backup_name, 'w', encoding='utf-8') as f:
        f.write(content)
    return backup_name

def replace_schemas(filename, new_schemas_xml):
    """파일의 모든 스키마를 새 스키마로 교체"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 기존 스키마 블록 모두 제거 (주석 포함)
    pattern = r'(\s*<!--[^>]*?(?:Product|FAQPage|WebSite|Organization|JSON-LD|구조화|BreadcrumbList|ItemList|Offer|Service|온누리|샘플|실측|시공사례|브레드크럼)[^>]*?-->\s*)?<script type="application/ld\+json">.*?</script>'
    cleaned = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # 연속된 빈 줄 정리
    cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned)
    
    # </head> 직전에 새 스키마 삽입
    if '</head>' in cleaned:
        new_content = cleaned.replace('</head>', '\n' + new_schemas_xml + '\n</head>', 1)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def verify(filename, expected_count):
    with open(filename, 'r', encoding='utf-8') as f:
        result = f.read()
    schema_count = result.count('application/ld+json')
    schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>', result, re.DOTALL)
    
    print(f"   - 스키마 개수: {schema_count}개 (기대값: {expected_count}개)")
    
    all_valid = True
    for i, s in enumerate(schemas, 1):
        try:
            json.loads(s.strip())
            print(f"   ✅ 스키마 {i}: JSON 유효")
        except Exception as e:
            print(f"   ❌ 스키마 {i}: JSON 오류 - {e}")
            all_valid = False
    
    return all_valid and schema_count == expected_count

# ============================================
# 1. baby-mat.html 스키마
# ============================================
def fix_baby_mat():
    print("\n" + "="*60)
    print("📄 baby-mat.html 수정")
    print("="*60)
    
    if not os.path.exists('baby-mat.html'):
        print("❌ baby-mat.html 파일이 없습니다.")
        return False
    
    backup = make_backup('baby-mat.html')
    print(f"✅ 백업: {backup}")
    
    product = {
        "@context": "https://schema.org",
        "@type": "Product",
        "@id": "https://www.dolbommat.com/baby-mat.html#product",
        "name": "돌봄매트 유아매트 (TPU 프리미엄)",
        "description": "층간소음 62% 저감, 충격흡수 67%, TPU 젖병 소재로 만든 프리미엄 유아매트. 내구연한 5년 이상, KCL 국가 인증.",
        "image": "https://www.dolbommat.com/og-image.jpg",
        "brand": {"@type": "Brand", "name": "돌봄매트"},
        "category": ["유아매트", "아기매트", "놀이매트", "층간소음매트", "미끄럼방지매트", "어린이집매트"],
        "manufacturer": ORGANIZATION_REF,
        "offers": {
            "@type": "AggregateOffer",
            "priceCurrency": "KRW",
            "lowPrice": "64500",
            "highPrice": "76500",
            "availability": "https://schema.org/InStock",
            "areaServed": ALL_AREAS,
            "seller": {"@id": "https://www.dolbommat.com/#organization"}
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "reviewCount": "6700",
            "bestRating": "5",
            "worstRating": "1"
        }
    }
    
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": "https://www.dolbommat.com/"},
            {"@type": "ListItem", "position": 2, "name": "유아매트", "item": "https://www.dolbommat.com/baby-mat.html"}
        ]
    }
    
    schemas_xml = f"""  <!-- ═══ 구조화 데이터 (JSON-LD) ═══ -->

  <!-- 1. Product (유아매트) -->
  <script type="application/ld+json">
{json.dumps(product, ensure_ascii=False, indent=2)}
  </script>

  <!-- 2. BreadcrumbList -->
  <script type="application/ld+json">
{json.dumps(breadcrumb, ensure_ascii=False, indent=2)}
  </script>
"""
    
    if replace_schemas('baby-mat.html', schemas_xml):
        print("✅ baby-mat.html 수정 완료")
        return verify('baby-mat.html', 2)
    return False

# ============================================
# 2. dog-mat.html 스키마
# ============================================
def fix_dog_mat():
    print("\n" + "="*60)
    print("📄 dog-mat.html 수정")
    print("="*60)
    
    if not os.path.exists('dog-mat.html'):
        print("❌ dog-mat.html 파일이 없습니다.")
        return False
    
    backup = make_backup('dog-mat.html')
    print(f"✅ 백업: {backup}")
    
    product = {
        "@context": "https://schema.org",
        "@type": "Product",
        "@id": "https://www.dolbommat.com/dog-mat.html#product",
        "name": "돌봄매트 애견매트 (반려동물 전용)",
        "description": "반려동물 미끄럼 방지 3중 논슬립 코팅, 슬개골 탈구 예방, 스크래치 방지 강화 코팅. TPU 안전 소재, 층간소음 62% 저감, 내구연한 5년 이상.",
        "image": "https://www.dolbommat.com/og-image.jpg",
        "brand": {"@type": "Brand", "name": "돌봄매트"},
        "category": ["애견매트", "반려동물매트", "강아지매트", "고양이매트", "미끄럼방지매트", "층간소음매트"],
        "manufacturer": ORGANIZATION_REF,
        "offers": {
            "@type": "AggregateOffer",
            "priceCurrency": "KRW",
            "lowPrice": "64500",
            "highPrice": "76500",
            "availability": "https://schema.org/InStock",
            "areaServed": ALL_AREAS,
            "seller": {"@id": "https://www.dolbommat.com/#organization"}
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "reviewCount": "6700",
            "bestRating": "5",
            "worstRating": "1"
        }
    }
    
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": "https://www.dolbommat.com/"},
            {"@type": "ListItem", "position": 2, "name": "애견매트", "item": "https://www.dolbommat.com/dog-mat.html"}
        ]
    }
    
    schemas_xml = f"""  <!-- ═══ 구조화 데이터 (JSON-LD) ═══ -->

  <!-- 1. Product (애견매트) -->
  <script type="application/ld+json">
{json.dumps(product, ensure_ascii=False, indent=2)}
  </script>

  <!-- 2. BreadcrumbList -->
  <script type="application/ld+json">
{json.dumps(breadcrumb, ensure_ascii=False, indent=2)}
  </script>
"""
    
    if replace_schemas('dog-mat.html', schemas_xml):
        print("✅ dog-mat.html 수정 완료")
        return verify('dog-mat.html', 2)
    return False

# ============================================
# 3. cases.html 스키마
# ============================================
def fix_cases():
    print("\n" + "="*60)
    print("📄 cases.html 수정")
    print("="*60)
    
    if not os.path.exists('cases.html'):
        print("❌ cases.html 파일이 없습니다.")
        return False
    
    backup = make_backup('cases.html')
    print(f"✅ 백업: {backup}")
    
    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "돌봄매트 전국 시공사례",
        "description": "2024년 기준 전국 6,700곳의 검증된 돌봄매트 시공 사례",
        "numberOfItems": 6700,
        "provider": {"@id": "https://www.dolbommat.com/#organization"},
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "item": {
                    "@type": "Place",
                    "name": "부산 파라다이스호텔 하바 키즈 라운지",
                    "address": {"@type": "PostalAddress", "addressLocality": "부산", "addressRegion": "해운대구", "addressCountry": "KR"},
                    "description": "모던화이트 매트 450장 시공"
                }
            },
            {
                "@type": "ListItem",
                "position": 2,
                "item": {
                    "@type": "Place",
                    "name": "경찰서 어린이보호구역 전국 5곳",
                    "description": "해운대 경찰서 어린이집 포함, 경찰서 부설 어린이보호구역 5곳 시공 완료"
                }
            },
            {
                "@type": "ListItem",
                "position": 3,
                "item": {
                    "@type": "Place",
                    "name": "국공립 어린이집 전국 80곳",
                    "description": "엄격한 국공립 기준을 통과한 전국 80곳 어린이집 시공"
                }
            },
            {
                "@type": "ListItem",
                "position": 4,
                "item": {
                    "@type": "Place",
                    "name": "디에이치아너힐즈 25평",
                    "address": {"@type": "PostalAddress", "addressLocality": "서울", "addressCountry": "KR"}
                }
            },
            {
                "@type": "ListItem",
                "position": 5,
                "item": {
                    "@type": "Place",
                    "name": "매교역푸르지오SK뷰 24평",
                    "address": {"@type": "PostalAddress", "addressLocality": "수원", "addressRegion": "경기도", "addressCountry": "KR"}
                }
            }
        ]
    }
    
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": "https://www.dolbommat.com/"},
            {"@type": "ListItem", "position": 2, "name": "시공사례", "item": "https://www.dolbommat.com/cases.html"}
        ]
    }
    
    schemas_xml = f"""  <!-- ═══ 구조화 데이터 (JSON-LD) ═══ -->

  <!-- 1. ItemList (시공사례 목록) -->
  <script type="application/ld+json">
{json.dumps(item_list, ensure_ascii=False, indent=2)}
  </script>

  <!-- 2. BreadcrumbList -->
  <script type="application/ld+json">
{json.dumps(breadcrumb, ensure_ascii=False, indent=2)}
  </script>
"""
    
    if replace_schemas('cases.html', schemas_xml):
        print("✅ cases.html 수정 완료")
        return verify('cases.html', 2)
    return False

# ============================================
# 4. event.html 스키마 (가장 중요한 수정!)
# ============================================
def fix_event():
    print("\n" + "="*60)
    print("📄 event.html 수정 (areaServed 정확히!)")
    print("="*60)
    
    if not os.path.exists('event.html'):
        print("❌ event.html 파일이 없습니다.")
        return False
    
    backup = make_backup('event.html')
    print(f"✅ 백업: {backup}")
    
    offer_onnuri = {
        "@context": "https://schema.org",
        "@type": "Offer",
        "name": "디지털온누리상품권 7% 할인",
        "description": "디지털온누리상품권으로 결제 시 누구나 7% 추가 할인 적용. 상시 진행, 중복 적용 가능.",
        "url": "https://www.dolbommat.com/event.html",
        "priceSpecification": {
            "@type": "PriceSpecification",
            "priceCurrency": "KRW"
        },
        "discount": "7%",
        "availability": "https://schema.org/InStock",
        "offeredBy": {"@id": "https://www.dolbommat.com/#organization"},
        "validFrom": "2026-01-01",
        "eligibleCustomerType": "https://schema.org/Enduser"
    }
    
    offer_sample = {
        "@context": "https://schema.org",
        "@type": "Offer",
        "name": "무료 샘플 배송 서비스",
        "description": "카카오톡으로 주소만 알려주시면 실제 매트 샘플을 무료 배송. 직접 만져보고 결정하세요.",
        "url": "https://www.dolbommat.com/event.html",
        "price": "0",
        "priceCurrency": "KRW",
        "availability": "https://schema.org/InStock",
        "offeredBy": {"@id": "https://www.dolbommat.com/#organization"}
    }
    
    # 🚨 가장 중요한 수정: areaServed를 정확한 가능 지역으로!
    service_measure = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": "무료 실측 방문 서비스",
        "description": "전문가가 직접 방문하여 정확한 견적을 안내. 당일 시공 가능, 2년 A/S 보증.",
        "provider": {"@id": "https://www.dolbommat.com/#organization"},
        "areaServed": ALL_AREAS,  # 정확한 가능 지역만!
        "serviceType": "무료 실측 방문",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "KRW",
            "description": "무료 방문 실측"
        }
    }
    
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "홈", "item": "https://www.dolbommat.com/"},
            {"@type": "ListItem", "position": 2, "name": "이벤트", "item": "https://www.dolbommat.com/event.html"}
        ]
    }
    
    schemas_xml = f"""  <!-- ═══ 구조화 데이터 (JSON-LD) ═══ -->

  <!-- 1. 온누리상품권 7% 할인 Offer -->
  <script type="application/ld+json">
{json.dumps(offer_onnuri, ensure_ascii=False, indent=2)}
  </script>

  <!-- 2. 무료 샘플 이벤트 -->
  <script type="application/ld+json">
{json.dumps(offer_sample, ensure_ascii=False, indent=2)}
  </script>

  <!-- 3. 무료 실측 서비스 (시공 가능 지역만 명시) -->
  <script type="application/ld+json">
{json.dumps(service_measure, ensure_ascii=False, indent=2)}
  </script>

  <!-- 4. BreadcrumbList -->
  <script type="application/ld+json">
{json.dumps(breadcrumb, ensure_ascii=False, indent=2)}
  </script>
"""
    
    if replace_schemas('event.html', schemas_xml):
        print("✅ event.html 수정 완료")
        print("   🎯 areaServed: '대한민국' → 정확한 가능 지역 15개로 수정!")
        return verify('event.html', 4)
    return False

# ============================================
# 메인
# ============================================
def main():
    print("="*60)
    print("🚀 4개 페이지 스키마 완벽 수정 시작")
    print("="*60)
    
    results = {
        'baby-mat.html': fix_baby_mat(),
        'dog-mat.html': fix_dog_mat(),
        'cases.html': fix_cases(),
        'event.html': fix_event()
    }
    
    print("\n" + "="*60)
    print("📊 최종 결과")
    print("="*60)
    
    all_ok = True
    for fname, ok in results.items():
        status = "✅ 성공" if ok else "❌ 실패"
        print(f"  {status}: {fname}")
        if not ok:
            all_ok = False
    
    if all_ok:
        print("\n🎉 모든 파일 완벽 수정 완료!")
        print()
        print("📋 수정 요약:")
        print("  ✅ baby-mat.html: areaServed, manufacturer 추가, Organization 연결")
        print("  ✅ dog-mat.html: areaServed, manufacturer 추가, Organization 연결")
        print("  ✅ cases.html: provider 연결 (Organization 참조)")
        print("  ✅ event.html: areaServed '대한민국' → 정확한 15개 지역으로 수정")
        print()
        print("🚨 가장 중요한 수정:")
        print("  event.html의 무료 실측 서비스 areaServed가")
        print("  '대한민국 전체' → '실제 시공 가능 지역 15개'로 정확히 수정됐습니다.")
        print("  이로 인해 광주/강원/전라/제주 사용자가 헛클릭하는 일이 줄어듭니다.")
    else:
        print("\n⚠️ 일부 파일 수정 실패. 백업에서 복구 가능합니다.")

if __name__ == '__main__':
    main()
