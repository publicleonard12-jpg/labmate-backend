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
        
        # Add sections
        sections = report_data.get('sections', {})
        
        section_order = [
            ('introduction', 'Introduction'),
            ('theory', 'Theory and Background'),
            ('materials', 'Materials and Equipment'),
            ('procedure', 'Procedure'),
            ('results', 'Results'),
            ('discussion', 'Discussion'),
            ('conclusion', 'Conclusion'),
            ('references', 'References')
        ]
        
        for section_key, section_title in section_order:
            if section_key in sections and sections[section_key]:
                story.extend(self._create_section(section_title, sections[section_key]))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def _create_header(self, report_data: Dict) -> list:
        """Create document header"""
        elements = []
        
        # Title
        title = report_data.get('title', 'Lab Report')
        elements.append(Paragraph(title, self.styles['CustomTitle']))
        
        # Course code
        course_code = report_data.get('course_code', '')
        if course_code:
            elements.append(Paragraph(course_code, self.styles['CourseCode']))
        
        # Metadata table
        metadata = [
            ['Student:', report_data.get('student_name', '[Student Name]')],
            ['Date:', report_data.get('date', datetime.now().strftime('%Y-%m-%d'))],
        ]
        
        table = Table(metadata, colWidths=[1.5*inch, 4*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_section(self, title: str, content: str) -> list:
        """Create a report section"""
        elements = []
        
        # Section heading
        elements.append(Paragraph(title, self.styles['SectionHeading']))
        
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
        
        elements.append(Spacer(1, 0.2*inch))
        
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
