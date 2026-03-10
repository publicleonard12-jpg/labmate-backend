from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import base64
import io

from ai_service import AIService
from report_generator import ReportGenerator
from pdf_generator import generate_pdf
from umat_docx_generator_module import UMATDocxGenerator

app = Flask(__name__)
CORS(app)

# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize services
ai_service = AIService()
report_generator = ReportGenerator(ai_service)
umat_docx_generator = UMATDocxGenerator()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_image(image_file):
    """Extract text from image using Claude vision"""
    try:
        image_data = image_file.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        prompt = """Extract ALL text from this image. This is either a data table or lab manual.
Return EXACT text preserving tables and structure."""

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": base64_image
                        }
                    }
                ]
            }
        ]
        
        return ai_service._make_request(messages, temperature=0.3, max_tokens=2000)
    
    except Exception as e:
        print(f"Error: {e}")
        return ""

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    """Generate report with file uploads"""
    try:
        data = {}
        
        # Get form data
        for key in request.form:
            data[key] = request.form[key]
        
        # Process data table file
        if 'data_table_file' in request.files:
            file = request.files['data_table_file']
            if file and allowed_file(file.filename):
                data['data_table'] = extract_text_from_image(file)
        
        # Process lab manual file
        if 'lab_manual_file' in request.files:
            file = request.files['lab_manual_file']
            if file and allowed_file(file.filename):
                data['lab_manual'] = extract_text_from_image(file)
        
        # Generate report
        report = report_generator.generate_full_report(data)
        
        return jsonify({
            'success': True,
            'report': report
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export-pdf', methods=['POST'])
def export_pdf():
    """Export report as PDF"""
    try:
        data = request.json
        report = data.get('report')
        
        pdf_bytes = generate_pdf(report)
        
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"{report['title']}.pdf"
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-docx', methods=['POST'])
def export_docx():
    """Export report as DOCX"""
    try:
        data = request.json
        report = data.get('report')
        
        docx_bytes = umat_docx_generator.generate_lab_report_docx(report)
        
        return send_file(
            io.BytesIO(docx_bytes),
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name=f"{report['title']}_UMAT.docx"
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
