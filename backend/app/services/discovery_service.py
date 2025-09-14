from exa_py import Exa
from duckduckgo_search import DDGS
from app.core.config import settings
from app.models.schemas import CompetitorInfo, DiscoveryResponse
from typing import List, Dict, Any
from datetime import datetime
import asyncio
import re
from urllib.parse import urlparse

class DiscoveryService:
    """Service for discovering competitors using Exa AI and DuckDuckGo"""

    def __init__(self):
        if settings.EXA_API_KEY:
            self.exa_client = Exa(api_key=settings.EXA_API_KEY)
        else:
            self.exa_client = None
        self.ddg = DDGS()

    async def discover_competitors(self, input_type: str, input_value: str) -> DiscoveryResponse:
        """Main method to discover competitors"""

        if input_type == "url":
            competitors = await self._discover_by_url(input_value)
        elif input_type == "description":
            competitors = await self._discover_by_description(input_value)
        else:
            raise ValueError("Invalid input_type. Must be 'url' or 'description'")

        # Remove duplicates and limit results
        unique_competitors = self._deduplicate_competitors(competitors)
        limited_competitors = unique_competitors[:settings.MAX_COMPETITORS]

        return DiscoveryResponse(
            competitors=limited_competitors,
            total_found=len(limited_competitors),
            timestamp=datetime.now()
        )

    async def _discover_by_url(self, url: str) -> List[CompetitorInfo]:
        """Discover competitors based on a company URL"""
        competitors = []

        # Use Exa to find similar companies
        if self.exa_client:
            try:
                exa_competitors = await self._exa_find_similar(url)
                competitors.extend(exa_competitors)
            except Exception as e:
                print(f"Exa discovery failed: {str(e)}")

        # Use DuckDuckGo for broader search
        try:
            # Extract domain and company name for search
            domain = urlparse(url).netloc.replace("www.", "")
            company_name = domain.split(".")[0]

            ddg_competitors = await self._ddg_find_competitors(f"{company_name} competitors alternatives")
            competitors.extend(ddg_competitors)
        except Exception as e:
            print(f"DuckDuckGo discovery failed: {str(e)}")

        return competitors

    async def _discover_by_description(self, description: str) -> List[CompetitorInfo]:
        """Discover competitors based on a business description"""
        competitors = []

        # Use Exa to find companies matching the description
        if self.exa_client:
            try:
                exa_competitors = await self._exa_search_by_description(description)
                competitors.extend(exa_competitors)
            except Exception as e:
                print(f"Exa description search failed: {str(e)}")

        # Use DuckDuckGo for broader search
        try:
            search_query = f"{description} companies startups software"
            ddg_competitors = await self._ddg_find_competitors(search_query)
            competitors.extend(ddg_competitors)
        except Exception as e:
            print(f"DuckDuckGo description search failed: {str(e)}")

        return competitors

    async def _exa_find_similar(self, url: str) -> List[CompetitorInfo]:
        """Use Exa to find similar companies"""
        try:
            # Run in executor to avoid blocking
            search_results = await asyncio.get_event_loop().run_in_executor(
                None, self._exa_similar_sync, url
            )

            competitors = []
            for result in search_results.results[:5]:  # Limit Exa results
                competitor = CompetitorInfo(
                    name=self._extract_company_name(result.title),
                    url=result.url,
                    description=result.text[:200] if result.text else "",
                    industry="Unknown",
                    size="Unknown"
                )
                competitors.append(competitor)

            return competitors
        except Exception as e:
            print(f"Exa similar search error: {str(e)}")
            return []

    def _exa_similar_sync(self, url: str):
        """Synchronous Exa similar search"""
        return self.exa_client.find_similar(
            url=url,
            num_results=5,
            include_domains=[],
            exclude_domains=["wikipedia.org", "linkedin.com", "crunchbase.com"]
        )

    async def _exa_search_by_description(self, description: str) -> List[CompetitorInfo]:
        """Use Exa to search by business description"""
        try:
            # Create a search query from the description
            search_query = f"companies that {description}"

            search_results = await asyncio.get_event_loop().run_in_executor(
                None, self._exa_search_sync, search_query
            )

            competitors = []
            for result in search_results.results[:5]:  # Limit Exa results
                competitor = CompetitorInfo(
                    name=self._extract_company_name(result.title),
                    url=result.url,
                    description=result.text[:200] if result.text else "",
                    industry="Unknown",
                    size="Unknown"
                )
                competitors.append(competitor)

            return competitors
        except Exception as e:
            print(f"Exa description search error: {str(e)}")
            return []

    def _exa_search_sync(self, query: str):
        """Synchronous Exa search"""
        return self.exa_client.search(
            query=query,
            num_results=5,
            include_domains=[],
            exclude_domains=["wikipedia.org", "linkedin.com", "crunchbase.com", "facebook.com", "twitter.com"]
        )

    async def _ddg_find_competitors(self, query: str) -> List[CompetitorInfo]:
        """Use DuckDuckGo to find competitors"""
        try:
            # Run in executor to avoid blocking
            search_results = await asyncio.get_event_loop().run_in_executor(
                None, self._ddg_search_sync, query
            )

            competitors = []
            for result in search_results[:8]:  # Limit DDG results
                # Skip certain domains
                if any(domain in result["href"] for domain in ["wikipedia.org", "linkedin.com", "facebook.com", "twitter.com"]):
                    continue

                competitor = CompetitorInfo(
                    name=self._extract_company_name(result["title"]),
                    url=result["href"],
                    description=result["body"][:200] if result.get("body") else "",
                    industry="Unknown",
                    size="Unknown"
                )
                competitors.append(competitor)

            return competitors
        except Exception as e:
            print(f"DuckDuckGo search error: {str(e)}")
            return []

    def _ddg_search_sync(self, query: str) -> List[Dict[str, Any]]:
        """Synchronous DuckDuckGo search"""
        return list(self.ddg.text(query, max_results=10))

    def _extract_company_name(self, title: str) -> str:
        """Extract company name from title"""
        # Clean up common title patterns
        title = re.sub(r'\s*-\s*.*$', '', title)  # Remove everything after dash
        title = re.sub(r'\s*\|\s*.*$', '', title)  # Remove everything after pipe
        title = re.sub(r'\s*•\s*.*$', '', title)  # Remove everything after bullet
        title = title.split(':')[0]  # Take everything before colon

        # Remove common words
        stop_words = ["Inc", "Inc.", "LLC", "Ltd", "Ltd.", "Corporation", "Corp", "Company", "Co."]
        for word in stop_words:
            title = title.replace(word, "").strip()

        return title.strip()

    def _deduplicate_competitors(self, competitors: List[CompetitorInfo]) -> List[CompetitorInfo]:
        """Remove duplicate competitors based on URL domain"""
        seen_domains = set()
        unique_competitors = []

        for competitor in competitors:
            try:
                domain = urlparse(competitor.url).netloc.lower().replace("www.", "")
                if domain not in seen_domains and domain:
                    seen_domains.add(domain)
                    unique_competitors.append(competitor)
            except Exception:
                # Skip malformed URLs
                continue

        return unique_competitors