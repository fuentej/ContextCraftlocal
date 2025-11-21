#!/usr/bin/env python3
"""
Enhanced AI Project Structure Generator
Creates folders and files using template files you can edit separately.
Now includes modern frontend frameworks!
V3.0.0
"""

import os
import shutil
from datetime import datetime
from pathlib import Path

class EnhancedProjectGenerator:
    """Creates project structure with editable template files and modern tech stacks."""
    
    def __init__(self):
        # Path to your template files (adjust as needed)
        self.template_dir = Path("templates")
        
        # Project types with their specific needs
        self.project_types = {
            "1": {"name": "AI Agent", "folder": "ai-agent"},
            "2": {"name": "Web App", "folder": "web-app"}, 
            "3": {"name": "API Service", "folder": "api-service"},
            "4": {"name": "Data Science", "folder": "data-science"},
            "5": {"name": "Full Stack App", "folder": "full-stack"},
            "6": {"name": "Custom", "folder": "custom"}
        }
        
        # Enhanced tech stacks with modern options
        self.tech_stacks = {
            "1": {"name": "Python/Flask", "folder": "python-flask", "type": "backend"},
            "2": {"name": "Python/FastAPI", "folder": "python-fastapi", "type": "backend"},
            "3": {"name": "Python/Streamlit", "folder": "python-streamlit", "type": "fullstack"},
            "4": {"name": "Node.js/Express", "folder": "node-express", "type": "backend"},
            "5": {"name": "React/TypeScript", "folder": "react-typescript", "type": "frontend"},
            "6": {"name": "Next.js/TypeScript", "folder": "nextjs-typescript", "type": "fullstack"},
            "7": {"name": "Vue.js/TypeScript", "folder": "vue-typescript", "type": "frontend"},
            "8": {"name": "Svelte/SvelteKit", "folder": "svelte-sveltekit", "type": "fullstack"},
            "9": {"name": "Python/Django", "folder": "python-django", "type": "backend"},
            "10": {"name": "Pydantic AI", "folder": "pydantic-ai", "type": "ai-agent"}
        }
    
    def create_project(self):
        """Main method to create a new project."""
        print("🚀 Enhanced AI Project Generator")
        print("=" * 50)
        
        # Get basic info
        project_name = self._get_project_name()
        project_type = self._get_project_type()
        tech_stack = self._get_tech_stack()
        
        # Create the project
        project_path = Path(project_name)
        self._create_folder_structure(project_path, project_type, tech_stack)
        self._copy_template_files(project_path, project_type, tech_stack)
        self._create_placeholder_files(project_path, project_name, project_type, tech_stack)
        
        print(f"\n✅ Project '{project_name}' created!")
        print(f"📁 Location: {project_path.absolute()}")
        self._print_next_steps(project_name, tech_stack)
    
    def _get_project_name(self):
        """Get and validate project name."""
        while True:
            name = input("Project name: ").strip()
            if not name:
                print("Please enter a project name.")
                continue
            if Path(name).exists():
                print(f"Directory '{name}' already exists!")
                continue
            return name
    
    def _get_project_type(self):
        """Get project type selection."""
        print("\nProject types:")
        for key, ptype in self.project_types.items():
            print(f"  {key}. {ptype['name']}")
        
        while True:
            choice = input("Choose project type (1-6): ").strip()
            if choice in self.project_types:
                return self.project_types[choice]
            print("Invalid choice. Please try again.")
    
    def _get_tech_stack(self):
        """Get tech stack selection."""
        print("\nTech stacks:")
        for key, stack in self.tech_stacks.items():
            stack_type = f"({stack['type']})"
            print(f"  {key}. {stack['name']} {stack_type}")
        
        while True:
            choice = input("Choose tech stack (1-10): ").strip()
            if choice in self.tech_stacks:
                return self.tech_stacks[choice]
            print("Invalid choice. Please try again.")
    
    def _create_folder_structure(self, project_path, project_type, tech_stack):
        """Create the basic folder structure."""
        project_path.mkdir()
        
        # Standard folders for all projects
        folders = [
            "docs",
            "tests", 
            "templates",  # For your editable template files
            "iac",        # Infrastructure as Code
            "docker"      # Docker configurations
        ]
        
        # Add project-type specific folders
        if project_type["name"] == "AI Agent":
            folders.extend(["agents", "tools", "prompts"])
        elif project_type["name"] == "Web App":
            folders.extend(["static", "app"])
        elif project_type["name"] == "API Service":
            folders.extend(["api", "models", "services"])
        elif project_type["name"] == "Data Science":
            folders.extend(["data", "notebooks", "models", "scripts"])
        elif project_type["name"] == "Full Stack App":
            folders.extend(["frontend", "backend", "shared"])
        
        # Add tech-stack specific folders
        if "python" in tech_stack["folder"]:
            folders.extend(["src", "config"])
        elif "node" in tech_stack["folder"] or "react" in tech_stack["folder"]:
            folders.extend(["src", "public"])
        elif "nextjs" in tech_stack["folder"]:
            folders.extend(["pages", "components", "styles", "public"])
        elif "vue" in tech_stack["folder"]:
            folders.extend(["src", "public", "components"])
        elif "svelte" in tech_stack["folder"]:
            folders.extend(["src", "static"])
        
        # Create all folders
        for folder in set(folders):  # set() removes duplicates
            (project_path / folder).mkdir(exist_ok=True)
            
        print(f"✅ Created folder structure")
    
    def _copy_template_files(self, project_path, project_type, tech_stack):
        """Copy template files if they exist."""
        # Check if template directory exists
        if not self.template_dir.exists():
            print(f"📝 Template directory not found at {self.template_dir}")
            print("   You can create template files manually in the 'templates' folder")
            return
        
        # Copy base templates
        base_templates = ["PLANNING.md", "TASK.md", "README.md", ".env.example", ".gitignore", ".cursorrules"]
        
        for template_file in base_templates:
            template_path = self.template_dir / template_file
            if template_path.exists():
                shutil.copy2(template_path, project_path / template_file)
                print(f"✅ Copied {template_file}")
            else:
                print(f"📝 Template {template_file} not found - will create placeholder")
    
    def _create_placeholder_files(self, project_path, project_name, project_type, tech_stack):
        """Create placeholder files where templates don't exist."""
        
        # Create main file based on tech stack
        self._create_main_file(project_path, project_name, project_type, tech_stack)
        
        # Create package/dependency files
        self._create_dependency_files(project_path, project_name, tech_stack)
        
        # Create Docker files
        self._create_docker_files(project_path, tech_stack)
        
        # Create IAC files
        self._create_iac_files(project_path)
        
        # Create template placeholders in project's templates folder
        self._create_template_placeholders(project_path)
    
    def _create_main_file(self, project_path, project_name, project_type, tech_stack):
        """Create main application file based on tech stack."""
        
        if "python" in tech_stack["folder"]:
            if "fastapi" in tech_stack["folder"]:
                content = f'''"""
{project_name} - FastAPI Application
Created: {datetime.now().strftime("%Y-%m-%d")}
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="{project_name}", version="1.0.0")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {{"message": "Hello from {project_name}!"}}

@app.get("/health")
async def health_check():
    return {{"status": "healthy"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
                filename = "main.py"
                
            elif "flask" in tech_stack["folder"]:
                content = f'''"""
{project_name} - Flask Application
Created: {datetime.now().strftime("%Y-%m-%d")}
"""

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

@app.route('/')
def home():
    return jsonify({{"message": "Hello from {project_name}!"}})

@app.route('/health')
def health_check():
    return jsonify({{"status": "healthy"}})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
'''
                filename = "app.py"
                
            elif "streamlit" in tech_stack["folder"]:
                content = f'''"""
{project_name} - Streamlit Application
Created: {datetime.now().strftime("%Y-%m-%d")}
"""

import streamlit as st

def main():
    st.set_page_config(page_title="{project_name}", page_icon="🚀")
    
    st.title("{project_name}")
    st.write("Welcome to your new Streamlit application!")
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Home", "About"])
    
    if page == "Home":
        st.header("Home Page")
        st.write("This is the home page of your application.")
        
    elif page == "About":
        st.header("About")
        st.write("Created with the Enhanced AI Project Generator")

if __name__ == "__main__":
    main()
'''
                filename = "app.py"
                
            elif "pydantic-ai" in tech_stack["folder"]:
                content = f'''"""
{project_name} - Pydantic AI Agent
Created: {datetime.now().strftime("%Y-%m-%d")}
"""

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class UserQuery(BaseModel):
    question: str
    context: str = ""

# Initialize the AI model
model = OpenAIModel("gpt-4o-mini")

# Create the agent
agent = Agent(
    model,
    system_prompt="""You are a helpful AI assistant for {project_name}.
    
    Your role is to:
    - Answer questions accurately and helpfully
    - Provide clear and concise responses
    - Be friendly and professional
    
    Always aim to be helpful while staying within your capabilities."""
)

async def run_agent(query: str, context: str = "") -> str:
    """Run the agent with a user query."""
    try:
        user_input = UserQuery(question=query, context=context)
        result = await agent.run(user_input.question)
        return result.data
    except Exception as e:
        return f"Error: {{str(e)}}"

if __name__ == "__main__":
    import asyncio
    
    async def main():
        print("🤖 {project_name} Agent")
        print("=" * 50)
        
        while True:
            query = input("\\nYou: ")
            if query.lower() in ['quit', 'exit', 'bye']:
                print("Goodbye!")
                break
                
            print("Agent: ", end="")
            response = await run_agent(query)
            print(response)
    
    asyncio.run(main())
'''
                filename = "main.py"
                
                # Create agent-specific files
                self._create_pydantic_ai_files(project_path, project_name)
                
            else:  # Basic Python
                content = f'''"""
{project_name} - Python Application
Created: {datetime.now().strftime("%Y-%m-%d")}
"""

def main():
    print("Hello from {project_name}!")

if __name__ == "__main__":
    main()
'''
                filename = "main.py"
                
        elif "react" in tech_stack["folder"]:
            # React App.tsx
            content = f'''import React from 'react';
import './App.css';

function App() {{
  return (
    <div className="App">
      <header className="App-header">
        <h1>{project_name}</h1>
        <p>Welcome to your new React TypeScript application!</p>
        <p>Created: {datetime.now().strftime("%Y-%m-%d")}</p>
      </header>
    </div>
  );
}}

export default App;
'''
            filename = "src/App.tsx"
            
            # Create index.tsx
            index_content = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
'''
            with open(project_path / "src" / "index.tsx", "w") as f:
                f.write(index_content)
            
            # Create public/index.html
            html_content = f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta
      name="description"
      content="Web site created using Enhanced AI Project Generator"
    />
    <title>{project_name}</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
'''
            with open(project_path / "public" / "index.html", "w") as f:
                f.write(html_content)
            
            # Create src/index.css
            index_css = '''body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}
'''
            with open(project_path / "src" / "index.css", "w") as f:
                f.write(index_css)
            
            # Create src/App.css
            app_css = '''.App {
  text-align: center;
}

.App-header {
  background-color: #282c34;
  padding: 20px;
  color: white;
  min-height: 50vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: calc(10px + 2vmin);
}
'''
            with open(project_path / "src" / "App.css", "w") as f:
                f.write(app_css)
            
            # Create tsconfig.json
            tsconfig_content = '''{
  "compilerOptions": {
    "target": "es5",
    "lib": [
      "dom",
      "dom.iterable",
      "esnext"
    ],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": [
    "src"
  ]
}
'''
            with open(project_path / "tsconfig.json", "w") as f:
                f.write(tsconfig_content)
                
        elif "nextjs" in tech_stack["folder"]:
            content = f'''import Head from 'next/head'
import styles from '../styles/Home.module.css'

export default function Home() {{
  return (
    <div className={{styles.container}}>
      <Head>
        <title>{project_name}</title>
        <meta name="description" content="Generated by Enhanced AI Project Generator" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={{styles.main}}>
        <h1 className={{styles.title}}>
          Welcome to {project_name}!
        </h1>

        <p className={{styles.description}}>
          Your Next.js TypeScript application is ready.
        </p>
        
        <p>Created: {datetime.now().strftime("%Y-%m-%d")}</p>
      </main>
    </div>
  )
}}
'''
            filename = "pages/index.tsx"
            
            # Create tsconfig.json for Next.js
            tsconfig_content = '''{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
'''
            with open(project_path / "tsconfig.json", "w") as f:
                f.write(tsconfig_content)
            
            # Create styles/Home.module.css
            home_css = '''.container {
  padding: 0 2rem;
}

.main {
  min-height: 100vh;
  padding: 4rem 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.title {
  margin: 0;
  line-height: 1.15;
  font-size: 4rem;
  text-align: center;
}

.description {
  margin: 4rem 0;
  line-height: 1.5;
  font-size: 1.5rem;
  text-align: center;
}
'''
            (project_path / "styles").mkdir(exist_ok=True)
            with open(project_path / "styles" / "Home.module.css", "w") as f:
                f.write(home_css)
            
        elif "vue" in tech_stack["folder"]:
            content = f'''<template>
  <div id="app">
    <header>
      <h1>{project_name}</h1>
      <p>Welcome to your new Vue.js TypeScript application!</p>
      <p>Created: {datetime.now().strftime("%Y-%m-%d")}</p>
    </header>
  </div>
</template>

<script lang="ts">
import {{ defineComponent }} from 'vue'

export default defineComponent({{
  name: 'App',
  components: {{
  }}
}})
</script>

<style>
#app {{
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}}
</style>
'''
            filename = "src/App.vue"
            
            # Create tsconfig.json for Vue
            tsconfig_content = '''{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "preserve",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src/**/*.ts", "src/**/*.tsx", "src/**/*.vue"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
'''
            with open(project_path / "tsconfig.json", "w") as f:
                f.write(tsconfig_content)
            
            # Create vite.config.ts
            vite_config = '''import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
})
'''
            with open(project_path / "vite.config.ts", "w") as f:
                f.write(vite_config)
            
            # Create src/main.ts
            main_ts = '''import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
'''
            with open(project_path / "src" / "main.ts", "w") as f:
                f.write(main_ts)
            
            # Create public/index.html
            html_content = f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{project_name}</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
'''
            with open(project_path / "public" / "index.html", "w") as f:
                f.write(html_content)
            
        elif "svelte" in tech_stack["folder"]:
            content = f'''<script lang="ts">
  let name = '{project_name}';
  let createdDate = '{datetime.now().strftime("%Y-%m-%d")}';
</script>

<main>
  <h1>Welcome to {{name}}!</h1>
  <p>Your new SvelteKit TypeScript application is ready.</p>
  <p>Created: {{createdDate}}</p>
</main>

<style>
  main {{
    text-align: center;
    padding: 1em;
    max-width: 240px;
    margin: 0 auto;
  }}

  h1 {{
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 4em;
    font-weight: 100;
  }}
</style>
'''
            filename = "src/app.html" if "sveltekit" in tech_stack["folder"] else "src/App.svelte"
            
        else:  # Node.js/Express
            content = f'''/**
 * {project_name} - Express Application
 * Created: {datetime.now().strftime("%Y-%m-%d")}
 */

const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.get('/', (req, res) => {{
  res.json({{ message: 'Hello from {project_name}!' }});
}});

app.get('/health', (req, res) => {{
  res.json({{ status: 'healthy' }});
}});

// Start server
app.listen(PORT, () => {{
  console.log(`Server running on port ${{PORT}}`);
}});
'''
            filename = "index.js"
        
        # Create the main file
        main_path = project_path / filename
        main_path.parent.mkdir(parents=True, exist_ok=True)
        with open(main_path, "w") as f:
            f.write(content)
        
        print(f"✅ Created {filename}")
    
    def _create_pydantic_ai_files(self, project_path, project_name):
        """Create Pydantic AI specific files."""
        
        # Create agents/agent.py
        agent_content = f'''"""
Main agent definition for {project_name}
"""

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel
from typing import List, Optional
import os

class AgentResponse(BaseModel):
    """Structured response from the agent."""
    answer: str
    confidence: float = 1.0
    sources: List[str] = []

class AgentConfig(BaseModel):
    """Configuration for the agent."""
    model_name: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 1000

# Initialize model
def get_model(config: AgentConfig) -> OpenAIModel:
    return OpenAIModel(
        config.model_name,
        temperature=config.temperature,
        max_tokens=config.max_tokens
    )

# Main agent definition
def create_agent(config: AgentConfig) -> Agent:
    model = get_model(config)
    
    return Agent(
        model,
        system_prompt=f"""You are an AI assistant for {project_name}.
        
        Your capabilities include:
        - Answering questions accurately and helpfully
        - Providing structured responses
        - Being transparent about your limitations
        
        Always respond in a helpful, professional manner.""",
        result_type=AgentResponse
    )
'''
        
        with open(project_path / "agents" / "agent.py", "w") as f:
            f.write(agent_content)
        
        # Create tools/tools.py
        tools_content = '''"""
Tools and functions for the AI agent
"""

from pydantic_ai.tools import Tool
from pydantic import BaseModel
from typing import List, Dict, Any
import json
from datetime import datetime

class SearchResult(BaseModel):
    """Result from a search operation."""
    title: str
    content: str
    url: str = ""

@Tool
def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@Tool  
def search_knowledge_base(query: str) -> List[SearchResult]:
    """Search a knowledge base for relevant information."""
    # This is a placeholder - implement your actual search logic
    return [
        SearchResult(
            title="Sample Result",
            content=f"This is a sample result for query: {query}",
            url="https://example.com"
        )
    ]

@Tool
def calculate_simple_math(expression: str) -> str:
    """Calculate simple mathematical expressions safely."""
    try:
        # Basic safety check - only allow numbers and basic operators
        allowed_chars = set('0123456789+-*/()., ')
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression"
        
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

# Tool registry
AVAILABLE_TOOLS = [
    get_current_time,
    search_knowledge_base,
    calculate_simple_math
]
'''
        
        with open(project_path / "tools" / "tools.py", "w") as f:
            f.write(tools_content)
        
        # Create prompts/prompts.py
        prompts_content = f'''"""
System prompts and prompt templates for {project_name}
"""

from typing import Dict, List
from pydantic import BaseModel

class PromptTemplate(BaseModel):
    """Template for generating prompts."""
    name: str
    template: str
    variables: List[str] = []

# System prompts
SYSTEM_PROMPTS = {{
    "default": f"""You are an AI assistant for {project_name}.
    
    Your role is to:
    - Provide accurate and helpful responses
    - Use available tools when appropriate
    - Be transparent about your capabilities and limitations
    - Maintain a professional and friendly tone
    
    When using tools, explain what you're doing and why.""",
    
    "analytical": f"""You are an analytical AI assistant for {project_name}.
    
    Your approach should be:
    - Methodical and systematic
    - Data-driven when possible
    - Clear about assumptions and limitations
    - Focused on providing actionable insights
    
    Break down complex problems into manageable parts.""",
    
    "creative": f"""You are a creative AI assistant for {project_name}.
    
    Your approach should be:
    - Imaginative and innovative
    - Open to exploring different perspectives
    - Encouraging of creative thinking
    - Balanced between creativity and practicality
    
    Help users think outside the box while staying grounded."""
}}

# Prompt templates for common tasks
PROMPT_TEMPLATES = [
    PromptTemplate(
        name="question_answering",
        template="Based on the following context: {{context}}\\n\\nPlease answer this question: {{question}}",
        variables=["context", "question"]
    ),
    PromptTemplate(
        name="task_breakdown", 
        template="Break down this task into manageable steps: {{task}}\\n\\nConsider: {{considerations}}",
        variables=["task", "considerations"]
    ),
    PromptTemplate(
        name="analysis_request",
        template="Analyze the following information: {{data}}\\n\\nFocus on: {{focus_areas}}",
        variables=["data", "focus_areas"]
    )
]

def get_prompt_template(name: str) -> PromptTemplate:
    """Get a prompt template by name."""
    for template in PROMPT_TEMPLATES:
        if template.name == name:
            return template
    raise ValueError(f"Template '{{name}}' not found")

def format_prompt(template_name: str, **kwargs) -> str:
    """Format a prompt template with given variables."""
    template = get_prompt_template(template_name)
    return template.template.format(**kwargs)
'''
        
        with open(project_path / "prompts" / "prompts.py", "w") as f:
            f.write(prompts_content)
        
        # Create api.py for FastAPI integration
        api_content = f'''"""
FastAPI server for {project_name} agent
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import asyncio
import os
from dotenv import load_dotenv

from agents.agent import create_agent, AgentConfig, AgentResponse
from tools.tools import AVAILABLE_TOOLS

# Load environment variables
load_dotenv()

app = FastAPI(title="{project_name} API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = ""
    agent_type: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    agent_type: str
    confidence: float = 1.0

# Initialize agent
config = AgentConfig()
agent = create_agent(config)

@app.get("/")
async def root():
    return {{"message": "Welcome to {project_name} API"}}

@app.get("/health")
async def health_check():
    return {{"status": "healthy", "agent": "ready"}}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the AI agent."""
    try:
        # Run the agent
        result = await agent.run(request.message)
        
        return ChatResponse(
            response=result.data.answer if hasattr(result.data, 'answer') else str(result.data),
            agent_type=request.agent_type,
            confidence=result.data.confidence if hasattr(result.data, 'confidence') else 1.0
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tools")
async def list_tools():
    """List available tools."""
    return {{
        "tools": [tool.__name__ for tool in AVAILABLE_TOOLS],
        "count": len(AVAILABLE_TOOLS)
    }}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        
        with open(project_path / "api.py", "w") as f:
            f.write(api_content)
        
        # Create .env.example with AI-specific variables
        env_content = '''# Environment Variables for Pydantic AI Agent
# Copy this file to .env and fill in your actual values

# OpenAI API Key (required for GPT models)
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic API Key (optional, for Claude models)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Agent Configuration
AGENT_MODEL=gpt-4o-mini
AGENT_TEMPERATURE=0.7
AGENT_MAX_TOKENS=1000

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=True

# Application Settings
LOG_LEVEL=INFO
'''
        
        with open(project_path / ".env.example", "w") as f:
            f.write(env_content)
        
        print("✅ Created Pydantic AI agent files")
    
    def _create_dependency_files(self, project_path, project_name, tech_stack):
        """Create dependency files based on tech stack."""
        
        if "python" in tech_stack["folder"]:
            # Python requirements.txt
            requirements = ["pytest>=7.0.0"]
            
            if "fastapi" in tech_stack["folder"]:
                requirements.extend([
                    "fastapi>=0.104.1", 
                    "uvicorn>=0.24.0", 
                    "python-dotenv>=1.0.0",
                    "python-multipart>=0.0.6"
                ])
            elif "flask" in tech_stack["folder"]:
                requirements.extend([
                    "Flask>=3.0.0", 
                    "flask-cors>=4.0.0", 
                    "python-dotenv>=1.0.0"
                ])
            elif "streamlit" in tech_stack["folder"]:
                requirements.extend([
                    "streamlit>=1.28.0", 
                    "python-dotenv>=1.0.0"
                ])
            elif "django" in tech_stack["folder"]:
                requirements.extend([
                    "Django>=5.0.0", 
                    "djangorestframework>=3.14.0",
                    "django-cors-headers>=4.3.0",
                    "python-dotenv>=1.0.0"
                ])
            elif "pydantic-ai" in tech_stack["folder"]:
                requirements.extend([
                    "pydantic-ai>=0.0.14",
                    "openai>=1.3.0",
                    "anthropic>=0.8.0",
                    "python-dotenv>=1.0.0",
                    "fastapi>=0.104.1",
                    "uvicorn>=0.24.0"
                ])
            
            content = "\n".join(requirements) + "\n"
            with open(project_path / "requirements.txt", "w") as f:
                f.write(content)
                
        else:  # JavaScript/TypeScript projects
            project_name_clean = project_name.lower().replace(' ', '-')
            
            if "react" in tech_stack["folder"]:
                package_content = '''{
  "name": "''' + project_name_clean + '''",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@types/node": "^16.18.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "typescript": "^4.9.0",
    "web-vitals": "^2.1.0"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^5.16.0",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^13.5.0"
  }
}'''
                
            elif "nextjs" in tech_stack["folder"]:
                package_content = '''{
  "name": "''' + project_name_clean + '''",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.0.0",
    "react": "^18",
    "react-dom": "^18"
  },
  "devDependencies": {
    "typescript": "^5",
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "eslint": "^8",
    "eslint-config-next": "14.0.0"
  }
}'''
                
            elif "vue" in tech_stack["folder"]:
                package_content = '''{
  "name": "''' + project_name_clean + '''",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.3.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.4.0",
    "typescript": "^5.0.0",
    "vite": "^4.4.0",
    "vue-tsc": "^1.8.0"
  }
}'''
                
            elif "svelte" in tech_stack["folder"]:
                package_content = '''{
  "name": "''' + project_name_clean + '''",
  "version": "0.0.1",
  "private": true,
  "scripts": {
    "build": "vite build",
    "dev": "vite dev",
    "preview": "vite preview"
  },
  "devDependencies": {
    "@sveltejs/adapter-auto": "^2.0.0",
    "@sveltejs/kit": "^1.20.4",
    "svelte": "^4.0.5",
    "typescript": "^5.0.0",
    "vite": "^4.4.2"
  },
  "type": "module"
}'''
                
            else:  # Node.js/Express
                package_content = '''{
  "name": "''' + project_name_clean + '''",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "dotenv": "^16.3.1"
  },
  "devDependencies": {
    "nodemon": "^3.0.1",
    "jest": "^29.7.0"
  }
}'''
            
            with open(project_path / "package.json", "w") as f:
                f.write(package_content)
        
        print("✅ Created dependency files")
    
    def _create_docker_files(self, project_path, tech_stack):
        """Create Docker configuration based on tech stack."""
        
        if "python" in tech_stack["folder"]:
            dockerfile_content = '''FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
'''
            port_mapping = "8000:8000"
            
        elif any(stack in tech_stack["folder"] for stack in ["react", "nextjs", "vue", "svelte"]):
            dockerfile_content = '''FROM node:18-alpine

WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./
RUN npm ci

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Expose port
EXPOSE 3000

# Run the application
CMD ["npm", "start"]
'''
            port_mapping = "3000:3000"
            
        else:  # Node.js/Express
            dockerfile_content = '''FROM node:18-alpine

WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./
RUN npm ci --only=production

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Run the application
CMD ["npm", "start"]
'''
            port_mapping = "3000:3000"
        
        with open(project_path / "docker" / "Dockerfile", "w") as f:
            f.write(dockerfile_content)
        
        # Docker Compose
        compose_content = f'''version: '3.8'

services:
  app:
    build: 
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "{port_mapping}"
    environment:
      - DEBUG=True
    volumes:
      - ..:/app
      - /app/node_modules  # Prevent overwriting node_modules
'''
        
        with open(project_path / "docker" / "docker-compose.yml", "w") as f:
            f.write(compose_content)
        
        print("✅ Created Docker configuration")
    
    def _create_iac_files(self, project_path):
        """Create basic Infrastructure as Code templates."""
        
        # Azure Resource Manager template
        arm_template = '''{
    "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "appName": {
            "type": "string",
            "defaultValue": "[uniqueString(resourceGroup().id)]"
        },
        "location": {
            "type": "string",
            "defaultValue": "[resourceGroup().location]"
        }
    },
    "resources": [
        {
            "type": "Microsoft.Web/serverfarms",
            "apiVersion": "2021-02-01",
            "name": "[concat(parameters('appName'), '-plan')]",
            "location": "[parameters('location')]",
            "sku": {
                "name": "B1",
                "tier": "Basic"
            }
        },
        {
            "type": "Microsoft.Web/sites",
            "apiVersion": "2021-02-01",
            "name": "[parameters('appName')]",
            "location": "[parameters('location')]",
            "dependsOn": [
                "[resourceId('Microsoft.Web/serverfarms', concat(parameters('appName'), '-plan'))]"
            ],
            "properties": {
                "serverFarmId": "[resourceId('Microsoft.Web/serverfarms', concat(parameters('appName'), '-plan'))]"
            }
        }
    ]
}'''
        
        with open(project_path / "iac" / "azure-template.json", "w") as f:
            f.write(arm_template)
        
        # Terraform example
        terraform_content = '''# Azure Resource Group
resource "azurerm_resource_group" "main" {
  name     = "${var.project_name}-rg"
  location = var.location
}

# App Service Plan
resource "azurerm_service_plan" "main" {
  name                = "${var.project_name}-plan"
  resource_group_name = azurerm_resource_group.main.name
  location           = azurerm_resource_group.main.location
  os_type            = "Linux"
  sku_name           = "B1"
}

# App Service
resource "azurerm_linux_web_app" "main" {
  name                = var.project_name
  resource_group_name = azurerm_resource_group.main.name
  location           = azurerm_service_plan.main.location
  service_plan_id    = azurerm_service_plan.main.id

  site_config {}
}
'''
        
        with open(project_path / "iac" / "main.tf", "w") as f:
            f.write(terraform_content)
        
        # Variables file
        variables_content = '''variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "East US"
}
'''
        
        with open(project_path / "iac" / "variables.tf", "w") as f:
            f.write(variables_content)
        
        print("✅ Created IAC templates")
    
    def _create_template_placeholders(self, project_path):
        """Create placeholder files in templates folder."""
        templates_dir = project_path / "templates"
        
        placeholder_files = [
            "PLANNING.md",
            "TASK.md", 
            "README.md",
            ".env.example",
            ".gitignore",
            ".cursorrules"
        ]
        
        for filename in placeholder_files:
            placeholder_path = templates_dir / filename
            with open(placeholder_path, "w") as f:
                f.write(f"# {filename} Template\n\n")
                f.write("<!-- Edit this file to customize the template -->\n")
                f.write("<!-- This file will be copied to new projects -->\n\n")
        
        print("✅ Created template placeholders")
    
    def _print_next_steps(self, project_name, tech_stack):
        """Print next steps for the user."""
        print(f"\n🚀 Next steps:")
        print(f"1. cd {project_name}")
        
        # Tech-specific instructions
        if "python" in tech_stack["folder"]:
            print("2. Create virtual environment: python -m venv venv")
            print("3. Activate it: venv\\Scripts\\activate (Windows) or source venv/bin/activate (Mac/Linux)")
            print("4. Install dependencies: pip install -r requirements.txt")
            if "streamlit" in tech_stack["folder"]:
                print("5. Run: streamlit run app.py")
            else:
                print("5. Run: python main.py")
            print("6. Edit template files in the 'templates/' folder")
            print("7. Start coding!")
        else:  # JavaScript/TypeScript
            print("2. Install dependencies: npm install")
            print("   (This creates package-lock.json needed for Docker)")
            if "react" in tech_stack["folder"]:
                print("3. Run locally: npm start")
            elif "nextjs" in tech_stack["folder"]:
                print("3. Run locally: npm run dev")
            elif "vue" in tech_stack["folder"]:
                print("3. Run locally: npm run dev")
            elif "svelte" in tech_stack["folder"]:
                print("3. Run locally: npm run dev")
            else:
                print("3. Run locally: npm run dev")
            print("4. Edit template files in the 'templates/' folder")
            print("5. Start coding!")
        
        print(f"\n🐳 Docker option (after npm install):")
        print(f"  docker-compose -f docker/docker-compose.yml up --build")
        
        print(f"\n📁 Folder structure created:")
        print("├── docs/           # Documentation")
        print("├── tests/          # Unit tests") 
        print("├── templates/      # Your editable template files")
        print("├── iac/            # Infrastructure as Code")
        print("├── docker/         # Docker configuration")
        print("├── src/            # Source code")
        print("└── main.py/index.js # Entry point")
        
        
        print(f"\n📁 Folder structure created:")
        print("├── docs/           # Documentation")
        print("├── tests/          # Unit tests") 
        print("├── templates/      # Your editable template files")
        print("├── iac/            # Infrastructure as Code")
        print("├── docker/         # Docker configuration")
        print("├── src/            # Source code")
        print("└── main.py/index.js # Entry point")
        
        # Tech-specific tips
        if tech_stack["type"] == "frontend":
            print(f"\n💡 Frontend Development:")
            print("  - Run 'npm install' first to create package-lock.json")
            print("  - Your app will run on http://localhost:3000")
            print("  - Edit components in the src/ folder")
            print("  - Hot reload is enabled for development")
        elif tech_stack["type"] == "backend":
            print(f"\n💡 Backend Development:")
            if "python" in tech_stack["folder"]:
                print("  - API will run on http://localhost:8000")
                if "fastapi" in tech_stack["folder"]:
                    print("  - API docs at http://localhost:8000/docs")
            else:
                print("  - Run 'npm install' first to create package-lock.json")
                print("  - API will run on http://localhost:3000")
        elif tech_stack["type"] == "fullstack":
            print(f"\n💡 Full Stack Development:")
            if "nextjs" in tech_stack["folder"] or "svelte" in tech_stack["folder"]:
                print("  - Run 'npm install' first to create package-lock.json")
            print("  - Single application with frontend and backend")
            if "nextjs" in tech_stack["folder"]:
                print("  - App runs on http://localhost:3000")
                print("  - API routes in pages/api/ folder")
            elif "streamlit" in tech_stack["folder"]:
                print("  - Interactive app on http://localhost:8501")


def main():
    """Run the enhanced project generator."""
    try:
        generator = EnhancedProjectGenerator()
        generator.create_project()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()