# 30-Day AI CLI Experimentation Plan

> **Objective:** Push minimum **7 commits** to GitHub over 30 days, showcasing experimentation with AI CLI tools based on this repository and current trends.
> **Repository:** [Agent Sandbox](https://github.com/dhyan2815/agent-sandbox)
> **Created:** 2026-05-16

---

## Overview

This plan guides you through 30 days of experimenting with AI CLI tools (Claude Code, Gemini CLI, Codex CLI, n8n, MCP). Each day has a specific focus, tasks, and tangible outputs that result in commits to this repository.

### Commit Target: Minimum 7 Commits
- **Week 1-2:** 2-3 commits (foundation + MCP exploration)
- **Week 3-4:** 2-3 commits (workflow + content)
- **Final Week:** 2 commits (integration + documentation)

---

## Day-by-Day Plan

### Week 1: Foundation & Claude Code Advanced Features

#### Day 1 — Claude Code: Project Scanning & Memory
**Focus:** Explore Claude Code's `/scan` command and memory system for this repository.

**Tasks:**
1. Run `/scan` on the repository to understand its structure
2. Review `.claude/memory/MEMORY.md` and existing memories
3. Create a new memory entry documenting your experimentation goals
4. Document findings in `docs/experiments/claude-code-scan-YYYY-MM-DD.md`

**Commit:** `docs/experiments/` folder with initial scan results

**Tools:** Claude Code (any command starting with `/`)

---

#### Day 2 — Claude Code: Prompt Caching Deep Dive
**Focus:** Understand and experiment with prompt caching in Claude Code.

**Tasks:**
1. Read about prompt caching in Claude documentation
2. Test long conversations to observe cache behavior
3. Create a test script that demonstrates caching efficiency
4. Document findings in `docs/experiments/prompt-caching-analysis.md`

**Commit:** Document with test results and findings

---

#### Day 3 — MCP Server: Introduction & Existing Tools
**Focus:** Explore MCP (Model Context Protocol) using existing tools.

**Tasks:**
1. Review `.mcp.json` configuration
2. List available MCP servers via `/mcp` or configuration
3. Test at least one MCP server (e.g., Notion, HuggingFace)
4. Document which MCP servers are connected in `docs/mcp-servers-status.md`

**Commit:** Updated `docs/mcp-servers-status.md`

---

#### Day 4 — MCP Server: Custom Server Planning
**Focus:** Plan a custom MCP server for this repository's needs.

**Tasks:**
1. Review `skills/skills-mcp-builder/SKILL.md` for guidance
2. Identify a gap: what MCP server would benefit this repo?
   - Examples: GitHub PR automation, content publishing, API testing
3. Create a SPEC.md for your custom MCP server in `docs/mcp/`
4. Document the architecture and tools needed

**Commit:** `docs/mcp/custom-mcp-server-spec.md`

---

#### Day 5 — MCP Server: Build Basic Server Structure
**Focus:** Start building the custom MCP server identified in Day 4.

**Tasks:**
1. Set up project structure for MCP server (Python or Node.js)
2. Implement basic server with `stdio` transport
3. Add one simple tool (e.g., `echo` or `get_timestamp`)
4. Test locally with Claude Code

**Commit:** New folder `mcp/custom-server/` with initial implementation

---

#### Day 6 — n8n: Workflow Audit & Enhancement
**Focus:** Review existing n8n workflows and plan improvements.

**Tasks:**
1. List all workflows in `n8n-workflows/`
2. Analyze each workflow for potential improvements
3. Identify one workflow to enhance (add AI integration, webhook, etc.)
4. Document current state and planned changes in `docs/workflow-audit.md`

**Commit:** `docs/workflow-audit.md`

---

#### Day 7 — n8n: Implement Workflow Enhancement
**Focus:** Implement the enhancement identified on Day 6.

**Tasks:**
1. Modify the selected n8n workflow
2. Add AI node (Claude/Gemini) or new trigger
3. Test the workflow
4. Update documentation with new workflow JSON

**Commit:** Updated workflow in `n8n-workflows/` + docs

---

### Week 2: Automation & Integration

#### Day 8 — Gemini CLI: Explore & Configure
**Focus:** Set up Gemini CLI and understand its capabilities.

**Tasks:**
1. Review `GEMINI.md` for existing setup
2. Configure Gemini CLI with API keys (if not done)
3. Test basic prompt execution
4. Document initial findings in `docs/experiments/gemini-cli-setup.md`

**Commit:** `docs/experiments/gemini-cli-setup.md`

---

#### Day 9 — Gemini CLI: Workflow Automation
**Focus:** Create a simple automation with Gemini CLI.

**Tasks:**
1. Identify a repetitive task (e.g., content generation, summarization)
2. Create a Gemini CLI workflow or script
3. Test and iterate
4. Document workflow in `docs/workflows/gemini-automation.md`

**Commit:** `docs/workflows/gemini-automation.md`

---

#### Day 10 — Codex CLI: Setup & Basic Testing
**Focus:** Explore Codex CLI from OpenAI.

**Tasks:**
1. Review `references/codex-tools.md` for existing notes
2. Install Codex CLI if not already done
3. Test basic commands (code completion, file generation)
4. Document capabilities in `docs/experiments/codex-cli-exploration.md`

**Commit:** `docs/experiments/codex-cli-exploration.md`

---

#### Day 11 — Codex CLI: Agentic Workflow
**Focus:** Use Codex for an agentic task.

**Tasks:**
1. Define a multi-step coding task (e.g., create a simple app)
2. Execute using Codex agent mode
3. Document the process and results
4. Compare with Claude Code approach

**Commit:** Documented comparison in `docs/`

---

#### Day 12 — Cross-Tool Integration: Claude + MCP
**Focus:** Connect Claude Code with your custom MCP server.

**Tasks:**
1. Update Claude Code configuration to use your MCP server
2. Test calling your custom tools via Claude Code
3. Debug any connection issues
4. Document integration steps in `docs/mcp/integration-guide.md`

**Commit:** `docs/mcp/integration-guide.md` + working MCP setup

---

#### Day 13 — Content Creation: LinkedIn Skill Enhancement
**Focus:** Improve an existing LinkedIn-related skill.

**Tasks:**
1. Choose one LinkedIn skill from `skills/linkedin/`
2. Analyze its current capabilities
3. Add new features (e.g., new comment variants, analytics integration)
4. Update SKILL.md with new features

**Commit:** Updated skill in `skills/linkedin/`

---

#### Day 14 — Content Creation: Graphic Designer Skill
**Focus:** Enhance the graphic-designer skill.

**Tasks:**
1. Review `skills/graphic-designer/SKILL.md`
2. Add new output formats or templates
3. Test with a sample content piece
4. Document new capabilities

**Commit:** Enhanced skill in `skills/graphic-designer/`

---

### Week 3: Developer Tools & Skills

#### Day 15 — Skills-MCP-Builder: Advanced Features
**Focus:** Explore advanced MCP server building patterns.

**Tasks:**
1. Review `skills/skills-mcp-builder/reference/mcp_best_practices.md`
2. Add error handling and logging to your custom server
3. Implement a more complex tool (e.g., file operations, API calls)
4. Document best practices learned

**Commit:** Improved MCP server + documentation

---

#### Day 16 — Excalidraw Diagram Generator
**Focus:** Create diagrams for your experiments.

**Tasks:**
1. Review `skills/excalidraw-diagram-generator/`
2. Generate a diagram for your MCP server architecture
3. Generate a diagram for your cross-tool workflow
4. Save to `visuals/` or `docs/diagrams/`

**Commit:** New diagrams in `visuals/` or `docs/diagrams/`

---

#### Day 17 — Mermaid Diagram Skill
**Focus:** Create technical diagrams using Mermaid.

**Tasks:**
1. Review `skills/design-doc-mermaid/`
2. Create architecture diagrams for your MCP server
3. Create sequence diagrams for tool interactions
4. Document in `docs/architecture/`

**Commit:** Mermaid diagrams in docs

---

#### Day 18 — Humanizer Skill: Testing & Refinement
**Focus:** Test and improve the humanizer skill.

**Tasks:**
1. Test the humanizer skill with AI-generated content
2. Identify areas for improvement
3. Refine the skill based on results
4. Document test cases and results

**Commit:** Updated `skills/humanizer/`

---

#### Day 19 — Apify Skills: Explore Lead Generation
**Focus:** Experiment with Apify for lead generation.

**Tasks:**
1. Review `skills/apify-lead-generation/SKILL.md`
2. Configure API keys (if not done)
3. Test a lead generation workflow
4. Document results in `docs/experiments/apify-lead-gen-test.md`

**Commit:** `docs/experiments/apify-lead-gen-test.md`

---

#### Day 20 — Apify Skills: Market Research Automation
**Focus:** Use Apify for market research.

**Tasks:**
1. Review `skills/apify-market-research/`
2. Run a small-scale market research test
3. Analyze results
4. Document methodology and findings

**Commit:** Research findings in `docs/`

---

### Week 4: Advanced Integration & Documentation

#### Day 21 — Project Idea Validator: Test with Live Data
**Focus:** Use the project-idea-validator skill.

**Tasks:**
1. Review `skills/project-idea-validator/`
2. Test with a project idea relevant to AI/ML
3. Analyze the validation results
4. Document the process

**Commit:** Validation results in `docs/`

---

#### Day 22 — Understand-Anything: Knowledge Graph
**Focus:** Explore the knowledge graph integration.

**Tasks:**
1. Review understanding skills available
2. Run a knowledge graph analysis on this repository
3. Document insights about the codebase structure
4. Save graph outputs to `docs/knowledge-graph/`

**Commit:** Knowledge graph analysis in `docs/knowledge-graph/`

---

#### Day 23 — Memory System: Optimization
**Focus:** Optimize Claude Code memory for this repo.

**Tasks:**
1. Review existing memories in `.claude/memory/`
2. Add new relevant memories (tools tested, lessons learned)
3. Clean up outdated information
4. Document memory strategy in `docs/memory-system-usage.md`

**Commit:** Updated memory files + documentation

---

#### Day 24 — Skill Builder: Create New Skill
**Focus:** Build a new skill from scratch.

**Tasks:**
1. Identify a gap in current skills
2. Follow skill structure from existing skills
3. Create SKILL.md with workflows and references
4. Test the skill

**Commit:** New skill in `skills/`

---

#### Day 25 — CI/CD & Automation: Git Workflow
**Focus:** Set up automated workflows.

**Tasks:**
1. Review `skills/creating-pr/SKILL.md`
2. Create a GitHub Actions workflow for automated testing
3. Document the workflow in `docs/ci/`
4. Test the workflow

**Commit:** New workflow in `.github/` or documented in `docs/`

---

#### Day 26 — Documentation: Consolidate Experiments
**Focus:** Organize all experiment documentation.

**Tasks:**
1. Review all experiment documents created
2. Consolidate key findings into a summary
3. Create an index for easy navigation
4. Update main README with key learnings

**Commit:** Consolidated documentation updates

---

#### Day 27 — Integration: Claude + n8n + MCP
**Focus:** Create a unified workflow combining tools.

**Tasks:**
1. Design a workflow that uses Claude Code, n8n, and MCP together
2. Implement the integration
3. Test end-to-end
4. Document the architecture

**Commit:** Integration documentation + working workflow

---

#### Day 28 — Performance: Optimization & Benchmarking
**Focus:** Benchmark tool performance.

**Tasks:**
1. Compare response times between Claude Code, Gemini CLI, Codex
2. Test MCP server latency
3. Document benchmarks in `docs/benchmarks/`
4. Identify optimization opportunities

**Commit:** Benchmark results in `docs/benchmarks/`

---

#### Day 29 — Review & Cleanup
**Focus:** Review all work and clean up.

**Tasks:**
1. Review all commits made so far
2. Clean up any incomplete or test files
3. Ensure all documentation is complete
4. Prepare summary of learnings

**Commit:** Cleanup and final documentation

---

#### Day 30 — Final Push & Reflection
**Focus:** Complete final commits and summarize.

**Tasks:**
1. Make final commits (target: 7+ total)
2. Write final summary in `docs/30-day-experiment-summary.md`
3. Update README with experiment results
4. Share learnings (optional: LinkedIn post)

**Commit:** Summary document + final README update

---

## Tracking Your Progress

### Commit Log Template

| Day | Focus | Commit Message | Files Changed |
|-----|-------|-----------------|---------------|
| 1 | Claude Code Scan | `docs: add initial Claude Code scan results` | docs/experiments/ |
| 3 | MCP Status | `docs: document MCP server status` | docs/mcp-servers-status.md |
| 5 | MCP Server | `mcp: add basic custom MCP server` | mcp/custom-server/ |
| 7 | n8n Workflow | `workflow: enhance n8n workflow` | n8n-workflows/ |
| ... | ... | ... | ... |

---

## Acceptance Criteria

- [ ] Minimum **7 commits** pushed to GitHub
- [ ] Each commit contains meaningful changes (not just documentation)
- [ ] All 30 days have corresponding experiment files or documentation
- [ ] Final summary document created at `docs/30-day-experiment-summary.md`

---

## Tools Reference

| Tool | Command/Path | Purpose |
|------|--------------|---------|
| Claude Code | `/command` | Agentic AI, skill invocation |
| Gemini CLI | `gemini` | Workflow automation |
| Codex CLI | `codex` | Code execution |
| n8n | `n8n-workflows/` | Automation |
| MCP | `.mcp.json` | Protocol integration |

---

## Notes

- Adjust days based on your schedule — some days can be combined
- Focus on quality over quantity for commits
- Document failures as well as successes — they're learning opportunities
- Use the memory system to track progress between sessions