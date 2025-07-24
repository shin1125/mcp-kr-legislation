"""
고급 법령 분석 도구들

이전에 사라진 중요한 고급 분석 기능들을 안전한 패턴으로 복구
"""

import logging
import json
import os
from typing import Optional, Union, List, Dict, Any
from mcp.types import TextContent

from ..server import mcp
from .legislation_tools import _make_legislation_request, _format_search_results

logger = logging.getLogger(__name__)

@mcp.tool(name="analyze_law_changes", description="법령의 변경사항을 심층 분석합니다. 개정 내용, 시행일, 주요 변화점을 종합적으로 분석하여 제공합니다.")
def analyze_law_changes(law_name: Optional[str] = None, period_start: Optional[str] = None, period_end: Optional[str] = None, display: int = 20) -> TextContent:
    """법령 변경 분석 - 안전한 패턴으로 구현"""
    search_law = law_name or "개인정보보호법"
    
    # 신구법비교로 변경사항 분석
    params = {"target": "oldAndNew", "query": search_law, "display": min(display, 50)}
    if period_start:
        params["ancYd"] = f"{period_start}~{period_end or period_start}"
    
    try:
        data = _make_legislation_request("oldAndNew", params)
        
        if isinstance(data, dict) and data.get('LawSearch'):
            items = data['LawSearch'].get('law', [])
            if items:
                analysis = f"📊 **법령 변경 분석: {search_law}**\n\n"
                analysis += f"🔍 **분석 기간**: {period_start or '전체'} ~ {period_end or '현재'}\n"
                analysis += f"📈 **총 변경 건수**: {len(items)}건\n\n"
                
                # 변경 유형별 분석
                change_types: Dict[str, int] = {}
                recent_changes: List[Dict[str, str]] = []
                
                for item in items:
                    change_type = item.get('제개정구분명', '기타')
                    change_types[change_type] = change_types.get(change_type, 0) + 1
                    
                    if len(recent_changes) < 10:
                        recent_changes.append({
                            '일자': item.get('공포일자', '미지정'),
                            '유형': change_type,
                            '내용': item.get('신구법명', '정보없음')[:50] + '...'
                        })
                
                analysis += "📋 **변경 유형별 통계:**\n"
                for change_type, count in sorted(change_types.items(), key=lambda x: x[1], reverse=True):
                    analysis += f"   - {change_type}: {count}건\n"
                
                analysis += "\n📅 **최근 주요 변경사항:**\n"
                for i, change in enumerate(recent_changes, 1):
                    analysis += f"{i}. **{change['일자']}** ({change['유형']})\n"
                    analysis += f"   - {change['내용']}\n\n"
                
                return TextContent(type="text", text=analysis)
        
        return TextContent(type="text", text=f"❌ '{search_law}' 변경사항 분석 중 오류가 발생했습니다.")
        
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령 변경 분석 중 오류: {str(e)}")

@mcp.tool(name="get_legislation_statistics", description="법령 통계를 조회합니다. 법령 수, 개정 현황, 부처별 분포 등 종합적인 법령 통계를 제공합니다.")
def get_legislation_statistics(category: Optional[str] = None, year: Optional[str] = None, display: int = 100) -> TextContent:
    """법령 통계 조회 - 안전한 패턴으로 구현"""
    search_params = {"target": "law", "display": min(display, 100)}
    
    if year:
        search_params["ancYd"] = f"{year}0101~{year}1231"
    if category:
        search_params["query"] = category
    
    try:
        data = _make_legislation_request("law", search_params)
        
        if isinstance(data, dict) and data.get('LawSearch'):
            items = data['LawSearch'].get('law', [])
            total_count = data['LawSearch'].get('totalCnt', len(items))
            
            if items:
                stats = f"📊 **법령 통계 분석**\n\n"
                stats += f"🔍 **조회 조건**: {category or '전체 법령'} ({year or '전체 기간'})\n"
                stats += f"📈 **총 법령 수**: {total_count:,}건\n\n"
                
                # 부처별 통계
                ministry_stats: Dict[str, int] = {}
                law_type_stats: Dict[str, int] = {}
                year_stats: Dict[str, int] = {}
                
                for item in items:
                    # 부처별
                    ministry = item.get('소관부처명', '미지정')
                    ministry_stats[ministry] = ministry_stats.get(ministry, 0) + 1
                    
                    # 법령 유형별
                    law_type = item.get('법령구분명', '미분류')
                    law_type_stats[law_type] = law_type_stats.get(law_type, 0) + 1
                    
                    # 연도별 (공포일자 기준)
                    enact_date = str(item.get('공포일자', ''))
                    if len(enact_date) >= 4:
                        year_key = enact_date[:4]
                        year_stats[year_key] = year_stats.get(year_key, 0) + 1
                
                # 상위 부처 통계
                stats += "🏛️ **주요 소관부처별 법령 수:**\n"
                top_ministries = sorted(ministry_stats.items(), key=lambda x: x[1], reverse=True)[:10]
                for ministry, count in top_ministries:
                    percentage = (count / len(items)) * 100
                    stats += f"   - {ministry}: {count}건 ({percentage:.1f}%)\n"
                
                # 법령 유형별 통계
                stats += "\n📋 **법령 유형별 분포:**\n"
                for law_type, count in sorted(law_type_stats.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / len(items)) * 100
                    stats += f"   - {law_type}: {count}건 ({percentage:.1f}%)\n"
                
                # 최근 5년 동향
                stats += "\n📅 **최근 연도별 동향:**\n"
                recent_years = sorted(year_stats.items(), key=lambda x: x[0], reverse=True)[:5]
                for year_key, count in recent_years:
                    stats += f"   - {year_key}년: {count}건\n"
                
                return TextContent(type="text", text=stats)
        
        return TextContent(type="text", text="❌ 법령 통계 조회 중 오류가 발생했습니다.")
        
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령 통계 조회 중 오류: {str(e)}")

@mcp.tool(name="get_law_system_info", description="법령 시스템 정보를 조회합니다. 법령 체계, 분류 구조, 시스템 현황 등의 정보를 제공합니다.")
def get_law_system_info(system_type: Optional[str] = None, display: int = 20) -> TextContent:
    """법령 시스템 정보 조회 - 안전한 패턴으로 구현"""
    
    # 체계도 정보로 시스템 구조 파악
    params = {"target": "lsStmd", "display": min(display, 50)}
    if system_type:
        params["query"] = system_type
    
    try:
        data = _make_legislation_request("lsStmd", params)
        
        system_info = f"🏗️ **법령 시스템 정보**\n\n"
        
        if isinstance(data, dict) and data.get('LawSearch'):
            items = data['LawSearch'].get('law', [])
            if items:
                system_info += f"📊 **시스템 현황**: {len(items)}개 체계도 발견\n\n"
                
                # 법령 분야별 체계 분석
                field_analysis: Dict[str, Any] = {}
                complexity_analysis = {"간단": 0, "보통": 0, "복잡": 0}
                
                system_info += "📋 **주요 법령 체계도:**\n"
                for i, item in enumerate(items[:10], 1):
                    law_name = item.get('법령명한글', item.get('법령명', f'체계도 {i}'))
                    ministry = item.get('소관부처명', '미지정')
                    enact_date = item.get('공포일자', '미지정')
                    
                    # 복잡도 추정 (법령명 길이 기준)
                    if len(law_name) < 10:
                        complexity = "간단"
                    elif len(law_name) < 20:
                        complexity = "보통"  
                    else:
                        complexity = "복잡"
                    complexity_analysis[complexity] += 1
                    
                    system_info += f"{i}. **{law_name}**\n"
                    system_info += f"   - 소관부처: {ministry}\n"
                    system_info += f"   - 공포일자: {enact_date}\n"
                    system_info += f"   - 복잡도: {complexity}\n\n"
                
                # 시스템 복잡도 분석
                system_info += "📈 **시스템 복잡도 분석:**\n"
                total = sum(complexity_analysis.values())
                if total > 0:
                    for level, count in complexity_analysis.items():
                        percentage = (count / total) * 100
                        system_info += f"   - {level}: {count}건 ({percentage:.1f}%)\n"
                
        else:
            # 기본 시스템 정보 제공
            system_info += "📋 **한국 법령 시스템 구조:**\n\n"
            system_info += "🏛️ **법령 체계:**\n"
            system_info += "   - 헌법 (최상위)\n"
            system_info += "   - 법률 (국회 제정)\n"
            system_info += "   - 대통령령 (시행령)\n"
            system_info += "   - 총리령·부령 (시행규칙)\n\n"
            
            system_info += "📚 **법령 분류:**\n"
            system_info += "   - 제1편: 헌법\n"
            system_info += "   - 제2편: 민사법\n"
            system_info += "   - 제3편: 상사법\n"
            system_info += "   - 제4편: 형사법\n"
            system_info += "   - 제5편: 행정법\n"
            system_info += "   - 기타 전문분야별 편제\n\n"
            
            system_info += "🔄 **운영 체계:**\n"
            system_info += "   - 법제처: 법령 총괄 관리\n"
            system_info += "   - 각 부처: 소관 법령 관리\n"
            system_info += "   - 국회: 법률 제정·개정\n"
            system_info += "   - 정부: 시행령·시행규칙 제정\n"
        
        return TextContent(type="text", text=system_info)
        
    except Exception as e:
        return TextContent(type="text", text=f"❌ 법령 시스템 정보 조회 중 오류: {str(e)}")

@mcp.tool(name="analyze_ministry_laws", description="부처별 법령 현황을 분석합니다. 특정 부처의 소관 법령, 개정 동향, 주요 분야를 분석하여 제공합니다.")
def analyze_ministry_laws(ministry_name: Optional[str] = None, year: Optional[str] = None, display: int = 50) -> TextContent:
    """부처별 법령 분석 - 안전한 패턴으로 구현"""
    target_ministry = ministry_name or "기획재정부"
    
    params = {"target": "law", "query": target_ministry, "display": min(display, 100)}
    if year:
        params["ancYd"] = f"{year}0101~{year}1231"
    
    try:
        data = _make_legislation_request("law", params)
        
        if isinstance(data, dict) and data.get('LawSearch'):
            items = data['LawSearch'].get('law', [])
            total_count = data['LawSearch'].get('totalCnt', len(items))
            
            if items:
                analysis = f"🏛️ **부처별 법령 분석: {target_ministry}**\n\n"
                analysis += f"📊 **총 소관 법령**: {total_count:,}건\n"
                analysis += f"🔍 **분석 대상**: {len(items)}건 (상위 표본)\n\n"
                
                # 법령 유형별 분석
                law_types: Dict[str, int] = {}
                recent_laws: List[Dict[str, str]] = []
                amendment_types: Dict[str, int] = {}
                
                for item in items:
                    # 법령 유형
                    law_type = item.get('법령구분명', '미분류')
                    law_types[law_type] = law_types.get(law_type, 0) + 1
                    
                    # 최근 법령
                    enact_date = item.get('공포일자', '')
                    if len(recent_laws) < 10 and enact_date:
                        recent_laws.append({
                            '법령명': item.get('법령명한글', '정보없음'),
                            '공포일자': enact_date,
                            '유형': law_type
                        })
                    
                    # 개정 유형
                    amendment_type = item.get('제개정구분명', '기타')
                    amendment_types[amendment_type] = amendment_types.get(amendment_type, 0) + 1
                
                # 법령 유형별 현황
                analysis += "📋 **법령 유형별 현황:**\n"
                for law_type, count in sorted(law_types.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / len(items)) * 100
                    analysis += f"   - {law_type}: {count}건 ({percentage:.1f}%)\n"
                
                # 개정 동향
                analysis += "\n🔄 **개정 동향:**\n"
                for amendment, count in sorted(amendment_types.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / len(items)) * 100
                    analysis += f"   - {amendment}: {count}건 ({percentage:.1f}%)\n"
                
                # 최근 주요 법령
                analysis += "\n📅 **최근 주요 법령:**\n"
                recent_laws.sort(key=lambda x: x['공포일자'], reverse=True)
                for i, law in enumerate(recent_laws[:8], 1):
                    analysis += f"{i}. **{law['법령명']}**\n"
                    analysis += f"   - 공포일자: {law['공포일자']}\n"
                    analysis += f"   - 유형: {law['유형']}\n\n"
                
                return TextContent(type="text", text=analysis)
        
        return TextContent(type="text", text=f"❌ '{target_ministry}' 법령 분석 중 오류가 발생했습니다.")
        
    except Exception as e:
        return TextContent(type="text", text=f"❌ 부처별 법령 분석 중 오류: {str(e)}")

logger.info("✅ 고급 법령 분석 도구 4개가 안전한 패턴으로 복구되었습니다!") 