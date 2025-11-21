# ContextCraft 🚀

> **Enhanced AI Project Structure Generator** - Rapidly scaffold professional software projects with modern tech stacks and best practices built-in.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Overview

ContextCraft automates the tedious process of project scaffolding. Instead of manually creating folders, configuration files, and boilerplate code, ContextCraft generates production-ready project structures in seconds. Perfect for rapid prototyping, hackathons, microservices, and standardizing project structures across teams.

## Key Features

✨ **10 Modern Tech Stacks**
- Backend: Flask, FastAPI, Express, Django
- Frontend: React, Vue.js, Svelte
- Full Stack: Streamlit, Next.js, SvelteKit
- AI: Pydantic AI

🏗️ **Complete Project Structure**
- Organized folder hierarchies
- Configuration files (requirements.txt, package.json, etc.)
- Docker & Docker Compose ready
- Environment variable templates
- .gitignore files
- Pre-configured test directories

📋 **6 Project Type Templates**
1. AI Agent Projects
2. Web Applications
3. API Services
4. Data Science Projects
5. Full Stack Applications
6. Custom Projects

🎯 **Interactive CLI**
- User-friendly prompts
- Clear next steps guidance
- Project history support (planned)
- Batch operations (planned)

## Installation

### Option 1: Direct Download
```bash
# Clone the repository
git clone https://github.com/fuentej/ContextCraftlocal.git
cd ContextCraftlocal

# Run directly
python newprojectv3.py
```

### Option 2: Global Installation (Coming Soon)
```bash
pip install contextcraft
contextcraft
```

### Option 3: Docker (Coming Soon)
```bash
docker run -it contextcraft:latest
```

## Quick Start

```bash
# Start the generator
python newprojectv3.py

# Follow the interactive prompts:
# 1. Enter your project name
# 2. Select project type (1-6)
# 3. Choose tech stack (1-10)
# 4. Done! Your project is ready

# Navigate to your new project
cd your_project_name

# Start coding!
```

## Supported Tech Stacks

| # | Tech Stack | Type | Best For |
|---|---|---|---|
| 1 | Python/Flask | Backend | Simple APIs, lightweight servers |
| 2 | Python/FastAPI | Backend | Modern async APIs, automatic docs |
| 3 | Python/Streamlit | Full Stack | Data dashboards, ML demos |
| 4 | Node.js/Express | Backend | JavaScript backends, real-time apps |
| 5 | React/TypeScript | Frontend | Interactive UIs, SPAs |
| 6 | Next.js/TypeScript | Full Stack | Full-stack React apps, SSR |
| 7 | Vue.js/TypeScript | Frontend | Progressive web apps |
| 8 | Svelte/SvelteKit | Full Stack | High-performance UIs, modern DX |
| 9 | Python/Django | Backend | Large projects, admin panels |
| 10 | Pydantic AI | AI Agent | AI agents, LLM applications |

## Project Types

### AI Agent
Scaffolding for AI-powered applications with LLM integration.
- Agent logic structure
- Environment configuration for API keys
- Example prompt templates
- Testing setup for agent behavior

### Web App
Frontend-focused application structure.
- Component organization
- State management setup
- Styling configuration
- Build optimization

### API Service
Backend API with database integration.
- Route organization
- Authentication setup
- Database configuration
- API documentation

### Data Science
Research and analysis project structure.
- Jupyter notebook directory
- Data storage organization
- Model artifact management
- Experiment tracking setup

### Full Stack App
Complete application with frontend and backend.
- Frontend and backend separation
- Database schema setup
- API integration examples
- Deployment configuration

### Custom
Completely blank structure for unique needs.
- Flexible folder organization
- No opinionated structure
- Ideal for experimental projects

## Generated Project Structure

Example structure for a FastAPI project:

```
my_api_project/
├── README.md              # Project documentation
├── PLANNING.md            # Project planning template
├── TASK.md                # Task tracking template
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git exclusions
├── .cursorrules           # Editor configuration
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Multi-container setup
├── app/
│   ├── main.py           # Application entry point
│   ├── config.py         # Configuration management
│   └── models/           # Data models
├── tests/
│   ├── __init__.py
│   └── test_main.py      # Test examples
├── docs/
│   └── API.md            # API documentation
└── terraform/            # Infrastructure as Code
    ├── main.tf
    └── variables.tf
```

## Usage Examples

### Create a FastAPI Backend
```bash
$ python newprojectv3.py
Project name: my-api
Choose project type (1-6): 3     # API Service
Choose tech stack (1-10): 2      # Python/FastAPI

✅ Project 'my-api' created!
📁 Location: /path/to/my-api

📦 Next steps:
1. cd my-api
2. python -m venv venv
3. source venv/bin/activate  # or venv\Scripts\activate on Windows
4. pip install -r requirements.txt
5. uvicorn app.main:app --reload
```

### Create a Full-Stack Next.js App
```bash
$ python newprojectv3.py
Project name: my-app
Choose project type (1-6): 5     # Full Stack App
Choose tech stack (1-10): 6      # Next.js/TypeScript

✅ Project 'my-app' created!
📁 Location: /path/to/my-app

📦 Next steps:
1. cd my-app
2. npm install
3. npm run dev
4. Open http://localhost:3000
```

### Create an AI Agent Project
```bash
$ python newprojectv3.py
Project name: ai-assistant
Choose project type (1-6): 1     # AI Agent
Choose tech stack (1-10): 10     # Pydantic AI

✅ Project 'ai-assistant' created!
📁 Location: /path/to/ai-assistant

📦 Next steps:
1. cd ai-assistant
2. python -m venv venv
3. source venv/bin/activate
4. pip install -r requirements.txt
5. python app/main.py
```

## What Gets Created

Each generated project includes:

📄 **Documentation**
- `README.md` - Project overview and setup instructions
- `PLANNING.md` - Project planning and architecture
- `TASK.md` - Task tracking and progress

⚙️ **Configuration**
- Dependency files (requirements.txt, package.json)
- Environment templates (.env.example)
- Build configurations (tsconfig.json for TypeScript projects)
- Editor configs (.cursorrules for Cursor IDE)

🐳 **DevOps**
- Dockerfile for containerization
- docker-compose.yml for orchestration
- Terraform/IAC templates for cloud deployment

📝 **Code Structure**
- Entry point file (app.py, main.py, package.json, etc.)
- Model/schema definitions
- Test directory with examples
- Placeholder files for additional code

🚀 **Deployment Ready**
- Production-ready configurations
- Environment variable management
- Container setup
- Infrastructure as Code templates

## Contributing

We welcome contributions! Here's how to get involved:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ContextCraftlocal.git
cd ContextCraftlocal

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dev dependencies (coming soon)
pip install -r requirements-dev.txt

# Run tests
pytest
```

## Roadmap

### Phase 1 (Q4 2024)
- [x] Core project generation
- [ ] Comprehensive documentation
- [ ] Unit tests
- [ ] PyPI package

### Phase 2 (Q1 2025)
- [ ] Web UI interface
- [ ] Advanced template customization
- [ ] GitHub Actions CI/CD
- [ ] Community templates

### Phase 3 (Q2 2025)
- [ ] AI-powered code generation
- [ ] Cloud deployment integration
- [ ] VS Code extension
- [ ] Template marketplace

### Phase 4 (Q3 2025+)
- [ ] Enterprise features
- [ ] Plugin ecosystem
- [ ] Team collaboration
- [ ] Advanced monitoring

## FAQ

**Q: Can I customize the templates?**
A: Yes! All templates are editable. Modify the template files in the `templates/` directory to customize generated projects.

**Q: Does ContextCraft work on Windows?**
A: Yes! ContextCraft works on Windows, macOS, and Linux.

**Q: Can I use ContextCraft for production projects?**
A: Absolutely! ContextCraft generates production-ready structures with best practices built-in.

**Q: How do I remove a generated project?**
A: Simply delete the project folder. ContextCraft doesn't modify your system beyond creating the project directory.

**Q: Can I contribute my own tech stack?**
A: Yes! We're planning a plugin system. Watch this repo for updates.

**Q: Is there a web version?**
A: Coming soon! We're working on a web UI for easier project creation.

## Performance & Stats

- ⚡ **Generation Time**: < 1 second
- 📦 **Supported Stacks**: 10
- 🎯 **Project Types**: 6
- 📂 **Files Generated**: 15-20 per project
- 🧪 **Test Coverage**: Coming soon

## Security

This project follows responsible disclosure practices. For security concerns, please see [SECURITY.md](SECURITY.md).

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Credits

Created by the ContextCraft team. Special thanks to all contributors.

## Support

- 📧 Email: support@contextcraft.dev (coming soon)
- 💬 Issues: [GitHub Issues](https://github.com/fuentej/ContextCraftlocal/issues)
- 🐦 Twitter: [@ContextCraft](https://twitter.com/contextcraft) (coming soon)
- 📚 Docs: [Full Documentation](https://contextcraft.dev) (coming soon)

## Acknowledgments

ContextCraft was inspired by:
- Cookiecutter
- Yeoman
- Create React App
- Django Startproject
- FastAPI Best Practices

---

**Happy scaffolding! 🎉**

Made with ❤️ by developers, for developers.
