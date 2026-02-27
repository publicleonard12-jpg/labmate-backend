"""
LabMate AI - Backend API
A STEM student assistant for lab reports, research papers, and video resources
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from datetime import datetime
import json
import io

# Import our modules
from ai_service import AIService
from video_service import VideoService
from research_service import ResearchService
from report_generator import ReportGenerator
from pdf_generator import PDFGenerator

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from mobile app

# Initialize services
ai_service = AIService()
video_service = VideoService()
research_service = ResearchService()
report_generator = ReportGenerator(ai_service)
pdf_generator = PDFGenerator()

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Check if API is running"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

# ===== LAB REPORT GENERATOR =====
@app.route('/api/generate-report', methods=['POST'])
def generate_lab_report():
    """
    Generate a complete lab report from experimental data
    
    Request Body:
    {
        "title": "Titration Experiment",
        "course_code": "CH 273",
        "objective": "To determine the concentration...",
        "materials": ["Burette", "Pipette", "NaOH solution"],
        "procedure": "1. Fill burette with NaOH...",
        "observations": "Initial reading: 0.0ml...",
        "data": [{"trial": 1, "volume": 25.5}]
    }
    """
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['title', 'course_code', 'objective', 'procedure', 'observations']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Generate the report
        report = report_generator.generate_full_report(data)
        
        return jsonify({
            'success': True,
            'report': report,
            'generated_at': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/format-report', methods=['POST'])
def format_report():
    """
    Format raw notes into structured lab report sections
    
    Request Body:
    {
        "raw_notes": "We heated the solution and observed...",
        "report_type": "chemistry" | "physics" | "biology"
    }
    """
    try:
        data = request.json
        raw_notes = data.get('raw_notes', '')
        report_type = data.get('report_type', 'chemistry')
        
        formatted = report_generator.format_raw_notes(raw_notes, report_type)
        
        return jsonify({
            'success': True,
            'formatted_report': formatted
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export-pdf', methods=['POST'])
def export_pdf():
    """
    Export a lab report as a PDF file
    
    Request Body:
    {
        "report": {
            "title": "Experiment Title",
            "course_code": "CH 273",
            "student_name": "John Doe",
            "date": "2026-02-26",
            "sections": {
                "introduction": "...",
                "theory": "...",
                etc.
            }
        }
    }
    
    Returns: PDF file for download
    """
    try:
        data = request.json
        report_data = data.get('report')
        
        if not report_data:
            return jsonify({'error': 'Report data is required'}), 400
        
        # Generate PDF
        pdf_bytes = pdf_generator.generate_lab_report_pdf(report_data)
        
        # Create filename
        title = report_data.get('title', 'lab_report').replace(' ', '_')
        filename = f"{title}.pdf"
        
        # Return PDF as downloadable file
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===== RESEARCH PAPER SUMMARIZER =====
@app.route('/api/search-papers', methods=['POST'])
def search_papers():
    """
    Search for research papers on arXiv
    
    Request Body:
    {
        "query": "heat transfer in chemical processes",
        "max_results": 10
    }
    """
    try:
        data = request.json
        query = data.get('query', '')
        max_results = data.get('max_results', 10)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        papers = research_service.search_papers(query, max_results)
        
        return jsonify({
            'success': True,
            'papers': papers,
            'count': len(papers)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/summarize-paper', methods=['POST'])
def summarize_paper():
    """
    Summarize a research paper
    
    Request Body:
    {
        "paper_url": "https://arxiv.org/abs/2301.12345",
        OR
        "paper_text": "Full text of the paper...",
        "summary_type": "brief" | "detailed"
    }
    """
    try:
        data = request.json
        paper_url = data.get('paper_url')
        paper_text = data.get('paper_text')
        summary_type = data.get('summary_type', 'brief')
        
        if not paper_url and not paper_text:
            return jsonify({'error': 'Either paper_url or paper_text is required'}), 400
        
        # Fetch paper if URL provided
        if paper_url:
            paper_text = research_service.fetch_paper_text(paper_url)
        
        # Generate summary
        summary = research_service.summarize_paper(paper_text, summary_type)
        
        return jsonify({
            'success': True,
            'summary': summary
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===== VIDEO RESOURCE FINDER =====
@app.route('/api/find-videos', methods=['POST'])
def find_videos():
    """
    Find relevant educational videos for a topic
    
    Request Body:
    {
        "topic": "organic chemistry reactions",
        "course_code": "CH 257",
        "max_results": 10,
        "difficulty": "beginner" | "intermediate" | "advanced"
    }
    """
    try:
        data = request.json
        topic = data.get('topic', '')
        course_code = data.get('course_code', '')
        max_results = data.get('max_results', 10)
        difficulty = data.get('difficulty', 'intermediate')
        
        if not topic:
            return jsonify({'error': 'Topic is required'}), 400
        
        # Search for videos
        videos = video_service.find_educational_videos(
            topic=topic,
            course_code=course_code,
            max_results=max_results,
            difficulty=difficulty
        )
        
        return jsonify({
            'success': True,
            'videos': videos,
            'count': len(videos)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/curate-playlist', methods=['POST'])
def curate_playlist():
    """
    Create a curated learning playlist for a course topic
    
    Request Body:
    {
        "course_code": "CH 275",
        "topics": ["titration", "pH calculations", "buffer solutions"]
    }
    """
    try:
        data = request.json
        course_code = data.get('course_code', '')
        topics = data.get('topics', [])
        
        if not topics:
            return jsonify({'error': 'Topics list is required'}), 400
        
        playlist = video_service.curate_learning_playlist(course_code, topics)
        
        return jsonify({
            'success': True,
            'playlist': playlist
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===== AI CHAT ASSISTANT =====
@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat with AI assistant for STEM questions
    
    Request Body:
    {
        "message": "Explain Le Chatelier's principle",
        "context": "CH 263 - Chemical Thermodynamics",
        "conversation_history": []
    }
    """
    try:
        data = request.json
        message = data.get('message', '')
        context = data.get('context', '')
        history = data.get('conversation_history', [])
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        response = ai_service.chat(message, context, history)
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===== STUDY HELPER =====
@app.route('/api/explain-concept', methods=['POST'])
def explain_concept():
    """
    Get detailed explanation of a STEM concept
    
    Request Body:
    {
        "concept": "enthalpy",
        "level": "undergraduate",
        "include_examples": true
    }
    """
    try:
        data = request.json
        concept = data.get('concept', '')
        level = data.get('level', 'undergraduate')
        include_examples = data.get('include_examples', True)
        
        if not concept:
            return jsonify({'error': 'Concept is required'}), 400
        
        explanation = ai_service.explain_concept(concept, level, include_examples)
        
        return jsonify({
            'success': True,
            'explanation': explanation
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ===== FORMULA HELPER =====
@app.route('/api/solve-formula', methods=['POST'])
def solve_formula():
    """
    Solve chemical/physics formulas with step-by-step explanation
    
    Request Body:
    {
        "formula": "PV = nRT",
        "known_values": {"P": 101.325, "V": 22.4, "T": 273.15},
        "solve_for": "n"
    }
    """
    try:
        data = request.json
        formula = data.get('formula', '')
        known_values = data.get('known_values', {})
        solve_for = data.get('solve_for', '')
        
        if not all([formula, known_values, solve_for]):
            return jsonify({'error': 'Formula, known_values, and solve_for are required'}), 400
        
        solution = ai_service.solve_formula(formula, known_values, solve_for)
        
        return jsonify({
            'success': True,
            'solution': solution
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
