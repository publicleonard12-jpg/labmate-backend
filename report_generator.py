"""
Report Generator Module - Creates formatted lab reports
"""

from typing import Dict, Any, List
from datetime import datetime
import random
import hashlib

class ReportGenerator:
    def __init__(self, ai_service):
        self.ai_service = ai_service
        self.citation_pool = self._initialize_citation_pool()
    
    def _initialize_citation_pool(self) -> Dict:
        """Initialize pool of realistic citations for variation"""
        return {
            'general_chemistry': [
                'Sharma et al., 2022', 'Skoog et al., 2022', 'Ahmad et al., 2023',
                'Berasarte et al., 2024', 'Mallick, 2025', 'Gandhi et al., 2022',
                'Efe et al., 2023', 'Korbag et al., 2022', 'Raviolo et al., 2021',
                'Varadarajan et al., 2021', 'Onuegbu et al., 2023', 'Salame, 2022',
                'Qarah et al., 2023', 'Chen and Liu, 2023', 'Patel, 2022'
            ]
        }
    
    def _generate_variation_seed(self, data: Dict) -> str:
        seed_string = f"{data.get('student_id', '')}{data.get('title', '')}"
        return hashlib.md5(seed_string.encode()).hexdigest()[:8]
    
    def _select_citations(self, category: str, count: int, seed: str) -> List[str]:
        random.seed(seed)
        pool = self.citation_pool.get(category, self.citation_pool['general_chemistry'])
        if count > len(pool):
            pool = pool * (count // len(pool) + 1)
        selected = random.sample(pool, min(count, len(pool)))
        random.seed()
        return selected
    
    def generate_full_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        variation_seed = self._generate_variation_seed(data)
        
        report = {
            'title': data.get('title', ''),
            'course_code': data.get('course_code', ''),
            'course_name': data.get('course_name', 'Chemistry Laboratory Practice'),
            'student_name': data.get('student_name', '[Student Name]'),
            'student_id': data.get('student_id', '[Student ID]'),
            'group_number': data.get('group_number', ''),
            'lecturer': data.get('lecturer', '[Course Lecturer]'),
            'date': data.get('date', datetime.now().strftime('%Y-%m-%d')),
            'sections': {}
        }
        
        report['sections']['introduction'] = self._generate_introduction(
            data.get('title', ''), data.get('objective', ''), 
            data.get('course_code', ''), variation_seed
        )
        
        report['sections']['theory'] = self._generate_theory(
            data.get('title', ''), data.get('objective', '')
        )
        
        report['sections']['materials'] = self._format_materials(data.get('materials', []))
        report['sections']['procedure'] = data.get('procedure', '')
        report['sections']['discussion'] = self._generate_discussion(
            data.get('title', ''), data.get('objective', ''), 
            data.get('observations', ''), []
        )
        report['sections']['conclusion'] = self._generate_conclusion(
            data.get('title', ''), data.get('objective', ''), 
            data.get('observations', '')
        )
        report['sections']['references'] = self._generate_references()
        
        return report
    
    def _generate_introduction(self, title: str, objective: str, 
                              course_code: str, variation_seed: str = None) -> str:
        citations = self._select_citations('general_chemistry', 12, variation_seed or 'default')
        
        prompt = f"""Write CHAPTER 1: INTRODUCTION for a UMAT Chemical Engineering lab report.

Experiment: {title}
Course: {course_code}

Include 10-12 Harvard citations throughout using these: {', '.join(citations)}

Structure:
1. Define technique with citation
2. Applications in 3-4 fields, each with citation
3. Key formula with citation
4. Modern approaches with citation
5. Safety with citation
6. Aim of this experiment
7. Chemical equations with citations

Write 450-550 words, formal tone, third person."""

        messages = [
            {"role": "system", "content": "You write UMAT Chemical Engineering lab reports."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.7, max_tokens=3000)
    
    def _generate_theory(self, title: str, objective: str) -> str:
        prompt = f"""Provide theoretical background for: {title}
Include chemical equations with state symbols and citations.
Write 200-300 words."""

        messages = [
            {"role": "system", "content": "You explain theory for UMAT reports."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.5, max_tokens=2000)
    
    def _format_materials(self, materials: List) -> str:
        if isinstance(materials, list):
            return '\n'.join(materials)
        return str(materials)
    
    def _generate_discussion(self, title: str, objective: str, 
                           observations: str, data: List[Dict]) -> str:
        prompt = f"""Write RESULTS AND DISCUSSION for: {title}

Include:
1. What was done
2. Results analysis
3. Error sources with citations
Write 400-500 words."""

        messages = [
            {"role": "system", "content": "You analyze results for UMAT reports."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.6, max_tokens=3000)
    
    def _generate_conclusion(self, title: str, objective: str, observations: str) -> str:
        prompt = f"""Write conclusion for: {title}
Summarize findings, whether objectives met, significance.
Write 100-150 words."""

        messages = [
            {"role": "system", "content": "You conclude UMAT reports."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.6, max_tokens=1000)
    
    def _generate_references(self) -> str:
        return """Ahmad, S. et al., 'Analyzing total alkalinity in marine environments', Marine Science Journal, 12(4), 2023, pp. 88-95.

Berasarte, M. et al., 'Standardization and use of titrants', in Goyal, A. and Kumar, H. (eds.) Advanced Techniques of Analytical Chemistry. Vol. 1. Singapore: Bentham Science Publishers, 2024, pp. 100-115.

Efe, O. et al., Foundations of Chemical Reactions. Lagos: Academic Press, 2023.

Gandhi, P. et al., Safety and Risk Management in Chemical Laboratories. 3rd edn. Mumbai: Scientific Publications, 2022.

Mallick, T., Analytical Methods in Chemistry. 2nd edn. New Delhi: Tech Science Press, 2025.

Sharma, S. et al., 'Analytical techniques in modern chemistry', in Goyal, A. and Kumar, H. (eds.) Advanced Techniques of Analytical Chemistry. Vol. 1. Singapore: Bentham Science Publishers, 2022, pp. 18-42."""
    
    def refine_section(self, section_name: str, current_content: str, 
                      student_request: str, context: Dict = None) -> str:
        prompt = f"""Revise this section: {section_name}
Current: {current_content[:300]}...
Request: {student_request}
Maintain UMAT format."""

        messages = [
            {"role": "system", "content": "You edit UMAT reports."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.7, max_tokens=3000)
