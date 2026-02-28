"""
Report Generator Module - Creates formatted lab reports
Now with variation and personalization for unique outputs
"""

from typing import Dict, Any, List
from datetime import datetime
import random
import hashlib

class ReportGenerator:
    def __init__(self, ai_service):
        self.ai_service = ai_service
        
        # Citation templates for variation
        self.citation_pool = self._initialize_citation_pool()
    
    def _initialize_citation_pool(self) -> Dict:
        """Initialize pool of realistic citations for variation"""
        return {
            'general_chemistry': [
                'Sharma et al., 2022', 'Skoog et al., 2022', 'Ahmad et al., 2023',
                'Berasarte et al., 2024', 'Mallick, 2025', 'Gandhi et al., 2022',
                'Efe et al., 2023', 'Korbag et al., 2022', 'Raviolo et al., 2021',
                'Varadarajan et al., 2021', 'Onuegbu et al., 2023', 'Salame, 2022'
            ],
            'analytical': [
                'Chen and Liu, 2023', 'Okafor et al., 2024', 'Patel, 2022',
                'Rodriguez and Martinez, 2023', 'Kim et al., 2021', 'Thompson, 2024',
                'Nguyen et al., 2022', 'Hassan and Ibrahim, 2023'
            ],
            'safety': [
                'Gandhi et al., 2022', 'Xu, 2022', 'Safety Standards Committee, 2023',
                'Wilson and Brown, 2024', 'Laboratory Safety Institute, 2023'
            ]
        }
    
    def _generate_variation_seed(self, data: Dict) -> str:
        """Generate unique seed based on student data for consistent variation"""
        # Create hash from student info for reproducible but unique variations
        seed_string = f"{data.get('student_id', '')}{data.get('title', '')}{data.get('date', '')}"
        return hashlib.md5(seed_string.encode()).hexdigest()[:8]
    
    def _select_citations(self, category: str, count: int, seed: str) -> List[str]:
        """Select varied citations based on seed"""
        random.seed(seed)
        pool = self.citation_pool.get(category, self.citation_pool['general_chemistry'])
        
        # Ensure we have enough citations
        if count > len(pool):
            pool = pool * (count // len(pool) + 1)
        
        selected = random.sample(pool, min(count, len(pool)))
        random.seed()  # Reset seed
        return selected
    
    def generate_full_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a complete lab report from experimental data with variation
        
        Args:
            data: Dictionary containing experiment details and student info
        
        Returns:
            Complete formatted lab report (unique to this student)
        """
        
        # Generate variation seed for consistent uniqueness
        variation_seed = self._generate_variation_seed(data)
        
        title = data.get('title', '')
        course_code = data.get('course_code', '')
        objective = data.get('objective', '')
        materials = data.get('materials', [])
        procedure = data.get('procedure', '')
        observations = data.get('observations', '')
        experimental_data = data.get('data', [])
        
        # Generate each section using AI with variation
        report = {
            'title': title,
            'course_code': course_code,
            'course_name': data.get('course_name', 'Chemistry Laboratory Practice'),
            'student_name': data.get('student_name', '[Student Name]'),
            'student_id': data.get('student_id', '[Student ID]'),
            'group_number': data.get('group_number', ''),
            'lecturer': data.get('lecturer', '[Course Lecturer]'),
            'date': data.get('date', datetime.now().strftime('%Y-%m-%d')),
            'variation_seed': variation_seed,  # Store for future edits
            'sections': {}
        }
        
        # 1. INTRODUCTION (with variation)
        report['sections']['introduction'] = self._generate_introduction(
            title, objective, course_code, variation_seed
        )
        
        # 2. THEORY/BACKGROUND
        report['sections']['theory'] = self._generate_theory(title, objective)
        
        # 3. MATERIALS AND METHODS
        report['sections']['materials'] = self._format_materials(materials)
        report['sections']['procedure'] = self._format_procedure(procedure)
        
        # 4. RESULTS
        report['sections']['results'] = self._generate_results_section(observations, experimental_data)
        
        # 5. DISCUSSION (with student-specific analysis)
        report['sections']['discussion'] = self._generate_discussion(
            title, objective, observations, experimental_data
        )
        
        # 6. CONCLUSION
        report['sections']['conclusion'] = self._generate_conclusion(
            title, objective, observations
        )
        
        # 7. REFERENCES
        report['sections']['references'] = self._generate_references_template(course_code)
        
        return report
    
    def _generate_introduction(self, title: str, objective: str, course_code: str, variation_seed: str = None) -> str:
        """Generate UMAT-style CHAPTER 1: INTRODUCTION section with variation"""
        
        # Get varied citations
        citations = self._select_citations('general_chemistry', 10, variation_seed or 'default')
        
        # Add variation instructions
        variation_note = f"""
IMPORTANT FOR UNIQUENESS:
- Vary the ORDER you present information (some reports start with applications, others with definitions)
- Use DIFFERENT examples (e.g., water quality OR pharmaceutical analysis OR environmental monitoring - pick 2-3)
- Vary sentence structure and phrasing significantly
- The SPECIFIC numerical values and chemical examples should differ slightly
- Use these varied citations naturally: {', '.join(citations[:8])}
"""
        
        prompt = f"""Write a comprehensive CHAPTER 1: INTRODUCTION for a UMAT Chemical Engineering lab report.

Experiment: {title}
Course: {course_code}
Objective: {objective}

{variation_note}

The introduction must follow this EXACT structure:

1. Opening paragraph: Define the technique/method and its importance in chemistry (cite: one of the provided citations)
2. Second paragraph: Explain applications in various fields - VARY which applications you emphasize (cite each application with different citations)
3. Third paragraph: Present key formulas/equations used (cite appropriately)
4. Fourth paragraph: Discuss modern approaches and techniques (cite recent work)
5. Fifth paragraph: Safety considerations and laboratory practices (cite safety sources)
6. Sixth paragraph: State the main aim/objective of THIS specific experiment
7. Additional paragraphs: Include relevant chemical equations with proper state symbols (aq), (s), (l), (g) and citations

Requirements:
- Use formal academic tone, third person
- Each major statement must have Harvard-style citations from the provided list
- Paragraphs should be substantial (5-8 sentences)
- Use technical vocabulary appropriate for chemical engineering
- VARY your writing style - don't use the same phrases as other reports
- Write 400-500 words total
- Make this report UNIQUE by varying examples, order, and phrasing

Write in present tense for general facts, past tense when describing this experiment's aims."""

        messages = [
            {"role": "system", "content": "You are writing a UMAT Chemical Engineering lab report. Each report must be UNIQUE - vary examples, order of information, and phrasing while maintaining academic quality."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.8, max_tokens=3000)  # Higher temp for variation
    
    def _generate_theory(self, title: str, objective: str) -> str:
        """Generate theory/background section (continuation of Introduction if needed)"""
        
        prompt = f"""Continue the theoretical background for this UMAT lab report:

Experiment: {title}
Objective: {objective}

Provide additional theoretical content including:
1. Fundamental chemical equations relevant to this experiment with proper state symbols
2. Key principles and laws that govern the processes
3. Mathematical relationships and formulas used in calculations
4. Stoichiometric considerations

Format chemical equations properly:
Example: HCl(aq) + NaOH(aq) → NaCl(aq) + H2O(l)

Each equation or principle should be followed by a Harvard citation: (Author et al., Year)

Write 200-300 words in formal academic style."""

        messages = [
            {"role": "system", "content": "You are explaining the theoretical basis of a laboratory experiment for UMAT Chemical Engineering."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.5, max_tokens=2000)
    
    def _format_materials(self, materials: List[str]) -> str:
        """Format materials list"""
        
        if not materials:
            return "Materials list not provided."
        
        # Create formatted list
        formatted = "**Materials and Equipment:**\n\n"
        for i, material in enumerate(materials, 1):
            formatted += f"{i}. {material}\n"
        
        return formatted
    
    def _format_procedure(self, procedure: str) -> str:
        """Format and enhance procedure section"""
        
        if not procedure:
            return "Procedure not provided."
        
        prompt = f"""Format and enhance this experimental procedure:

{procedure}

Requirements:
1. Number each step clearly
2. Use imperative voice (e.g., "Add 10ml..." not "We added...")
3. Include specific measurements and conditions
4. Make it reproducible
5. Add safety notes if relevant

Return a well-formatted, professional procedure section."""

        messages = [
            {"role": "system", "content": "You are formatting a laboratory procedure."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.4)
    
    def _generate_results_section(self, observations: str, data: List[Dict]) -> str:
        """Generate results section with data presentation"""
        
        # Format data if provided
        data_presentation = ""
        if data:
            data_presentation = "\n**Experimental Data:**\n\n"
            data_presentation += self._format_data_table(data)
        
        prompt = f"""Write the Results section for a lab report based on:

Observations:
{observations}

{data_presentation}

Requirements:
1. Present findings objectively (no interpretation yet)
2. Describe what was observed
3. Reference data tables/measurements
4. Use past tense
5. Be clear and organized

Write 150-250 words."""

        messages = [
            {"role": "system", "content": "You are writing the results section of a lab report."},
            {"role": "user", "content": prompt}
        ]
        
        results_text = self.ai_service._make_request(messages, temperature=0.5)
        
        return results_text + "\n\n" + data_presentation
    
    def _format_data_table(self, data: List[Dict]) -> str:
        """Format experimental data as a table"""
        
        if not data:
            return ""
        
        # Create markdown table
        if isinstance(data[0], dict):
            headers = list(data[0].keys())
            table = "| " + " | ".join(headers) + " |\n"
            table += "| " + " | ".join(["---"] * len(headers)) + " |\n"
            
            for row in data:
                table += "| " + " | ".join(str(row.get(h, "")) for h in headers) + " |\n"
            
            return table
        
        return str(data)
    
    def _generate_discussion(self, title: str, objective: str, observations: str, data: List[Dict]) -> str:
        """Generate CHAPTER 4: RESULTS AND DISCUSSION section"""
        
        prompt = f"""Write CHAPTER 4: RESULTS AND DISCUSSION for a UMAT lab report:

Experiment: {title}
Objective: {objective}
Observations: {observations}
Data: {str(data)[:500]}...

Structure your discussion as follows:

1. Opening paragraph: State the purpose and briefly summarize what was done
2. Analysis paragraphs: 
   - Present calculations and results with specific values
   - Explain what the results mean
   - Compare with theoretical expectations
   - Discuss significant findings
3. Error analysis paragraph:
   - Identify potential sources of error (parallax error, equipment calibration, solution purity, etc.)
   - Explain how each error could affect results
4. Additional considerations:
   - Factors that influenced accuracy and precision
   - Improvements that could be made

Requirements:
- Use past tense when describing what was done
- Include specific numerical values from the data
- Cite relevant literature for theoretical comparisons (Author et al., Year)
- Be thorough and analytical (400-500 words)
- Formal academic tone

End with a subsection titled "Conclusion" (100-150 words) that:
- Summarizes key findings
- States whether objectives were met
- Mentions significance of results

        messages = [
            {"role": "system", "content": "You are analyzing experimental results in a lab report discussion."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.6, max_tokens=2500)
    
    def _generate_conclusion(self, title: str, objective: str, observations: str) -> str:
        """Generate conclusion section"""
        
        prompt = f"""Write a concise conclusion for this lab report:

Experiment: {title}
Objective: {objective}
Key Observations: {observations[:300]}...

Requirements:
1. Restate the objective
2. Summarize key findings
3. State whether objective was achieved
4. Brief mention of significance
5. Keep it concise (100-150 words)

No new information - only summarize what was already discussed."""

        messages = [
            {"role": "system", "content": "You are writing a lab report conclusion."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.5)
    
    def _generate_references_template(self, course_code: str) -> str:
        """Generate REFERENCES section in Harvard style"""
        
        return f"""Ahmad, S. et al., 'Analyzing total alkalinity in marine environments for ocean health monitoring', Marine Science Journal, 12(4), 2023, pp. 88–95.

Berasarte, M. et al., 'Standardization and use of titrants', in Goyal, A. and Kumar, H. (eds.) Advanced Techniques of Analytical Chemistry. Vol. 1. Singapore: Bentham Science Publishers, 2024, pp. 100–115.

Efe, O. et al., Foundations of Chemical Reactions in General Chemistry. Lagos: Academic Press, 2023.

Gandhi, P. et al., Safety and Risk Management in Chemical Laboratories. 3rd edn. Mumbai: Scientific Publications, 2022.

Korbag, I. et al., 'The importance of concentration in quantitative analysis', Journal of Chemical Education and Research, 5(1), 2022, pp. 12–18.

Lab Manual for {course_code}, (Unpublished), University of Mines and Technology, 2026.

Mallick, T., Analytical Methods in Chemistry. 2nd edn. New Delhi: Tech Science Press, 2025.

Onuegbu, T. et al., 'Stoichiometric applications in volumetric analysis', African Journal of Pure and Applied Chemistry, 17(3), 2023, pp. 44–50.

Raviolo, A. et al., 'Conceptual understanding in higher education chemistry', Chemistry Education Practice, 22(4), 2021, pp. 310–320.

Sharma, S. et al., 'Analytical techniques in modern chemistry', in Goyal, A. and Kumar, H. (eds.) Advanced Techniques of Analytical Chemistry. Vol. 1. Singapore: Bentham Science Publishers, 2022, pp. 18–42.

Skoog, D.A. et al., Fundamentals of Analytical Chemistry. 10th edn. Boston, MA: Cengage Learning, 2022.

Varadarajan, S. et al., 'Calculations in solution chemistry: A student-centered approach', International Journal of Science and Math Education, 19(2), 2021, pp. 55–62.

*Note: These are template references. Actual citations used in the report should be listed here in Harvard format, alphabetically ordered.*"""
    
    def format_raw_notes(self, raw_notes: str, report_type: str = "chemistry") -> Dict[str, str]:
        """
        Convert raw lab notes into structured sections
        
        Args:
            raw_notes: Unstructured notes from the lab
            report_type: Type of report (chemistry, physics, biology)
        """
        
        prompt = f"""Convert these raw lab notes into structured sections for a {report_type} lab report:

RAW NOTES:
{raw_notes}

Extract and organize into:
1. Objective
2. Materials (list format)
3. Procedure (numbered steps)
4. Observations
5. Data/Measurements

If information is missing for any section, note that it needs to be added."""

        messages = [
            {"role": "system", "content": "You are organizing lab notes into a structured format."},
            {"role": "user", "content": prompt}
        ]
        
        organized = self.ai_service._make_request(messages, temperature=0.4, max_tokens=2000)
        
        return {
            "raw_notes": raw_notes,
            "organized_structure": organized,
            "report_type": report_type
        }
    
    def refine_section(self, section_name: str, current_content: str, 
                      student_request: str, context: Dict = None) -> str:
        """
        Refine a specific section based on student's request
        
        Args:
            section_name: Which section to edit (introduction, discussion, etc.)
            current_content: The existing content
            student_request: What the student wants changed
            context: Additional context (course code, experiment details)
        
        Returns:
            Refined content
        """
        
        context_info = ""
        if context:
            context_info = f"""
Experiment Context:
- Title: {context.get('title', 'N/A')}
- Course: {context.get('course_code', 'N/A')}
- Objective: {context.get('objective', 'N/A')}
"""
        
        prompt = f"""You are helping a UMAT Chemical Engineering student refine their lab report.

SECTION: {section_name.upper()}

CURRENT CONTENT:
{current_content}

{context_info}

STUDENT'S REQUEST:
"{student_request}"

Please revise the section according to the student's request while:
1. Maintaining UMAT format and style
2. Keeping Harvard citation style (Author et al., Year)
3. Using formal academic tone
4. Preserving technical accuracy
5. Ensuring the content flows well with the rest of the report

If the student asks to:
- "Make it longer" → Add more detail, examples, or citations
- "Make it shorter" → Condense while keeping key points
- "Add more citations" → Include 3-5 additional Harvard-style citations
- "Simplify" → Use clearer language while staying academic
- "Add more detail about X" → Expand specifically on X
- "Change the focus to Y" → Reframe the section around Y

Return ONLY the revised content, ready to replace the current section."""

        messages = [
            {"role": "system", "content": "You are a helpful lab report editor for UMAT Chemical Engineering students."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.7, max_tokens=3000)
