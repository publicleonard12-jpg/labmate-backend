"""
Research Service Module - Finds and summarizes research papers
Uses arXiv API (free, no key needed) and Semantic Scholar API
"""

import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from urllib.parse import urlencode, quote
import re

class ResearchService:
    def __init__(self):
        self.arxiv_base_url = "http://export.arxiv.org/api/query"
        self.semantic_scholar_url = "https://api.semanticscholar.org/graph/v1"
    
    def search_papers(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for research papers on arXiv
        
        Args:
            query: Search query (e.g., "heat transfer chemical engineering")
            max_results: Maximum number of papers to return
        
        Returns:
            List of paper metadata
        """
        
        # Try arXiv first
        arxiv_papers = self._search_arxiv(query, max_results)
        
        # If not enough results, try Semantic Scholar
        if len(arxiv_papers) < max_results:
            semantic_papers = self._search_semantic_scholar(query, max_results - len(arxiv_papers))
            arxiv_papers.extend(semantic_papers)
        
        return arxiv_papers[:max_results]
    
    def _search_arxiv(self, query: str, max_results: int) -> List[Dict]:
        """Search arXiv API"""
        
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        
        try:
            url = f"{self.arxiv_base_url}?{urlencode(params)}"
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            
            papers = self._parse_arxiv_response(response.text)
            return papers
            
        except Exception as e:
            print(f"arXiv API Error: {e}")
            return []
    
    def _parse_arxiv_response(self, xml_text: str) -> List[Dict]:
        """Parse arXiv XML response"""
        
        papers = []
        
        try:
            root = ET.fromstring(xml_text)
            
            # arXiv uses Atom namespace
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            for entry in root.findall('atom:entry', ns):
                # Extract paper information
                paper = {
                    'source': 'arXiv',
                    'title': self._get_text(entry, 'atom:title', ns),
                    'authors': [author.find('atom:name', ns).text 
                               for author in entry.findall('atom:author', ns)],
                    'summary': self._get_text(entry, 'atom:summary', ns),
                    'published': self._get_text(entry, 'atom:published', ns),
                    'updated': self._get_text(entry, 'atom:updated', ns),
                    'url': self._get_text(entry, 'atom:id', ns),
                    'pdf_url': None,
                    'categories': []
                }
                
                # Get PDF link
                for link in entry.findall('atom:link', ns):
                    if link.get('title') == 'pdf':
                        paper['pdf_url'] = link.get('href')
                        break
                
                # Get categories
                for category in entry.findall('atom:category', ns):
                    paper['categories'].append(category.get('term'))
                
                # Clean up text
                paper['title'] = self._clean_text(paper['title'])
                paper['summary'] = self._clean_text(paper['summary'])
                
                papers.append(paper)
        
        except Exception as e:
            print(f"XML Parsing Error: {e}")
        
        return papers
    
    def _search_semantic_scholar(self, query: str, max_results: int) -> List[Dict]:
        """Search Semantic Scholar API (no key needed for basic usage)"""
        
        try:
            url = f"{self.semantic_scholar_url}/paper/search"
            params = {
                'query': query,
                'limit': max_results,
                'fields': 'title,authors,abstract,year,url,citationCount,publicationDate'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            papers = []
            
            for item in data.get('data', []):
                paper = {
                    'source': 'Semantic Scholar',
                    'title': item.get('title', ''),
                    'authors': [author.get('name', '') for author in item.get('authors', [])],
                    'summary': item.get('abstract', 'No abstract available'),
                    'published': item.get('publicationDate', ''),
                    'year': item.get('year', ''),
                    'url': item.get('url', ''),
                    'pdf_url': None,
                    'citations': item.get('citationCount', 0),
                    'categories': []
                }
                papers.append(paper)
            
            return papers
            
        except Exception as e:
            print(f"Semantic Scholar API Error: {e}")
            return []
    
    def _get_text(self, element, path: str, namespace: dict) -> str:
        """Safely get text from XML element"""
        found = element.find(path, namespace)
        return found.text if found is not None else ""
    
    def _clean_text(self, text: str) -> str:
        """Clean text by removing extra whitespace and newlines"""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def fetch_paper_text(self, paper_url: str) -> str:
        """
        Fetch full text of a paper (simplified version)
        
        Args:
            paper_url: URL to the paper (arXiv or direct link)
        
        Returns:
            Paper text (or abstract if full text unavailable)
        """
        
        # For arXiv papers, we can get the abstract easily
        if 'arxiv.org' in paper_url:
            paper_id = self._extract_arxiv_id(paper_url)
            if paper_id:
                papers = self._search_arxiv(paper_id, 1)
                if papers:
                    return papers[0].get('summary', '')
        
        # For other papers, would need more sophisticated scraping
        # Placeholder for now
        return f"[Full text extraction for {paper_url} requires additional implementation]"
    
    def _extract_arxiv_id(self, url: str) -> str:
        """Extract arXiv ID from URL"""
        match = re.search(r'(\d{4}\.\d{4,5})', url)
        return match.group(1) if match else ""
    
    def summarize_paper(self, paper_text: str, summary_type: str = "brief", 
                       ai_service=None) -> Dict[str, Any]:
        """
        Summarize a research paper
        
        Args:
            paper_text: Full text or abstract of the paper
            summary_type: 'brief' or 'detailed'
            ai_service: AIService instance for generating summaries
        
        Returns:
            Structured summary
        """
        
        if not ai_service:
            # Return basic summary without AI
            return {
                'type': summary_type,
                'summary': paper_text[:500] + "..." if len(paper_text) > 500 else paper_text,
                'note': 'AI service not available for detailed summary'
            }
        
        if summary_type == "brief":
            prompt = f"""Provide a brief summary (3-4 sentences) of this research paper:

{paper_text[:3000]}

Focus on:
1. Main research question
2. Key methodology
3. Primary findings
"""
        else:  # detailed
            prompt = f"""Provide a detailed summary of this research paper:

{paper_text[:5000]}

Include:
1. **Research Objective**: What problem is being addressed?
2. **Methodology**: How was the research conducted?
3. **Key Findings**: What were the main results?
4. **Significance**: Why does this matter?
5. **Limitations**: Any noted limitations or future work?
6. **Relevance to Students**: How can this be useful for learning?

Structure it clearly with headers."""

        messages = [
            {"role": "system", "content": "You are summarizing academic research for STEM students."},
            {"role": "user", "content": prompt}
        ]
        
        summary_text = ai_service._make_request(messages, temperature=0.5, max_tokens=2500)
        
        return {
            'type': summary_type,
            'summary': summary_text,
            'paper_length': len(paper_text)
        }
    
    def extract_key_concepts(self, paper_text: str, ai_service=None) -> List[str]:
        """
        Extract key concepts/terms from a paper
        
        Args:
            paper_text: Paper text
            ai_service: AIService instance
        
        Returns:
            List of key concepts
        """
        
        if not ai_service:
            # Simple keyword extraction without AI
            words = paper_text.lower().split()
            # This is very basic - just for demo
            common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
            keywords = [w for w in set(words) if len(w) > 5 and w not in common_words]
            return keywords[:10]
        
        prompt = f"""Extract the 10 most important technical concepts/terms from this research paper:

{paper_text[:2000]}

Return ONLY a comma-separated list of terms, no explanations."""

        messages = [
            {"role": "system", "content": "You are identifying key technical concepts."},
            {"role": "user", "content": prompt}
        ]
        
        response = ai_service._make_request(messages, temperature=0.3, max_tokens=200)
        
        # Parse comma-separated list
        concepts = [c.strip() for c in response.split(',')]
        return concepts[:10]
    
    def find_related_papers(self, paper_title: str, max_results: int = 5) -> List[Dict]:
        """
        Find papers related to a given paper
        
        Args:
            paper_title: Title of the reference paper
            max_results: Maximum number of related papers
        
        Returns:
            List of related papers
        """
        
        # Search for papers with similar topics
        return self.search_papers(paper_title, max_results)
    
    def get_paper_recommendations(self, course_code: str, topic: str, 
                                 student_level: str = "undergraduate") -> List[Dict]:
        """
        Get paper recommendations for a course topic
        
        Args:
            course_code: Course code (e.g., CH 275)
            topic: Specific topic within the course
            student_level: Academic level
        
        Returns:
            Curated list of recommended papers
        """
        
        # Build search query
        if student_level == "undergraduate":
            query = f"{topic} introduction review tutorial"
        else:
            query = f"{topic} advanced research"
        
        papers = self.search_papers(query, max_results=10)
        
        # Filter for relevance (basic filtering)
        # In production, this would be more sophisticated
        recommended = []
        for paper in papers:
            # Prefer review papers and tutorials for undergrads
            title_lower = paper['title'].lower()
            if student_level == "undergraduate":
                if any(word in title_lower for word in ['review', 'tutorial', 'introduction', 'overview']):
                    recommended.append(paper)
            else:
                recommended.append(paper)
            
            if len(recommended) >= 5:
                break
        
        return recommended
