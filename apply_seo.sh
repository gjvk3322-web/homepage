#!/bin/bash
# 돌봄매트 SEO 강화 자동 적용 스크립트
# 작성: 2026-04-26
# 실행: bash apply_seo.sh

set -e  # 에러 발생시 즉시 중단

echo "=========================================="
echo "🚀 돌봄매트 SEO 강화 작업 시작"
echo "=========================================="

cd ~/homepage

# ============================================
# 1. 추가 백업 (안전을 위한 이중 백업)
# ============================================
BACKUP_DIR="backup_seo_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp index.html baby-mat.html dog-mat.html cases.html event.html sitemap.xml robots.txt "$BACKUP_DIR/"
echo "✅ 추가 백업 완료: $BACKUP_DIR"

# ============================================
# 2. 메인 페이지 schema (index.html)
# ============================================
cat > /tmp/schema_index.html << 'SCHEMA_EOF'
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://www.dolbommat.com/#organization",
      "name": "돌봄매트",
      "alternateName": ["DOLBOMMAT", "돌봄"],
      "url": "https://www.dolbommat.com",
      "logo": {
        "@type": "ImageObject",
        "url": "https://www.dolbommat.com/logo.png",
        "width": 512,
        "height": 512
      },
      "image": "https://www.dolbommat.com/og-image.jpg",
      "description": "층간소음 62% 저감 프리미엄 TPU 매트 시공 전문. 6,700가정·국공립 어린이집 80곳·5성급 호텔 키즈룸 시공 완료.",
      "foundingDate": "2020-11-23",
      "founder": {"@type": "Person", "name": "허민석"},
      "telephone": "+82-507-1345-4146",
      "email": "dolbommat@naver.com",
      "sameAs": [
        "https://www.instagram.com/dolbomstore",
        "https://blog.naver.com/dolbommatt1004",
        "https://pf.kakao.com/_UMyBK/chat"
      ],
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "강변대로 570 부산건축자재판매단지 F동 11호",
        "addressLocality": "사상구",
        "addressRegion": "부산광역시",
        "addressCountry": "KR"
      }
    },
    {
      "@type": "LocalBusiness",
      "@id": "https://www.dolbommat.com/#localbusiness-busan",
      "name": "돌봄매트 부산본사",
      "image": "https://www.dolbommat.com/og-image.jpg",
      "telephone": "+82-507-1345-4146",
      "email": "dolbommat@naver.com",
      "url": "https://www.dolbommat.com",
      "priceRange": "₩₩",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "강변대로 570 부산건축자재판매단지 F동 11호",
        "addressLocality": "사상구",
        "addressRegion": "부산광역시",
        "addressCountry": "KR"
      },
      "openingHoursSpecification": {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
        "opens": "00:00",
        "closes": "23:59"
      },
      "areaServed": [
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
    },
    {
      "@type": "LocalBusiness",
      "@id": "https://www.dolbommat.com/#localbusiness-gyeonggi",
      "name": "돌봄매트 경기지점",
      "image": "https://www.dolbommat.com/og-image.jpg",
      "telephone": "+82-507-1345-4146",
      "email": "dolbommat@naver.com",
      "url": "https://www.dolbommat.com",
      "priceRange": "₩₩",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "산단로 325 리드스마트스퀘어 F동 205호",
        "addressLocality": "단원구",
        "addressRegion": "경기도 안산시",
        "addressCountry": "KR"
      },
      "openingHoursSpecification": {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
        "opens": "00:00",
        "closes": "23:59"
      },
      "areaServed": [
        {"@type": "AdministrativeArea", "name": "경기도"},
        {"@type": "City", "name": "인천광역시"},
        {"@type": "City", "name": "서울특별시"},
        {"@type": "AdministrativeArea", "name": "충청도"}
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://www.dolbommat.com/#website",
      "url": "https://www.dolbommat.com",
      "name": "돌봄매트",
      "description": "층간소음 62% 저감 프리미엄 TPU 매트 시공 전문",
      "publisher": {"@id": "https://www.dolbommat.com/#organization"},
      "inLanguage": "ko-KR"
    },
    {
      "@type": "Service",
      "serviceType": "층간소음매트 시공",
      "provider": {"@id": "https://www.dolbommat.com/#organization"},
      "name": "돌봄매트 시공 서비스",
      "description": "TPU 소재 프리미엄 매트 직접 시공. 층간소음 62% 저감, 미끄럼 방지, 무료 샘플 제공.",
      "areaServed": ["부산광역시","울산광역시","대구광역시","경상남도","경기도","인천광역시","서울특별시","충청도"],
      "category": ["층간소음매트","매트시공","시공매트","미끄럼방지매트","유아매트","애견매트","어린이집매트","TPU매트","거실매트","놀이매트"],
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "reviewCount": "6700",
        "bestRating": "5",
        "worstRating": "1"
      }
    }
  ]
}
</script>
SCHEMA_EOF

# ============================================
# 3. 유아매트 페이지 schema (baby-mat.html)
# ============================================
cat > /tmp/schema_baby.html << 'SCHEMA_EOF'
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "돌봄매트 유아매트",
  "image": "https://www.dolbommat.com/og-image.jpg",
  "description": "아이 안전을 위한 프리미엄 TPU 유아매트. 층간소음 62% 저감, 미끄럼 방지, 친환경 인증. 국공립 어린이집 80곳 시공 완료.",
  "brand": {
    "@type": "Brand",
    "name": "돌봄매트"
  },
  "category": ["유아매트","아기매트","놀이매트","층간소음매트","미끄럼방지매트","어린이집매트"],
  "manufacturer": {
    "@type": "Organization",
    "name": "돌봄매트",
    "url": "https://www.dolbommat.com"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://www.dolbommat.com/baby-mat.html",
    "priceCurrency": "KRW",
    "price": "0",
    "priceValidUntil": "2027-12-31",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "description": "무료 샘플 제공 + 무료 시공",
    "seller": {
      "@type": "Organization",
      "name": "돌봄매트"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "6700",
    "bestRating": "5",
    "worstRating": "1"
  }
}
</script>
SCHEMA_EOF

# ============================================
# 4. 애견매트 페이지 schema (dog-mat.html)
# ============================================
cat > /tmp/schema_dog.html << 'SCHEMA_EOF'
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "돌봄매트 애견매트",
  "image": "https://www.dolbommat.com/og-image.jpg",
  "description": "반려동물 관절 보호 프리미엄 TPU 애견매트. 미끄럼 방지로 슬개골 탈구 예방. 청소 간편, 친환경 인증.",
  "brand": {
    "@type": "Brand",
    "name": "돌봄매트"
  },
  "category": ["애견매트","반려동물매트","미끄럼방지매트","강아지매트","고양이매트"],
  "manufacturer": {
    "@type": "Organization",
    "name": "돌봄매트",
    "url": "https://www.dolbommat.com"
  },
  "offers": {
    "@type": "Offer",
    "url": "https://www.dolbommat.com/dog-mat.html",
    "priceCurrency": "KRW",
    "price": "0",
    "priceValidUntil": "2027-12-31",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "description": "무료 샘플 제공 + 무료 시공",
    "seller": {
      "@type": "Organization",
      "name": "돌봄매트"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "6700",
    "bestRating": "5",
    "worstRating": "1"
  }
}
</script>
SCHEMA_EOF

# ============================================
# 5. 시공사례 페이지 schema (cases.html)
# ============================================
cat > /tmp/schema_cases.html << 'SCHEMA_EOF'
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "돌봄매트 시공사례",
  "description": "6,700건 이상의 실제 시공사례. 부산·경기·인천·서울 등 전국 매트 시공 갤러리.",
  "url": "https://www.dolbommat.com/cases.html",
  "isPartOf": {
    "@type": "WebSite",
    "url": "https://www.dolbommat.com",
    "name": "돌봄매트"
  },
  "about": {
    "@type": "Service",
    "name": "층간소음매트 시공",
    "provider": {
      "@type": "Organization",
      "name": "돌봄매트",
      "url": "https://www.dolbommat.com"
    }
  },
  "breadcrumb": {
    "@type": "BreadcrumbList",
    "itemListElement": [
      {"@type": "ListItem", "position": 1, "name": "홈", "item": "https://www.dolbommat.com"},
      {"@type": "ListItem", "position": 2, "name": "시공사례", "item": "https://www.dolbommat.com/cases.html"}
    ]
  }
}
</script>
SCHEMA_EOF

# ============================================
# 6. 이벤트 페이지 schema (event.html)
# ============================================
cat > /tmp/schema_event.html << 'SCHEMA_EOF'
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "돌봄매트 이벤트",
  "description": "돌봄매트 시공 후기 이벤트, 무료 샘플 신청, 6주년 할인 프로모션.",
  "url": "https://www.dolbommat.com/event.html",
  "isPartOf": {
    "@type": "WebSite",
    "url": "https://www.dolbommat.com",
    "name": "돌봄매트"
  },
  "breadcrumb": {
    "@type": "BreadcrumbList",
    "itemListElement": [
      {"@type": "ListItem", "position": 1, "name": "홈", "item": "https://www.dolbommat.com"},
      {"@type": "ListItem", "position": 2, "name": "이벤트", "item": "https://www.dolbommat.com/event.html"}
    ]
  }
}
</script>
SCHEMA_EOF

echo "✅ 5개 schema 파일 임시 생성 완료"

# ============================================
# 7. HTML 파일에 schema 삽입 (Python 사용 - 안전)
# ============================================
python3 << 'PYEOF'
import os

mappings = [
    ('index.html', '/tmp/schema_index.html'),
    ('baby-mat.html', '/tmp/schema_baby.html'),
    ('dog-mat.html', '/tmp/schema_dog.html'),
    ('cases.html', '/tmp/schema_cases.html'),
    ('event.html', '/tmp/schema_event.html'),
]

for html_file, schema_file in mappings:
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 이미 schema가 있는지 체크 (중복 방지)
    if 'application/ld+json' in html:
        print(f"⚠️  {html_file}: 이미 JSON-LD 스키마 존재 - 건너뜀")
        continue
    
    with open(schema_file, 'r', encoding='utf-8') as f:
        schema = f.read()
    
    # </head> 바로 앞에 schema 삽입
    if '</head>' in html:
        new_html = html.replace('</head>', schema + '\n</head>', 1)
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"✅ {html_file}: schema 삽입 완료")
    else:
        print(f"❌ {html_file}: </head> 태그를 찾을 수 없음")

print("✅ HTML 파일 schema 삽입 완료")
PYEOF

# ============================================
# 8. robots.txt 최적화
# ============================================
cat > robots.txt << 'ROBOTS_EOF'
# 돌봄매트 robots.txt
# 모든 검색엔진 크롤링 허용

User-agent: *
Allow: /
Disallow: /backup_*/
Disallow: /naver*.html

# 네이버 봇
User-agent: Yeti
Allow: /
Crawl-delay: 1

# 구글 봇
User-agent: Googlebot
Allow: /

# 다음 봇
User-agent: Daumoa
Allow: /

# 빙 봇
User-agent: Bingbot
Allow: /

# 사이트맵 위치
Sitemap: https://www.dolbommat.com/sitemap.xml
ROBOTS_EOF
echo "✅ robots.txt 최적화 완료"

# ============================================
# 9. sitemap.xml lastmod 업데이트
# ============================================
TODAY=$(date +%Y-%m-%d)
sed -i '' "s|<lastmod>2026-04-21</lastmod>|<lastmod>$TODAY</lastmod>|g" sitemap.xml
echo "✅ sitemap.xml 업데이트 완료 ($TODAY)"

# ============================================
# 10. 최종 검증
# ============================================
echo ""
echo "=========================================="
echo "📊 최종 검증"
echo "=========================================="

echo ""
echo "▶ JSON-LD schema 추가 확인:"
for f in index.html baby-mat.html dog-mat.html cases.html event.html; do
    count=$(grep -c "application/ld+json" "$f" 2>/dev/null || echo "0")
    if [ "$count" -gt "0" ]; then
        echo "   ✅ $f: $count 개"
    else
        echo "   ❌ $f: schema 없음!"
    fi
done

echo ""
echo "▶ www 도메인 통일 확인:"
WRONG_COUNT=$(grep -l "https://dolbommat\.com" index.html baby-mat.html dog-mat.html cases.html event.html sitemap.xml robots.txt 2>/dev/null | wc -l)
if [ "$WRONG_COUNT" -eq "0" ]; then
    echo "   ✅ 모든 파일이 www.dolbommat.com 사용 중"
else
    echo "   ⚠️  일부 파일에 www 없는 URL 잔존: $WRONG_COUNT 개"
fi

echo ""
echo "▶ robots.txt 사이트맵 명시 확인:"
if grep -q "Sitemap: https://www.dolbommat.com/sitemap.xml" robots.txt; then
    echo "   ✅ Sitemap 정상 명시"
else
    echo "   ❌ Sitemap 누락"
fi

echo ""
echo "=========================================="
echo "🎉 SEO 강화 작업 완료!"
echo "=========================================="
echo ""
echo "다음 단계:"
echo "  1. git add . "
echo "  2. git commit -m \"SEO 강화: JSON-LD 스키마, www 통일, robots.txt 최적화\""
echo "  3. git push"
echo ""
echo "백업 위치: ~/homepage/$BACKUP_DIR"
