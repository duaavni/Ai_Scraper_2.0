# AI Web Scraper 🕸️

A professional AI-powered web scraping solution that combines advanced web scraping with intelligent content extraction using state-of-the-art language models.

## 🚀 Features

- **🧠 Intelligent Web Scraping**: Advanced scraping for both static and dynamic websites
- **🤖 AI-Powered Extraction**: Natural language instructions for content extraction
- **🏗️ DOM Structure Analysis**: Comprehensive analysis of webpage structure
- **📊 Performance Monitoring**: Real-time metrics and health monitoring
- **🔧 Professional Architecture**: Clean, scalable, and maintainable code
- **⚡ High Performance**: Optimized for speed and efficiency

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd WebScraper
   ```

2. **Create virtual environment**
   ```bash
   python -m venv ai
   ai\Scripts\activate  # Windows
   # or
   source ai/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Ollama and pull a model**
   ```bash
   # Install Ollama from https://ollama.ai
   ollama pull llama3.2:1b
   ```

## 🎯 Usage

### Web Interface (Streamlit)

```bash
streamlit run main.py
```

Then open your browser to `http://localhost:8501`

### Features Available:
- **🕸️ Web Scraping**: Scrape any website with intelligent content extraction
- **🤖 AI Extraction**: Use natural language to extract specific information
- **🏗️ DOM Analysis**: View complete webpage structure and analysis
- **📊 Performance Metrics**: Monitor scraping and extraction performance
- **🔧 System Health**: Check service status and configuration

## 📖 How It Works

1. **Web Scraping**: Uses Selenium for dynamic content or requests for static content
2. **Content Cleaning**: Removes unnecessary HTML elements and extracts clean text
3. **AI Processing**: Uses Ollama with LangChain to intelligently extract specific information
4. **Results**: Returns structured, extracted data ready for use

## 🔧 Configuration

Create a `.env` file to customize settings:

```env
AI_MODEL=llama3.2:1b
AI_TEMPERATURE=0.1
CHUNK_SIZE=6000
HEADLESS=true
TIMEOUT=30
API_HOST=0.0.0.0
API_PORT=8000
```

## 🏗️ Architecture

### **Clean Service Architecture**
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │   AI Service     │    │ Scraping Service│
│   (main.py)     │    │   (ai_service.py)│    │(scraping_service│
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌──────────────────┐
                    │   Configuration  │
                    │   (config.py)    │
                    └──────────────────┘
```

### **Key Components**
- **ProfessionalAIService**: Advanced AI content extraction with error handling
- **ProfessionalScrapingService**: Robust web scraping with DOM analysis
- **Configuration Management**: Environment-based settings
- **Performance Monitoring**: Real-time metrics and health checks

## 🎯 Example Use Cases

- **E-commerce**: Extract product names, prices, and descriptions
- **News Sites**: Extract article titles, dates, and content
- **Business Directories**: Extract contact information and company details
- **Research**: Extract specific data points from multiple pages
- **Data Collection**: Extract structured information from various sources

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Interface │    │   REST API       │    │   AI Service    │
│   (Streamlit)   │    │   (FastAPI)      │    │   (LangChain)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌──────────────────┐
                    │ Scraping Service │
                    │   (Selenium)     │
                    └──────────────────┘
```

## 🚀 Perfect for Gen AI Roles

This project demonstrates:
- **AI Integration**: Using LangChain and Ollama for intelligent content processing
- **Modern Python**: FastAPI, Streamlit, and async programming
- **Clean Architecture**: Separated concerns and easy to understand code
- **Scalability**: Built with production-ready frameworks
- **Real-world Application**: Practical use case for AI in web scraping

## 📝 License

MIT License - feel free to use this project for your Gen AI role interviews!

## 🤝 Contributing

Contributions are welcome! This is a simple, educational project perfect for learning and demonstrating AI skills.
