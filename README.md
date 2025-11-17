# PrepCall

AI-powered intelligence brief generation for presales meetings. Get comprehensive company research, technical analysis, and meeting preparation in seconds instead of hours.

## The Problem

Every presales engineer and sales professional manually researches prospects before calls:

- Company website, LinkedIn, and recent news review
- Tech stack analysis (BuiltWith, job postings)
- Prior emails and CRM notes
- Competitor research
- Talking points and objection prep

**Time Cost**: 1-2 hours per meeting × 5-10 meetings/week = 5-20 hours/week lost to manual research.

## The Opportunity

### What Exists (And Why It's Not Enough)

**Data Aggregation Tools** (not synthesis):
- ZoomInfo, Apollo, Cognism - Contact data dumps, no analysis
- Clearbit, BuiltWith - Tech stack lists, no context
- Clay - Manual workflow building, requires setup

**Post-Meeting Analysis** (wrong timing):
- Gong, Chorus, Fireflies, Fathom - Transcribe after calls
- Useful for coaching, useless for prep

**Intent/Signals** (not actionable):
- 6sense, Demandbase - "In-market" signals without guidance
- Don't tell you what to actually say

**Closest Competitors**:
- Attention AI, Sybill - Shallow pre-call briefings (basic scraping + CRM)
- Wingman - AE-focused, not presales-specific
- Momentum (YC) - CRM updates, light prep features

### The Gap We Fill

No tools provide:
- **Deep technical context synthesis** for presales engineers
- **Tech stack → security gaps → talking points** (actionable insights)
- **Competitive landscape → predicted objections** (strategic positioning)
- **Company news → business priorities → solution fit** (contextual relevance)
- **Persona-specific tailoring** (CISO vs IT manager vs procurement)

### Why This Works

- **Underserved Market**: Presales engineers are overlooked (most tools target AEs)
- **Clear Value Prop**: 2 hours → 20 seconds = 30-60x time savings
- **Low Technical Risk**: API orchestration, not ML invention
- **Proven Need**: Every B2B company needs this, no one has solved it well

## What It Does

Generate comprehensive intelligence briefs for presales meetings with:

- **Company Context** - Overview, recent news, business priorities, and industry position
- **Attendee Analysis** - Role-based insights and engagement strategies (when attendees provided)
- **Tech Stack & Security** - Technology analysis, security gaps, and modernization needs
- **Competitive Landscape** - Current vendors, competitive positioning, and key differentiators
- **Talking Points** - Discovery questions, objection handling, and value propositions

## Features

- **Fast Generation** - Get comprehensive briefs in 15-30 seconds
- **Real-Time Data** - Live company information from Google Knowledge Graph and recent news
- **AI-Powered** - GPT-4 synthesizes data into actionable insights
- **Brief History** - Access and review previously generated briefs
- **Modern UI** - Clean, responsive interface built with DaisyUI
- **Print & Export** - Copy to clipboard or print briefs for offline use

## Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: HTMX + Jinja2 + DaisyUI
- **AI**: OpenAI GPT-4 Turbo
- **Data Sources**: SerpAPI (Google Search & News)
- **Database**: SQLite (upgradeable to PostgreSQL)
- **Deployment**: Docker-ready

## Quick Start

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

## Usage

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

## Project Structure

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

## Configuration

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

## Docker Deployment

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

## Cloud Deployment

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

## API Endpoints

### Web Interface

- `GET /` - Landing page with brief generation form
- `POST /briefs/generate` - Generate new intelligence brief
- `GET /briefs/history` - View all generated briefs
- `GET /briefs/{id}` - View specific brief details

### API Documentation

When running locally, access interactive API docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Development

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

## Performance

- **Average Generation Time**: 20 seconds
- **SerpAPI Calls**: 2 per brief (~3-5 seconds)
- **GPT-4 Generation**: ~10-15 seconds
- **Database**: SQLite (suitable for single-user MVP)

## Security Considerations

- Store API keys in environment variables (never commit to git)
- Use `.env` file locally (already in `.gitignore`)
- For production, use secret management (Fly.io secrets, Railway env vars, etc.)
- Consider rate limiting for public deployments
- Add authentication before multi-user deployment

## Roadmap

### Current Status: MVP Validation

This is a validation MVP built to test the core hypothesis: Can AI-generated briefs replace manual research for presales engineers?

### Planned Enhancements

**Data Sources** (High Priority):
- [ ] Clearbit API - Company data and tech stack enrichment
- [ ] LinkedIn Sales Navigator - Attendee research and background
- [ ] BuiltWith API - Actual technology detection
- [ ] CRM integrations (Salesforce, HubSpot) - Internal notes and history

**Features**:
- [ ] User authentication and teams
- [ ] Brief templates customization
- [ ] PDF export with branding
- [ ] Calendar integration for automatic brief scheduling
- [ ] Email briefs before meetings
- [ ] Collaborative notes and feedback

**Technical**:
- [ ] PostgreSQL migration for production
- [ ] Redis caching for faster repeated lookups
- [ ] Rate limiting and usage monitoring
- [ ] React frontend upgrade (post-validation)
- [ ] Comprehensive test coverage

## Contributing

This is currently a validation MVP. Contributions welcome after product-market fit is established.

## License

MIT License - see LICENSE file for details

## Acknowledgments

- OpenAI for GPT-4 API
- SerpAPI for Google search access
- FastAPI for the excellent web framework
- DaisyUI for beautiful components
- HTMX for simple dynamic interactions

## Support

For issues, questions, or feature requests, please open an issue in the repository.

---

**PrepCall - Built for presales professionals who want to win more deals.**

Visit us at [prepcall.io](https://prepcall.io)

