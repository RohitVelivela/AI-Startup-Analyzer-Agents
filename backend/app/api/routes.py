from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from app.models.schemas import (
    CompetitorDiscoveryRequest,
    DiscoveryResponse,
    AnalysisResponse,
    ComparisonReport,
    ExportRequest
)
from app.services.discovery_service import DiscoveryService
from app.services.analysis_service import AnalysisService
from app.services.comparison_service import ComparisonService
from app.services.export_service import ExportService
import uuid
from typing import List

api_router = APIRouter()

@api_router.post("/discover", response_model=DiscoveryResponse)
async def discover_competitors(request: CompetitorDiscoveryRequest):
    """Discover competitors based on URL or business description"""
    try:
        discovery_service = DiscoveryService()
        result = await discovery_service.discover_competitors(
            input_type=request.input_type,
            input_value=request.input_value
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/analyze", response_model=AnalysisResponse)
async def analyze_competitors(competitor_urls: List[str]):
    """Analyze competitors and generate comprehensive reports"""
    try:
        analysis_service = AnalysisService()
        result = await analysis_service.analyze_competitors(competitor_urls)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/compare", response_model=ComparisonReport)
async def compare_competitors(company_a_url: str, company_b_url: str):
    """Compare two competitors side by side"""
    try:
        comparison_service = ComparisonService()
        result = await comparison_service.compare_competitors(company_a_url, company_b_url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/export")
async def export_report(request: ExportRequest):
    """Export analysis or comparison reports as PDF or CSV"""
    try:
        export_service = ExportService()
        file_path = await export_service.export_data(
            format=request.format,
            data_type=request.data_type,
            data=request.data
        )

        filename = f"competitor_report_{uuid.uuid4()}.{request.format}"
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/octet-stream'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "AI Competitor Intelligence Platform is running"}