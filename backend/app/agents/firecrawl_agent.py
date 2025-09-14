from .base_agent import BaseAgent
from firecrawl import FirecrawlApp
from app.core.config import settings
from typing import Dict, Any, List
import asyncio

class FirecrawlAgent(BaseAgent):
    """Agent responsible for web crawling and data extraction using Firecrawl"""

    def __init__(self):
        super().__init__("firecrawl_agent")
        if not settings.FIRECRAWL_API_KEY:
            raise ValueError("FIRECRAWL_API_KEY is required")
        self.client = FirecrawlApp(api_key=settings.FIRECRAWL_API_KEY)

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute web crawling for competitor websites"""
        urls = kwargs.get("urls", [])
        if not urls:
            raise ValueError("URLs are required for crawling")

        await self.log_execution(f"Starting crawl for {len(urls)} URLs")

        results = []
        for url in urls:
            try:
                # Use asyncio to make the synchronous call non-blocking
                crawl_result = await asyncio.get_event_loop().run_in_executor(
                    None, self._crawl_single_url, url
                )
                results.append({
                    "url": url,
                    "success": True,
                    "data": crawl_result
                })
                await self.log_execution(f"Successfully crawled {url}")
            except Exception as e:
                results.append({
                    "url": url,
                    "success": False,
                    "error": str(e)
                })
                await self.log_execution(f"Failed to crawl {url}: {str(e)}")

        return {
            "crawl_results": results,
            "total_urls": len(urls),
            "successful_crawls": len([r for r in results if r["success"]])
        }

    def _crawl_single_url(self, url: str) -> Dict[str, Any]:
        """Crawl a single URL using Firecrawl"""
        try:
            # Scrape with structured data extraction
            scrape_result = self.client.scrape_url(
                url=url,
                params={
                    "formats": ["markdown", "html"],
                    "includeTags": ["title", "meta", "h1", "h2", "h3", "p", "div"],
                    "onlyMainContent": True,
                    "waitFor": 3000
                }
            )

            # Extract structured data
            structured_data = self._extract_structured_data(scrape_result)

            return {
                "content": scrape_result.get("markdown", ""),
                "html": scrape_result.get("html", ""),
                "metadata": scrape_result.get("metadata", {}),
                "structured_data": structured_data
            }
        except Exception as e:
            raise Exception(f"Firecrawl error for {url}: {str(e)}")

    def _extract_structured_data(self, scrape_result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract structured business data from crawled content"""
        content = scrape_result.get("markdown", "")
        metadata = scrape_result.get("metadata", {})

        structured = {
            "title": metadata.get("title", ""),
            "description": metadata.get("description", ""),
            "keywords": metadata.get("keywords", []),
            "company_info": self._extract_company_info(content),
            "products_services": self._extract_products_services(content),
            "pricing_info": self._extract_pricing_info(content),
            "contact_info": self._extract_contact_info(content)
        }

        return structured

    def _extract_company_info(self, content: str) -> Dict[str, Any]:
        """Extract company information from content"""
        # Basic extraction logic - could be enhanced with NLP
        lines = content.lower().split('\n')
        company_info = {
            "about": "",
            "industry": "",
            "size": "",
            "founded": ""
        }

        for line in lines:
            if any(keyword in line for keyword in ["about us", "about", "company"]):
                company_info["about"] = line.strip()
            elif any(keyword in line for keyword in ["industry", "sector"]):
                company_info["industry"] = line.strip()
            elif any(keyword in line for keyword in ["founded", "established"]):
                company_info["founded"] = line.strip()

        return company_info

    def _extract_products_services(self, content: str) -> List[str]:
        """Extract products and services from content"""
        products = []
        lines = content.lower().split('\n')

        for line in lines:
            if any(keyword in line for keyword in ["products", "services", "solutions", "offerings"]):
                products.append(line.strip())

        return products[:10]  # Limit to top 10

    def _extract_pricing_info(self, content: str) -> Dict[str, Any]:
        """Extract pricing information from content"""
        pricing = {
            "has_pricing": False,
            "pricing_model": "",
            "plans": []
        }

        content_lower = content.lower()
        if any(keyword in content_lower for keyword in ["pricing", "price", "cost", "$", "€", "£"]):
            pricing["has_pricing"] = True

            # Extract pricing models
            if "subscription" in content_lower or "monthly" in content_lower:
                pricing["pricing_model"] = "subscription"
            elif "one-time" in content_lower or "purchase" in content_lower:
                pricing["pricing_model"] = "one-time"
            elif "freemium" in content_lower or "free trial" in content_lower:
                pricing["pricing_model"] = "freemium"

        return pricing

    def _extract_contact_info(self, content: str) -> Dict[str, Any]:
        """Extract contact information from content"""
        contact = {
            "email": "",
            "phone": "",
            "address": ""
        }

        # Simple regex-like extraction
        lines = content.split('\n')
        for line in lines:
            if "@" in line and "." in line:
                contact["email"] = line.strip()
            elif any(keyword in line.lower() for keyword in ["phone", "tel", "call"]):
                contact["phone"] = line.strip()
            elif any(keyword in line.lower() for keyword in ["address", "location"]):
                contact["address"] = line.strip()

        return contact