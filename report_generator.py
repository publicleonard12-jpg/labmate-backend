"""
Report Generator Module - Creates formatted lab reports
"""

from typing import Dict, Any, List
from datetime import datetime

class ReportGenerator:
    def __init__(self, ai_service):
        self.ai_service = ai_service
    
    def generate_full_report(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a complete lab report from experimental data
        
        Args:
            data: Dictionary containing:
                - title: Experiment title
                - course_code: Course code (e.g., CH 273)
                - objective: Experiment objective
                - materials: List of materials used
                - procedure: Experimental procedure
                - observations: Observations made
                - data: Experimental data (optional)
        
        Returns:
            Complete formatted lab report
        """
        
        title = data.get('title', '')
        course_code = data.get('course_code', '')
        objective = data.get('objective', '')
        materials = data.get('materials', [])
        procedure = data.get('procedure', '')
        observations = data.get('observations', '')
        experimental_data = data.get('data', [])
        
        # Generate each section using AI
        report = {
            'title': title,
            'course_code': course_code,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'student_name': '[Student Name]',  # User can fill this in
            'sections': {}
        }
        
        # 1. INTRODUCTION
        report['sections']['introduction'] = self._generate_introduction(title, objective, course_code)
        
        # 2. THEORY/BACKGROUND
        report['sections']['theory'] = self._generate_theory(title, objective)
        
        # 3. MATERIALS AND METHODS
        report['sections']['materials'] = self._format_materials(materials)
        report['sections']['procedure'] = self._format_procedure(procedure)
        
        # 4. RESULTS
        report['sections']['results'] = self._generate_results_section(observations, experimental_data)
        
        # 5. DISCUSSION
        report['sections']['discussion'] = self._generate_discussion(
            title, objective, observations, experimental_data
        )
        
        # 6. CONCLUSION
        report['sections']['conclusion'] = self._generate_conclusion(
            title, objective, observations
        )
        
        # 7. REFERENCES (template)
        report['sections']['references'] = self._generate_references_template(course_code)
        
        return report
    
    def _generate_introduction(self, title: str, objective: str, course_code: str) -> str:
        """Generate introduction section"""
        
        prompt = f"""Write a professional introduction for a lab report:

Experiment: {title}
Course: {course_code}
Objective: {objective}

The introduction should:
1. Provide context and background (2-3 sentences)
2. State the importance/relevance of the experiment
3. Clearly state the objective
4. Be concise (about 150-200 words)

Write in formal scientific style."""

        messages = [
            {"role": "system", "content": "You are writing a university-level lab report introduction."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.6)
    
    def _generate_theory(self, title: str, objective: str) -> str:
        """Generate theory/background section"""
        
        prompt = f"""Write the theoretical background section for this experiment:

Experiment: {title}
Objective: {objective}

Include:
1. Relevant scientific principles and theories
2. Key equations or formulas (if applicable)
3. Expected relationships between variables
4. Prior research or established knowledge

Keep it focused and relevant (200-300 words). Use formal scientific language."""

        messages = [
            {"role": "system", "content": "You are explaining the theoretical basis of a laboratory experiment."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.5)
    
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
        """Generate discussion section with analysis"""
        
        prompt = f"""Write the Discussion section for this lab report:

Experiment: {title}
Objective: {objective}
Observations: {observations}
Data: {str(data)[:500]}...

Requirements:
1. Interpret the results
2. Explain what the findings mean
3. Compare with theoretical expectations
4. Discuss sources of error
5. Suggest improvements
6. Relate to course concepts

Write 300-400 words with critical analysis."""

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
        """Generate references template"""
        
        return f"""**References:**

1. [Course Textbook] - {course_code} Course Materials
2. [Laboratory Manual] - {course_code} Lab Manual
3. [Additional sources as needed]

*Note: Add specific references used during the experiment.*"""
    
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
    
    def enhance_section(self, section_name: str, content: str, course_code: str = "") -> str:
        """
        Enhance a specific section of the report
        
        Args:
            section_name: Name of section (introduction, theory, discussion, etc.)
            content: Current content to enhance
            course_code: Course code for context
        """
        
        prompt = f"""Enhance this {section_name} section of a lab report:

Current Content:
{content}

Course: {course_code}

Requirements:
1. Improve clarity and flow
2. Add more technical detail where appropriate
3. Ensure proper scientific writing style
4. Maintain accuracy
5. Keep it concise but comprehensive

Return the enhanced version."""

        messages = [
            {"role": "system", "content": f"You are improving the {section_name} section of a scientific report."},
            {"role": "user", "content": prompt}
        ]
        
        return self.ai_service._make_request(messages, temperature=0.6)
