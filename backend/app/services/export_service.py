import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from typing import Dict, Any
import tempfile
import os
from datetime import datetime

class ExportService:
    """Service for exporting analysis and comparison reports"""

    def __init__(self):
        self.styles = getSampleStyleSheet()

    async def export_data(self, format: str, data_type: str, data: Dict[str, Any]) -> str:
        """Export data in the specified format"""
        if format.lower() == "pdf":
            return await self._export_pdf(data_type, data)
        elif format.lower() == "csv":
            return await self._export_csv(data_type, data)
        else:
            raise ValueError("Unsupported export format. Use 'pdf' or 'csv'")

    async def _export_pdf(self, data_type: str, data: Dict[str, Any]) -> str:
        """Export data as PDF"""
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_file.close()

        doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
        story = []

        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Center alignment
        )

        if data_type == "analysis":
            story.append(Paragraph("Competitor Analysis Report", title_style))
            story.append(Spacer(1, 12))
            self._add_analysis_content_to_pdf(story, data)
        elif data_type == "comparison":
            story.append(Paragraph("Competitor Comparison Report", title_style))
            story.append(Spacer(1, 12))
            self._add_comparison_content_to_pdf(story, data)

        # Add timestamp
        story.append(Spacer(1, 24))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", self.styles['Normal']))

        doc.build(story)
        return temp_file.name

    async def _export_csv(self, data_type: str, data: Dict[str, Any]) -> str:
        """Export data as CSV"""
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        temp_file.close()

        if data_type == "analysis":
            df = self._create_analysis_dataframe(data)
        elif data_type == "comparison":
            df = self._create_comparison_dataframe(data)
        else:
            raise ValueError("Unsupported data type for CSV export")

        df.to_csv(temp_file.name, index=False)
        return temp_file.name

    def _add_analysis_content_to_pdf(self, story: list, data: Dict[str, Any]):
        """Add analysis content to PDF story"""
        reports = data.get("reports", [])

        for i, report in enumerate(reports):
            # Company header
            story.append(Paragraph(f"Company {i+1}: {report['competitor']['name']}", self.styles['Heading2']))
            story.append(Paragraph(f"URL: {report['competitor']['url']}", self.styles['Normal']))
            story.append(Paragraph(f"Industry: {report['competitor']['industry']}", self.styles['Normal']))
            story.append(Spacer(1, 12))

            # Strengths
            story.append(Paragraph("Strengths:", self.styles['Heading3']))
            for strength in report.get("strengths", []):
                story.append(Paragraph(f"• {strength}", self.styles['Normal']))
            story.append(Spacer(1, 8))

            # Weaknesses
            story.append(Paragraph("Weaknesses:", self.styles['Heading3']))
            for weakness in report.get("weaknesses", []):
                story.append(Paragraph(f"• {weakness}", self.styles['Normal']))
            story.append(Spacer(1, 8))

            # Market Position
            story.append(Paragraph("Market Position:", self.styles['Heading3']))
            story.append(Paragraph(report.get("market_position", "Unknown"), self.styles['Normal']))
            story.append(Spacer(1, 8))

            # Key Differentiators
            story.append(Paragraph("Key Differentiators:", self.styles['Heading3']))
            for diff in report.get("key_differentiators", []):
                story.append(Paragraph(f"• {diff}", self.styles['Normal']))

            story.append(Spacer(1, 24))

        # Summary
        if data.get("summary"):
            story.append(Paragraph("Executive Summary", self.styles['Heading2']))
            story.append(Paragraph(data["summary"], self.styles['Normal']))

    def _add_comparison_content_to_pdf(self, story: list, data: Dict[str, Any]):
        """Add comparison content to PDF story"""
        # Company information
        story.append(Paragraph("Companies Compared", self.styles['Heading2']))
        story.append(Paragraph(f"Company A: {data['company_a']['name']} ({data['company_a']['url']})", self.styles['Normal']))
        story.append(Paragraph(f"Company B: {data['company_b']['name']} ({data['company_b']['url']})", self.styles['Normal']))
        story.append(Spacer(1, 12))

        # Feature comparison table
        if data.get("feature_comparison"):
            story.append(Paragraph("Feature Comparison", self.styles['Heading3']))

            # Create table data
            table_data = [["Feature", "Company A", "Company B", "Advantage"]]
            for feature in data["feature_comparison"]:
                table_data.append([
                    feature["feature"],
                    feature["company_a"],
                    feature["company_b"],
                    feature["advantage"]
                ])

            # Create table
            table = Table(table_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            story.append(table)
            story.append(Spacer(1, 12))

        # Overall assessment
        if data.get("overall_assessment"):
            story.append(Paragraph("Overall Assessment", self.styles['Heading3']))
            story.append(Paragraph(data["overall_assessment"], self.styles['Normal']))
            story.append(Spacer(1, 12))

        # Recommendations
        if data.get("recommendations"):
            story.append(Paragraph("Recommendations", self.styles['Heading3']))
            for rec in data["recommendations"]:
                story.append(Paragraph(f"• {rec}", self.styles['Normal']))

    def _create_analysis_dataframe(self, data: Dict[str, Any]) -> pd.DataFrame:
        """Create DataFrame from analysis data"""
        rows = []

        for report in data.get("reports", []):
            competitor = report["competitor"]

            # Create a row with flattened data
            row = {
                "Company Name": competitor["name"],
                "URL": competitor["url"],
                "Industry": competitor["industry"],
                "Market Position": report.get("market_position", ""),
                "Strengths": "; ".join(report.get("strengths", [])),
                "Weaknesses": "; ".join(report.get("weaknesses", [])),
                "Key Differentiators": "; ".join(report.get("key_differentiators", [])),
                "Growth Opportunities": "; ".join(report.get("growth_opportunities", [])),
                "Market Gaps": "; ".join(report.get("market_gaps", []))
            }

            # Add pricing strategy if available
            pricing = report.get("pricing_strategy", {})
            if pricing:
                row["Pricing Model"] = pricing.get("model", "")
                row["Pricing Positioning"] = pricing.get("positioning", "")
                row["Pricing Transparency"] = pricing.get("transparency", "")

            rows.append(row)

        return pd.DataFrame(rows)

    def _create_comparison_dataframe(self, data: Dict[str, Any]) -> pd.DataFrame:
        """Create DataFrame from comparison data"""
        rows = []

        # Basic company info
        basic_row = {
            "Metric": "Company Information",
            "Company A": f"{data['company_a']['name']} ({data['company_a']['industry']})",
            "Company B": f"{data['company_b']['name']} ({data['company_b']['industry']})",
            "Advantage": "N/A"
        }
        rows.append(basic_row)

        # Feature comparisons
        for feature in data.get("feature_comparison", []):
            row = {
                "Metric": feature["feature"],
                "Company A": feature["company_a"],
                "Company B": feature["company_b"],
                "Advantage": feature["advantage"]
            }
            rows.append(row)

        return pd.DataFrame(rows)