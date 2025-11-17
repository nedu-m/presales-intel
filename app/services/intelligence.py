import os
import re
from typing import Optional, Dict
from openai import OpenAI
from dotenv import load_dotenv
from app.services.data_sources import DataSourceService

load_dotenv()


class IntelligenceService:
    """Service for generating intelligence briefs using GPT-4"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4-turbo-preview"
        self.data_service = DataSourceService()
    
    async def generate_brief(
        self,
        company_name: str,
        attendees: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generate a comprehensive intelligence brief for a presales meeting
        
        Returns:
            Dict with sections: company_context, attendee_analysis, tech_stack,
            competitive_landscape, suggested_questions, full_brief
        """
        
        # Fetch real-time data
        company_info = await self.data_service.search_company_info(company_name)
        news_data = await self.data_service.search_company_news(company_name)
        
        # Build context for the prompt
        context = f"Company: {company_name}\n"
        if attendees:
            context += f"Attendees: {attendees}\n"
        
        # Add real-time data context
        enrichment = "\n\n## Real-time Research Data:\n\n"
        
        # Add company info from knowledge graph
        if company_info.get("knowledge_graph"):
            kg = company_info["knowledge_graph"]
            enrichment += "### Company Overview (from Google Knowledge Graph):\n"
            if kg.get("description"):
                enrichment += f"- Description: {kg['description']}\n"
            if kg.get("type"):
                enrichment += f"- Type: {kg['type']}\n"
            if kg.get("founded"):
                enrichment += f"- Founded: {kg['founded']}\n"
            if kg.get("headquarters"):
                enrichment += f"- Headquarters: {kg['headquarters']}\n"
            enrichment += "\n"
        
        # Add recent news
        if news_data.get("news") and len(news_data["news"]) > 0:
            enrichment += "### Recent News:\n"
            for news_item in news_data["news"]:
                enrichment += f"- **{news_item['title']}**\n"
                if news_item.get('date'):
                    enrichment += f"  Date: {news_item['date']}\n"
                if news_item.get('snippet'):
                    enrichment += f"  {news_item['snippet']}\n"
                enrichment += "\n"
        
        prompt = f"""You are a presales intelligence analyst. Generate a comprehensive brief for an upcoming meeting.

{context}
{enrichment}

Use the real-time research data provided above to inform your analysis. Be specific and cite recent developments when relevant.

Generate a detailed intelligence brief with the following sections:

1. COMPANY CONTEXT
- Brief company overview
- Recent news and developments
- Business priorities and challenges
- Industry position

2. ATTENDEE ANALYSIS (if attendees provided)
- Role and background of each attendee
- Likely priorities and concerns
- Best approach for engagement

3. TECH STACK & SECURITY POSTURE
- Known technologies in use
- Potential security gaps or vulnerabilities
- Modernization needs

4. COMPETITIVE LANDSCAPE
- Current vendors/solutions they likely use
- Competitive positioning
- Key differentiators to emphasize

5. SUGGESTED QUESTIONS & TALKING POINTS
- Discovery questions to ask
- Likely objections and how to address them
- Value propositions to emphasize
- Topics to avoid

Format the output as clear, scannable markdown. Be specific and actionable. Focus on what a presales engineer needs to know to run an effective technical discovery call."""

        # Call OpenAI
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a presales intelligence analyst who generates comprehensive, actionable meeting briefs."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096,
            temperature=0.7
        )
        
        full_brief = response.choices[0].message.content
        
        # Parse sections (basic parsing for now)
        sections = self._parse_sections(full_brief)
        
        return {
            "company_context": sections.get("company_context", ""),
            "attendee_analysis": sections.get("attendee_analysis", ""),
            "tech_stack": sections.get("tech_stack", ""),
            "competitive_landscape": sections.get("competitive_landscape", ""),
            "suggested_questions": sections.get("suggested_questions", ""),
            "full_brief": full_brief
        }
    
    def _parse_sections(self, brief_text: str) -> Dict[str, str]:
        """Parse the markdown brief into its major sections."""
        alias_map = {
            "company context": "company_context",
            "company overview": "company_context",
            "attendee analysis": "attendee_analysis",
            "attendees": "attendee_analysis",
            "personas": "attendee_analysis",
            "tech stack": "tech_stack",
            "security posture": "tech_stack",
            "technical landscape": "tech_stack",
            "competitive landscape": "competitive_landscape",
            "competition": "competitive_landscape",
            "competitors": "competitive_landscape",
            "suggested questions": "suggested_questions",
            "talking points": "suggested_questions",
            "discovery questions": "suggested_questions"
        }
        section_keys = [
            "company_context",
            "attendee_analysis",
            "tech_stack",
            "competitive_landscape",
            "suggested_questions"
        ]
        buffers = {key: [] for key in section_keys}
        current_key = "company_context"
        lines = brief_text.splitlines()

        for raw_line in lines:
            stripped = raw_line.strip()

            if stripped.startswith("#"):
                heading_text = stripped.lstrip("#").strip()
                heading_text = re.sub(r"^[\d\.\)]*\s*", "", heading_text)
                normalized = heading_text.lower().replace("&", "and")
                normalized = normalized.split("(")[0].strip()

                matched_key = None
                for alias, target in alias_map.items():
                    if alias in normalized:
                        matched_key = target
                        break

                if matched_key:
                    current_key = matched_key
                    continue
                elif current_key:
                    buffers[current_key].append(raw_line)
                    continue
                else:
                    continue

            if current_key:
                buffers[current_key].append(raw_line)
            else:
                buffers["company_context"].append(raw_line)

        parsed = {key: "\n".join(value).strip() for key, value in buffers.items()}
        if not parsed["company_context"]:
            parsed["company_context"] = brief_text.strip()
        return parsed

