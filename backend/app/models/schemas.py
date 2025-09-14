from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Any, Optional
from datetime import datetime

class CompetitorDiscoveryRequest(BaseModel):
    input_type: str  # "url" or "description"
    input_value: str

class CompetitorInfo(BaseModel):
    name: str
    url: str
    description: str
    industry: str
    size: Optional[str] = None
    founded: Optional[str] = None

class AnalysisReport(BaseModel):
    competitor: CompetitorInfo
    strengths: List[str]
    weaknesses: List[str]
    pricing_strategy: Dict[str, Any]
    market_position: str
    growth_opportunities: List[str]
    market_gaps: List[str]
    key_differentiators: List[str]
    timestamp: datetime

class ComparisonItem(BaseModel):
    feature: str
    company_a: str
    company_b: str
    advantage: str  # "company_a", "company_b", or "tie"

class ComparisonReport(BaseModel):
    company_a: CompetitorInfo
    company_b: CompetitorInfo
    feature_comparison: List[ComparisonItem]
    overall_assessment: str
    recommendations: List[str]
    timestamp: datetime

class DiscoveryResponse(BaseModel):
    competitors: List[CompetitorInfo]
    total_found: int
    timestamp: datetime

class AnalysisResponse(BaseModel):
    reports: List[AnalysisReport]
    summary: str
    timestamp: datetime

class ExportRequest(BaseModel):
    format: str  # "pdf" or "csv"
    data_type: str  # "analysis" or "comparison"
    data: Dict[str, Any]