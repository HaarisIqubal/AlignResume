<h1 align="center">
  <a href="">
    Athenis 
  </a>
</h1>
<p align="center">
  <strong>Automated Resume Builder 📑</strong>
  <br>
  Build better resume.
</p>

<p align="center">
  <a href="https://github.com/HaarisIqubal/AlignResume/blob/main/LICENSE.txt">
    <img src="https://img.shields.io/badge/license-GPL3.0-blue.svg" alt="Align Resume is released under the GPL3.0 license." />
  </a>
</p>

## Introduction
An intelligent CV/Resume builder that automates the process of creating tailored resumes by extracting information from existing CVs and job descriptions. Built with Streamlit and powered by advanced text processing techniques.

## 🚀 Features

- **PDF Resume Extraction**: Upload and extract text from PDF resumes
- **Job Description Scraping**: Extract job requirements from job portal URLs
- **Resume Analysis**: Parse and categorize resume sections (skills, experience, education)
- **Interactive UI**: Clean, user-friendly Streamlit interface

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Web Scraping**: BeautifulSoup4, Requests
- **Text Processing**: Regular Expressions, NLP libraries, spacy, SentenceTransformers
- **Python Version**: 3.11+

## 📋 Prerequisites

- Python 3.11 or higher
- pip package manager
- Internet connection (for job description extraction)

## 🔧 Installation

### Local Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AlignResume
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Installation using UV

1. **Install UV from your vendor provider**
   Follow the link : [UV Installation](https://docs.astral.sh/uv/getting-started/installation/)

2. **Install dependencies**
   ```bash
   uv pip install -e .
   ```

## 🚀 How to Run

1. **Start the application**
   ```bash
   streamlit run main.py
   ```

2. **Access the web interface**
   - Open your browser and navigate to `http://localhost:8501`
   - The application will launch automatically

## 📦 Required Dependencies

```
"beautifulsoup4>=4.13.4",
"docling>=2.42.2",
"html2text>=2025.4.15",
"langchain>=0.3.26",
"langchain-google-genai>=2.1.8",
"langchain-ollama>=0.3.6",
"langchain-openai>=0.3.28",
"pydantic>=2.11.7",
"pypdf2>=3.0.1",
"reportlab>=4.4.3",
"sentence-transformers>=5.0.0",
"streamlit>=1.47.0"
```

## 📃 Documentation

1. [How to use](https://github.com/HaarisIqubal/AlignResume/wiki/Usage-Guide)
2. [Project structure](https://github.com/HaarisIqubal/AlignResume/wiki/Project-Structure)
3. [Development guide](https://github.com/HaarisIqubal/AlignResume/wiki/Development-Guide)
4. [Contribution guide](https://github.com/HaarisIqubal/AlignResume/wiki/Contribution-Guide)
5. [How to use](https://github.com/HaarisIqubal/AlignResume/wiki/Usage-Guide)
6. [Future enhancement](https://github.com/HaarisIqubal/AlignResume/wiki/Future-Enhancement)

## 💾 Supported File Formats

### Input Formats
- **Resume**: PDF files (`.pdf`)
- **Job URLs**: Web links from major job portals
- **User Modification**: User can describe how they want to add new data and new things.

### Output Formats
- **Text**: Plain text extraction
- **Markdown**: Structured content with formatting
- **Streamlit Display**: Interactive web interface
- **Downloadable PDF**: User can download the resume from the internet

## ➕ Support

For support, bug reports, or feature requests:
- Create an issue on GitHub
- Review troubleshooting section

---

### **Note**: This tool is designed to assist in resume building and should be used responsibly. Always review generated content before submitting applications.

---

<p align="center">><strong>Developed with ❤️ for automated resume building from 🇩🇪.</strong> </p>
