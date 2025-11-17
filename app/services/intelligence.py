import os
from datetime import datetime
from typing import Optional, Dict
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class IntelligenceService:
    """Service for generating intelligence briefs using GPT-4"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4-turbo-preview"
    
    async def generate_brief(
        self,
        company_name: str,
        meeting_date: Optional[datetime] = None,
        attendees: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generate a comprehensive intelligence brief for a presales meeting
        
        Returns:
            Dict with sections: company_context, attendee_analysis, tech_stack,
            competitive_landscape, suggested_questions, full_brief
        """
        
        # Build context for the prompt
        context = f"Company: {company_name}\n"
        if meeting_date:
            context += f"Meeting Date: {meeting_date.strftime('%Y-%m-%d')}\n"
        if attendees:
            context += f"Attendees: {attendees}\n"
        
        prompt = f"""You are a presales intelligence analyst. Generate a comprehensive brief for an upcoming meeting.

{context}

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
        """Parse the brief into sections (simple implementation)"""
        # For MVP, just return the full text for each section
        # In production, you'd use structured outputs or better parsing
        return {
            "company_context": brief_text,
            "attendee_analysis": "",
            "tech_stack": "",
            "competitive_landscape": "",
            "suggested_questions": ""
        }

