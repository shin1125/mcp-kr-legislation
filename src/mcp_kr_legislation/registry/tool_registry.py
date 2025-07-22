"""
MCP 도구 레지스트리
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field

@dataclass
class ToolInfo:
    """도구 정보를 담는 데이터클래스"""
    name: str
    korean_name: str
    description: str
    parameters: Dict[str, Any]
    linked_tools: List[str] = field(default_factory=list)

class ToolRegistry:
    """MCP 도구 레지스트리 클래스"""
    
    def __init__(self):
        self.tools: Dict[str, ToolInfo] = {}
    
    def register_tool(self, 
                     name: str, 
                     korean_name: str, 
                     description: str, 
                     parameters: Dict[str, Any], 
                     linked_tools: Optional[List[str]] = None) -> None:
        """도구를 레지스트리에 등록"""
        if linked_tools is None:
            linked_tools = []
        
        tool_info = ToolInfo(
            name=name,
            korean_name=korean_name,
            description=description,
            parameters=parameters,
            linked_tools=linked_tools
        )
        
        self.tools[name] = tool_info
    
    def get_tool(self, name: str) -> Optional[ToolInfo]:
        """도구 정보 조회"""
        return self.tools.get(name)
    
    def get_all_tools(self) -> Dict[str, ToolInfo]:
        """모든 도구 정보 조회"""
        return self.tools
    
    def get_linked_tools(self, name: str) -> List[str]:
        """연관 도구 목록 조회"""
        tool = self.get_tool(name)
        return tool.linked_tools if tool else [] 