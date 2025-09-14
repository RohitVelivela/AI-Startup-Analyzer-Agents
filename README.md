# AI Startup Analyzer Agents

A comprehensive AI-powered platform for analyzing startup opportunities, market research, and competitor intelligence using multiple AI agents.

## 🚀 Overview

This project consists of a React frontend and FastAPI backend that leverages multiple AI agents to provide startup analysis, market research, and competitive intelligence. The system uses Google's Gemini AI and various web scraping tools to gather and analyze business data.

## 🏗️ Architecture

### Frontend (React)
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Heroicons, Lucide React
- **Charts**: Recharts for data visualization
- **HTTP Client**: Axios
- **Notifications**: React Hot Toast

### Backend (FastAPI)
- **Framework**: FastAPI with Python
- **AI Integration**: Google Generative AI (Gemini)
- **Web Scraping**: Exa, DuckDuckGo Search, Firecrawl
- **Data Processing**: Pandas
- **Report Generation**: ReportLab, WeasyPrint
- **Agent Framework**: Agno

## 📂 Project Structure

```
AI-Startup-Analyzer-Agents/
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── Dockerfile
│   └── tailwind.config.js
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── .env.example
├── .gitignore
└── README.md
```

## 🛠️ Installation & Setup

### Prerequisites
- Node.js (v16+)
- Python (3.8+)
- Docker (optional)

### Environment Variables
1. Copy `.env.example` to `.env`
2. Fill in your API keys:
   - Google AI API key
   - Exa API key
   - Other required API keys

### Local Development

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

### Docker Setup

#### Build and run with Docker
```bash
# Build backend
cd backend
docker build -t startup-analyzer-backend .

# Build frontend
cd frontend
docker build -t startup-analyzer-frontend .

# Run containers
docker run -p 8000:8000 startup-analyzer-backend
docker run -p 3000:3000 startup-analyzer-frontend
```

## 🤖 AI Agents

The platform includes multiple specialized AI agents:

1. **Market Research Agent** - Analyzes market trends and opportunities
2. **Competitor Analysis Agent** - Researches competitors and market positioning
3. **Financial Analysis Agent** - Evaluates financial metrics and projections
4. **Content Generation Agent** - Creates reports and summaries

## 📊 Features

- **Startup Analysis**: Comprehensive evaluation of startup ideas and business models
- **Market Research**: Deep dive into target markets and customer segments
- **Competitor Intelligence**: Detailed competitor analysis and positioning
- **Financial Projections**: AI-powered financial modeling and analysis
- **Report Generation**: Automated PDF report creation
- **Interactive Dashboard**: Real-time data visualization and insights

## 🚀 Usage

1. Access the web application at http://localhost:3000
2. Input your startup idea or company information
3. Select the type of analysis you want to perform
4. Let the AI agents gather and analyze the data
5. Review the generated insights and download reports

## 🔧 API Endpoints

- `GET /health` - Health check
- `POST /analyze/startup` - Startup analysis
- `POST /analyze/market` - Market research
- `POST /analyze/competitors` - Competitor analysis
- `GET /reports/{report_id}` - Download generated reports

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- [GitHub Repository](https://github.com/RohitVelivela/AI-Startup-Analyzer-Agents)
- [Documentation](#) (coming soon)
- [Demo](#) (coming soon)

## 🆘 Support

For support and questions, please open an issue on GitHub or contact the development team.