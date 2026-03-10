from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

def generate_pdf(report_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    story.append(Paragraph(report_data.get('title', 'Report'), styles['Title']))
    story.append(Spacer(1, 12))
    
    sections = report_data.get('sections', {})
    for key, content in sections.items():
        story.append(Paragraph(key.upper(), styles['Heading2']))
        story.append(Paragraph(content.replace('\n', '<br/>'), styles['BodyText']))
        story.append(Spacer(1, 12))
    
    doc.build(story)
    return buffer.getvalue()