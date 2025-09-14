from .base_agent import BaseAgent
import google.generativeai as genai
from app.core.config import settings
from typing import Dict, Any, List
import json

class AnalysisAgent(BaseAgent):
    """Agent responsible for AI-powered competitor analysis using Gemini"""

    def __init__(self):
        super().__init__("analysis_agent")
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")

        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute comprehensive competitor analysis"""
        crawl_data = kwargs.get("crawl_data", [])
        if not crawl_data:
            raise ValueError("Crawl data is required for analysis")

        await self.log_execution(f"Starting analysis for {len(crawl_data)} competitors")

        analysis_results = []
        for data in crawl_data:
            if not data.get("success"):
                continue

            try:
                analysis = await self._analyze_single_competitor(data)
                analysis_results.append({
                    "url": data["url"],
                    "analysis": analysis,
                    "success": True
                })
                await self.log_execution(f"Completed analysis for {data['url']}")
            except Exception as e:
                analysis_results.append({
                    "url": data["url"],
                    "error": str(e),
                    "success": False
                })
                await self.log_execution(f"Failed analysis for {data['url']}: {str(e)}")

        # Generate summary analysis
        summary = await self._generate_summary_analysis(analysis_results)

        return {
            "competitor_analyses": analysis_results,
            "summary": summary,
            "total_analyzed": len([r for r in analysis_results if r["success"]])
        }

    async def _analyze_single_competitor(self, crawl_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single competitor using Gemini AI"""
        url = crawl_data["url"]
        content = crawl_data["data"]["content"]
        structured_data = crawl_data["data"]["structured_data"]

        analysis_prompt = self._build_analysis_prompt(url, content, structured_data)

        try:
            response = self.model.generate_content(analysis_prompt)
            analysis_text = response.text

            # Parse the structured response
            analysis = self._parse_analysis_response(analysis_text)
            return analysis

        except Exception as e:
            raise Exception(f"Gemini AI error for {url}: {str(e)}")

    def _build_analysis_prompt(self, url: str, content: str, structured_data: Dict[str, Any]) -> str:
        """Build a comprehensive analysis prompt for Gemini"""
        prompt = f"""
        Analyze the following competitor company and provide a comprehensive business intelligence report.

        Company URL: {url}
        Company Title: {structured_data.get('title', 'N/A')}
        Company Description: {structured_data.get('description', 'N/A')}

        Website Content:
        {content[:4000]}  # Limit content to avoid token limits

        Structured Data:
        {json.dumps(structured_data, indent=2)[:2000]}

        Please provide a detailed analysis in the following JSON format:
        {{
            "company_name": "string",
            "industry": "string",
            "company_size": "string (startup/small/medium/large/enterprise)",
            "target_market": "string",
            "strengths": ["list of key strengths"],
            "weaknesses": ["list of potential weaknesses"],
            "pricing_strategy": {{
                "model": "string (freemium/subscription/one-time/enterprise/custom)",
                "positioning": "string (budget/mid-market/premium/luxury)",
                "transparency": "string (transparent/hidden/complex)"
            }},
            "market_position": "string (leader/challenger/follower/niche)",
            "key_differentiators": ["list of unique value propositions"],
            "growth_opportunities": ["list of potential growth areas"],
            "market_gaps": ["list of market gaps this company could fill"],
            "competitive_threats": ["list of potential threats"],
            "business_model": "string",
            "technology_stack": ["list of identified technologies"],
            "marketing_strategy": "string",
            "customer_focus": "string"
        }}

        Important: Respond ONLY with valid JSON. Do not include any explanatory text before or after the JSON.
        """
        return prompt

    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """Parse the AI response into structured data"""
        try:
            # Clean the response text
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            analysis = json.loads(response_text.strip())

            # Validate required fields
            required_fields = [
                "company_name", "industry", "strengths", "weaknesses",
                "pricing_strategy", "market_position", "key_differentiators",
                "growth_opportunities", "market_gaps"
            ]

            for field in required_fields:
                if field not in analysis:
                    analysis[field] = "Not available"

            return analysis

        except json.JSONDecodeError as e:
            # Fallback: create a basic analysis structure
            return {
                "company_name": "Unknown",
                "industry": "Not identified",
                "strengths": ["Analysis failed"],
                "weaknesses": ["Unable to determine"],
                "pricing_strategy": {"model": "unknown", "positioning": "unknown", "transparency": "unknown"},
                "market_position": "unknown",
                "key_differentiators": ["Unable to analyze"],
                "growth_opportunities": ["Analysis incomplete"],
                "market_gaps": ["Analysis incomplete"],
                "error": f"Failed to parse AI response: {str(e)}"
            }

    async def _generate_summary_analysis(self, analysis_results: List[Dict[str, Any]]) -> str:
        """Generate a summary analysis across all competitors"""
        successful_analyses = [r for r in analysis_results if r["success"]]

        if not successful_analyses:
            return "No successful analyses to summarize."

        summary_prompt = f"""
        Based on the following competitor analyses, provide a strategic market overview and insights.

        Number of competitors analyzed: {len(successful_analyses)}

        Competitor Data:
        {json.dumps([r["analysis"] for r in successful_analyses], indent=2)[:3000]}

        Please provide a strategic summary covering:
        1. Market landscape overview
        2. Common strengths across competitors
        3. Common weaknesses and market gaps
        4. Pricing trends and strategies
        5. Key opportunities for market entry or differentiation
        6. Competitive threats and challenges

        Keep the summary concise but insightful (300-500 words).
        """

        try:
            response = self.model.generate_content(summary_prompt)
            return response.text
        except Exception as e:
            return f"Failed to generate summary analysis: {str(e)}"