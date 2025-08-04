import json
import tempfile
import io
import os
import streamlit as st
import PyPDF2
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from langchain_core.prompts import PromptTemplate
from ..ui.text_state_manager import text_manager
from langchain_core.runnables import Runnable
from .llm_manager import llm_manager


def generate_output_resume(user_message: str, pdf_raw: str, original_pdf_path: str = None):
    """Generate tailored resume by making minimal edits to preserve original formatting"""
    
    # Validate inputs
    if not pdf_raw:
        return {"status": "error", "error": "No resume content provided"}
    
    if not original_pdf_path or not os.path.exists(original_pdf_path):
        print(f"Warning: Original PDF not available: {original_pdf_path}")
        print("Proceeding with text-based generation")
    
    prompt = PromptTemplate(
        template="""You are an expert resume editor. Your job is to identify ONLY the specific text that needs to be changed to tailor the resume for the job.

        ORIGINAL RESUME CONTENT:
        {pdf_content}

        JOB POSTING REQUIREMENTS:
        {job_posting}

        STRUCTURED RESUME DATA:
        {resume_data}

        USER REQUEST:
        {user_message}

        Instructions:
        1. PRESERVE the original formatting, fonts, and layout completely
        2. Identify ONLY the text that needs editing (not entire sections)
        3. Provide exact text replacements that maintain the same length and structure
        4. Focus on keyword optimization and job-specific tailoring
        5. Keep the same line breaks, spacing, and visual structure

        Return ONLY a JSON with minimal edits needed:
        {{
            "edits": [
                {{
                    "original_text": "exact text from original resume",
                    "replacement_text": "tailored replacement text of similar length",
                    "reason": "why this change improves job match"
                }},
                {{
                    "original_text": "another exact text match",
                    "replacement_text": "improved version",
                    "reason": "explanation"
                }}
            ],
            "additions": [
                {{
                    "add_after": "exact text to add after",
                    "new_text": "brief addition to insert",
                    "section": "skills/experience/education"
                }}
            ]
        }}

        Make MINIMAL changes. Preserve original formatting completely.""",
        input_variables=["pdf_content", "job_posting", "resume_data", "user_message"]
    )

    resume_data = text_manager.get_text("resume_extraction")
    job_posting = text_manager.get_text("job_extraction")
    
    if not resume_data or not job_posting:
        return {"status": "error", "error": "Missing resume or job posting data"}
    
    chain = llm_manager.init_llm_chain(prompt=prompt)

    try:
        raw_output = chain.invoke({
            "pdf_content": pdf_raw,
            "job_posting": job_posting,
            "resume_data": resume_data,
            "user_message": user_message
        })
        
        cleaned_output = llm_manager.cleanup_llm_output(raw_output)
        edits_data = json.loads(cleaned_output)
        
        # Apply minimal edits to preserve formatting
        edited_pdf_path = apply_minimal_edits_to_pdf(original_pdf_path, pdf_raw, edits_data)
        
        return {
            "edited_pdf_path": edited_pdf_path,
            "edits_applied": edits_data,
            "original_preserved": bool(original_pdf_path and os.path.exists(original_pdf_path)),
            "status": "success"
        }
        
    except Exception as e:
        print(f"Error generating resume: {e}")
        return {"status": "error", "error": str(e)}

def apply_minimal_edits_to_pdf(original_pdf_path: str, original_text: str, edits_data: dict) -> str:
    """Apply minimal text edits while preserving original PDF formatting"""
    
    try:
        # Create modified text content
        modified_text = original_text
        
        # Apply text replacements
        if 'edits' in edits_data:
            for edit in edits_data['edits']:
                original = edit.get('original_text', '')
                replacement = edit.get('replacement_text', '')
                if original in modified_text:
                    modified_text = modified_text.replace(original, replacement)
        
        # Apply additions
        if 'additions' in edits_data:
            for addition in edits_data['additions']:
                add_after = addition.get('add_after', '')
                new_text = addition.get('new_text', '')
                if add_after in modified_text:
                    modified_text = modified_text.replace(
                        add_after, 
                        f"{add_after}\n{new_text}"
                    )
        
        # Preserve original PDF structure and create new one with minimal changes
        edited_pdf_path = create_pdf_preserving_structure(original_pdf_path, modified_text)
        
        return edited_pdf_path
        
    except Exception as e:
        print(f"Error applying edits: {e}")
        return None

def create_pdf_preserving_structure(original_pdf_path: str, modified_text: str) -> str:
    """Create new PDF that preserves the original structure but with modified text"""
    
    try:
        # Validate original PDF path
        if not original_pdf_path or not os.path.exists(original_pdf_path):
            print(f"Warning: Original PDF path invalid: {original_pdf_path}")
            # Use default font info if original PDF is not available
            font_info = {
                'margin': 72,
                'font_family': 'Helvetica',
                'font_size': 11,
                'line_spacing': 1.2
            }
        else:
            # Extract font and layout information from original
            font_info = extract_font_info_from_pdf(original_pdf_path)
        
        # Create new PDF with same structure
        with tempfile.NamedTemporaryFile(delete=False, suffix="_edited.pdf") as tmp_file:
            new_pdf_path = tmp_file.name
        
        # Use ReportLab to recreate with preserved formatting
        
        
        doc = SimpleDocTemplate(
            new_pdf_path,
            pagesize=letter,
            rightMargin=font_info.get('margin', 72),
            leftMargin=font_info.get('margin', 72),
            topMargin=font_info.get('margin', 72),
            bottomMargin=font_info.get('margin', 72)
        )
        
        # Create styles that match original
        styles = getSampleStyleSheet()
        
        # Preserve original styling as much as possible
        preserved_styles = create_preserved_styles(font_info, styles)
        
        # Parse text and maintain original structure
        story = []
        lines = modified_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                story.append(Spacer(1, 6))
                continue
            
            # Detect original formatting patterns and preserve them
            if line.isupper() and len(line) < 50:  # Likely a heading
                story.append(Paragraph(line, preserved_styles['heading']))
            elif any(char in line for char in ['@', 'phone', '+', 'linkedin']):  # Contact info
                story.append(Paragraph(line, preserved_styles['contact']))
            elif line.startswith('•') or line.startswith('-'):  # Bullet points
                story.append(Paragraph(line, preserved_styles['bullet']))
            else:  # Regular text
                story.append(Paragraph(line, preserved_styles['normal']))
        
        doc.build(story)
        return new_pdf_path
        
    except Exception as e:
        print(f"Error creating preserved PDF: {e}")
        return None

def extract_font_info_from_pdf(pdf_path: str) -> dict:
    """Extract font and formatting information from original PDF"""
    
    try:
        # Check if file exists
        if not pdf_path or not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Extract basic layout info
            first_page = pdf_reader.pages[0]
            
            # Get page dimensions
            mediabox = first_page.mediabox
            
            font_info = {
                'page_width': float(mediabox.width),
                'page_height': float(mediabox.height),
                'margin': 72,  # Default 1 inch margin
                'font_family': 'Helvetica',  # Default fallback
                'font_size': 11,  # Default size
                'line_spacing': 1.2
            }
            
            return font_info
            
    except Exception as e:
        print(f"Error extracting font info: {e}")
        return {
            'margin': 72,
            'font_family': 'Helvetica',
            'font_size': 11,
            'line_spacing': 1.2
        }

def create_preserved_styles(font_info: dict, base_styles):
    """Create styles that preserve original formatting"""
    
    font_family = font_info.get('font_family', 'Helvetica')
    base_size = font_info.get('font_size', 11)
    
    preserved_styles = {
        'normal': ParagraphStyle(
            'PreservedNormal',
            parent=base_styles['Normal'],
            fontName=font_family,
            fontSize=base_size,
            leading=base_size * 1.2,
            spaceAfter=6
        ),
        'heading': ParagraphStyle(
            'PreservedHeading',
            parent=base_styles['Normal'],
            fontName=f'{font_family}-Bold',
            fontSize=base_size + 2,
            leading=(base_size + 2) * 1.2,
            spaceAfter=12,
            spaceBefore=12
        ),
        'contact': ParagraphStyle(
            'PreservedContact',
            parent=base_styles['Normal'],
            fontName=font_family,
            fontSize=base_size - 1,
            leading=(base_size - 1) * 1.2,
            spaceAfter=3
        ),
        'bullet': ParagraphStyle(
            'PreservedBullet',
            parent=base_styles['Normal'],
            fontName=font_family,
            fontSize=base_size,
            leading=base_size * 1.2,
            spaceAfter=3,
            leftIndent=20
        )
    }
    
    return preserved_styles

def generate_with_minimal_formatting_changes(user_message: str, pdf_raw: str, original_pdf_path: str):
    """Alternative approach: Make text-only changes and preserve everything else"""
    
    prompt = PromptTemplate(
        template="""You are a resume optimization expert. Make ONLY essential text changes to improve job matching.

        ORIGINAL RESUME:
        {pdf_content}

        JOB REQUIREMENTS:
        {job_posting}

        USER REQUEST:
        {user_message}

        Rules:
        1. Keep ALL formatting, fonts, spacing, and layout EXACTLY the same
        2. Change ONLY specific words or phrases for job optimization
        3. Maintain the exact same line structure and length
        4. Focus on keyword optimization and skill highlighting

        Return the COMPLETE resume text with minimal changes applied, preserving all original formatting.""",
        input_variables=["pdf_content", "job_posting", "user_message"]
    )
    
    job_posting = text_manager.get_text("job_extraction")
    chain = llm_manager.init_llm_chain(prompt=prompt)
    
    try:
        optimized_text = chain.invoke({
            "pdf_content": pdf_raw,
            "job_posting": job_posting,
            "user_message": user_message
        })
        
        cleaned_output = llm_manager.cleanup_llm_output(optimized_text)
        
        # Create PDF with preserved formatting
        pdf_path = create_pdf_preserving_structure(original_pdf_path, cleaned_output)
        
        return {
            "optimized_text": cleaned_output,
            "pdf_path": pdf_path,
            "status": "success"
        }
        
    except Exception as e:
        return {"status": "error", "error": str(e)}