"""
PDF Generator Module - Creates formatted PDFs from lab reports
Uses ReportLab for professional document generation
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from datetime import datetime
import io
from typing import Dict, Any

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Create custom paragraph styles for the document"""
        
        # Title style
        if 'CustomTitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=18,
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            ))
        
        # Course code style
        if 'CourseCode' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CourseCode',
                parent=self.styles['Normal'],
                fontSize=12,
                textColor=colors.HexColor('#666666'),
                spaceAfter=20,
                alignment=TA_CENTER,
                fontName='Helvetica'
            ))
        
        # Section heading style
        if 'SectionHeading' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='SectionHeading',
                parent=self.styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=12,
                spaceBefore=20,
                fontName='Helvetica-Bold'
            ))
        
        # Body text style
        if 'LabBodyText' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='LabBodyText',
                parent=self.styles['Normal'],
                fontSize=11,
                textColor=colors.HexColor('#333333'),
                spaceAfter=12,
                alignment=TA_JUSTIFY,
                leading=16,
                fontName='Helvetica'
            ))
    
    def generate_lab_report_pdf(self, report_data: Dict[str, Any]) -> bytes:
        """
        Generate a formatted PDF from lab report data
        
        Args:
            report_data: Dictionary containing report sections
        
        Returns:
            PDF file as bytes
        """
        
        # Create PDF in memory
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build the document content
        story = []
        
        # Add header
        story.extend(self._create_header(report_data))
        
        # Add sections with chapter numbers
        sections = report_data.get('sections', {})
        
        # CHAPTER 1: Introduction
        if 'introduction' in sections and sections['introduction']:
            story.extend(self._create_section('INTRODUCTION', sections['introduction'], chapter_number=1))
        
        # Add theory to Chapter 1 if it exists
        if 'theory' in sections and sections['theory']:
            story.extend(self._create_section('THEORETICAL BACKGROUND', sections['theory']))
        
        # CHAPTER 2: Methodology
        methodology_sections = []
        if 'materials' in sections and sections['materials']:
            methodology_sections.append(('Equipment/Materials', sections['materials']))
        if 'procedure' in sections and sections['procedure']:
            methodology_sections.append(('Procedure', sections['procedure']))
        
        if methodology_sections:
            # Add Chapter 2 heading
            story.append(PageBreak())
            chapter_style = ParagraphStyle(
                'ChapterHeading',
                parent=self.styles['Heading1'],
                fontSize=14,
                fontName='Helvetica-Bold',
                spaceAfter=12,
                spaceBefore=24,
                alignment=TA_CENTER
            )
            story.append(Paragraph("CHAPTER 2", chapter_style))
            story.append(Paragraph("METHODOLOGY", self.styles['SectionHeading']))
            story.append(Spacer(1, 0.2*inch))
            
            for section_title, content in methodology_sections:
                story.extend(self._create_section(section_title, content))
        
        # CHAPTER 3: Data (if included)
        if 'data' in sections and sections['data']:
            story.append(PageBreak())
            story.extend(self._create_section('DATA', sections['data'], chapter_number=3))
        
        # CHAPTER 4: Results and Discussion
        if 'results' in sections and sections['results']:
            story.append(PageBreak())
            story.extend(self._create_section('RESULTS AND DISCUSSION', sections['results'], chapter_number=4))
        
        if 'discussion' in sections and sections['discussion']:
            story.extend(self._create_section('', sections['discussion']))
        
        if 'conclusion' in sections and sections['conclusion']:
            story.extend(self._create_section('Conclusion', sections['conclusion']))
        
        # References section
        if 'references' in sections and sections['references']:
            story.append(PageBreak())
            story.extend(self._create_section('REFERENCES', sections['references']))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def _create_header(self, report_data: Dict) -> list:
        """Create UMAT-style title page"""
        elements = []
        
        # University header - centered
        university_style = ParagraphStyle(
            'UniversityHeader',
            parent=self.styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        )
        
        elements.append(Paragraph("UNIVERSITY OF MINES AND TECHNOLOGY, (UMAT).", university_style))
        elements.append(Paragraph("TARKWA, GHANA.", university_style))
        elements.append(Paragraph("SCHOOL OF PETROLEUM STUDIES.", university_style))
        elements.append(Paragraph("DEPARTMENT OF CHEMICAL AND PETROCHEMICAL ENGINEERING", university_style))
        elements.append(Spacer(1, 0.5*inch))
        
        # Title - centered, larger
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=self.styles['CustomTitle'],
            fontSize=14,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            spaceAfter=30
        )
        
        title = report_data.get('title', 'Lab Report').upper()
        elements.append(Paragraph(f"A REPORT ON {title}.", title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Student info - centered
        info_style = ParagraphStyle(
            'StudentInfo',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_CENTER,
            spaceAfter=8,
            fontName='Helvetica'
        )
        
        student_name = report_data.get('student_name', '[STUDENT NAME]').upper()
        elements.append(Paragraph(f"BY: {student_name}.", info_style))
        
        student_id = report_data.get('student_id', '[STUDENT ID]')
        elements.append(Paragraph(student_id, info_style))
        
        course_code = report_data.get('course_code', '')
        elements.append(Paragraph(f"{course_code}.", info_style))
        
        group_number = report_data.get('group_number', '')
        if group_number:
            elements.append(Paragraph(f"GROUP {group_number}", info_style))
        
        course_name = report_data.get('course_name', 'CHEMISTRY LABORATORY PRACTICE').upper()
        elements.append(Paragraph(course_name, info_style))
        
        lecturer = report_data.get('lecturer', '[COURSE LECTURER]').upper()
        elements.append(Paragraph(f"COURSE LECTURER: {lecturer}.", info_style))
        
        # Date in UMAT format
        date_str = report_data.get('date', datetime.now().strftime('%Y-%m-%d'))
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            day = date_obj.day
            suffix = 'TH' if 11 <= day <= 13 else {1: 'ST', 2: 'ND', 3: 'RD'}.get(day % 10, 'TH')
            formatted_date = date_obj.strftime(f'%d{suffix} %B, %Y').upper()
        except:
            formatted_date = date_str.upper()
        
        elements.append(Paragraph(formatted_date, info_style))
        elements.append(PageBreak())
        
        return elements
    
    def _create_section(self, title: str, content: str, chapter_number: int = None) -> list:
        """Create a report section with optional chapter numbering"""
        elements = []
        
        # Add chapter heading if provided
        if chapter_number:
            chapter_style = ParagraphStyle(
                'ChapterHeading',
                parent=self.styles['Heading1'],
                fontSize=14,
                fontName='Helvetica-Bold',
                spaceAfter=12,
                spaceBefore=24,
                alignment=TA_CENTER
            )
            elements.append(Paragraph(f"CHAPTER {chapter_number}", chapter_style))
        
        # Section heading
        section_style = ParagraphStyle(
            'UMATSectionHeading',
            parent=self.styles['SectionHeading'],
            fontSize=12,
            alignment=TA_CENTER if chapter_number else TA_LEFT,
            fontName='Helvetica-Bold'
        )
        elements.append(Paragraph(title.upper(), section_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Section content - split by paragraphs
        paragraphs = content.split('\n\n')
        
        for para in paragraphs:
            if para.strip():
                # Check if it's a list (starts with number or bullet)
                if para.strip().startswith(('1.', '2.', '3.', '•', '-')):
                    # Keep list formatting
                    para_text = para.replace('\n', '<br/>')
                else:
                    # Regular paragraph
                    para_text = para.replace('\n', ' ')
                
                elements.append(Paragraph(para_text, self.styles['LabBodyText']))
                elements.append(Spacer(1, 0.15*inch))
        
        return elements
    
    def generate_simple_pdf(self, title: str, content: str) -> bytes:
        """
        Generate a simple PDF with title and content
        
        Args:
            title: Document title
            content: Main content text
        
        Returns:
            PDF file as bytes
        """
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        
        story = []
        
        # Title
        story.append(Paragraph(title, self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))
        
        # Content
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                story.append(Paragraph(para.replace('\n', '<br/>'), self.styles['LabBodyText']))
        
        doc.build(story)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
