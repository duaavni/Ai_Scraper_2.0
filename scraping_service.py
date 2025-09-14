"""
Professional Web Scraping Service
Clean, efficient, and scalable web scraping with DOM analysis
"""
import time
import logging
from typing import Dict, Any, List, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup
import requests
from config import HEADLESS, TIMEOUT, USER_AGENT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProfessionalScrapingService:
    """
    Professional web scraping service with advanced DOM analysis
    Features: Multiple scraping methods, DOM analysis, error handling, and performance monitoring
    """
    
    def __init__(self):
        """Initialize the scraping service"""
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        logger.info("Scraping service initialized")
    
    def scrape_website(self, url: str, use_selenium: bool = False, extract_links: bool = False, extract_images: bool = False) -> Dict[str, Any]:
        """
        Scrape a website with professional error handling and analysis
        
        Args:
            url: The URL to scrape
            use_selenium: Whether to use Selenium for dynamic content
        
        Returns:
            Dictionary with scraped content, DOM analysis, and metadata
        """
        start_time = time.time()
        
        try:
            # Validate URL
            if not url or not url.strip():
                return self._create_error_result("Invalid URL provided", start_time)
            
            # Scrape content
            if use_selenium:
                raw_content = self._scrape_with_selenium(url)
                method = "selenium"
            else:
                raw_content = self._scrape_with_requests(url)
                method = "requests"
            
            # Analyze DOM structure
            dom_analysis = self._analyze_dom_structure(raw_content)
            
            # Clean content
            cleaned_content = self._clean_content(raw_content)
            
            # Extract links and images if requested
            extracted_links = []
            extracted_images = []
            
            if extract_links:
                extracted_links = self.extract_links(raw_content)
            
            if extract_images:
                extracted_images = self.extract_images(raw_content)
            
            processing_time = time.time() - start_time
            
            logger.info(f"Successfully scraped {url} in {processing_time:.2f}s using {method}")
            
            return {
                "success": True,
                "url": url,
                "content": cleaned_content,
                "raw_content": raw_content,
                "dom_analysis": dom_analysis,
                "extracted_links": extracted_links,
                "extracted_images": extracted_images,
                "processing_time": processing_time,
                "method": method,
                "metadata": {
                    "content_length": len(cleaned_content),
                    "raw_length": len(raw_content),
                    "elements_count": dom_analysis["total_elements"],
                    "links_count": dom_analysis["links"],
                    "images_count": dom_analysis["images"]
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to scrape {url}: {e}")
            return self._create_error_result(str(e), start_time)
    
    def _scrape_with_requests(self, url: str) -> str:
        """Scrape using requests (faster for static content)"""
        try:
            response = self.session.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"HTTP request failed: {e}")
    
    def _scrape_with_selenium(self, url: str) -> str:
        """Scrape using Selenium (better for dynamic content)"""
        chrome_options = Options()
        if HEADLESS:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(f"--user-agent={USER_AGENT}")
        
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        try:
            driver.get(url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Additional wait for dynamic content
            time.sleep(2)
            
            return driver.page_source
            
        except TimeoutException:
            raise Exception("Page load timeout - content may be too slow to load")
        except WebDriverException as e:
            raise Exception(f"Selenium error: {e}")
        finally:
            driver.quit()
    
    def _analyze_dom_structure(self, html_content: str) -> Dict[str, Any]:
        """
        Comprehensive DOM structure analysis
        """
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Basic element counts
            analysis = {
                "total_elements": len(soup.find_all()),
                "headings": {},
                "links": len(soup.find_all("a")),
                "images": len(soup.find_all("img")),
                "forms": len(soup.find_all("form")),
                "tables": len(soup.find_all("table")),
                "divs": len(soup.find_all("div")),
                "paragraphs": len(soup.find_all("p")),
                "lists": len(soup.find_all(["ul", "ol"])),
                "classes": [],
                "ids": [],
                "scripts": len(soup.find_all("script")),
                "styles": len(soup.find_all("style"))
            }
            
            # Count heading levels
            for i in range(1, 7):
                headings = soup.find_all(f"h{i}")
                analysis["headings"][f"h{i}"] = len(headings)
            
            # Extract unique classes and IDs
            all_classes = set()
            all_ids = set()
            
            for element in soup.find_all(class_=True):
                classes = element.get("class", [])
                if isinstance(classes, list):
                    all_classes.update(classes)
                else:
                    all_classes.add(classes)
            
            for element in soup.find_all(id=True):
                element_id = element.get("id")
                if element_id:
                    all_ids.add(element_id)
            
            analysis["classes"] = sorted(list(all_classes))[:50]  # Limit to 50
            analysis["ids"] = sorted(list(all_ids))[:50]  # Limit to 50
            
            # Content analysis
            text_content = soup.get_text()
            analysis["text_length"] = len(text_content)
            analysis["word_count"] = len(text_content.split())
            
            # Structure quality indicators
            analysis["structure_quality"] = self._assess_structure_quality(analysis)
            
            return analysis
            
        except Exception as e:
            logger.warning(f"DOM analysis failed: {e}")
            return {"error": str(e), "total_elements": 0}
    
    def _assess_structure_quality(self, analysis: Dict[str, Any]) -> str:
        """Assess the quality of DOM structure"""
        score = 0
        
        # Check for semantic elements
        if analysis["headings"].get("h1", 0) > 0:
            score += 2
        if analysis["paragraphs"] > 0:
            score += 1
        if analysis["links"] > 0:
            score += 1
        if analysis["images"] > 0:
            score += 1
        
        # Check for structure
        if analysis["divs"] > 0:
            score += 1
        if analysis["tables"] > 0:
            score += 1
        
        # Check for accessibility
        if analysis["ids"]:
            score += 1
        if analysis["classes"]:
            score += 1
        
        if score >= 7:
            return "excellent"
        elif score >= 5:
            return "good"
        elif score >= 3:
            return "fair"
        else:
            return "poor"
    
    def _clean_content(self, html_content: str) -> str:
        """
        Clean HTML content and extract meaningful text
        """
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Remove unwanted elements
            unwanted_tags = ["script", "style", "nav", "footer", "header", "aside", "noscript"]
            for tag in soup(unwanted_tags):
                tag.decompose()
            
            # Get text content with proper spacing
            text = soup.get_text(separator="\n")
            
            # Clean up whitespace
            lines = []
            for line in text.splitlines():
                cleaned_line = line.strip()
                if cleaned_line:
                    lines.append(cleaned_line)
            
            return "\n".join(lines)
            
        except Exception as e:
            logger.warning(f"Content cleaning failed: {e}")
            return html_content
    
    def extract_links(self, html_content: str) -> List[Dict[str, str]]:
        """Extract all links from HTML content"""
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            links = []
            
            for link in soup.find_all("a", href=True):
                href = link["href"]
                text = link.get_text().strip()
                
                if href and text:  # Only include links with both href and text
                    links.append({
                        "text": text,
                        "href": href,
                        "title": link.get("title", "")
                    })
            
            return links
            
        except Exception as e:
            logger.warning(f"Link extraction failed: {e}")
            return []
    
    def extract_images(self, html_content: str) -> List[Dict[str, str]]:
        """Extract all images from HTML content"""
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            images = []
            
            for img in soup.find_all("img", src=True):
                images.append({
                    "src": img["src"],
                    "alt": img.get("alt", ""),
                    "title": img.get("title", ""),
                    "width": img.get("width", ""),
                    "height": img.get("height", "")
                })
            
            return images
            
        except Exception as e:
            logger.warning(f"Image extraction failed: {e}")
            return []
    
    def _create_error_result(self, error_message: str, start_time: float) -> Dict[str, Any]:
        """Create a standardized error result"""
        return {
            "success": False,
            "url": "",
            "content": "",
            "raw_content": "",
            "dom_analysis": {},
            "extracted_links": [],
            "extracted_images": [],
            "error": error_message,
            "processing_time": time.time() - start_time,
            "method": "none"
        }
    
    def get_service_info(self) -> Dict[str, Any]:
        """Get service information"""
        return {
            "status": "operational",
            "methods": ["requests", "selenium"],
            "features": [
                "dom_analysis",
                "content_cleaning",
                "link_extraction",
                "image_extraction",
                "structure_quality_assessment"
            ],
            "user_agent": USER_AGENT,
            "timeout": TIMEOUT
        }


class AdvancedWebScrapingService:
    """
    Advanced async web scraping service for dashboard
    Wrapper around ProfessionalScrapingService with async support
    """
    
    def __init__(self):
        self.scraping_service = ProfessionalScrapingService()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
    
    async def scrape_website_async(self, url: str, use_selenium: bool = False, 
                                 wait_for_elements: List[str] = None,
                                 extract_images: bool = False, 
                                 extract_links: bool = False):
        """
        Async wrapper for scraping website
        
        Args:
            url: The URL to scrape
            use_selenium: Whether to use Selenium for dynamic content
            wait_for_elements: CSS selectors to wait for (not implemented in sync version)
            extract_images: Whether to extract and return all images
            extract_links: Whether to extract and return all links
        
        Returns:
            Scraping result
        """
        # For now, we'll use the sync version
        # In a real implementation, you'd want to use asyncio.to_thread or similar
        import asyncio
        result = await asyncio.to_thread(
            self.scraping_service.scrape_website,
            url=url,
            use_selenium=use_selenium,
            extract_links=extract_links,
            extract_images=extract_images
        )
        
        # Convert to a simple object for dashboard compatibility
        class ScrapingResult:
            def __init__(self, data):
                self.url = data.get("url", "")
                self.success = data.get("success", False)
                self.content = data.get("content", "")
                self.raw_content = data.get("raw_content", "")
                self.dom_analysis = data.get("dom_analysis", {})
                self.extracted_links = data.get("extracted_links", [])
                self.extracted_images = data.get("extracted_images", [])
                self.processing_time = data.get("processing_time", 0)
                self.method = data.get("method", "none")
                self.status_code = 200 if data.get("success", False) else 400
                self.error = data.get("error", "")
                self.metadata = data.get("metadata", {})
        
        return ScrapingResult(result)
    
    async def scrape_multiple_urls(self, urls: List[str], max_concurrent: int = 5, 
                                 use_selenium: bool = False):
        """
        Scrape multiple URLs concurrently
        
        Args:
            urls: List of URLs to scrape
            max_concurrent: Maximum concurrent requests
            use_selenium: Whether to use Selenium for dynamic content
        
        Returns:
            List of scraping results
        """
        import asyncio
        import aiohttp
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def scrape_single(url):
            async with semaphore:
                try:
                    return await self.scrape_website_async(url, use_selenium=use_selenium)
                except Exception as e:
                    return e
        
        tasks = [scrape_single(url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)