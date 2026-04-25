#!/usr/bin/env python3
"""
돌봄매트 index.html 스키마 완벽 수정 스크립트
실행: cd ~/homepage && python3 fix_index_schema.py

수정 내용:
1. LocalBusiness를 부산본사 + 경기지점 2개로 분리
2. 시공 가능 지역 정확히 명시 (광주/강원/전라/제주 제외)
3. 영업시간 + 카톡 24시간 명시
4. 사업자등록번호, 통신판매업 추가
5. 인스타, 네이버 블로그 추가
6. FAQ 시공 지역 답변 정확히 수정
"""

import re
import json
import os
from datetime import datetime

INDEX_FILE = 'index.html'
BACKUP_FILE = f'index.html.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'

# ============================================
# 새 스키마 정의 (정확한 정보)
# ============================================

# 부산팀 시공 가능 지역
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

# 경기팀 시공 가능 지역
GYEONGGI_AREAS = [
    {"@type": "AdministrativeArea", "name": "경기도"},
    {"@type": "City", "name": "인천광역시"},
    {"@type": "City", "name": "서울특별시"},
    {"@type": "AdministrativeArea", "name": "충청남도"},
    {"@type": "AdministrativeArea", "name": "충청북도"}
]

# 모든 가능 지역 (Service용)
ALL_AREAS = [a['name'] for a in BUSAN_AREAS + GYEONGGI_AREAS]

# SNS / 외부 링크
SAME_AS = [
    "https://www.instagram.com/dolbomstore",
    "https://blog.naver.com/dolbommatt1004",
    "https://pf.kakao.com/_UMyBK",
    "https://pf.kakao.com/_UMyBK/chat"
]

# ============================================
# 스키마 1: LocalBusiness 부산본사
# ============================================
LOCAL_BUSINESS_BUSAN = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "@id": "https://www.dolbommat.com/#localbusiness-busan",
    "name": "돌봄매트 부산본사",
    "alternateName": ["돌봄매트", "DOLBOMMAT", "돌봄"],
    "description": "층간소음 62% 저감 프리미엄 TPU 매트 시공 전문업체. 6,700가정·국공립 어린이집 80곳·5성급 호텔 키즈룸 시공 완료.",
    "url": "https://www.dolbommat.com/",
    "logo": "https://www.dolbommat.com/logo.png",
    "image": "https://www.dolbommat.com/og-image.jpg",
    "telephone": "+82-507-1345-4146",
    "email": "dolbommat@naver.com",
    "priceRange": "₩₩",
    "foundingDate": "2020-11-23",
    "founder": {"@type": "Person", "name": "허민석"},
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "강변대로 570 부산건축자재판매단지 F동 11호",
        "addressLocality": "사상구",
        "addressRegion": "부산광역시",
        "addressCountry": "KR"
    },
    "openingHoursSpecification": [
        {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
            "opens": "00:00",
            "closes": "23:59",
            "description": "카카오톡 채널 24시간 응대"
        }
    ],
    "areaServed": BUSAN_AREAS,
    "sameAs": SAME_AS,
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "reviewCount": "6700",
        "bestRating": "5",
        "worstRating": "1"
    },
    "identifier": [
        {"@type": "PropertyValue", "name": "사업자등록번호", "value": "680-37-00893"},
        {"@type": "PropertyValue", "name": "통신판매업신고번호", "value": "2021-부산강서구-0154"}
    ]
}

# ============================================
# 스키마 2: LocalBusiness 경기지점
# ============================================
LOCAL_BUSINESS_GYEONGGI = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "@id": "https://www.dolbommat.com/#localbusiness-gyeonggi",
    "name": "돌봄매트 경기지점",
    "alternateName": ["돌봄매트 안산", "돌봄매트 수도권"],
    "description": "수도권 매트 시공 전문. 경기·인천·서울·충청 지역 직접 방문 시공.",
    "url": "https://www.dolbommat.com/",
    "logo": "https://www.dolbommat.com/logo.png",
    "image": "https://www.dolbommat.com/og-image.jpg",
    "telephone": "+82-507-1345-4146",
    "email": "dolbommat@naver.com",
    "priceRange": "₩₩",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "산단로 325 리드스마트스퀘어 F동 205호",
        "addressLocality": "단원구",
        "addressRegion": "경기도 안산시",
        "addressCountry": "KR"
    },
    "openingHoursSpecification": [
        {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
            "opens": "00:00",
            "closes": "23:59",
            "description": "카카오톡 채널 24시간 응대"
        }
    ],
    "areaServed": GYEONGGI_AREAS,
    "sameAs": SAME_AS,
    "parentOrganization": {"@id": "https://www.dolbommat.com/#localbusiness-busan"}
}

# ============================================
# 스키마 3: Product (기존 유지 + 보완)
# ============================================
PRODUCT = {
    "@context": "https://schema.org",
    "@type": "Product",
    "@id": "https://www.dolbommat.com/#product",
    "name": "돌봄매트 프리미엄 TPU 매트",
    "description": "층간소음 62% 저감, 미끄럼 방지, 공기순환 케어 시스템을 갖춘 프리미엄 TPU 바닥매트. 1m × 1m 대형 사이즈로 이음새 최소화.",
    "brand": {"@type": "Brand", "name": "돌봄매트"},
    "image": "https://www.dolbommat.com/og-image.jpg",
    "category": ["층간소음매트", "매트시공", "시공매트", "미끄럼방지매트", "유아매트", "애견매트", "어린이집매트", "TPU매트", "거실매트", "놀이매트"],
    "manufacturer": {"@type": "Organization", "name": "돌봄매트", "url": "https://www.dolbommat.com/"},
    "offers": {
        "@type": "AggregateOffer",
        "priceCurrency": "KRW",
        "lowPrice": "16900",
        "highPrice": "3000000",
        "offerCount": "3",
        "availability": "https://schema.org/InStock",
        "seller": {"@type": "Organization", "name": "돌봄매트"}
    },
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "reviewCount": "6700",
        "bestRating": "5",
        "worstRating": "1"
    }
}

# ============================================
# 스키마 4: FAQPage (시공 지역 답변 수정)
# ============================================
FAQ_PAGE = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {
            "@type": "Question",
            "name": "시공 시간이 얼마나 걸리나요?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "평형에 따라 차이가 있지만 평균 2~3시간 정도 소요됩니다. 24평 기준 약 2시간, 33평 기준 약 3시간입니다. 가구가 많거나 구조가 복잡한 경우 추가 시간이 소요될 수 있습니다."
            }
        },
        {
            "@type": "Question",
            "name": "바닥손상 / 이사할 때 뜯어서 가져갈 수 있나요?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "네, 바닥에 직접 접착하지 않고 마스킹 테이프 + 3M 폼 테이프 이중 구조로 시공해 바닥 손상 없이 깔끔하게 뜯어갈 수 있습니다. 일반 테이프 시공 타사와 차별화된 부분입니다. 이사 시공도 도와드리고 있으니 카카오톡으로 문의해주세요."
            }
        },
        {
            "@type": "Question",
            "name": "바닥 난방(온돌)과 함께 사용해도 되나요?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "네, 문제없습니다. 돌봄매트는 내열성이 뛰어난 TPU 소재를 사용하여 바닥 난방 위에서도 안전하게 사용 가능합니다. 유해물질 걱정도 없습니다."
            }
        },
        {
            "@type": "Question",
            "name": "시공 가능한 지역이 어디인가요?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "부산본사와 경기지점에서 시공팀을 운영합니다. [부산팀] 부산·울산·대구·경상남도·경상북도(포항·경주·김천·구미·경산·영천) 시공 가능. [경기팀] 경기도·인천·서울·충청남도·충청북도 시공 가능. ※ 광주광역시·강원도·전라도·제주도·경상북도(위 6곳 외)는 현재 시공이 어렵습니다. 정확한 지역은 카카오톡으로 문의해주세요."
            }
        },
        {
            "@type": "Question",
            "name": "무료 샘플을 받아볼 수 있나요?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": "네, 무료로 보내드립니다. 카카오톡으로 '샘플'이라고 입력하시면 샘플 신청 페이지를 안내해드립니다. 실제 매트를 직접 만져보고 결정하실 수 있습니다."
            }
        }
    ]
}

# ============================================
# 스키마 5: WebSite (기존 유지)
# ============================================
WEBSITE = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": "https://www.dolbommat.com/#website",
    "url": "https://www.dolbommat.com/",
    "name": "돌봄매트",
    "description": "층간소음 62% 저감 프리미엄 TPU 매트 시공 전문",
    "inLanguage": "ko-KR",
    "publisher": {"@id": "https://www.dolbommat.com/#organization"}
}

# ============================================
# 스키마 6: Organization (강화)
# ============================================
ORGANIZATION = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": "https://www.dolbommat.com/#organization",
    "name": "돌봄매트",
    "alternateName": ["DOLBOMMAT", "돌봄"],
    "legalName": "돌봄",
    "url": "https://www.dolbommat.com/",
    "logo": {
        "@type": "ImageObject",
        "url": "https://www.dolbommat.com/logo.png",
        "width": "512",
        "height": "512"
    },
    "image": "https://www.dolbommat.com/og-image.jpg",
    "description": "층간소음 62% 저감 프리미엄 TPU 매트 시공 전문업체. 2020년 창업, 6,700가정 시공 완료.",
    "foundingDate": "2020-11-23",
    "founder": {"@type": "Person", "name": "허민석"},
    "contactPoint": [
        {
            "@type": "ContactPoint",
            "telephone": "+82-507-1345-4146",
            "contactType": "customer service",
            "areaServed": "KR",
            "availableLanguage": "Korean",
            "hoursAvailable": {
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
                "opens": "00:00",
                "closes": "23:59"
            }
        }
    ],
    "address": [
        {
            "@type": "PostalAddress",
            "name": "부산본사",
            "streetAddress": "강변대로 570 부산건축자재판매단지 F동 11호",
            "addressLocality": "사상구",
            "addressRegion": "부산광역시",
            "addressCountry": "KR"
        },
        {
            "@type": "PostalAddress",
            "name": "경기지점",
            "streetAddress": "산단로 325 리드스마트스퀘어 F동 205호",
            "addressLocality": "단원구",
            "addressRegion": "경기도 안산시",
            "addressCountry": "KR"
        }
    ],
    "sameAs": SAME_AS,
    "identifier": [
        {"@type": "PropertyValue", "name": "사업자등록번호", "value": "680-37-00893"},
        {"@type": "PropertyValue", "name": "통신판매업신고번호", "value": "2021-부산강서구-0154"}
    ]
}

# ============================================
# 스키마 7: Service (신규 추가 - SEO 강화)
# ============================================
SERVICE = {
    "@context": "https://schema.org",
    "@type": "Service",
    "@id": "https://www.dolbommat.com/#service",
    "name": "돌봄매트 시공 서비스",
    "description": "TPU 소재 프리미엄 매트 직접 시공. 층간소음 62% 저감, 미끄럼 방지, 무료 샘플 제공.",
    "provider": {"@id": "https://www.dolbommat.com/#organization"},
    "serviceType": "층간소음매트 시공",
    "category": ["층간소음매트", "매트시공", "시공매트", "미끄럼방지매트", "유아매트", "애견매트", "어린이집매트", "TPU매트"],
    "areaServed": ALL_AREAS,
    "offers": {
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
}

# ============================================
# 메인 작업 시작
# ============================================
def main():
    if not os.path.exists(INDEX_FILE):
        print(f"❌ {INDEX_FILE} 파일이 없습니다. ~/homepage 폴더에서 실행하세요.")
        return False
    
    # 백업
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        original = f.read()
    with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
        f.write(original)
    print(f"✅ 백업 생성: {BACKUP_FILE}")
    
    # 새 스키마 블록 생성
    new_schemas_block = """  <!-- ===== JSON-LD 구조화된 데이터 (SEO 강화) ===== -->
  <!-- 1. LocalBusiness (부산본사) -->
  <script type="application/ld+json">
""" + json.dumps(LOCAL_BUSINESS_BUSAN, ensure_ascii=False, indent=2) + """
  </script>

  <!-- 2. LocalBusiness (경기지점) -->
  <script type="application/ld+json">
""" + json.dumps(LOCAL_BUSINESS_GYEONGGI, ensure_ascii=False, indent=2) + """
  </script>

  <!-- 3. Product (제품) -->
  <script type="application/ld+json">
""" + json.dumps(PRODUCT, ensure_ascii=False, indent=2) + """
  </script>

  <!-- 4. FAQPage (자주 묻는 질문 - 구글 검색 결과에 리치 스니펫으로 노출) -->
  <script type="application/ld+json">
""" + json.dumps(FAQ_PAGE, ensure_ascii=False, indent=2) + """
  </script>

  <!-- 5. WebSite (사이트 검색 기능 지원) -->
  <script type="application/ld+json">
""" + json.dumps(WEBSITE, ensure_ascii=False, indent=2) + """
  </script>

  <!-- 6. Organization (브랜드 정보) -->
  <script type="application/ld+json">
""" + json.dumps(ORGANIZATION, ensure_ascii=False, indent=2) + """
  </script>

  <!-- 7. Service (시공 서비스 정보) -->
  <script type="application/ld+json">
""" + json.dumps(SERVICE, ensure_ascii=False, indent=2) + """
  </script>
"""
    
    # 기존 스키마 블록 모두 제거
    # 패턴: 주석(있을 수도, 없을 수도) + <script type="application/ld+json">...</script>
    pattern = r'(\s*<!--[^>]*?(?:LocalBusiness|Product|FAQPage|WebSite|Organization|JSON-LD|구조화)[^>]*?-->\s*)?<script type="application/ld\+json">.*?</script>'
    
    cleaned = re.sub(pattern, '', original, flags=re.DOTALL)
    
    # 연속된 빈 줄 정리
    cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned)
    
    # </head> 직전에 새 스키마 삽입
    if '</head>' in cleaned:
        new_content = cleaned.replace('</head>', '\n' + new_schemas_block + '\n</head>', 1)
    else:
        print("❌ </head> 태그를 찾을 수 없습니다.")
        return False
    
    # 파일 저장
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    # 검증
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        result = f.read()
    
    schema_count = result.count('application/ld+json')
    print(f"✅ index.html 수정 완료")
    print(f"   - 스키마 개수: {schema_count}개 (기대값: 7개)")
    
    # JSON 유효성 체크
    schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>', result, re.DOTALL)
    all_valid = True
    for i, s in enumerate(schemas, 1):
        try:
            json.loads(s.strip())
            print(f"   ✅ 스키마 {i}: JSON 유효")
        except Exception as e:
            print(f"   ❌ 스키마 {i}: JSON 오류 - {e}")
            all_valid = False
    
    if all_valid and schema_count == 7:
        print()
        print("🎉 모든 스키마 적용 완료!")
        print()
        print("📊 추가/수정된 정보:")
        print("   ✅ LocalBusiness 부산본사 + 경기지점 분리 (정확한 주소)")
        print("   ✅ 시공 가능 지역 정확히 명시 (10개+5개)")
        print("   ✅ 광주/강원/전라/제주 제외 (정확한 정보)")
        print("   ✅ 카카오톡 24시간 응대 명시")
        print("   ✅ 사업자등록번호: 680-37-00893")
        print("   ✅ 통신판매업: 2021-부산강서구-0154")
        print("   ✅ sameAs: 카톡 + 인스타 + 네이버 블로그")
        print("   ✅ FAQ 시공 지역 답변 정확히 수정")
        print("   ✅ Service 스키마 신규 추가")
        return True
    else:
        print(f"⚠️  검증 실패 - 백업에서 복구하려면: cp {BACKUP_FILE} {INDEX_FILE}")
        return False

if __name__ == '__main__':
    main()
