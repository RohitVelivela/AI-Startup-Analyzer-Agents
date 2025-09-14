from app.agents import FirecrawlAgent, ComparisonAgent
from app.models.schemas import ComparisonReport, CompetitorInfo, ComparisonItem
from typing import List
from datetime import datetime

class ComparisonService:
    """Service for coordinating competitor comparisons"""

    def __init__(self):
        self.firecrawl_agent = FirecrawlAgent()
        self.comparison_agent = ComparisonAgent()

    async def compare_competitors(self, company_a_url: str, company_b_url: str) -> ComparisonReport:
        """Compare two competitors side by side"""

        # Crawl both companies
        crawl_results = await self.firecrawl_agent.execute(urls=[company_a_url, company_b_url])

        if len(crawl_results.get("crawl_results", [])) < 2:
            raise Exception("Failed to crawl both companies for comparison")

        company_a_data = None
        company_b_data = None

        for result in crawl_results["crawl_results"]:
            if result["url"] == company_a_url and result["success"]:
                company_a_data = result
            elif result["url"] == company_b_url and result["success"]:
                company_b_data = result

        if not company_a_data or not company_b_data:
            raise Exception("Failed to successfully crawl both companies")

        # Generate comparison
        comparison_results = await self.comparison_agent.execute(
            company_a_data=company_a_data,
            company_b_data=company_b_data
        )

        if not comparison_results.get("success"):
            raise Exception(f"Comparison failed: {comparison_results.get('error')}")

        comparison_data = comparison_results["comparison"]

        # Convert to response format
        company_a_info = CompetitorInfo(
            name=comparison_data["company_a"]["name"],
            url=comparison_data["company_a"]["url"],
            description=comparison_data["company_a"]["description"],
            industry=comparison_data["company_a"]["industry"]
        )

        company_b_info = CompetitorInfo(
            name=comparison_data["company_b"]["name"],
            url=comparison_data["company_b"]["url"],
            description=comparison_data["company_b"]["description"],
            industry=comparison_data["company_b"]["industry"]
        )

        # Convert feature comparisons
        feature_comparisons = []
        for feature in comparison_data.get("feature_comparison", []):
            comparison_item = ComparisonItem(
                feature=f"{feature.get('category', '')}: {feature.get('feature', '')}",
                company_a=feature.get("company_a_value", ""),
                company_b=feature.get("company_b_value", ""),
                advantage=feature.get("advantage", "tie")
            )
            feature_comparisons.append(comparison_item)

        # Generate recommendations
        recommendations = []
        if "recommendations" in comparison_data:
            recommendations.extend(comparison_data["recommendations"].get("for_company_a", []))
            recommendations.extend(comparison_data["recommendations"].get("for_company_b", []))
            recommendations.extend(comparison_data["recommendations"].get("market_opportunities", []))

        return ComparisonReport(
            company_a=company_a_info,
            company_b=company_b_info,
            feature_comparison=feature_comparisons,
            overall_assessment=comparison_data.get("overall_assessment", "Comparison completed"),
            recommendations=recommendations,
            timestamp=datetime.now()
        )