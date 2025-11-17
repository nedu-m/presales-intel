"""
Data source integrations for enriching intelligence briefs

Add integrations as needed:
- Clearbit for company data
- SerpAPI for web search/news
- LinkedIn Sales Navigator API
- BuiltWith for tech stack
- Your CRM API
"""

import httpx
import os
from typing import Dict, Optional, List
from dotenv import load_dotenv

load_dotenv()


class DataSourceService:
    """Fetch data from various external sources"""
    
    def __init__(self):
        self.clearbit_key = os.getenv("CLEARBIT_API_KEY")
        self.serp_key = os.getenv("SERP_API_KEY")
        self.serp_base_url = "https://serpapi.com/search"
    
    async def fetch_company_data(self, company_name: str) -> Dict:
        """Fetch company information from Clearbit"""
        if not self.clearbit_key:
            return {"error": "Clearbit API key not configured"}
        
        # TODO: Implement Clearbit integration
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(
        #         f"https://company.clearbit.com/v2/companies/find?name={company_name}",
        #         headers={"Authorization": f"Bearer {self.clearbit_key}"}
        #     )
        #     return response.json()
        
        return {"error": "Clearbit integration pending"}
    
    async def search_company_news(self, company_name: str, limit: int = 5) -> Dict:
        """Search for recent company news using SerpAPI"""
        if not self.serp_key:
            return {"error": "SerpAPI key not configured"}
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Search for recent news
                params = {
                    "engine": "google",
                    "q": f"{company_name} news",
                    "api_key": self.serp_key,
                    "num": limit,
                    "tbm": "nws"  # News results
                }
                
                response = await client.get(self.serp_base_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                news_results = []
                if "news_results" in data:
                    for item in data["news_results"][:limit]:
                        news_results.append({
                            "title": item.get("title", ""),
                            "link": item.get("link", ""),
                            "source": item.get("source", ""),
                            "date": item.get("date", ""),
                            "snippet": item.get("snippet", "")
                        })
                
                return {
                    "news": news_results,
                    "count": len(news_results)
                }
                
        except httpx.HTTPStatusError as e:
            return {"error": f"SerpAPI HTTP error: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"SerpAPI error: {str(e)}"}
    
    async def search_company_info(self, company_name: str) -> Dict:
        """Search for general company information using SerpAPI"""
        if not self.serp_key:
            return {"error": "SerpAPI key not configured"}
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # General company search
                params = {
                    "engine": "google",
                    "q": f"{company_name} company",
                    "api_key": self.serp_key,
                    "num": 5
                }
                
                response = await client.get(self.serp_base_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                # Extract knowledge graph if available
                knowledge_graph = data.get("knowledge_graph", {})
                
                # Extract organic results
                organic_results = []
                if "organic_results" in data:
                    for item in data["organic_results"][:3]:
                        organic_results.append({
                            "title": item.get("title", ""),
                            "link": item.get("link", ""),
                            "snippet": item.get("snippet", "")
                        })
                
                return {
                    "knowledge_graph": knowledge_graph,
                    "organic_results": organic_results
                }
                
        except httpx.HTTPStatusError as e:
            return {"error": f"SerpAPI HTTP error: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"SerpAPI error: {str(e)}"}
    
    async def fetch_tech_stack(self, company_domain: str) -> Dict:
        """Fetch technology stack information"""
        # TODO: Implement BuiltWith or similar integration
        return {"error": "Tech stack detection pending"}

