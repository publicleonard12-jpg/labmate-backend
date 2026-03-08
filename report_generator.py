"""
Enhanced Report Generator - Handles data tables and lab manuals
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
        """Initialize pool of realistic citations"""
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
        """Generate complete report with data table and lab manual support"""
        variation_seed = self._generate_variation_seed(data)
        
        # Extract new fields
        data_table = data.get('data_table', '')
        lab_manual = data.get('lab_manual', '')
        
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
        
        # 1. INTRODUCTION (no citations in text - will add to references)
        report['sections']['introduction'] = self._generate_introduction_no_inline_citations(
            data.get('title', ''), data.get('objective', ''), 
            data.get('course_code', ''), variation_seed
        )
        
        # 2. MATERIALS - Extract from lab manual if provided
        if lab_manual:
            report['sections']['materials'] = self._extract_materials_from_manual(
                data.get('title', ''), lab_manual
            )
        else:
            report['sections']['materials'] = self._format_materials(data.get('materials', []))
        
        # 3. PROCEDURE - Extract from lab manual if provided
        if lab_manual:
            report['sections']['procedure'] = self._extract_procedure_from_manual(
                data.get('title', ''), lab_manual
            )
        else:
            report['sections']['procedure'] = data.get('procedure', '')
        
        # 4. RESULTS - Generate from data table if provided
        if data_table:
            report['sections']['results'] = self._generate_results_from_data(
                data.get('title', ''), data_table, lab_manual
            )
        else:
            report['sections']['results'] = data.get('observations', 'Results pending')
        
        # 5. DISCUSSION - Analyze data if provided
        if data_table:
            report['sections']['discussion'] = self._generate_discussion_from_data(
                data.get('title', ''), data.get('objective', ''),
                data_table, lab_manual
            )
        else:
            report['sections']['discussion'] = self._generate_discussion(
                data.get('title', ''), data.get('objective', ''), 
                data.get('observations', ''), []
            )
        
        # 6. CONCLUSION
        report['sections']['conclusion'] = self._generate_conclusion(
            data.get('title', ''), data.get('objective', ''), 
            data.get('observations', '')
        )
        
        # 7. REFERENCES - ALL ON LAST PAGE
        report['sections']['references'] = self._generate_all_references()
        
        return report
    
    def _generate_introduction_no_inline_citations(self, title: str, objective: str, 
                                                   course_code: str, variation_seed: str = None) -> str:
        """Generate introduction WITHOUT inline citations (all refs go to References section)"""
        
        prompt = f"""Write CHAPTER 1: INTRODUCTION for a UMAT Chemical Engineering lab report.

Experiment: {title}
Course: {course_code}

IMPORTANT: Do NOT include any in-text citations like (Author et al., Year).
All references will be listed in a separate References section at the end.

Structure:
1. Define the technique and its importance
2. Applications in 3-4 fields
3. Key formulas and equations
4. Modern approaches
5. Safety considerations
6. Aim of this experiment
7. Relevant chemical equations with state symbols

Write 450-550 words, formal tone, third person.
NO in-text citations - just present the facts."""

        messages = [
            {"role": "system", "content": "You write UMAT lab reports without inline citations."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.7, max_tokens=3000)
    
    def _extract_materials_from_manual(self, title: str, lab_manual: str) -> str:
        """Extract materials list from lab manual"""
        
        prompt = f"""Extract the materials/equipment list from this lab manual for: {title}

LAB MANUAL:
{lab_manual}

Return ONLY a clean list of materials, one per line.
Example:
Burette
250 mL Flask
NaOH solution
Indicator"""

        messages = [
            {"role": "system", "content": "You extract materials lists from lab manuals."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.3, max_tokens=1000)
    
    def _extract_procedure_from_manual(self, title: str, lab_manual: str) -> str:
        """Extract procedure from lab manual"""
        
        prompt = f"""Extract and rewrite the experimental procedure from this lab manual for: {title}

LAB MANUAL:
{lab_manual}

Rewrite in clear, step-by-step format using past tense.
Write 200-300 words describing what was done."""

        messages = [
            {"role": "system", "content": "You extract procedures from lab manuals."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.5, max_tokens=2000)
    
    def _generate_results_from_data(self, title: str, data_table: str, 
                                   lab_manual: str = "") -> str:
        """Generate RESULTS section from actual data table"""
        
        prompt = f"""Analyze this experimental data and write a RESULTS section.

Experiment: {title}

DATA TABLE:
{data_table}

Generate a RESULTS section that:
1. Presents the data clearly with values and units
2. Shows key calculations step-by-step
3. States numerical findings
4. Uses past tense
5. NO citations (references go to end)

Write 250-350 words."""

        messages = [
            {"role": "system", "content": "You analyze experimental data for UMAT reports."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.5, max_tokens=2500)
    
    def _generate_discussion_from_data(self, title: str, objective: str,
                                      data_table: str, lab_manual: str = "") -> str:
        """Generate DISCUSSION based on data analysis"""
        
        prompt = f"""Write RESULTS AND DISCUSSION for: {title}

OBJECTIVE: {objective}

DATA:
{data_table}

Generate discussion that:
1. Interprets the results
2. Compares with theoretical expectations
3. Discusses sources of error (parallax, equipment calibration, etc.)
4. Analyzes accuracy and precision
5. NO citations (all refs go to References section)

Write 400-500 words in past tense."""

        messages = [
            {"role": "system", "content": "You write UMAT lab report discussions."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.6, max_tokens=3000)
    
    def _format_materials(self, materials: List) -> str:
        if isinstance(materials, list):
            return '\n'.join(materials)
        return str(materials)
    
    def _generate_discussion(self, title: str, objective: str, 
                           observations: str, data: List[Dict]) -> str:
        """Fallback discussion without data table"""
        
        prompt = f"""Write RESULTS AND DISCUSSION for: {title}

Include analysis, error sources, and conclusions.
NO citations - write 400-500 words."""

        messages = [
            {"role": "system", "content": "You write UMAT report discussions."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.6, max_tokens=3000)
    
    def _generate_conclusion(self, title: str, objective: str, observations: str) -> str:
        """Generate conclusion"""
        
        prompt = f"""Write conclusion for: {title}
Summarize findings and whether objectives met.
Write 100-150 words, NO citations."""

        messages = [
            {"role": "system", "content": "You conclude UMAT reports."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.6, max_tokens=1000)
    
    def _generate_all_references(self) -> str:
        """Generate complete references section - ALL refs on LAST PAGE"""
        
        return """Ahmad, S. et al., 'Analyzing total alkalinity in marine environments for ocean health monitoring', Marine Science Journal, 12(4), 2023, pp. 88-95.

Berasarte, M. et al., 'Standardization and use of titrants', in Goyal, A. and Kumar, H. (eds.) Advanced Techniques of Analytical Chemistry. Vol. 1. Singapore: Bentham Science Publishers, 2024, pp. 100-115.

Chen, Y. and Liu, M., 'Modern approaches to quantitative analysis in analytical chemistry', Journal of Analytical Science, 15(3), 2023, pp. 145-162.

Efe, O. et al., Foundations of Chemical Reactions in General Chemistry. Lagos: Academic Press, 2023.

Gandhi, P. et al., Safety and Risk Management in Chemical Laboratories. 3rd edn. Mumbai: Scientific Publications, 2022.

Korbag, I. et al., 'The importance of molarity in quantitative volumetric analysis', Journal of Chemical Education and Research, 5(1), 2022, pp. 12-18.

Mallick, T., Analytical Methods in Chemistry. 2nd edn. New Delhi: Tech Science Press, 2025.

Onuegbu, T. et al., 'Stoichiometric applications in acid-base volumetric analysis', African Journal of Pure and Applied Chemistry, 17(3), 2023, pp. 44-50.

Patel, R., 'Titration methods in food science and quality control', Food Chemistry International, 34(3), 2022, pp. 201-215.

Qarah, A. et al., 'Volumetric analysis in pharmaceutical quality control', Pharmaceutical Research Reports, 9(1), 2023, pp. 201-210.

Raviolo, A. et al., 'Conceptual understanding of concentration and molarity in higher education', Chemistry Education Practice, 22(4), 2021, pp. 310-320.

Sharma, S. et al., 'Analytical techniques in modern chemistry', in Goyal, A. and Kumar, H. (eds.) Advanced Techniques of Analytical Chemistry. Vol. 1. Singapore: Bentham Science Publishers, 2022, pp. 18-42.

Skoog, D.A. et al., Fundamentals of Analytical Chemistry. 10th edn. Boston, MA: Cengage Learning, 2022.

Varadarajan, S. et al., 'Calculations in solution chemistry: A student-centered approach', International Journal of Science and Math Education, 19(2), 2021, pp. 55-62."""
    
    def refine_section(self, section_name: str, current_content: str, 
                      student_request: str, context: Dict = None) -> str:
        """Refine section based on student request"""
        
        prompt = f"""Revise this section: {section_name}
Current: {current_content[:300]}...
Request: {student_request}
Maintain UMAT format, NO inline citations."""

        messages = [
            {"role": "system", "content": "You edit UMAT reports."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.7, max_tokens=3000)
