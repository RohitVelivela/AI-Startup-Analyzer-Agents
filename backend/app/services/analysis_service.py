from app.agents import AgentOrchestrator, FirecrawlAgent, AnalysisAgent
from app.models.schemas import AnalysisResponse, AnalysisReport, CompetitorInfo
from typing import List
from datetime import datetime
import asyncio

class AnalysisService:
    """Service for coordinating competitor analysis using AI agents"""

    def __init__(self):
        self.orchestrator = AgentOrchestrator()

        # Register agents
        self.firecrawl_agent = FirecrawlAgent()
        self.analysis_agent = AnalysisAgent()

        self.orchestrator.register_agent(self.firecrawl_agent)
        self.orchestrator.register_agent(self.analysis_agent)

    async def analyze_competitors(self, competitor_urls: List[str]) -> AnalysisResponse:
        """Analyze a list of competitor URLs"""

        # Define workflow for analysis
        workflow = [
            {
                "agent": "firecrawl_agent",
                "action": "crawl",
                "params": {"urls": competitor_urls}
            },
            {
                "agent": "analysis_agent",
                "action": "analyze",
                "params": {}  # Will use crawl results
            }
        ]

        # Execute crawling first
        crawl_results = await self.firecrawl_agent.execute(urls=competitor_urls)

        if not crawl_results.get("crawl_results"):
            raise Exception("No crawl results available for analysis")

        # Execute analysis with crawl data
        analysis_results = await self.analysis_agent.execute(
            crawl_data=crawl_results["crawl_results"]
        )

        # Convert to response format
        reports = []
        for analysis in analysis_results.get("competitor_analyses", []):
            if not analysis.get("success"):
                continue

            # Create competitor info from analysis
            analysis_data = analysis["analysis"]
            competitor_info = CompetitorInfo(
                name=analysis_data.get("company_name", "Unknown"),
                url=analysis["url"],
                description=analysis_data.get("business_model", ""),
                industry=analysis_data.get("industry", "Unknown"),
                size=analysis_data.get("company_size", "Unknown")
            )

            # Create analysis report
            report = AnalysisReport(
                competitor=competitor_info,
                strengths=analysis_data.get("strengths", []),
                weaknesses=analysis_data.get("weaknesses", []),
                pricing_strategy=analysis_data.get("pricing_strategy", {}),
                market_position=analysis_data.get("market_position", "Unknown"),
                growth_opportunities=analysis_data.get("growth_opportunities", []),
                market_gaps=analysis_data.get("market_gaps", []),
                key_differentiators=analysis_data.get("key_differentiators", []),
                timestamp=datetime.now()
            )
            reports.append(report)

        return AnalysisResponse(
            reports=reports,
            summary=analysis_results.get("summary", "Analysis completed"),
            timestamp=datetime.now()
        )