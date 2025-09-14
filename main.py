"""
Professional AI Web Scraper
Clean, efficient, and scalable web scraping with intelligent content extraction
"""
import streamlit as st
import time
import logging
import pandas as pd
from ai_service import ProfessionalAIService
from scraping_service import ProfessionalScrapingService
from config import DEBUG, LOG_LEVEL

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL))
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="AI Web Scraper",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .success-metric {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    .info-metric {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    .warning-metric {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize services
@st.cache_resource
def get_services():
    """Initialize AI and scraping services"""
    try:
        ai_service = ProfessionalAIService()
        scraping_service = ProfessionalScrapingService()
        return ai_service, scraping_service
    except Exception as e:
        st.error(f"Failed to initialize services: {e}")
        return None, None

ai_service, scraping_service = get_services()

# Initialize session state
if 'scraping_history' not in st.session_state:
    st.session_state.scraping_history = []
if 'extraction_history' not in st.session_state:
    st.session_state.extraction_history = []
if 'performance_metrics' not in st.session_state:
    st.session_state.performance_metrics = {
        'total_scrapes': 0,
        'total_extractions': 0,
        'avg_scraping_time': 0,
        'avg_extraction_time': 0,
        'success_rate': 0
    }

# Header
st.markdown('<h1 class="main-header">🕸️ AI Web Scraper</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    if ai_service:
        # AI Model info
        model_info = ai_service.get_service_info()
        st.subheader("🤖 AI Model")
        st.info(f"Model: {model_info['model']}")
        st.info(f"Temperature: {model_info['temperature']}")
        st.info(f"Chunk Size: {model_info['chunk_size']}")
        
        # Service status
        health = ai_service.health_check()
        status_color = "🟢" if health["status"] == "healthy" else "🔴"
        st.info(f"Status: {status_color} {health['status'].title()}")
    else:
        st.error("AI Service not available")
    
    # Scraping options
    st.subheader("🕸️ Scraping Options")
    use_selenium = st.checkbox("Use Selenium (for dynamic content)", value=False)
    
    # Performance metrics
    st.subheader("📊 Performance")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Websites Scraped", st.session_state.performance_metrics['total_scrapes'])
        st.metric("Success Rate", f"{st.session_state.performance_metrics['success_rate']:.1f}%")
    with col2:
        st.metric("AI Extractions", st.session_state.performance_metrics['total_extractions'])
        st.metric("Avg Processing", f"{st.session_state.performance_metrics['avg_scraping_time']:.1f}s")

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "🕸️ Scrape & Extract", "📊 Results", "🔧 System Info"])

with tab1:
    st.header("Welcome to AI Web Scraper")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 What it does")
        st.markdown("""
        This professional AI-powered web scraper provides:
        - **Intelligent Web Scraping** (static and dynamic content)
        - **AI-Powered Extraction** using advanced language models
        - **DOM Structure Analysis** for technical insights
        - **Professional Error Handling** and performance monitoring
        - **Scalable Architecture** for production use
        """)
    
    with col2:
        st.subheader("🚀 Key Features")
        features = [
            "🧠 **AI Content Extraction** - Natural language instructions",
            "🏗️ **DOM Analysis** - Complete structure breakdown",
            "⚡ **Dual Scraping** - Requests + Selenium support",
            "📊 **Performance Metrics** - Real-time monitoring",
            "🔧 **Professional Architecture** - Clean, maintainable code",
            "📈 **Scalable Design** - Ready for production deployment"
        ]
        
        for feature in features:
            st.markdown(f"• {feature}")
    
    # Quick stats
    st.subheader("📈 System Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card success-metric">', unsafe_allow_html=True)
        st.metric("Total Scrapes", st.session_state.performance_metrics['total_scrapes'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card info-metric">', unsafe_allow_html=True)
        st.metric("Success Rate", f"{st.session_state.performance_metrics['success_rate']:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card warning-metric">', unsafe_allow_html=True)
        st.metric("AI Extractions", st.session_state.performance_metrics['total_extractions'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg Time", f"{st.session_state.performance_metrics['avg_scraping_time']:.1f}s")
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.header("🕸️ Scrape & Extract")
    
    if not ai_service or not scraping_service:
        st.error("Services not available. Please check the configuration.")
        st.stop()
    
    # URL input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        url = st.text_input(
            "Enter Website URL",
            placeholder="https://quotes.toscrape.com",
            help="Enter the URL you want to scrape"
        )
        
        with st.expander("🔧 More Options"):
            # Advanced options
            col_a, col_b = st.columns(2)
            with col_a:
                st.session_state.extract_links = st.checkbox("Extract Links", value=st.session_state.get('extract_links', False))
            with col_b:
                st.session_state.extract_images = st.checkbox("Extract Images", value=st.session_state.get('extract_images', False))
            
    
    with col2:
        if st.button("🚀 Scrape Website", type="primary", use_container_width=True):
            if url:
                with st.spinner("Scraping website..."):
                    result = scraping_service.scrape_website(url, use_selenium, st.session_state.extract_links, st.session_state.extract_images)
                    
                    if result["success"]:
                        st.session_state.scraping_result = result
                        st.session_state.scraping_count = st.session_state.performance_metrics['total_scrapes'] + 1
                        st.session_state.performance_metrics['total_scrapes'] = st.session_state.scraping_count
                        
                        # Update success rate
                        if result["success"]:
                            current_rate = st.session_state.performance_metrics['success_rate']
                            total = st.session_state.performance_metrics['total_scrapes']
                            st.session_state.performance_metrics['success_rate'] = (
                                (current_rate * (total - 1) + 100) / total
                            )
                        
                        # Update average time
                        current_avg = st.session_state.performance_metrics['avg_scraping_time']
                        total = st.session_state.performance_metrics['total_scrapes']
                        st.session_state.performance_metrics['avg_scraping_time'] = (
                            (current_avg * (total - 1) + result["processing_time"]) / total
                        )
                        
                        st.success("✅ Website scraped successfully!")
                    else:
                        st.error(f"❌ Error: {result['error']}")
            else:
                st.warning("Please enter a URL")
    
    # Display scraping results
    if 'scraping_result' in st.session_state:
        result = st.session_state.scraping_result
        
        st.subheader("📄 Scraping Results")
        
        # Show metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Status", "✅ Success" if result["success"] else "❌ Failed")
        with col2:
            st.metric("Processing Time", f"{result['processing_time']:.2f}s")
        with col3:
            st.metric("Content Length", f"{len(result['content']):,} characters")
        with col4:
            st.metric("Method", result["method"].title())
        
        # Additional metrics for extracted content
        if result.get("extracted_links") or result.get("extracted_images"):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Extracted Links", len(result.get("extracted_links", [])))
            with col2:
                st.metric("Extracted Images", len(result.get("extracted_images", [])))
            with col3:
                st.metric("Total DOM Links", result.get("dom_analysis", {}).get("links", 0))
            with col4:
                st.metric("Total DOM Images", result.get("dom_analysis", {}).get("images", 0))
        
        # Content display
        with st.expander("🔍 View Scraped Content"):
            st.text_area("Content", result["content"], height=300)
        
        # Extracted Links
        if result.get("extracted_links"):
            with st.expander("🔗 Extracted Links"):
                links = result["extracted_links"]
                st.write(f"**Found {len(links)} links:**")
                
                # Create a DataFrame for better display
                links_data = []
                for i, link in enumerate(links[:50]):  # Limit to first 50 links
                    links_data.append({
                        "Text": link["text"][:100] + "..." if len(link["text"]) > 100 else link["text"],
                        "URL": link["href"],
                        "Title": link.get("title", "")
                    })
                
                if links_data:
                    df = pd.DataFrame(links_data)
                    st.dataframe(df, use_container_width=True)
                    
                    if len(links) > 50:
                        st.info(f"Showing first 50 of {len(links)} links. Use AI extraction to get all links.")
                else:
                    st.info("No links with text found.")
        
        # Extracted Images
        if result.get("extracted_images"):
            with st.expander("🖼️ Extracted Images"):
                images = result["extracted_images"]
                st.write(f"**Found {len(images)} images:**")
                
                # Create a DataFrame for better display
                images_data = []
                for i, img in enumerate(images[:50]):  # Limit to first 50 images
                    images_data.append({
                        "Source": img["src"],
                        "Alt Text": img.get("alt", ""),
                        "Title": img.get("title", ""),
                        "Dimensions": f"{img.get('width', '?')}x{img.get('height', '?')}"
                    })
                
                if images_data:
                    df = pd.DataFrame(images_data)
                    st.dataframe(df, use_container_width=True)
                    
                    if len(images) > 50:
                        st.info(f"Showing first 50 of {len(images)} images. Use AI extraction to get all images.")
                else:
                    st.info("No images found.")
        
        # DOM Structure
        with st.expander("🏗️ DOM Structure Analysis"):
            dom_analysis = result.get("dom_analysis", {})
            
            if dom_analysis:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Element Counts")
                    st.metric("Total Elements", dom_analysis.get("total_elements", 0))
                    st.metric("Links", dom_analysis.get("links", 0))
                    st.metric("Images", dom_analysis.get("images", 0))
                    st.metric("Divs", dom_analysis.get("divs", 0))
                
                with col2:
                    st.subheader("Content Analysis")
                    st.metric("Word Count", dom_analysis.get("word_count", 0))
                    st.metric("Paragraphs", dom_analysis.get("paragraphs", 0))
                    st.metric("Tables", dom_analysis.get("tables", 0))
                    st.metric("Structure Quality", dom_analysis.get("structure_quality", "Unknown"))
                
                # Show headings
                headings = dom_analysis.get("headings", {})
                if any(count > 0 for count in headings.values()):
                    st.subheader("Heading Structure")
                    for heading, count in headings.items():
                        if count > 0:
                            st.metric(f"{heading.upper()}", count)
                
                # Show classes and IDs
                if dom_analysis.get("classes"):
                    st.subheader("CSS Classes (first 20)")
                    st.write(", ".join(dom_analysis["classes"][:20]))
                
                if dom_analysis.get("ids"):
                    st.subheader("Element IDs (first 20)")
                    st.write(", ".join(dom_analysis["ids"][:20]))
        
        # Raw HTML
        with st.expander("📄 Raw HTML"):
            st.text_area("HTML Source", result["raw_content"], height=300)
        
        # AI Extraction
        st.subheader("🤖 AI Content Extraction")
        
        extraction_instructions = st.text_area(
            "What do you want to extract?",
            placeholder="e.g., Extract all quotes and their authors, or Extract product names and prices...",
            height=100
        )
        
        if st.button("🧠 Extract with AI", type="primary"):
            if extraction_instructions.strip():
                with st.spinner("AI is analyzing and extracting content..."):
                    extraction_result = ai_service.extract_content(
                        result["content"], 
                        extraction_instructions
                    )
                    
                    if extraction_result["success"]:
                        st.session_state.extraction_result = extraction_result
                        st.session_state.performance_metrics['total_extractions'] += 1
                        
                        # Update average extraction time
                        current_avg = st.session_state.performance_metrics['avg_extraction_time']
                        total = st.session_state.performance_metrics['total_extractions']
                        st.session_state.performance_metrics['avg_extraction_time'] = (
                            (current_avg * (total - 1) + extraction_result["processing_time"]) / total
                        )
                        
                        st.success("✅ AI extraction completed!")
                    else:
                        st.error(f"❌ Extraction failed: {extraction_result['error']}")
            else:
                st.warning("Please describe what you want to extract")

with tab3:
    st.header("📊 Results & Analytics")
    
    # Show extraction results
    if 'extraction_result' in st.session_state:
        result = st.session_state.extraction_result
        
        st.subheader("🤖 AI Extraction Results")
        
        # Show metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Status", "✅ Success" if result["success"] else "❌ Failed")
        with col2:
            st.metric("Confidence", f"{result['confidence']:.2f}")
        with col3:
            st.metric("Processing Time", f"{result['processing_time']:.2f}s")
        with col4:
            st.metric("Chunks Processed", result.get("chunks_processed", 0))
        
        # Show extracted content
        st.subheader("📄 Extracted Content")
        st.text_area("AI Extracted Data", result["content"], height=400)
        
        # Show metadata
        with st.expander("📊 Processing Details"):
            metadata = result.get("metadata", {})
            st.json({
                "Model Used": result.get("model_used", "Unknown"),
                "Processing Time": f"{result['processing_time']:.2f} seconds",
                "Chunks Processed": result.get("chunks_processed", 0),
                "Successful Chunks": result.get("successful_chunks", 0),
                "Confidence Score": f"{result['confidence']:.2f}",
                "Content Length": metadata.get("content_length", 0),
                "Chunk Size": metadata.get("chunk_size", 0),
                "Temperature": metadata.get("temperature", 0)
            })
    
    else:
        st.info("No extraction results yet. Go to 'Scrape & Extract' tab to get started!")
    
    # Show statistics
    if st.session_state.performance_metrics['total_scrapes'] > 0 or st.session_state.performance_metrics['total_extractions'] > 0:
        st.subheader("📈 Performance Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Websites Scraped", st.session_state.performance_metrics['total_scrapes'])
            st.metric("Average Scraping Time", f"{st.session_state.performance_metrics['avg_scraping_time']:.2f}s")
        
        with col2:
            st.metric("Total AI Extractions", st.session_state.performance_metrics['total_extractions'])
            st.metric("Average Extraction Time", f"{st.session_state.performance_metrics['avg_extraction_time']:.2f}s")

with tab4:
    st.header("🔧 System Information")
    
    if ai_service and scraping_service:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🤖 AI Service")
            ai_info = ai_service.get_service_info()
            st.json(ai_info)
            
            st.subheader("🕸️ Scraping Service")
            scraping_info = scraping_service.get_service_info()
            st.json(scraping_info)
        
        with col2:
            st.subheader("📊 System Health")
            ai_health = ai_service.health_check()
            st.json(ai_health)
            
            st.subheader("⚙️ Configuration")
            config_info = {
                "Debug Mode": DEBUG,
                "Log Level": LOG_LEVEL,
                "AI Model": ai_info.get("model", "Unknown"),
                "Temperature": ai_info.get("temperature", "Unknown"),
                "Chunk Size": ai_info.get("chunk_size", "Unknown")
            }
            st.json(config_info)
    else:
        st.error("Services not available")

# Footer
st.markdown("---")
st.markdown("**AI Web Scraper | Smart Web Scraping**")