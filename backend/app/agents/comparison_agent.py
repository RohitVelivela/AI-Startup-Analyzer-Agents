from .base_agent import BaseAgent
import google.generativeai as genai
from app.core.config import settings
from typing import Dict, Any, List
import json

class ComparisonAgent(BaseAgent):
    """Agent responsible for side-by-side competitor comparisons"""

    def __init__(self):
        super().__init__("comparison_agent")
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")

        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute side-by-side competitor comparison"""
        company_a_data = kwargs.get("company_a_data")
        company_b_data = kwargs.get("company_b_data")

        if not company_a_data or not company_b_data:
            raise ValueError("Both company data sets are required for comparison")

        await self.log_execution(f"Comparing {company_a_data.get('url')} vs {company_b_data.get('url')}")

        try:
            comparison = await self._generate_comparison(company_a_data, company_b_data)
            return {
                "comparison": comparison,
                "success": True
            }
        except Exception as e:
            await self.log_execution(f"Comparison failed: {str(e)}")
            return {
                "error": str(e),
                "success": False
            }

    async def _generate_comparison(self, company_a_data: Dict[str, Any], company_b_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive comparison between two companies"""

        comparison_prompt = self._build_comparison_prompt(company_a_data, company_b_data)

        try:
            response = self.model.generate_content(comparison_prompt)
            comparison_text = response.text

            # Parse the structured response
            comparison = self._parse_comparison_response(comparison_text)
            return comparison

        except Exception as e:
            raise Exception(f"Gemini AI comparison error: {str(e)}")

    def _build_comparison_prompt(self, company_a_data: Dict[str, Any], company_b_data: Dict[str, Any]) -> str:
        """Build a comprehensive comparison prompt"""

        # Extract relevant data
        company_a_content = company_a_data.get("data", {}).get("content", "")[:2000]
        company_b_content = company_b_data.get("data", {}).get("content", "")[:2000]

        company_a_structured = company_a_data.get("data", {}).get("structured_data", {})
        company_b_structured = company_b_data.get("data", {}).get("structured_data", {})

        prompt = f"""
        Compare the following two companies and provide a detailed side-by-side analysis.

        COMPANY A:
        URL: {company_a_data.get('url')}
        Title: {company_a_structured.get('title', 'N/A')}
        Description: {company_a_structured.get('description', 'N/A')}
        Content: {company_a_content}

        COMPANY B:
        URL: {company_b_data.get('url')}
        Title: {company_b_structured.get('title', 'N/A')}
        Description: {company_b_structured.get('description', 'N/A')}
        Content: {company_b_content}

        Provide a comprehensive comparison in the following JSON format:
        {{
            "company_a": {{
                "name": "string",
                "url": "string",
                "industry": "string",
                "description": "string"
            }},
            "company_b": {{
                "name": "string",
                "url": "string",
                "industry": "string",
                "description": "string"
            }},
            "feature_comparison": [
                {{
                    "category": "string",
                    "feature": "string",
                    "company_a_value": "string",
                    "company_b_value": "string",
                    "advantage": "company_a|company_b|tie",
                    "explanation": "string"
                }}
            ],
            "strengths_comparison": {{
                "company_a_strengths": ["list of strengths"],
                "company_b_strengths": ["list of strengths"],
                "unique_to_a": ["strengths unique to company A"],
                "unique_to_b": ["strengths unique to company B"]
            }},
            "weaknesses_comparison": {{
                "company_a_weaknesses": ["list of weaknesses"],
                "company_b_weaknesses": ["list of weaknesses"],
                "common_weaknesses": ["weaknesses both share"]
            }},
            "pricing_comparison": {{
                "company_a_pricing": {{
                    "model": "string",
                    "positioning": "string",
                    "transparency": "string"
                }},
                "company_b_pricing": {{
                    "model": "string",
                    "positioning": "string",
                    "transparency": "string"
                }},
                "pricing_advantage": "company_a|company_b|tie",
                "pricing_analysis": "string"
            }},
            "market_positioning": {{
                "company_a_position": "string",
                "company_b_position": "string",
                "positioning_analysis": "string"
            }},
            "competitive_dynamics": {{
                "direct_competitors": "boolean",
                "competition_level": "high|medium|low",
                "competitive_overlap": "percentage or description"
            }},
            "overall_assessment": "string (300-500 words)",
            "recommendations": {{
                "for_company_a": ["list of recommendations"],
                "for_company_b": ["list of recommendations"],
                "market_opportunities": ["list of opportunities"]
            }}
        }}

        Focus on key business dimensions: products/services, pricing, market positioning, target audience, technology, marketing approach, competitive advantages, and growth potential.

        Important: Respond ONLY with valid JSON. Do not include explanatory text before or after the JSON.
        """
        return prompt

    def _parse_comparison_response(self, response_text: str) -> Dict[str, Any]:
        """Parse the AI comparison response into structured data"""
        try:
            # Clean the response text
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            comparison = json.loads(response_text.strip())

            # Validate and provide defaults for required fields
            if "company_a" not in comparison:
                comparison["company_a"] = {"name": "Company A", "url": "", "industry": "Unknown", "description": ""}
            if "company_b" not in comparison:
                comparison["company_b"] = {"name": "Company B", "url": "", "industry": "Unknown", "description": ""}
            if "feature_comparison" not in comparison:
                comparison["feature_comparison"] = []
            if "overall_assessment" not in comparison:
                comparison["overall_assessment"] = "Comparison analysis unavailable"
            if "recommendations" not in comparison:
                comparison["recommendations"] = {
                    "for_company_a": [],
                    "for_company_b": [],
                    "market_opportunities": []
                }

            return comparison

        except json.JSONDecodeError as e:
            # Fallback: create a basic comparison structure
            return {
                "company_a": {"name": "Company A", "url": "", "industry": "Unknown", "description": ""},
                "company_b": {"name": "Company B", "url": "", "industry": "Unknown", "description": ""},
                "feature_comparison": [],
                "strengths_comparison": {
                    "company_a_strengths": [],
                    "company_b_strengths": [],
                    "unique_to_a": [],
                    "unique_to_b": []
                },
                "weaknesses_comparison": {
                    "company_a_weaknesses": [],
                    "company_b_weaknesses": [],
                    "common_weaknesses": []
                },
                "pricing_comparison": {
                    "company_a_pricing": {"model": "unknown", "positioning": "unknown", "transparency": "unknown"},
                    "company_b_pricing": {"model": "unknown", "positioning": "unknown", "transparency": "unknown"},
                    "pricing_advantage": "tie",
                    "pricing_analysis": "Unable to analyze pricing"
                },
                "market_positioning": {
                    "company_a_position": "unknown",
                    "company_b_position": "unknown",
                    "positioning_analysis": "Unable to analyze positioning"
                },
                "competitive_dynamics": {
                    "direct_competitors": False,
                    "competition_level": "unknown",
                    "competitive_overlap": "Unable to determine"
                },
                "overall_assessment": f"Failed to generate comparison analysis: {str(e)}",
                "recommendations": {
                    "for_company_a": ["Analysis incomplete"],
                    "for_company_b": ["Analysis incomplete"],
                    "market_opportunities": ["Analysis incomplete"]
                },
                "error": f"Failed to parse AI response: {str(e)}"
            }