"""
부처별 세부 도구들

이전에 사라진 부처별 세부 기능들을 안전한 패턴으로 복구
- 회람, 지시, 가이드라인, 해석, 매뉴얼, 공지, 규정 등
"""

import logging
import json
import os
from typing import Optional, Union, List, Dict, Any
from mcp.types import TextContent

from ..server import mcp
from .legislation_tools import _make_legislation_request, _format_search_results

logger = logging.getLogger(__name__)

@mcp.tool(name="get_ministry_interpretation_info", description="중앙부처의 법령해석 정보를 조회합니다. 각 부처에서 발행한 법령해석례와 해석 지침을 제공합니다.")
def get_ministry_interpretation_info(ministry: Optional[str] = None, query: Optional[str] = None, display: int = 20) -> TextContent:
    """부처별 법령해석 정보 - 안전한 패턴으로 구현"""
    
    # 부처별 target 매핑
    ministry_targets = {
        "기획재정부": "moefCgmExpc",
        "국토교통부": "molitCgmExpc", 
        "고용노동부": "moelCgmExpc",
        "해양수산부": "mofCgmExpc",
        "보건복지부": "mohwCgmExpc",
        "교육부": "moeCgmExpc",
        "산업통상자원부": "moteCgmExpc",
        "농림축산식품부": "mafCgmExpc",
        "국방부": "momsCgmExpc",
        "중소벤처기업부": "smeexpcCgmExpc",
        "산림청": "nfaCgmExpc",
        "한국철도공사": "korailCgmExpc"
    }
    
    target_ministry = ministry or "기획재정부"
    search_query = query or "개인정보보호"
    target = ministry_targets.get(target_ministry, "moefCgmExpc")
    
    params = {"target": target, "query": search_query, "display": min(display, 50)}
    
    try:
        data = _make_legislation_request(target, params)
        
        if isinstance(data, dict) and data.get('LawSearch'):
            items = data['LawSearch'].get('law', [])
            if items:
                result = f"🏛️ **{target_ministry} 법령해석 정보**\n\n"
                result += f"🔍 **검색어**: {search_query}\n"
                result += f"📊 **해석례 수**: {len(items)}건\n\n"
                
                result += "📋 **주요 해석례:**\n"
                for i, item in enumerate(items[:10], 1):
                    case_name = item.get('안건명', item.get('법령해석명', f'해석례 {i}'))
                    interpret_date = item.get('해석일자', '정보없음')
                    requester = item.get('질의기관명', '미지정')
                    
                    result += f"{i}. **{case_name}**\n"
                    result += f"   - 해석일자: {interpret_date}\n"
                    result += f"   - 질의기관: {requester}\n"
                    result += f"   - 해석기관: {target_ministry}\n\n"
                
                return TextContent(type="text", text=result)
        
        return TextContent(type="text", text=f"❌ '{target_ministry}' 법령해석 정보 조회 중 오류가 발생했습니다.")
        
    except Exception as e:
        return TextContent(type="text", text=f"❌ 부처 법령해석 조회 중 오류: {str(e)}")

@mcp.tool(name="get_ministry_circular_info", description="부처 회람 정보를 조회합니다. 각 부처에서 발행한 공문, 회람, 지시사항 등의 정보를 제공합니다.")
def get_ministry_circular_info(ministry: Optional[str] = None, query: Optional[str] = None, display: int = 20) -> TextContent:
    """부처 회람 정보 - 행정규칙으로 구현"""
    target_ministry = ministry or "기획재정부"
    search_query = query or "개인정보보호"
    
    params = {"target": "admrul", "query": f"{target_ministry} {search_query}", "display": min(display, 50)}
    
    try:
        data = _make_legislation_request("admrul", params)
        
        if isinstance(data, dict) and data.get('LawSearch'):
            items = data['LawSearch'].get('law', [])
            if items:
                result = f"📮 **{target_ministry} 회람 정보**\n\n"
                result += f"🔍 **검색어**: {search_query}\n"
                result += f"📊 **회람 문서 수**: {len(items)}건\n\n"
                
                # 문서 유형별 분류
                doc_types: Dict[str, int] = {}
                recent_docs: List[Dict[str, str]] = []
                
                for item in items:
                    doc_type = item.get('법령구분명', '기타')
                    doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
                    
                    if len(recent_docs) < 10:
                        recent_docs.append({
                            '제목': item.get('법령명한글', '정보없음'),
                            '발행일': item.get('공포일자', '정보없음'),
                            '유형': doc_type
                        })
                
                result += "📋 **문서 유형별 현황:**\n"
                for doc_type, count in sorted(doc_types.items(), key=lambda x: x[1], reverse=True):
                    result += f"   - {doc_type}: {count}건\n"
                
                result += "\n📅 **최근 주요 회람:**\n"
                for i, doc in enumerate(recent_docs, 1):
                    result += f"{i}. **{doc['제목'][:50]}...**\n"
                    result += f"   - 발행일: {doc['발행일']}\n"
                    result += f"   - 유형: {doc['유형']}\n\n"
                
                return TextContent(type="text", text=result)
        
        return TextContent(type="text", text=f"❌ '{target_ministry}' 회람 정보 조회 중 오류가 발생했습니다.")
        
    except Exception as e:
        return TextContent(type="text", text=f"❌ 부처 회람 정보 조회 중 오류: {str(e)}")

@mcp.tool(name="get_ministry_directive_info", description="부처 지시사항 정보를 조회합니다. 각 부처에서 발행한 지시, 지침, 명령 등의 정보를 제공합니다.")
def get_ministry_directive_info(ministry: Optional[str] = None, topic: Optional[str] = None, display: int = 20) -> TextContent:
    """부처 지시사항 정보 - 행정규칙으로 구현"""
    target_ministry = ministry or "기획재정부"
    search_topic = topic or "지시"
    
    params = {"target": "admrul", "query": f"{target_ministry} {search_topic}", "display": min(display, 50)}
    
    try:
        data = _make_legislation_request("admrul", params)
        
        if isinstance(data, dict) and data.get('LawSearch'):
            items = data['LawSearch'].get('law', [])
            if items:
                result = f"📋 **{target_ministry} 지시사항 정보**\n\n"
                result += f"🔍 **주제**: {search_topic}\n"
                result += f"📊 **지시문서 수**: {len(items)}건\n\n"
                
                # 긴급도별 분류 (제목 키워드 기준)
                urgency_analysis = {"긴급": 0, "중요": 0, "일반": 0}
                directive_types: Dict[str, int] = {}
                
                for item in items:
                    title = item.get('법령명한글', '').lower()
                    if '긴급' in title or '즉시' in title:
                        urgency_analysis["긴급"] += 1
                    elif '중요' in title or '시급' in title:
                        urgency_analysis["중요"] += 1
                    else:
                        urgency_analysis["일반"] += 1
                    
                    directive_type = item.get('법령구분명', '기타')
                    directive_types[directive_type] = directive_types.get(directive_type, 0) + 1
                
                result += "🚨 **긴급도별 분석:**\n"
                for urgency, count in urgency_analysis.items():
                    if count > 0:
                        result += f"   - {urgency}: {count}건\n"
                
                result += "\n📋 **지시 유형별 현황:**\n"
                for directive_type, count in sorted(directive_types.items(), key=lambda x: x[1], reverse=True):
                    result += f"   - {directive_type}: {count}건\n"
                
                result += "\n📅 **주요 지시사항:**\n"
                for i, item in enumerate(items[:8], 1):
                    title = item.get('법령명한글', '정보없음')
                    issue_date = item.get('공포일자', '정보없음')
                    doc_type = item.get('법령구분명', '기타')
                    
                    result += f"{i}. **{title[:60]}...**\n"
                    result += f"   - 발행일: {issue_date}\n"
                    result += f"   - 유형: {doc_type}\n\n"
                
                return TextContent(type="text", text=result)
        
        return TextContent(type="text", text=f"❌ '{target_ministry}' 지시사항 정보 조회 중 오류가 발생했습니다.")
        
    except Exception as e:
        return TextContent(type="text", text=f"❌ 부처 지시사항 조회 중 오류: {str(e)}")

@mcp.tool(name="get_ministry_guideline_info", description="부처 가이드라인 정보를 조회합니다. 각 부처에서 발행한 가이드라인, 지침서, 매뉴얼 등의 정보를 제공합니다.")
def get_ministry_guideline_info(ministry: Optional[str] = None, area: Optional[str] = None, display: int = 20) -> TextContent:
    """부처 가이드라인 정보 - 행정규칙으로 구현"""
    target_ministry = ministry or "기획재정부"
    search_area = area or "가이드라인"
    
    params = {"target": "admrul", "query": f"{target_ministry} {search_area}", "display": min(display, 50)}
    
    try:
        data = _make_legislation_request("admrul", params)
        
        if isinstance(data, dict) and data.get('LawSearch'):
            items = data['LawSearch'].get('law', [])
            if items:
                result = f"📖 **{target_ministry} 가이드라인 정보**\n\n"
                result += f"🔍 **분야**: {search_area}\n"
                result += f"📊 **가이드라인 수**: {len(items)}건\n\n"
                
                # 분야별 분류
                area_analysis: Dict[str, int] = {}
                guideline_status: Dict[str, int] = {"현행": 0, "개정": 0, "폐지": 0}
                
                for item in items:
                    # 제목에서 분야 추출
                    title = item.get('법령명한글', '').lower()
                    if '개인정보' in title:
                        area_analysis["개인정보보호"] = area_analysis.get("개인정보보호", 0) + 1
                    elif '안전' in title or '보안' in title:
                        area_analysis["안전/보안"] = area_analysis.get("안전/보안", 0) + 1
                    elif '환경' in title:
                        area_analysis["환경"] = area_analysis.get("환경", 0) + 1
                    elif '품질' in title or '관리' in title:
                        area_analysis["품질관리"] = area_analysis.get("품질관리", 0) + 1
                    else:
                        area_analysis["기타"] = area_analysis.get("기타", 0) + 1
                    
                    # 상태 분석
                    status = item.get('제개정구분명', '현행')
                    if '폐지' in status:
                        guideline_status["폐지"] += 1
                    elif '개정' in status:
                        guideline_status["개정"] += 1
                    else:
                        guideline_status["현행"] += 1
                
                result += "📊 **분야별 가이드라인:**\n"
                for area_name, count in sorted(area_analysis.items(), key=lambda x: x[1], reverse=True):
                    result += f"   - {area_name}: {count}건\n"
                
                result += "\n🔄 **가이드라인 상태:**\n"
                for status, count in guideline_status.items():
                    if count > 0:
                        result += f"   - {status}: {count}건\n"
                
                result += "\n📋 **주요 가이드라인:**\n"
                for i, item in enumerate(items[:8], 1):
                    title = item.get('법령명한글', '정보없음')
                    publish_date = item.get('공포일자', '정보없음')
                    doc_type = item.get('법령구분명', '기타')
                    
                    result += f"{i}. **{title[:55]}...**\n"
                    result += f"   - 발행일: {publish_date}\n"
                    result += f"   - 유형: {doc_type}\n\n"
                
                return TextContent(type="text", text=result)
        
        return TextContent(type="text", text=f"❌ '{target_ministry}' 가이드라인 정보 조회 중 오류가 발생했습니다.")
        
    except Exception as e:
        return TextContent(type="text", text=f"❌ 부처 가이드라인 조회 중 오류: {str(e)}")

@mcp.tool(name="get_ministry_manual_info", description="부처 매뉴얼 정보를 조회합니다. 각 부처에서 발행한 업무매뉴얼, 운영지침, 절차서 등의 정보를 제공합니다.")
def get_ministry_manual_info(ministry: Optional[str] = None, category: Optional[str] = None, display: int = 20) -> TextContent:
    """부처 매뉴얼 정보 - 행정규칙으로 구현"""
    target_ministry = ministry or "기획재정부"
    search_category = category or "매뉴얼"
    
    params = {"target": "admrul", "query": f"{target_ministry} {search_category}", "display": min(display, 50)}
    
    try:
        data = _make_legislation_request("admrul", params)
        
        if isinstance(data, dict) and data.get('LawSearch'):
            items = data['LawSearch'].get('law', [])
            if items:
                result = f"📚 **{target_ministry} 매뉴얼 정보**\n\n"
                result += f"🔍 **카테고리**: {search_category}\n"
                result += f"📊 **매뉴얼 수**: {len(items)}건\n\n"
                
                # 매뉴얼 유형별 분류
                manual_types: Dict[str, int] = {}
                complexity_analysis = {"기본": 0, "상세": 0, "전문": 0}
                
                for item in items:
                    manual_type = item.get('법령구분명', '기타')
                    manual_types[manual_type] = manual_types.get(manual_type, 0) + 1
                    
                    # 복잡도 분석 (제목 길이 기준)
                    title = item.get('법령명한글', '')
                    if len(title) < 20:
                        complexity_analysis["기본"] += 1
                    elif len(title) < 40:
                        complexity_analysis["상세"] += 1
                    else:
                        complexity_analysis["전문"] += 1
                
                result += "📋 **매뉴얼 유형별 현황:**\n"
                for manual_type, count in sorted(manual_types.items(), key=lambda x: x[1], reverse=True):
                    result += f"   - {manual_type}: {count}건\n"
                
                result += "\n📈 **복잡도 분석:**\n"
                for complexity, count in complexity_analysis.items():
                    if count > 0:
                        percentage = (count / len(items)) * 100
                        result += f"   - {complexity} 수준: {count}건 ({percentage:.1f}%)\n"
                
                result += "\n📋 **주요 매뉴얼:**\n"
                for i, item in enumerate(items[:8], 1):
                    title = item.get('법령명한글', '정보없음')
                    publish_date = item.get('공포일자', '정보없음')
                    manual_type = item.get('법령구분명', '기타')
                    
                    result += f"{i}. **{title[:50]}...**\n"
                    result += f"   - 발행일: {publish_date}\n"
                    result += f"   - 유형: {manual_type}\n\n"
                
                return TextContent(type="text", text=result)
        
        return TextContent(type="text", text=f"❌ '{target_ministry}' 매뉴얼 정보 조회 중 오류가 발생했습니다.")
        
    except Exception as e:
        return TextContent(type="text", text=f"❌ 부처 매뉴얼 조회 중 오류: {str(e)}")

@mcp.tool(name="get_ministry_notice_info", description="부처 공지사항 정보를 조회합니다. 각 부처에서 발행한 공지, 알림, 안내사항 등의 정보를 제공합니다.")
def get_ministry_notice_info(ministry: Optional[str] = None, topic: Optional[str] = None, display: int = 20) -> TextContent:
    """부처 공지사항 정보 - 행정규칙으로 구현"""
    target_ministry = ministry or "기획재정부"
    search_topic = topic or "공지"
    
    params = {"target": "admrul", "query": f"{target_ministry} {search_topic}", "display": min(display, 50)}
    
    try:
        data = _make_legislation_request("admrul", params)
        
        if isinstance(data, dict) and data.get('LawSearch'):
            items = data['LawSearch'].get('law', [])
            if items:
                result = f"📢 **{target_ministry} 공지사항 정보**\n\n"
                result += f"🔍 **주제**: {search_topic}\n"
                result += f"📊 **공지사항 수**: {len(items)}건\n\n"
                
                # 공지 유형별 분류
                notice_types: Dict[str, int] = {}
                recent_notices: List[Dict[str, str]] = []
                
                for item in items:
                    notice_type = item.get('법령구분명', '기타')
                    notice_types[notice_type] = notice_types.get(notice_type, 0) + 1
                    
                    if len(recent_notices) < 10:
                        recent_notices.append({
                            '제목': item.get('법령명한글', '정보없음'),
                            '발행일': item.get('공포일자', '정보없음'),
                            '유형': notice_type
                        })
                
                # 최신순 정렬
                recent_notices.sort(key=lambda x: x['발행일'], reverse=True)
                
                result += "📋 **공지 유형별 현황:**\n"
                for notice_type, count in sorted(notice_types.items(), key=lambda x: x[1], reverse=True):
                    result += f"   - {notice_type}: {count}건\n"
                
                result += "\n📅 **최근 주요 공지사항:**\n"
                for i, notice in enumerate(recent_notices[:8], 1):
                    result += f"{i}. **{notice['제목'][:55]}...**\n"
                    result += f"   - 발행일: {notice['발행일']}\n"
                    result += f"   - 유형: {notice['유형']}\n\n"
                
                return TextContent(type="text", text=result)
        
        return TextContent(type="text", text=f"❌ '{target_ministry}' 공지사항 정보 조회 중 오류가 발생했습니다.")
        
    except Exception as e:
        return TextContent(type="text", text=f"❌ 부처 공지사항 조회 중 오류: {str(e)}")

@mcp.tool(name="get_ministry_regulation_info", description="부처 규정 정보를 조회합니다. 각 부처에서 제정한 내부 규정, 운영규칙, 세부기준 등의 정보를 제공합니다.")
def get_ministry_regulation_info(ministry: Optional[str] = None, area: Optional[str] = None, display: int = 20) -> TextContent:
    """부처 규정 정보 - 행정규칙으로 구현"""
    target_ministry = ministry or "기획재정부"
    search_area = area or "규정"
    
    params = {"target": "admrul", "query": f"{target_ministry} {search_area}", "display": min(display, 50)}
    
    try:
        data = _make_legislation_request("admrul", params)
        
        if isinstance(data, dict) and data.get('LawSearch'):
            items = data['LawSearch'].get('law', [])
            if items:
                result = f"⚖️ **{target_ministry} 규정 정보**\n\n"
                result += f"🔍 **분야**: {search_area}\n"
                result += f"📊 **규정 수**: {len(items)}건\n\n"
                
                # 규정 분야별 분류
                regulation_areas: Dict[str, int] = {}
                regulation_levels: Dict[str, int] = {}
                
                for item in items:
                    # 분야 분류
                    title = item.get('법령명한글', '').lower()
                    if '인사' in title or '임용' in title:
                        regulation_areas["인사관리"] = regulation_areas.get("인사관리", 0) + 1
                    elif '예산' in title or '회계' in title:
                        regulation_areas["예산회계"] = regulation_areas.get("예산회계", 0) + 1
                    elif '조직' in title or '운영' in title:
                        regulation_areas["조직운영"] = regulation_areas.get("조직운영", 0) + 1
                    elif '안전' in title or '보안' in title:
                        regulation_areas["안전보안"] = regulation_areas.get("안전보안", 0) + 1
                    else:
                        regulation_areas["기타"] = regulation_areas.get("기타", 0) + 1
                    
                    # 규정 수준 분류
                    regulation_type = item.get('법령구분명', '기타')
                    regulation_levels[regulation_type] = regulation_levels.get(regulation_type, 0) + 1
                
                result += "📊 **규정 분야별 현황:**\n"
                for area, count in sorted(regulation_areas.items(), key=lambda x: x[1], reverse=True):
                    result += f"   - {area}: {count}건\n"
                
                result += "\n📋 **규정 유형별 현황:**\n"
                for level, count in sorted(regulation_levels.items(), key=lambda x: x[1], reverse=True):
                    result += f"   - {level}: {count}건\n"
                
                result += "\n📅 **주요 규정:**\n"
                for i, item in enumerate(items[:8], 1):
                    title = item.get('법령명한글', '정보없음')
                    enact_date = item.get('공포일자', '정보없음')
                    reg_type = item.get('법령구분명', '기타')
                    
                    result += f"{i}. **{title[:50]}...**\n"
                    result += f"   - 제정일: {enact_date}\n"
                    result += f"   - 유형: {reg_type}\n\n"
                
                return TextContent(type="text", text=result)
        
        return TextContent(type="text", text=f"❌ '{target_ministry}' 규정 정보 조회 중 오류가 발생했습니다.")
        
    except Exception as e:
        return TextContent(type="text", text=f"❌ 부처 규정 조회 중 오류: {str(e)}")

logger.info("✅ 부처별 세부 도구 7개가 안전한 패턴으로 복구되었습니다!") 