# Presales Intel

AI-powered intelligence brief generation for presales meetings. Get comprehensive company research, technical analysis, and meeting preparation in seconds instead of hours.

## 🎯 What It Does

Generate comprehensive intelligence briefs for presales meetings with:

- **Company Context** - Overview, recent news, business priorities, and industry position
- **Attendee Analysis** - Role-based insights and engagement strategies (when attendees provided)
- **Tech Stack & Security** - Technology analysis, security gaps, and modernization needs
- **Competitive Landscape** - Current vendors, competitive positioning, and key differentiators
- **Talking Points** - Discovery questions, objection handling, and value propositions

## ✨ Features

- ⚡ **Fast Generation** - Get comprehensive briefs in 15-30 seconds
- 🔄 **Real-Time Data** - Live company information from Google Knowledge Graph and recent news
- 🤖 **AI-Powered** - GPT-4 synthesizes data into actionable insights
- 📊 **Brief History** - Access and review previously generated briefs
- 🎨 **Modern UI** - Clean, responsive interface built with DaisyUI
- 📱 **Print & Export** - Copy to clipboard or print briefs for offline use

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: HTMX + Jinja2 + DaisyUI
- **AI**: OpenAI GPT-4 Turbo
- **Data Sources**: SerpAPI (Google Search & News)
- **Database**: SQLite (upgradeable to PostgreSQL)
- **Deployment**: Docker-ready

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))
- SerpAPI key ([get one here](https://serpapi.com/) - 100 free searches/month)

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd presales-intel
```

2. **Create virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment**

Copy the example environment file and add your API keys:

```bash
cp env.example .env
```

Edit `.env` and add:

```env
OPENAI_API_KEY=sk-your-openai-key-here
SERP_API_KEY=your-serpapi-key-here
```

5. **Run the application**

```bash
uvicorn app.main:app --reload
```

6. **Open in browser**

Navigate to http://localhost:8000

## 📖 Usage

### Generating a Brief

1. Enter a company name (required)
2. Optionally add key attendees with their titles
3. Click "Generate Intelligence Brief"
4. Wait 15-30 seconds for AI generation
5. Review the formatted brief with proper markdown rendering

### Viewing History

- Click "History" in the navigation bar
- View all previously generated briefs
- Click any brief to see full details

### Exporting Briefs

- **Print**: Click the print button to save as PDF
- **Copy**: Use the copy button to copy brief text to clipboard

## 🏗️ Project Structure

```
presales-intel/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # Database configuration
│   ├── models.py               # SQLAlchemy models
│   ├── templates_config.py     # Shared Jinja2 configuration
│   ├── routers/
│   │   └── briefs.py           # Brief generation endpoints
│   ├── services/
│   │   ├── intelligence.py    # GPT-4 brief generation
│   │   └── data_sources.py    # SerpAPI integrations
│   ├── templates/              # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── history.html
│   │   ├── brief_detail.html
│   │   └── components/
│   └── static/                 # Static files
├── requirements.txt
├── Dockerfile
├── env.example
└── README.md
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 | Yes |
| `SERP_API_KEY` | SerpAPI key for Google search | Yes |
| `DATABASE_URL` | Database connection string | No (defaults to SQLite) |
| `DEBUG` | Enable debug mode | No |

### API Rate Limits

- **SerpAPI Free Tier**: 100 searches/month (50 briefs)
- **OpenAI GPT-4**: Pay-per-use (~$0.10-0.15 per brief)

## 🐳 Docker Deployment

### Build and Run

```bash
docker build -t presales-intel .
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e SERP_API_KEY=your_key \
  --name presales-intel \
  presales-intel
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - SERP_API_KEY=${SERP_API_KEY}
    volumes:
      - ./presales_intel.db:/app/presales_intel.db
```

Run with:

```bash
docker-compose up -d
```

## ☁️ Cloud Deployment

### Fly.io

```bash
fly launch
fly secrets set OPENAI_API_KEY=your_key SERP_API_KEY=your_key
fly deploy
```

### Railway

1. Connect your Git repository
2. Add environment variables in dashboard
3. Deploy automatically on push

### Other Platforms

The application can be deployed to any platform supporting Python/Docker:
- Heroku
- Render
- DigitalOcean App Platform
- AWS App Runner

## 🔌 API Endpoints

### Web Interface

- `GET /` - Landing page with brief generation form
- `POST /briefs/generate` - Generate new intelligence brief
- `GET /briefs/history` - View all generated briefs
- `GET /briefs/{id}` - View specific brief details

### API Documentation

When running locally, access interactive API docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Development

### Running in Development Mode

```bash
uvicorn app.main:app --reload
```

The `--reload` flag enables auto-reload on code changes.

### Database Management

The SQLite database is created automatically on first run. To inspect:

```bash
sqlite3 presales_intel.db
.tables
SELECT * FROM briefs;
```

### Adding Data Sources

To add new data integrations:

1. Add API key to `.env`
2. Implement method in `app/services/data_sources.py`
3. Call from `app/services/intelligence.py` before GPT-4 generation

Example integrations to add:
- Clearbit (company data)
- LinkedIn Sales Navigator (attendee research)
- BuiltWith (tech stack detection)
- CRM APIs (Salesforce, HubSpot)

## 📊 Performance

- **Average Generation Time**: 20 seconds
- **SerpAPI Calls**: 2 per brief (~3-5 seconds)
- **GPT-4 Generation**: ~10-15 seconds
- **Database**: SQLite (suitable for single-user MVP)

## 🔒 Security Considerations

- Store API keys in environment variables (never commit to git)
- Use `.env` file locally (already in `.gitignore`)
- For production, use secret management (Fly.io secrets, Railway env vars, etc.)
- Consider rate limiting for public deployments
- Add authentication before multi-user deployment

## 🛣️ Roadmap

### Planned Features

- [ ] User authentication and teams
- [ ] Additional data sources (Clearbit, LinkedIn, BuiltWith)
- [ ] CRM integrations (Salesforce, HubSpot)
- [ ] Brief templates customization
- [ ] PDF export
- [ ] Calendar integration for automatic brief scheduling
- [ ] Email briefs before meetings
- [ ] PostgreSQL migration for production
- [ ] React frontend upgrade (post-validation)

## 🤝 Contributing

This is currently a validation MVP. Contributions welcome after product-market fit is established.

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- SerpAPI for Google search access
- FastAPI for the excellent web framework
- DaisyUI for beautiful components
- HTMX for simple dynamic interactions

## 📧 Support

For issues, questions, or feature requests, please open an issue in the repository.

---

**Built with ❤️ for presales professionals who want to win more deals.**

