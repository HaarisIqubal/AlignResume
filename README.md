# AlignResume - Automated Resume Builder 📑

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


## 📦 Required Dependencies

```
"beautifulsoup4>=4.13.4",
"docling>=2.42.2",
"html2text>=2025.4.15",
"langchain>=0.3.26",
"sentence-transformers>=5.0.0",
"streamlit>=1.47.0"
```

## 🚀 How to Run

1. **Start the application**
   ```bash
   streamlit run main.py
   ```

2. **Access the web interface**
   - Open your browser and navigate to `http://localhost:8501`
   - The application will launch automatically

## 📖 How to Use

### 1. Upload Your Resume
- Click "Upload your CV" in the sidebar
- Select a PDF file (supported format: `.pdf`)
- Click "Process CV" to extract text content
- ✅ Success indicator will show when processing is complete

### 2. Extract Job Description
- Paste a job portal URL in the "Enter Job portal URL" field
- Click "Extract job description" to scrape job requirements
- ✅ Success indicator will confirm extraction

### 3. Add Personal Description
- Use the "Enter your CV description" text area
- Add any additional information or customizations
- Content is automatically saved as you type

### 4. Build Tailored CV
- Click "Let's build it 🔨..." to generate your tailored resume
- The system will match your skills with job requirements
- View results in the main interface

## 📁 Project Structure

```
cv_maker/
├── main.py                 # Application entry point
├── src/
│   ├── ui/
│   │   ├── setupview.py    # Main UI layout
│   │   ├── sidebar.py      # Sidebar components
│   │   └── text_state_manager.py  # State management
│   └── tool/
│       ├── document_extractor.py  # PDF processing
│       └── job_extractor.py       # Web scraping
├── LICENSE.txt             # GPL v3 License
├── .python-version         # Python version specification
└── README.md              # Project documentation
```

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

## 🎯 Key Features Explained

### Job Description Extractor
- Scrapes job requirements from popular job portals
- Converts HTML to clean markdown format

### Text State Management
- Centralized storage for all extracted content
- Persistent state across user interactions
- Easy access to resume data, job descriptions, and user inputs

## 🔍 Browser Compatibility

- **Chrome**: ✅ Fully supported
- **Safari**: ✅ Fully supported


## 🐛 Troubleshooting

### Common Issues

1. **PDF extraction fails**
   - Ensure PDF is text-based (not scanned images)
   - Check file size (max 200MB recommended)
   - Try re-uploading the file

2. **Job description extraction returns empty**
   - Verify the URL is accessible
   - Some sites may block automated requests
   - Try a different job portal URL

3. **Application won't start**
   - Check Python version: `python --version`
   - Verify all dependencies are installed
   - Try running: `pip install --upgrade streamlit`

### Error Messages

- `"Error processing content"`: PDF may be corrupted or password-protected
- `"Error fetching URL"`: Network issue or blocked request
- `"No resume uploaded yet"`: Upload a PDF file first

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.txt](LICENSE.txt) file for details.

## 🔮 Future Enhancements

- [ ] Support for more documents formats (.docx, latex)
- [ ] AI-powered skill matching
- [ ] Multiple output formats (PDF, Word, HTML)
- [ ] Resume templates and themes
- [ ] Batch processing capabilities
- [ ] Integration with job application APIs

## 👨‍💻 Author

Developed with ❤️ for automated resume building from 🇩🇪.

## 📞 Support

For support, bug reports, or feature requests:
- Create an issue on GitHub
- Review troubleshooting section

---

### **Note**: This tool is designed to assist in resume building and should be used responsibly. Always review generated content before submitting applications.

---