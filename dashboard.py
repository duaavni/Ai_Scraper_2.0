"""
Enhanced Streamlit Dashboard for AI Web Scraper
Features advanced UI, real-time monitoring, and comprehensive analytics
"""
import streamlit as st
import asyncio
import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import time
from typing import Dict, List, Any

from ai_service import ProfessionalAIService
from scraping_service import AdvancedWebScrapingService
from config import AI_MODEL, AI_TEMPERATURE, CHUNK_SIZE, DEBUG, LOG_LEVEL

# Page configuration
st.set_page_config(
    page_title="AI Web Scraper Dashboard",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
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
    .warning-metric {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .info-metric {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-left: 20px;
        padding-right: 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

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

# Initialize services
@st.cache_resource
def get_services():
    """Get AI and scraping services"""
    return ProfessionalAIService(), AdvancedWebScrapingService()

ai_service, scraping_service = get_services()

# Header
st.markdown('<h1 class="main-header">🕸️ AI Web Scraper Dashboard</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # AI Model Selection
    st.subheader("AI Model")
    selected_model = st.selectbox(
        "Select AI Model",
        [AI_MODEL, "llama3.2:3b", "llama3.2:7b"],
        index=0
    )
    
    # Extraction Type
    st.subheader("Extraction Type")
    extraction_type = st.selectbox(
        "Select Extraction Type",
        ["text", "json", "structured"],
        index=0
    )
    
    # Advanced Settings
    st.subheader("Advanced Settings")
    use_selenium = st.checkbox("Use Selenium (for dynamic content)", value=False)
    chunk_size = st.slider("Chunk Size", 1000, 10000, CHUNK_SIZE)
    max_concurrent = st.slider("Max Concurrent Requests", 1, 10, 5)
    
    # Performance Metrics
    st.subheader("📊 Performance")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Scrapes", st.session_state.performance_metrics['total_scrapes'])
        st.metric("Success Rate", f"{st.session_state.performance_metrics['success_rate']:.1f}%")
    with col2:
        st.metric("Avg Scraping Time", f"{st.session_state.performance_metrics['avg_scraping_time']:.2f}s")
        st.metric("Avg Extraction Time", f"{st.session_state.performance_metrics['avg_extraction_time']:.2f}s")

# Main content tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Home", "🕸️ Scraping", "🤖 AI Extraction", "📊 Analytics", "⚡ Batch Processing"
])

with tab1:
    st.header("Welcome to AI Web Scraper Dashboard")
    
    # Quick stats
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
        st.metric("Avg Processing Time", f"{st.session_state.performance_metrics['avg_scraping_time']:.2f}s")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Available Models", 3)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent activity
    st.subheader("📈 Recent Activity")
    if st.session_state.scraping_history:
        recent_data = pd.DataFrame(st.session_state.scraping_history[-10:])
        st.dataframe(recent_data[['url', 'success', 'processing_time', 'timestamp']], use_container_width=True)
    else:
        st.info("No recent activity. Start scraping to see data here!")

with tab2:
    st.header("🕸️ Web Scraping")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        url = st.text_input(
            "Enter Website URL",
            placeholder="https://example.com",
            help="Enter the URL you want to scrape"
        )
        
        # Advanced options
        with st.expander("🔧 Advanced Options"):
            wait_for_elements = st.text_input(
                "Wait for Elements (CSS selectors, comma-separated)",
                placeholder=".content, #main, .article",
                help="CSS selectors to wait for before scraping"
            )
            extract_images = st.checkbox("Extract Images", value=False)
            extract_links = st.checkbox("Extract Links", value=False)
    
    with col2:
        st.subheader("Quick Actions")
        if st.button("🚀 Scrape Website", type="primary", use_container_width=True):
            if url:
                with st.spinner("Scraping website..."):
                    try:
                        # Run scraping directly
                        from scraping_service import ProfessionalScrapingService
                        scraper = ProfessionalScrapingService()
                        result_data = scraper.scrape_website(
                            url=url,
                            use_selenium=use_selenium,
                            extract_links=extract_links,
                            extract_images=extract_images
                        )
                        
                        # Convert to ScrapingResult object for compatibility
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
                        
                        result = ScrapingResult(result_data)
                        
                        # Store result
                        st.session_state.scraping_result = result
                        st.session_state.scraping_history.append({
                            'url': result.url,
                            'success': result.success,
                            'processing_time': result.processing_time,
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'status_code': result.status_code
                        })
                        
                        # Update metrics
                        st.session_state.performance_metrics['total_scrapes'] += 1
                        if result.success:
                            st.session_state.performance_metrics['success_rate'] = (
                                st.session_state.performance_metrics['success_rate'] * 
                                (st.session_state.performance_metrics['total_scrapes'] - 1) + 100
                            ) / st.session_state.performance_metrics['total_scrapes']
                        
                        st.session_state.performance_metrics['avg_scraping_time'] = (
                            st.session_state.performance_metrics['avg_scraping_time'] * 
                            (st.session_state.performance_metrics['total_scrapes'] - 1) + result.processing_time
                        ) / st.session_state.performance_metrics['total_scrapes']
                        
                        st.success("Scraping completed successfully!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error scraping website: {e}")
            else:
                st.warning("Please enter a URL to scrape")
        
        if st.button("🔄 Clear Results", use_container_width=True):
            if 'scraping_result' in st.session_state:
                del st.session_state.scraping_result
            st.rerun()
    
    # Display results
    if 'scraping_result' in st.session_state:
        result = st.session_state.scraping_result
        
        st.subheader("📄 Scraping Results")
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Status", "✅ Success" if result.success else "❌ Failed")
        with col2:
            st.metric("Processing Time", f"{result.processing_time:.2f}s")
        with col3:
            st.metric("Content Length", f"{len(result.content):,} characters")
        
        # Additional metrics for extracted content
        if hasattr(result, 'extracted_links') and result.extracted_links or hasattr(result, 'extracted_images') and result.extracted_images:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Extracted Links", len(getattr(result, 'extracted_links', [])))
            with col2:
                st.metric("Extracted Images", len(getattr(result, 'extracted_images', [])))
            with col3:
                st.metric("Total DOM Links", result.dom_analysis.get("links", 0) if hasattr(result, 'dom_analysis') else 0)
            with col4:
                st.metric("Total DOM Images", result.dom_analysis.get("images", 0) if hasattr(result, 'dom_analysis') else 0)
        
        # Content display
        with st.expander("🔍 View Scraped Content"):
            st.text_area("Content", result.content, height=300)
        
        # Extracted Links
        if hasattr(result, 'extracted_links') and result.extracted_links:
            with st.expander("🔗 Extracted Links"):
                links = result.extracted_links
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
        if hasattr(result, 'extracted_images') and result.extracted_images:
            with st.expander("🖼️ Extracted Images"):
                images = result.extracted_images
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
        
        # Metadata
        if result.metadata:
            with st.expander("📊 Metadata"):
                st.json(result.metadata)

with tab3:
    st.header("🤖 AI Content Extraction")
    
    if 'scraping_result' not in st.session_state:
        st.warning("Please scrape a website first to extract content from it.")
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            extraction_description = st.text_area(
                "Describe what to extract",
                placeholder="e.g., Extract all product names, prices, and descriptions...",
                height=100
            )
            
            # Content preview
            with st.expander("📄 Content Preview"):
                content_preview = st.session_state.scraping_result.content[:1000] + "..."
                st.text(content_preview)
        
        with col2:
            if st.button("🧠 Extract Content", type="primary", use_container_width=True):
                if extraction_description.strip():
                    with st.spinner("Extracting content with AI..."):
                        try:
                            # Clean content
                            body_content = scraping_service.scraping_service.extract_body_content(st.session_state.scraping_result.content)
                            cleaned_content = scraping_service.scraping_service.clean_body_content(body_content)
                            
                            # Split into chunks
                            chunks = scraping_service.scraping_service.split_dom_content(cleaned_content, chunk_size)
                            
                            # Extract content directly
                            result = ai_service.extract_content(
                                content=cleaned_content,
                                instructions=extraction_description
                            )
                            
                            # Store result
                            st.session_state.extraction_result = result
                            st.session_state.extraction_history.append({
                                'description': extraction_description,
                                'confidence': result.get('confidence', 0.0),
                                'processing_time': result.get('processing_time', 0.0),
                                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'extraction_type': extraction_type
                            })
                            
                            # Update metrics
                            st.session_state.performance_metrics['total_extractions'] += 1
                            st.session_state.performance_metrics['avg_extraction_time'] = (
                                st.session_state.performance_metrics['avg_extraction_time'] * 
                                (st.session_state.performance_metrics['total_extractions'] - 1) + result.get('processing_time', 0.0)
                            ) / st.session_state.performance_metrics['total_extractions']
                            
                            st.success("Content extraction completed!")
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"Error extracting content: {e}")
                else:
                    st.warning("Please describe what you want to extract")
        
        # Display extraction results
        if 'extraction_result' in st.session_state:
            result = st.session_state.extraction_result
            
            st.subheader("📄 Extraction Results")
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Confidence", f"{result.get('confidence', 0.0):.2f}")
            with col2:
                st.metric("Processing Time", f"{result.get('processing_time', 0.0):.2f}s")
            with col3:
                st.metric("Extraction Type", extraction_type)
            
            # Extracted content
            st.text_area("Extracted Content", result.get('content', ''), height=300)
            
            # Metadata
            if result.get('metadata'):
                with st.expander("📊 Extraction Metadata"):
                    st.json(result.get('metadata', {}))

with tab4:
    st.header("📊 Analytics & Monitoring")
    
    # Performance charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Scraping Performance")
        if st.session_state.scraping_history:
            df = pd.DataFrame(st.session_state.scraping_history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Success rate over time
            df['success_numeric'] = df['success'].astype(int)
            success_rate = df.groupby(df['timestamp'].dt.date)['success_numeric'].mean() * 100
            
            # fig = px.line(
            #     x=success_rate.index, 
            #     y=success_rate.values,
            #     title="Success Rate Over Time",
            #     labels={'x': 'Date', 'y': 'Success Rate (%)'}
            # )
            # st.plotly_chart(fig, use_container_width=True)
            st.info("Charts require plotly installation: pip install plotly")
        else:
            st.info("No scraping data available for analytics")
    
    with col2:
        st.subheader("Processing Time Trends")
        if st.session_state.scraping_history:
            df = pd.DataFrame(st.session_state.scraping_history)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # fig = px.scatter(
            #     df, 
            #     x='timestamp', 
            #     y='processing_time',
            #     color='success',
            #     title="Processing Time vs Time",
            #     labels={'processing_time': 'Processing Time (s)', 'timestamp': 'Time'}
            # )
            # st.plotly_chart(fig, use_container_width=True)
            st.info("Charts require plotly installation: pip install plotly")
        else:
            st.info("No data available for processing time analysis")
    
    # Model performance
    if st.session_state.extraction_history:
        st.subheader("AI Model Performance")
        df = pd.DataFrame(st.session_state.extraction_history)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Confidence distribution
            # fig = px.histogram(
            #     df, 
            #     x='confidence',
            #     title="Confidence Score Distribution",
            #     labels={'confidence': 'Confidence Score', 'count': 'Frequency'}
            # )
            # st.plotly_chart(fig, use_container_width=True)
            st.info("Charts require plotly installation: pip install plotly")
        
        with col2:
            # Processing time by extraction type
            # fig = px.box(
            #     df, 
            #     x='extraction_type', 
            #     y='processing_time',
            #     title="Processing Time by Extraction Type",
            #     labels={'processing_time': 'Processing Time (s)', 'extraction_type': 'Extraction Type'}
            # )
            # st.plotly_chart(fig, use_container_width=True)
            st.info("Charts require plotly installation: pip install plotly")

with tab5:
    st.header("⚡ Batch Processing")
    
    st.subheader("Multiple URL Scraping")
    
    # URL input
    urls_text = st.text_area(
        "Enter URLs (one per line)",
        placeholder="https://example1.com\nhttps://example2.com\nhttps://example3.com",
        height=150
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        batch_extraction_description = st.text_area(
            "Extraction Description",
            placeholder="e.g., Extract all article titles and publication dates...",
            height=100
        )
    
    with col2:
        if st.button("🚀 Start Batch Processing", type="primary", use_container_width=True):
            if urls_text.strip():
                urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
                
                if urls:
                    with st.spinner(f"Processing {len(urls)} URLs..."):
                        try:
                            # Run batch scraping
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            
                            async def batch_scrape():
                                async with AdvancedWebScrapingService() as scraper:
                                    return await scraper.scrape_multiple_urls(
                                        urls=urls,
                                        max_concurrent=max_concurrent,
                                        use_selenium=use_selenium
                                    )
                            
                            results = loop.run_until_complete(batch_scrape())
                            loop.close()
                            
                            # Store results
                            st.session_state.batch_results = results
                            
                            st.success(f"Batch processing completed! Processed {len(urls)} URLs.")
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"Error in batch processing: {e}")
                else:
                    st.warning("Please enter at least one valid URL")
            else:
                st.warning("Please enter URLs to process")
    
    # Display batch results
    if 'batch_results' in st.session_state:
        st.subheader("📊 Batch Processing Results")
        
        results = st.session_state.batch_results
        successful = [r for r in results if not isinstance(r, Exception) and r.success]
        failed = [r for r in results if isinstance(r, Exception) or not r.success]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total URLs", len(results))
        with col2:
            st.metric("Successful", len(successful))
        with col3:
            st.metric("Failed", len(failed))
        
        # Results table
        results_data = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                results_data.append({
                    'URL': f"URL {i+1}",
                    'Status': '❌ Error',
                    'Processing Time': 'N/A',
                    'Error': str(result)
                })
            else:
                results_data.append({
                    'URL': result.url,
                    'Status': '✅ Success' if result.success else '❌ Failed',
                    'Processing Time': f"{result.processing_time:.2f}s",
                    'Error': result.error or 'None'
                })
        
        st.dataframe(pd.DataFrame(results_data), use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "Built with ❤️ using Streamlit, LangChain, and Ollama | "
    "AI Web Scraper Dashboard v2.0"
)
