# 🚀 돌봄매트 홈페이지 SEO + 추적 시스템 설치 가이드 v2

> 작성일: 2026-04-21
> 대상: 대장님 (코딩 초보 기준)
> 소요시간: ID 발급 30분 + 교체 5분 = **총 35분**

---

## 🎯 v2의 핵심 변화

이전 버전에서는 각 HTML 페이지마다 추적 ID를 박아야 했어요. **v2는 `tracking.js` 한 파일에서만 교체하면 모든 페이지에 자동 반영됩니다.**

---

## 📦 전달받은 파일 (10개)

```
dolbom-homepage/
├── index.html           ← 메인 페이지 (SEO + 추적)
├── baby-mat.html        ← 유아매트 (SEO + Product 스키마)
├── dog-mat.html         ← 애견매트 (SEO + Product 스키마)
├── cases.html           ← 시공사례 (SEO + ItemList 스키마)
├── event.html           ← 이벤트 (SEO + Offer 스키마)
├── tracking.js          ← ⭐ 추적 중앙 관리 (여기만 수정!)
├── style.css            ← 공통 스타일
├── robots.txt           ← 검색엔진 크롤러 안내
├── sitemap.xml          ← 사이트 구조 (검색엔진 제출용)
├── site.webmanifest     ← 모바일 앱 아이콘
├── dolbom-video.mp4     ← 메인 영상 (최적화 필요)
└── img/                 ← 이미지 폴더
```

---

## 🔴 ⚠️ 반드시 할 일 — tracking.js 한 파일만 수정

### tracking.js를 열면 맨 위에 이 영역이 있어요

```javascript
  var CONFIG = {
    GA4_ID: 'G-XXXXXXXXXX',              ← 이것만 교체
    META_PIXEL_ID: 'YOUR_META_PIXEL_ID',   ← 이것만 교체
    KAKAO_PIXEL_ID: 'YOUR_KAKAO_PIXEL_ID', ← 이것만 교체
    NAVER_WA_KEY: 'YOUR_NAVER_WA_KEY'      ← 이것만 교체
  };
```

### 이 4개만 발급받은 실제 값으로 바꾸면 끝

**index.html·baby-mat.html·dog-mat.html·cases.html·event.html 모든 파일이 tracking.js를 공유하므로, 다른 파일은 수정 안 해도 됩니다.**

---

# Part 1 · 4개 ID 발급 (30분)

## 🅰️ GA4 (구글 애널리틱스 4) — 가장 중요

### 발급 순서
1. https://analytics.google.com 접속
2. 구글 계정 로그인 (gmail)
3. **「측정 시작」** 클릭
4. 계정 이름: **돌봄매트**
5. 속성 이름: **돌봄매트 홈페이지**
6. 보고 시간대: **대한민국** | 통화: **KRW**
7. 비즈니스 카테고리: **소매**
8. 플랫폼 선택: **웹**
9. 웹사이트 URL: `https://dolbommat.com`
10. **측정 ID 복사** (예: `G-A1B2C3D4E5`)

### tracking.js에서 교체
```
찾기: G-XXXXXXXXXX
교체: G-A1B2C3D4E5    (본인이 받은 측정 ID)
```

---

## 🅱️ Meta Pixel (페이스북·인스타그램 광고)

### 발급 순서
1. https://business.facebook.com/events_manager2 접속
2. **「데이터 소스 연결」 → 「웹」 → 「Meta Pixel」**
3. 픽셀 이름: **돌봄매트 홈페이지**
4. 웹사이트 URL: `https://dolbommat.com`
5. **픽셀 ID 복사** (15-16자리 숫자, 예: `123456789012345`)

### tracking.js에서 교체
```
찾기: YOUR_META_PIXEL_ID
교체: 123456789012345    (본인이 받은 픽셀 ID)
```

---

## 🅲️ Kakao Pixel (카카오 광고)

### 발급 순서
1. https://business.kakao.com 접속
2. **「광고자산 관리」 → 「픽셀 & SDK」 → 「픽셀 만들기」**
3. 이름: **돌봄매트 홈페이지**
4. 도메인: `dolbommat.com`
5. **픽셀 ID 복사**

### tracking.js에서 교체
```
찾기: YOUR_KAKAO_PIXEL_ID
교체: (본인이 받은 카카오 픽셀 ID)
```

> 💡 지금 카카오 광고 안 해도 픽셀은 깔아두세요. 나중에 광고 시작할 때 과거 데이터가 쌓여있으면 훨씬 유리합니다.

---

## 🅳️ Naver Wcs (네이버 검색광고 전환 추적)

### 발급 순서
1. https://analytics.naver.com 접속
2. 네이버 아이디 로그인
3. **사이트 등록** → 도메인 입력
4. **「설정」 → 「사이트 관리」**에서 `wa` 값 확인 (예: `s_12a3b45c6d7e`)

### tracking.js에서 교체
```
찾기: YOUR_NAVER_WA_KEY
교체: s_12a3b45c6d7e    (본인이 받은 WA 키)
```

---

## 🅴️ 사이트 소유 확인 (보너스)

### 구글 서치콘솔
1. https://search.google.com/search-console
2. **「속성 추가」 → 「URL 접두어」**: `https://dolbommat.com/`
3. **「HTML 태그」** 방식 선택 → `content="..."` 값 복사
4. `index.html` 파일 열어서 `GOOGLE_VERIFICATION_CODE_HERE` 교체
5. 서치콘솔에서 **「확인」** → **「사이트맵」** → `sitemap.xml` 제출

### 네이버 서치어드바이저
1. https://searchadvisor.naver.com
2. **「사이트 등록」**: `https://dolbommat.com/`
3. **「HTML 태그」** 방식 → `content="..."` 값 복사
4. `index.html`에서 `NAVER_VERIFICATION_CODE_HERE` 교체
5. **「소유 확인」 → 「요청」 → 「사이트맵 제출」**: `https://dolbommat.com/sitemap.xml`

> 이 두 개 확인 코드만 `index.html` 직접 수정이 필요해요 (tracking.js가 아님)

---

# Part 2 · 수정 방법 (5분)

## 방법 1 · VSCode로 열어서 찾아바꾸기 (추천)

1. VSCode에서 `tracking.js` 열기
2. `Cmd+F` (찾기) → `G-XXXXXXXXXX` 검색
3. 실제 값으로 입력 (2곳 자동 반영)
4. 같은 방식으로 다른 3개도 교체
5. 저장

## 방법 2 · 터미널 (맥북)

```bash
cd ~/바탕화면/homepage   # 본인 폴더 경로로

# GA4
sed -i '' 's/G-XXXXXXXXXX/G-실제측정ID/g' tracking.js

# Meta Pixel
sed -i '' 's/YOUR_META_PIXEL_ID/실제픽셀ID/g' tracking.js

# Kakao Pixel
sed -i '' 's/YOUR_KAKAO_PIXEL_ID/실제카카오ID/g' tracking.js

# Naver Wcs
sed -i '' 's/YOUR_NAVER_WA_KEY/s_실제키/g' tracking.js

# 확인
grep "CONFIG = {" -A 6 tracking.js
```

---

# Part 3 · 배포 (도메인 이전 후)

## 현재 상태
- `dolbommat.com` → 카페24 (현재 운영 중)
- 이 파일 패키지는 **새 서버에 설치 후 도메인만 옮길 예정**

## 배포 체크리스트

### 🔴 도메인 이전 전
- [ ] `tracking.js` 수정 완료 (ID 4개)
- [ ] `index.html`의 서치콘솔/서치어드바이저 확인 코드 2개 교체
- [ ] `dolbom-video.mp4` 최적화 (14.4MB → 4~5MB)
- [ ] `og-image.jpg` 준비 (1200×630px) — 카톡 공유 썸네일
- [ ] 파비콘 준비: `favicon-32x32.png`, `favicon-16x16.png`, `apple-touch-icon.png`
- [ ] 새 서버에 모든 파일 업로드
- [ ] 새 서버 임시 URL로 페이지 정상 작동 확인

### 🟡 도메인 이전 당일
- [ ] 카페24 도메인 해제
- [ ] DNS 변경 (새 서버 IP 지정)
- [ ] SSL(HTTPS) 인증서 설치 → **필수!**
- [ ] DNS 전파 대기 (1~24시간)

### 🟢 도메인 이전 후
- [ ] `https://dolbommat.com` 정상 접속 확인
- [ ] 카톡에 `https://dolbommat.com` 보내서 썸네일 뜨는지 확인
- [ ] GA4 실시간 보고서에서 본인 접속 잡히는지 확인
- [ ] `https://dolbommat.com/robots.txt` 열리는지 확인
- [ ] `https://dolbommat.com/sitemap.xml` 열리는지 확인
- [ ] 구글 서치콘솔 sitemap 제출
- [ ] 네이버 서치어드바이저 sitemap 제출

---

# Part 4 · 자동 추적되는 이벤트 (10종)

tracking.js가 설치되면 아래 이벤트가 자동 수집됩니다:

| 이벤트명 | 언제 발동 | 의미 |
|:---|:---|:---|
| `page_view` | 페이지 방문 | 방문자 수 |
| `kakao_channel_click` | 카톡 버튼 클릭 | **핵심 지표** |
| `phone_click` | 전화번호 클릭 | 전화 문의 |
| `sample_request_click` | 샘플 신청 | 리드 생성 |
| `quote_click` | 견적 링크 | 견적 관심 |
| `faq_open` | FAQ 질문 열기 | 어떤 질문 많은지 |
| `nav_click` | 네비게이션 클릭 | 페이지 간 이동 |
| `event_view` | 이벤트 카드 보기 | 혜택 관심도 |
| `scroll_depth` | 25/50/75/100% | 이탈 지점 |
| `time_on_page` | 페이지 떠날 때 | 체류시간 |

## Meta Pixel 자동 전송
- `PageView` — 모든 방문
- `Contact` — 카톡/전화 클릭 → 상담 전환 최적화
- `Lead` — 샘플 신청 → 리드 전환 최적화
- `InitiateCheckout` — 견적 시작 → 구매 전환 전단계

---

# Part 5 · 구조화 데이터 (검색 결과 리치 스니펫)

각 페이지별로 다른 JSON-LD 스키마가 박혀있어요:

| 페이지 | 스키마 종류 | 검색 결과에 뜨는 것 |
|:---|:---|:---|
| `index.html` | LocalBusiness, Product, FAQPage, Organization | 별점, FAQ 펼침, 지도 |
| `baby-mat.html` | Product, BreadcrumbList | 가격, 별점, 경로 |
| `dog-mat.html` | Product, BreadcrumbList | 가격, 별점, 경로 |
| `cases.html` | ItemList, BreadcrumbList | 시공사례 목록 |
| `event.html` | Offer × 2, Service, BreadcrumbList | **할인 정보 카드** |

---

# Part 6 · 30일 체크 스케줄

## 첫째 주
- GA4 → 실시간 보고서로 본인 방문 확인
- 하루 평균 방문자 수 감 잡기

## 2~4주차
- GA4 → **「획득」 → 「트래픽 획득」** 에서 채널별 비교
- 네이버 vs 인스타 vs 직접 유입의 **카톡 전환율** 비교
- → 전환율 높은 채널에 광고비 몰빵

## 한 달 후
- 가장 많이 본 페이지 확인 (baby-mat vs dog-mat vs cases)
- 스크롤 75% 도달률 낮은 페이지 → 중간 섹션 개선

---

# 🔐 따로 기록해둔 우려사항

> **cs-welcome.html 중간 단계 삽입 — 보류**
> - 장점: 카톡 유입 고객 이름·번호 확정 수집
> - 단점: 이탈률 상승 위험
> - 재검토: 3~6개월 후 GA4 데이터로 카톡 클릭 → 실제 상담 전환율 추정 가능해지면

---

# 💬 문제 생기면

- 측정 ID 교체 어려움 → 스크린샷 Claude에게 공유
- GA4에 데이터 안 들어옴 → 브라우저 캐시 삭제 + 하루 대기
- `tracking.js 404` 에러 → 모든 HTML 파일과 같은 폴더에 있는지 확인

---

**35분만 투자하시면 앞으로 수년간 복리로 쌓일 데이터 기반이 만들어집니다.** 🚀
