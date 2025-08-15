import requests
from bs4 import BeautifulSoup
import re
import json
import html
import html2text

def crawl_job_detail(url: str) -> str:
    """
    Extract and clean data extracted from website link.
    Parameters
    ----------
    url : str
        The string of url that need to fetch.

    Returns
    -------
    content : str
            This will cleaned web content.
    """
    try:
        headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": "cookie_consent_accepted=true; other_cookie=other_value",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1"
        }
        response = requests.get(url, timeout=10, headers=headers, allow_redirects=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html5lib')
        soup = clean_html_content(soup)
        
        # Extract job title and description
        job_title = extract_job_title(soup)
        job_description = extract_job_description(soup)

        # Combine and format the result
        cleaned_content = format_job(job_title, job_description)

        return cleaned_content
    
    except requests.RequestException as e:
        return f"Error fetching URL: {str(e)}"
    except Exception as e:
        return f"Error processing content: {str(e)}"

def extract_job_description_from_jsonld(soup: BeautifulSoup) -> str:
    """Scraping the value from jsonld file and able to give the desired job posting output."""
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string)
            # If the script contains a list, iterate through it
            if isinstance(data, list):
                for entry in data:
                    if entry.get("@type") == "JobPosting" and "description" in entry:
                        return html.unescape(entry["description"])
            # If it's a dict
            elif data.get("@type") == "JobPosting" and "description" in data:
                return html.unescape(data["description"])
        except Exception:
            continue
    return ""

def clean_html_content(soup: BeautifulSoup) -> BeautifulSoup:
    """Return unwanted cleanup html tags requires for job description"""

    # Removing all the script tags
    for script in soup.find_all('script'):
        script.decompose()
    
    # Remove style tags
    for style in soup.find_all('style'):
        style.decompose()

    # Remove navigation content

    for nav in soup.find_all(['nav', 'header', 'footer']):
        nav.decompose()

    # Remove sidebar and other elements
    unwanted_classes = [
        'sidebar', 'advertisement', 'ads', 'banner', 'popup',
        'social-media', 'share', 'related', 'recommended',
        'comments', 'footer', 'header', 'navigation', 'menu'
    ]

    for class_name in unwanted_classes:
        for element in soup.find_all(class_=re.compile(class_name, re.I)):
            element.decompose()

    # Remove elements with common unwanted IDs
    unwanted_ids = [
        'header', 'footer', 'sidebar', 'navigation', 'ads',
        'social', 'share', 'comments', 'related'
    ]

    for id_name in unwanted_ids:
        for element in soup.find_all(id=re.compile(id_name, re.I)):
            element.decompose()

    # Remove cookie consent banners
    cookie_keywords = ['cookie', 'consent', 'gdpr', 'eu-cookie', 'cc-banner', 'cookie-banner']
    for keyword in cookie_keywords:
        # Remove by class
        for tag in soup.find_all(class_=re.compile(keyword, re.I)):
            tag.decompose()
        # Remove by id
        for tag in soup.find_all(id=re.compile(keyword, re.I)):
            tag.decompose()

    # Remove link tags
    for link in soup.find_all('a'):
        link.unwrap()
    
    return soup


def extract_job_title(soup: BeautifulSoup) -> str:
    """Extract job title from the page"""

    # Common selectors for job titles
    title_selectors = [
        'h1',
        '[class*="job-title"]',
        '[class*="title"]',
        '[id*="job-title"]',
        '[id*="title"]',
        'title'
    ]

    for selector in title_selectors:
        title_element = soup.select_one(selector)
        if title_element:
            title = title_element.get_text().strip()
            if title and len(title) > 5:
                return title
            
    title_tag = soup.find('title')
    if title_tag:
        return title_tag.get_text().strip()
    
    return "Job title not found"

def extract_job_description(soup: BeautifulSoup) -> str:
    """Extract job description from the page and convert to markdown"""
    
    # Try JSON-LD first
    jsonld_desc = extract_job_description_from_jsonld(soup)
    if jsonld_desc and len(jsonld_desc.strip()) > 50:
        return jsonld_desc

    description_selectors = [
        '[class*="job-description"]',
        '[class*="description"]',
        '[class*="job-detail"]',
        '[class*="job-content"]',
        '[class*="position-details"]',
        '[class*="position-job-container"]',
        '[class*="wrapper-content"]',
        '[id*="job-description"]',
        '[id*="description"]',
        '[id*="jobdetails-jobsummary"]',
        '[id*="jobdetails-jobdescription-titleheading"]',
        '[id*="jobdetails-minimumqualifications-titleheading"]',
        '[id*="jobdetails-preferredqualifications-titleheading"]',
        'main',
        'article',
        '.content',
        '#content',
        '.job-description',
        '#job-description'
    ]

    markdown_candidates = []
    for selector in description_selectors:
        desc_element = soup.select_one(selector)
        if desc_element:
            markdown_content = html_to_markdown(desc_element)
            if markdown_content and len(markdown_content.strip()) > 50:
                markdown_candidates.append(markdown_content)
    
    if markdown_candidates:
        # Return the longest markdown content (or you can change logic as needed)
        return max(markdown_candidates, key=len)

    # Fallback: try to find the main content area
    main_content = soup.find('main') or soup.find('article')
    if main_content:
        return html_to_markdown(main_content)
    
    # Last resort: get all paragraphs and lists
    content_elements = soup.find_all(['p', 'ul', 'ol', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    if content_elements:
        combined_html = BeautifulSoup('', 'html.parser')
        for element in content_elements:
            combined_html.append(element)
        return html_to_markdown(combined_html)
    
    return "Job description not found"

def html_to_markdown(element) -> str:
    """Convert HTML element to markdown format"""
    
    # Configure html2text
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.ignore_emphasis = False
    h.body_width = 0  # Don't wrap lines
    h.unicode_snob = True
    h.skip_internal_links = True
    
    # Convert to markdown
    markdown = h.handle(str(element))
    
    # Clean up the markdown
    markdown = clean_markdown_content(markdown)
    
    return markdown

def clean_markdown_content(text: str) -> str:
    """Clean and format markdown content"""
    
    # Remove excessive blank lines
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    
    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    # Remove excessive spaces
    text = re.sub(r' +', ' ', text)
    
    # Clean up bullet points
    text = re.sub(r'^\s*[\*\-\+]\s*$', '', text, flags=re.MULTILINE)
    
    # Remove empty list items
    text = re.sub(r'^\s*[\*\-\+]\s*\n', '', text, flags=re.MULTILINE)
    
    return text.strip()

def clean_text_content(text: str)-> str:
    """Clean and format text content"""

    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters and weird symbols
    text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\/\&\$\%\@\#]', ' ', text)
    
    # Remove multiple spaces
    text = re.sub(r' +', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text

def format_job(title: str, description: str) -> str:
    """Format the final job content"""
    formatted_content = f"""
    JOB TITLE:
    {title}

    JOB DESCRIPTION:
    {description}    
    """
    return formatted_content.strip()