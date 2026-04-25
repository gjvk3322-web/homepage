#!/usr/bin/env python3
"""
index.html 화면 FAQ '시공 가능한 지역' 답변 수정
스키마(JSON-LD)와 화면 표시 답변을 동일하게 통일
실행: cd ~/homepage && python3 fix_faq_html.py
"""

import os
from datetime import datetime

INDEX_FILE = 'index.html'
BACKUP_FILE = f'index.html.backup_faq_{datetime.now().strftime("%Y%m%d_%H%M%S")}'

# 기존 화면 FAQ 답변 (정확히 매칭해야 함)
OLD_ANSWER = '''<p style="font-size:14px;color:var(--soft);line-height:1.8"><strong style="color:var(--text)">수도권·충남·영남 지역에서<br>시공 가능합니다.</strong><br><br>· 수도권: 서울·경기·인천<br>· 충청: 충남<br>· 영남: 부산·대구·울산·경남·경북<br><br>해당 지역 외 방문이 필요한 경우,<br>카카오톡으로 문의해주시면 일정 조정을 도와드릴게요.</p>'''

# 새 답변 (스키마와 100% 동일)
NEW_ANSWER = '''<p style="font-size:14px;color:var(--soft);line-height:1.8"><strong style="color:var(--text)">부산본사·경기지점에서<br>시공팀을 운영합니다.</strong><br><br>· <strong style="color:var(--text)">부산팀</strong>: 부산·울산·대구·경상남도<br>&nbsp;&nbsp;경상북도(포항·경주·김천·구미·경산·영천)<br>· <strong style="color:var(--text)">경기팀</strong>: 경기·인천·서울·충청남도·충청북도<br><br><span style="color:#c0392b;font-size:13px">※ 광주광역시·강원도·전라도·제주도·경상북도(위 6곳 외)는<br>&nbsp;&nbsp;&nbsp;현재 시공이 어렵습니다.</span><br><br>해당 지역 외 방문이 필요한 경우,<br>카카오톡으로 문의해주시면 일정 조정을 도와드릴게요.</p>'''

def main():
    if not os.path.exists(INDEX_FILE):
        print(f"❌ {INDEX_FILE} 파일이 없습니다.")
        return False
    
    # 백업
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 백업 생성: {BACKUP_FILE}")
    
    # 매칭 확인
    if OLD_ANSWER not in content:
        print("❌ 기존 FAQ 답변을 찾을 수 없습니다.")
        print("   파일이 이미 수정됐거나, 답변 내용이 다를 수 있습니다.")
        return False
    
    # 교체
    new_content = content.replace(OLD_ANSWER, NEW_ANSWER, 1)
    
    # 저장
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    # 검증
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        result = f.read()
    
    if NEW_ANSWER in result:
        print("✅ FAQ 답변 수정 완료")
        print()
        print("📋 수정 내용:")
        print("   ❌ 기존: '수도권·충남·영남 지역에서 시공 가능합니다.'")
        print("           영남: 부산·대구·울산·경남·경북")
        print()
        print("   ✅ 신규: '부산본사·경기지점에서 시공팀을 운영합니다.'")
        print("           부산팀: 부산·울산·대구·경남·경북(포항·경주·김천·구미·경산·영천)")
        print("           경기팀: 경기·인천·서울·충남·충북")
        print("           ※ 광주·강원·전라·제주 시공 불가 명시")
        print()
        print("🎯 효과:")
        print("   - 화면 FAQ와 JSON-LD 스키마 100% 통일")
        print("   - 검색엔진과 사용자에게 동일한 정확한 정보 제공")
        print("   - 헛클릭 방지로 마케팅 효율 상승")
        return True
    else:
        print("❌ 수정 후 검증 실패")
        return False

if __name__ == '__main__':
    main()
