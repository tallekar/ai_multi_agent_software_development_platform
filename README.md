# 🤖 AI Multi-Agent Software Development Platform

An AI-powered software development platform that uses multiple specialized AI agents to automate and coordinate different stages of the software development lifecycle.

The platform uses **CrewAI** for multi-agent orchestration, **FastAPI** for the backend API, **React + Vite** for the frontend, and **LLM-based agents** for research, coding, and project coordination.

---

## 📌 Overview

Traditional software development requires developers to perform several activities manually, including:

* Understanding requirements
* Researching technical solutions
* Designing an implementation approach
* Writing code
* Reviewing and improving the implementation

This project explores how **Agentic AI** can divide these responsibilities among specialized AI agents.

Instead of relying on a single AI agent, the system uses multiple agents with different responsibilities.

### Core Concept

```text
                        User
                          │
                          ▼
                   React Frontend
                          │
                     HTTP Request
                          │
                          ▼
                    FastAPI Backend
                          │
                          ▼
                    CrewAI Workflow
                          │
                          ▼
                    Manager Agent
                     /           \
                    /             \
                   ▼               ▼
           Research Agent     Coding Agent
                   │               │
                   ▼               ▼
              Research         Implementation
                   │               │
                   └───────┬───────┘
                           ▼
                     Final Result
                           │
                           ▼
                    React Frontend
```

---

# ✨ Features

* 🤖 Multi-agent AI architecture
* 🔬 Dedicated research agent
* 💻 Dedicated coding agent
* 🧠 Manager/project-management agent
* 🔄 Agent orchestration using CrewAI
* ⚡ FastAPI REST backend
* ⚛️ React frontend
* 🧩 Modular backend architecture
* 🔧 Centralized LLM configuration
* 📋 Task-based agent execution
* 🔌 Separation between frontend and backend

---

# 🏗️ Architecture

The application follows a modular architecture.

```text
┌──────────────────────────────────────────┐
│              React Frontend              │
│                                          │
│        User Interface / Requests         │
└────────────────────┬─────────────────────┘
                     │
                     │ REST API
                     ▼
┌──────────────────────────────────────────┐
│             FastAPI Backend              │
│                                          │
│              API Routes                  │
└────────────────────┬─────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────┐
│              CrewAI Layer                │
│                                          │
│          Agent Orchestration             │
└───────────────┬──────────┬───────────────┘
                │          │
                ▼          ▼
        ┌────────────┐ ┌────────────┐
        │  Research  │ │  Coding    │
        │   Agent    │ │   Agent    │
        └────────────┘ └────────────┘
                \          /
                 \        /
                  ▼      ▼
              ┌─────────────┐
              │   Manager   │
              │    Agent    │
              └──────┬──────┘
                     │
                     ▼
               Final Response
```

---

# 📁 Project Structure

```text
ai_multi_agent_software_development_platform/
│
├── app/
│   │
│   ├── agents/
│   │   ├── coding_agent.py
│   │   ├── manager_agent.py
│   │   └── research_agent.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── llm_config.py
│   │
│   ├── crew/
│   │   └── crew_setup.py
│   │
│   ├── tasks/
│   │   └── ...
│   │
│   ├── utils/
│   │   └── ...
│   │
│   ├── __init__.py
│   └── main.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   └── eslint.config.js
│
├── .gitignore
├── requirements.txt
└── README.md
```

The current repository contains separate modules for agents, API routes, configuration, CrewAI orchestration, tasks, and utilities, with a separate React frontend.

---

# 🧠 AI Agents

The system is based on specialized agents rather than one general-purpose agent.

## 1. Research Agent

### Responsibility

The Research Agent analyzes the user's software requirements and provides technical research and recommendations.

### Example responsibilities

* Understand the problem
* Identify technical requirements
* Research implementation approaches
* Recommend libraries and technologies
* Identify possible architectural approaches
* Provide technical context to other agents

### Flow

```text
User Requirement
       │
       ▼
Research Agent
       │
       ├── Requirement Analysis
       ├── Technology Analysis
       ├── Architecture Research
       └── Technical Recommendations
       │
       ▼
Research Output
```

---

# 💻 2. Coding Agent

The Coding Agent focuses on software implementation.

### Responsibilities

* Analyze the development requirements
* Use research/context provided by other agents
* Generate implementation logic
* Produce code
* Suggest project structure
* Implement requested functionality

### Flow

```text
Requirements
     │
     ▼
Coding Agent
     │
     ├── Analyze Requirements
     ├── Design Implementation
     ├── Generate Code
     └── Improve Implementation
     │
     ▼
Code Output
```

---

# 🧠 3. Manager Agent

The Manager Agent acts as the coordinator of the multi-agent workflow.

Instead of requiring the user to manually coordinate the agents, the manager determines how the available agents should work together.

### Responsibilities

* Coordinate agents
* Manage task execution
* Connect outputs between agents
* Maintain the overall workflow
* Produce a final coordinated result

### Example

```text
                    Manager Agent
                    /           \
                   /             \
                  ▼               ▼
          Research Agent     Coding Agent
                  │               │
                  ▼               ▼
              Research          Code
                  │               │
                  └───────┬───────┘
                          ▼
                     Final Output
```

---

# 🔄 Agent Workflow

A typical request follows this workflow:

### Step 1 — User submits requirement

Example:

```text
Build a REST API for a Book Management System.
```

### Step 2 — Request reaches FastAPI

```text
React
  │
  ▼
FastAPI
```

### Step 3 — CrewAI initializes the workflow

```text
FastAPI
   │
   ▼
CrewAI
```

### Step 4 — Manager coordinates the agents

```text
Manager Agent
      │
      ├───────────────┐
      ▼               ▼
Research Agent   Coding Agent
```

### Step 5 — Research Agent analyzes the problem

It can determine:

```text
Technology
Database
API structure
Authentication
Project architecture
Implementation approach
```

### Step 6 — Coding Agent creates the implementation

The coding agent uses the available context to produce the requested implementation.

### Step 7 — Final result is returned

```text
Agents
  │
  ▼
CrewAI
  │
  ▼
FastAPI
  │
  ▼
React
  │
  ▼
User
```

---

# ⚡ Backend

The backend is implemented using **FastAPI**.

The main application entry point is:

```text
app/main.py
```

The backend is responsible for:

* Starting the API server
* Registering API routes
* Receiving frontend requests
* Triggering the AI workflow
* Returning results to the frontend

### Backend architecture

```text
app/main.py
     │
     ▼
API Routes
     │
     ▼
Crew Setup
     │
     ▼
Agents
     │
     ▼
Tasks
     │
     ▼
LLM
```

---

# 🔌 API Layer

API routes are separated into:

```text
app/api/routes.py
```

This keeps HTTP/API concerns separate from AI-agent logic.

The intended architecture is:

```text
HTTP Request
     │
     ▼
routes.py
     │
     ▼
CrewAI
     │
     ▼
Agents
     │
     ▼
Response
```

This separation makes the application easier to maintain and extend.

---

# 🧩 CrewAI Layer

CrewAI is used to coordinate the specialized AI agents.

The orchestration layer is located at:

```text
app/crew/crew_setup.py
```

Its responsibility is to bring together:

```text
Agents
+
Tasks
+
Execution Process
```

Conceptually:

```text
Agents
  +
Tasks
  +
Crew
  │
  ▼
Workflow Execution
```

---

# 📋 Tasks

Tasks define the actual work that agents need to perform.

The project separates tasks into:

```text
app/tasks/
```

This follows an important multi-agent design principle:

```text
Agent = Who performs the work?

Task = What work needs to be performed?

Crew = How are agents coordinated?
```

---

# ⚙️ Configuration

LLM configuration is separated into:

```text
app/config/llm_config.py
```

This provides a centralized place for configuring the language-model layer instead of scattering configuration throughout individual agents.

Conceptually:

```text
Application
     │
     ▼
LLM Configuration
     │
     ▼
Language Model
     │
     ▼
AI Agents
```

---

# 🎨 Frontend

The frontend is built using:

* React
* Vite
* JavaScript
* CSS

The frontend is located inside:

```text
frontend/
```

Its responsibility is to provide the user interface for interacting with the AI development platform.

### Frontend workflow

```text
User
 │
 ▼
React UI
 │
 ▼
API Request
 │
 ▼
FastAPI
 │
 ▼
AI Agents
 │
 ▼
API Response
 │
 ▼
React UI
```

---

# 🛠️ Technology Stack

| Category             | Technology  |
| -------------------- | ----------- |
| Programming Language | Python      |
| Backend Framework    | FastAPI     |
| AI Agent Framework   | CrewAI      |
| LLM Framework        | LangChain   |
| Frontend             | React       |
| Frontend Tooling     | Vite        |
| API Style            | REST        |
| AI Architecture      | Multi-Agent |
| Server               | Uvicorn     |

The repository identifies Python, FastAPI, CrewAI, LangChain and React as its primary technologies.

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/tallekar/ai_multi_agent_software_development_platform.git
```

```bash
cd ai_multi_agent_software_development_platform
```

---

# 🐍 Backend Setup

Create a virtual environment:

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

# 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

> Make sure `requirements.txt` contains all backend dependencies required by the project before installation.

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

Example:

```env
LLM_API_KEY=your_api_key_here
```

If your selected LLM provider requires additional configuration, add those values to `.env` as well.

### Important

Never commit API keys to GitHub.

Add:

```text
.env
```

to `.gitignore`.

---

# ▶️ Run Backend

From the project root:

```bash
uvicorn app.main:app --reload
```

The backend will normally be available at:

```text
http://127.0.0.1:8000
```

FastAPI also provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

---

# ▶️ Run Frontend

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The Vite development server will provide the frontend URL in the terminal.

---

# 🔗 Backend + Frontend

During development, both applications run independently:

```text
Frontend
React + Vite
     │
     │ HTTP requests
     ▼
Backend
FastAPI + Uvicorn
     │
     ▼
CrewAI
     │
     ▼
AI Agents
```

---

# 🧪 Example Use Case

### User Request

```text
Create a FastAPI REST API for employee management.
```

### AI Workflow

```text
                    User Request
                         │
                         ▼
                    FastAPI API
                         │
                         ▼
                   Manager Agent
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       Research Agent          Coding Agent
              │                     │
              ▼                     ▼
       API Architecture       Implementation
              │                     │
              └──────────┬──────────┘
                         ▼
                    Final Result
```

---

# 🎯 Project Goals

The main goals of the project are:

1. Explore Agentic AI architectures.
2. Demonstrate multi-agent collaboration.
3. Automate parts of software development.
4. Separate software-development responsibilities across specialized agents.
5. Build a practical AI application using FastAPI and React.
6. Understand LLM orchestration using CrewAI and LangChain.

---

# 🔮 Future Improvements

The platform can be extended with additional specialized agents.

### Planned Agent Architecture

```text
                    Manager Agent
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
 Research Agent     Coding Agent      Testing Agent
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
                         ▼
                   Code Review Agent
                         │
                         ▼
                    Final Project
```

Potential future improvements include:

* 🧪 Automated testing agent
* 🔍 Code review agent
* 🐛 Debugging agent
* 🏗️ Architecture/design agent
* 📚 Documentation agent
* 🔐 Security analysis agent
* 🗄️ Database design agent
* 🐳 Docker integration
* 🔄 CI/CD integration
* 💾 Persistent project storage
* 📊 Agent execution monitoring
* 🔑 Authentication and authorization
* 📁 Automated project/file generation

---

# 🔒 Security Considerations

For production deployment:

* Store API keys in environment variables.
* Never commit `.env`.
* Restrict CORS origins.
* Validate API requests.
* Add authentication and authorization.
* Implement rate limiting.
* Add proper logging.
* Validate AI-generated code before execution.
* Avoid executing untrusted generated code directly on the host system.

---

# 📈 Production Architecture

A future production version could use:

```text
                   ┌───────────────┐
                   │ React Frontend│
                   └───────┬───────┘
                           │
                           ▼
                    ┌────────────┐
                    │ API Gateway│
                    └─────┬──────┘
                          │
                          ▼
                    ┌────────────┐
                    │  FastAPI   │
                    └─────┬──────┘
                          │
                          ▼
                    ┌────────────┐
                    │ CrewAI     │
                    │ Orchestrator│
                    └─────┬──────┘
                          │
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
       Research        Coding        Testing
         Agent          Agent          Agent
            │             │             │
            └─────────────┼─────────────┘
                          ▼
                     LLM Provider
                          │
                          ▼
                    Final Response
```

---

# 👨‍💻 Developer

**Niket Talekar**

B.Tech — Artificial Intelligence & Data Science

Interested in:

* Artificial Intelligence
* Machine Learning
* Generative AI
* Agentic AI
* Python Backend Development
* FastAPI
* Computer Vision
* LLM Applications

---

# ⭐ Project Highlights

This project demonstrates practical experience with:

```text
Python
   │
   ├── FastAPI
   ├── REST APIs
   └── Backend Architecture

Generative AI
   │
   ├── LLMs
   ├── LangChain
   └── CrewAI

Agentic AI
   │
   ├── Multi-Agent Systems
   ├── Agent Orchestration
   └── Specialized AI Agents

Frontend
   │
   ├── React
   └── Vite
```

---

# 📄 License

This project is intended for educational, experimental, and portfolio purposes.

---

## 🔗 Repository

GitHub:

https://github.com/tallekar/ai_multi_agent_software_development_platform
