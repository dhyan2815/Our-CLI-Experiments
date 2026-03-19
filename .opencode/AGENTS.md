# AGENTS.md - Agentic Guidelines for General Project

This document provides essential context, standards, and commands for AI agents (like Claude Code, Gemini CLI, etc.) operating within this repository. It is designed to ensure consistency, safety, and efficiency when performing automated tasks.

## 1. Project Overview & Mission
This repository is a central hub for **n8n automation workflows**, **MCP (Model Context Protocol) configurations**, and **system architecture documentation**. The primary goal is to bridge the gap between AI assistants and automated business processes (e.g., Loan Consulting System, Lead Generation, CRM enrichment).

### Core Technologies
- **n8n**: Primary workflow automation platform.
- **MCP**: Protocol for connecting AI to tools and workflows.
- **Markdown**: For high-fidelity documentation and changelogs.
- **Excalidraw**: For visual representations of complex logic and architecture.
- **Node.js/npm**: Used for utility scripts and local validation.

---

## 2. Common Commands

### 2.1 Environment & MCP Management
- **List Configured Servers**: `claude mcp list` (Use to verify which n8n instances are connected).
- **Add n8n MCP Server**:
  ```bash
  claude mcp add n8n-mcp --transport http https://<your-n8n-domain>/mcp-server/http --header "Authorization: Bearer <TOKEN>"
  ```
- **Connectivity Check**: Use `mcp__n8n-mcp__n8n_health_check` tool to verify instance status.

### 2.2 Validation & Linting
Since this repository consists mainly of JSON and Markdown:
- **Validate JSON Syntax**: `node -e "JSON.parse(require('fs').readFileSync('filename.json'))"`
- **Markdown Consistency**: Ensure all headers follow `#`, `##`, `###` hierarchy without skipping levels.
- **Check Workflow Metadata**: Ensure `.json` exports contain the `meta` object with correct `n8nVersion`.

### 2.3 Testing & Execution
- **Execute Local Workflow**: If n8n is running locally, use `n8n execute:workflow --file <path>`.
- **Trigger Remote Workflow**: Use `mcp__n8n-mcp__n8n_execute_workflow --id <workflow_id>`.
- **Run Single Node**: Currently, node-level testing is performed via the n8n UI or by isolating nodes in temporary workflows.

---

## 3. Code & Workflow Standards

### 3.1 n8n Workflow Design (JSON)
- **File Naming**: Use `[System Name] - [Function].json` (e.g., `Loan Consulting - Lead Intake.json`).
- **Node Naming**: Every node must have a descriptive, unique name.
  - *Bad*: `HTTP Request`, `Set 1`.
  - *Good*: `HTTP: Fetch CRM Data`, `Set: Map Lead Fields`.
- **Error Handling (Mandatory)**: 
  - Every production workflow **must** be connected to an "Error Trigger" node.
  - Implement retry logic on "HTTP Request" nodes (at least 3 retries with exponential backoff).
- **Complexity**: If a workflow exceeds 20 nodes, consider breaking it into sub-workflows called via the "Execute Workflow" node.
- **Variables**: Use `{{ $env.VARIABLE_NAME }}` for environment variables. Never hardcode sensitive values.

### 3.2 Documentation (Markdown)
- **Formatting**: Use GitHub-flavored Markdown. Use bolding for UI elements and backticks for technical terms.
- **Changelog Protocol**: Update `GEMINI.md` with every major change. Format:
  ```markdown
  ### YYYY-MM-DD
  - [Action Verb] Description of the change (e.g., "Modified Lead Intake workflow").
  ```
- **Relative Linking**: Use relative paths for internal references: `[MCP Guide](n8n_MCP_GUIDE.md)`.

### 3.3 Visual Diagrams (Excalidraw)
- **Storage**: Place all diagrams in the `excalidraw diagrams/` directory.
- **Naming**: Use `UPPER_SNAKE_CASE_DIAGRAM.excalidraw`.
- **Color Coding**:
  - **Blue**: Triggers/Entry points.
  - **Green**: Core logic/Actions.
  - **Yellow**: Conditional branches/Filters.
  - **Red**: Error handling nodes.

---

## 4. Coding Conventions (Python/JavaScript)
If source code is added to the repository, follow these rules:
- **Python**: PEP 8 compliance. Use `ruff` for linting. Typing is required (`from typing import ...`).
- **JavaScript**: Standard style. Use ES6+ modules (`import/export`). No `var`, only `const/let`.
- **Error Handling**: Use `try/except` or `try/catch` with explicit error logging.
- **Imports**: Group imports (Standard Library, Third-Party, Local).

---

## 5. Repository Structure
- `/`: Root directory containing workflows, primary docs (`CLAUDE.md`, `GEMINI.md`, `n8n_MCP_GUIDE.md`).
- `/excalidraw diagrams/`: Visual representations of logic and system architecture.
- `/.claude/`: Local agent configuration, including tool permissions and settings.

---

## 6. Safety & Security Protocols

### 6.1 Secret Management
- **CRITICAL**: Never commit `.env` files, API keys, or plain-text tokens.
- **Scanning**: Run a `grep` for "Bearer", "API_KEY", or "SECRET" before pushing changes.

### 6.2 Destructive Actions
- **No Deletions**: Do not delete n8n workflows or documents unless explicitly requested by the user.
- **Version Control**: When editing a workflow, create a backup file (e.g., `filename.json.bak`) before modification if not using Git.

### 6.3 State Verification
- After modifying a JSON file, always run a JSON parse check to ensure validity.
- After updating MCP settings, run `claude mcp list` to ensure the server is still connected.

---

## 7. Interaction Guidelines for Agents
- **Tone**: Professional, technical, and concise.
- **Response Length**: Keep text descriptions under 5 lines unless explaining complex architecture.
- **Proactiveness**: 
  - If a workflow change is made, offer to update the relevant documentation.
  - If an error is detected in a JSON file, fix it immediately.
- **Clarity**: If a user request is ambiguous regarding which n8n instance to target, ask for clarification.

---

## 8. Agent-Specific Tool Usage
- **MCP Preferred**: Always prefer `mcp__n8n` tools for real-time interaction with the n8n environment over static file editing when possible.
- **Context Search**: Use `grep` and `glob` extensively to find relevant nodes or documentation before proposing changes.

---

## 9. Version Control & Git Guidelines
Even if the current repository state is documentation-heavy, follow these Git practices:
- **Commit Messages**: Use imperative mood (e.g., "Add Lead Intake workflow" NOT "Added...").
- **Atomic Commits**: Keep changes small and focused. One workflow or one doc change per commit.
- **Branching**: Use feature branches for major workflow overhauls (e.g., `feature/crm-integration`).
- **Review**: Before committing, use `git diff` to ensure no accidental changes to sensitive JSON fields.

## 10. External Resources & References
Agents should refer to these for specific technical details:
- **n8n Documentation**: [docs.n8n.io](https://docs.n8n.io)
- **MCP Protocol**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Project Guide**: Refer to `n8n_MCP_GUIDE.md` for specific connection strings and setup steps.

---

## 11. Advanced n8n Development Patterns
When scaling the "Loan Consulting System" or similar complex logic, prioritize:
- **Modular Workflows**: Use the "Execute Workflow" node to call sub-workflows instead of building massive monolithic flows.
- **Dynamic Expressions**: Use JavaScript within expressions to handle complex logic: `{{ $json.data.map(i => i.id).join(",") }}`.
- **Global Data Persistence**: Use the "HTTP Request" node to call a central database or CRM for state management across executions.
- **AI-Native Nodes**: Prefer using the "AI Agent" or "Basic LLM Chain" nodes in n8n for tasks requiring natural language understanding.

---
*Last Updated: 2026-03-18*
*Targeted Audience: AI Coding Agents (Claude Code, Gemini CLI, etc.)*
