/* ═══════════════════════════════════════════════════════════════
   돌봄매트 통합 추적 스크립트 · tracking.js
   ═══════════════════════════════════════════════════════════════
   이 파일 하나만 수정하면 모든 페이지(index, baby-mat, dog-mat,
   cases, event, 지역페이지들)에 추적이 자동 반영됩니다.

   ⚠️ 설치 후 아래 4개 플레이스홀더만 실제 값으로 교체하세요:
   - G-Z98MT8N5WK           → 구글 애널리틱스 4 측정 ID
   - 1216917209082764     → 페이스북·인스타 픽셀 ID
   - 5533083905425296341    → 카카오 광고 픽셀 ID
   - adcb2177545fe0      → 네이버 검색광고 WA 키

   발급 방법: INSTALL_GUIDE.md 참고
   ═══════════════════════════════════════════════════════════════ */

(function() {
  'use strict';

  // ───── ID 설정 (교체 필요) ─────
  var CONFIG = {
    GA4_ID: 'G-Z98MT8N5WK',
    META_PIXEL_ID: '1216917209082764',
    KAKAO_PIXEL_ID: '5533083905425296341',
    NAVER_WA_KEY: 'adcb2177545fe0'
  };

  // ═══════════════════════════════════════════════════════════════
  // 1. GA4 (Google Analytics 4) 로드
  // ═══════════════════════════════════════════════════════════════
  (function() {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + CONFIG.GA4_ID;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function() { window.dataLayer.push(arguments); };
    gtag('js', new Date());
    gtag('config', CONFIG.GA4_ID, {
      send_page_view: true,
      cookie_flags: 'SameSite=None;Secure'
    });
  })();

  // ═══════════════════════════════════════════════════════════════
  // 2. Meta Pixel (페이스북·인스타그램)
  // ═══════════════════════════════════════════════════════════════
  (function(f, b, e, v, n, t, s) {
    if (f.fbq) return;
    n = f.fbq = function() {
      n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
    };
    if (!f._fbq) f._fbq = n;
    n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = [];
    t = b.createElement(e); t.async = !0; t.src = v;
    s = b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t, s);
  })(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', CONFIG.META_PIXEL_ID);
  fbq('track', 'PageView');

  // ═══════════════════════════════════════════════════════════════
  // 3. Kakao Pixel
  // ═══════════════════════════════════════════════════════════════
  (function() {
    var s = document.createElement('script');
    s.src = '//t1.daumcdn.net/kas/static/kp.js';
    s.onload = function() {
      if (typeof kakaoPixel === 'function') {
        try { kakaoPixel(CONFIG.KAKAO_PIXEL_ID).pageView(); } catch(e){}
      }
    };
    document.head.appendChild(s);
  })();

  // ═══════════════════════════════════════════════════════════════
  // 4. Naver Wcs (네이버 검색광고)
  // ═══════════════════════════════════════════════════════════════
  (function() {
    var s = document.createElement('script');
    s.src = '//wcs.naver.net/wcslog.js';
    s.onload = function() {
      if (!window.wcs_add) window.wcs_add = {};
      window.wcs_add['wa'] = CONFIG.NAVER_WA_KEY;
      if (window.wcs) { wcs_do(); }
    };
    document.head.appendChild(s);
  })();

  // ═══════════════════════════════════════════════════════════════
  // 5. 공용 이벤트 전송 함수 (GA4 + Meta + Kakao 동시 전송)
  // ═══════════════════════════════════════════════════════════════
  function trackEvent(eventName, params) {
    params = params || {};
    try {
      // GA4
      if (typeof gtag === 'function') {
        gtag('event', eventName, params);
      }
      // Meta Pixel (표준 이벤트 매핑)
      if (typeof fbq === 'function') {
        var fbMap = {
          'kakao_channel_click': 'Contact',
          'phone_click': 'Contact',
          'sample_request_click': 'Lead',
          'quote_click': 'InitiateCheckout'
        };
        if (fbMap[eventName]) {
          fbq('track', fbMap[eventName], params);
        } else {
          fbq('trackCustom', eventName, params);
        }
      }
      // Kakao Pixel
      if (typeof kakaoPixel === 'function') {
        var kMap = {
          'kakao_channel_click': 'participation',
          'phone_click': 'participation',
          'sample_request_click': 'completeRegistration',
          'quote_click': 'addCart'
        };
        if (kMap[eventName]) {
          try { kakaoPixel(CONFIG.KAKAO_PIXEL_ID)[kMap[eventName]](); } catch(e){}
        }
      }
    } catch(e) {
      console.warn('[돌봄매트] Event tracking failed:', e);
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // 6. DOM 로드 완료 후 이벤트 바인딩
  // ═══════════════════════════════════════════════════════════════
  function bindTrackingEvents() {

    // ───── 카카오톡 채널 클릭 ─────
    document.querySelectorAll('a[href*="pf.kakao.com"]').forEach(function(link) {
      link.addEventListener('click', function() {
        var label = (link.textContent || '').trim().substring(0, 30) || 'kakao_link';
        trackEvent('kakao_channel_click', {
          event_category: 'engagement',
          event_label: label,
          page_path: location.pathname
        });
      });
    });

    // ───── 전화번호 클릭 ─────
    document.querySelectorAll('a[href^="tel:"]').forEach(function(link) {
      link.addEventListener('click', function() {
        trackEvent('phone_click', {
          event_category: 'engagement',
          phone_number: link.getAttribute('href').replace('tel:', ''),
          page_path: location.pathname
        });
      });
    });

    // ───── 샘플 신청 버튼 ─────
    document.querySelectorAll('a[href*="sample"]').forEach(function(link) {
      link.addEventListener('click', function() {
        trackEvent('sample_request_click', {
          event_category: 'conversion',
          event_label: (link.textContent || '').trim().substring(0, 30),
          page_path: location.pathname
        });
      });
    });

    // ───── 견적 링크 ─────
    document.querySelectorAll('a[href*="quote"]').forEach(function(link) {
      link.addEventListener('click', function() {
        trackEvent('quote_click', {
          event_category: 'conversion',
          event_label: (link.textContent || '').trim().substring(0, 30),
          page_path: location.pathname
        });
      });
    });

    // ───── FAQ 열람 (faq-item 클래스 기준) ─────
    document.querySelectorAll('.faq-item').forEach(function(item) {
      item.addEventListener('click', function() {
        var q = item.querySelector('p');
        var question = q ? (q.textContent || '').trim().substring(0, 50) : 'unknown';
        trackEvent('faq_open', {
          event_category: 'engagement',
          faq_question: question
        });
      }, { once: true });
    });

    // ───── 네비게이션 클릭 (페이지 간 이동 추적) ─────
    document.querySelectorAll('.site-nav a, .nav-links a').forEach(function(link) {
      link.addEventListener('click', function() {
        trackEvent('nav_click', {
          event_category: 'navigation',
          event_label: (link.textContent || '').trim(),
          to_page: link.getAttribute('href') || ''
        });
      });
    });

    // ───── 이벤트 페이지 CTA (온누리상품권 · 실측 · 샘플) ─────
    document.querySelectorAll('.event-badge').forEach(function(badge) {
      var parent = badge.closest('.card');
      if (!parent) return;
      parent.addEventListener('click', function(e) {
        if (e.target.closest('a')) return; // 링크는 위에서 처리됨
        var title = parent.querySelector('p[style*="font-size:clamp"]');
        trackEvent('event_view', {
          event_category: 'engagement',
          event_name: title ? title.textContent.trim().substring(0, 40) : 'event'
        });
      });
    });
  }

  // ═══════════════════════════════════════════════════════════════
  // 7. 스크롤 깊이 추적 (25·50·75·100%)
  // ═══════════════════════════════════════════════════════════════
  var scrollMarks = { 25: false, 50: false, 75: false, 100: false };
  var scrollTimer;
  function checkScrollDepth() {
    var scrollTop = window.scrollY || document.documentElement.scrollTop;
    var windowHeight = window.innerHeight;
    var docHeight = document.documentElement.scrollHeight - windowHeight;
    if (docHeight <= 0) return;
    var scrollPct = Math.round((scrollTop / docHeight) * 100);
    Object.keys(scrollMarks).forEach(function(pct) {
      pct = parseInt(pct);
      if (scrollPct >= pct && !scrollMarks[pct]) {
        scrollMarks[pct] = true;
        trackEvent('scroll_depth', {
          event_category: 'engagement',
          scroll_percentage: pct,
          page_path: location.pathname
        });
      }
    });
  }
  window.addEventListener('scroll', function() {
    clearTimeout(scrollTimer);
    scrollTimer = setTimeout(checkScrollDepth, 150);
  }, { passive: true });

  // ═══════════════════════════════════════════════════════════════
  // 8. 체류시간 추적
  // ═══════════════════════════════════════════════════════════════
  var pageStartTime = Date.now();
  var timeReported = false;
  function reportTimeOnPage() {
    if (timeReported) return;
    timeReported = true;
    var seconds = Math.round((Date.now() - pageStartTime) / 1000);
    if (seconds < 3) return;
    trackEvent('time_on_page', {
      event_category: 'engagement',
      time_seconds: seconds,
      time_bucket: seconds < 10 ? '0-10s' :
                   seconds < 30 ? '10-30s' :
                   seconds < 60 ? '30-60s' :
                   seconds < 180 ? '1-3min' :
                   seconds < 600 ? '3-10min' : '10min+',
      page_path: location.pathname
    });
  }
  window.addEventListener('pagehide', reportTimeOnPage);
  document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'hidden') reportTimeOnPage();
  });

  // ═══════════════════════════════════════════════════════════════
  // 9. 초기화
  // ═══════════════════════════════════════════════════════════════
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindTrackingEvents);
  } else {
    bindTrackingEvents();
  }

  // 전역에 노출 (특정 페이지에서 커스텀 이벤트 보낼 때 사용)
  window.dolbomTrack = trackEvent;

  console.log('[돌봄매트] 추적 시스템 활성화 ·', new Date().toLocaleTimeString());

})();
