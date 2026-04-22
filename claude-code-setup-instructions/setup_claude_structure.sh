#!/bin/bash
# Setup script to initialize token-optimized .claude directory structure

set -e

PROJECT_ROOT="${1:-.}"
CLAUDE_DIR="$PROJECT_ROOT/.claude"

echo "🚀 Initializing Claude Code project structure in: $CLAUDE_DIR"
echo ""

# Create directory structure
mkdir -p "$CLAUDE_DIR"/{agents,rules,commands,memory,patterns,docs}

echo "✅ Created directories:"
echo "   - .claude/agents/"
echo "   - .claude/rules/"
echo "   - .claude/commands/"
echo "   - .claude/memory/"
echo "   - .claude/patterns/"
echo "   - .claude/docs/"
echo ""

# Create README files for each section
echo "📝 Creating README files..."

cat > "$CLAUDE_DIR/agents/README.md" << 'EOF'
# Agents Directory

Defines AI agent behaviors, capabilities, and expected outputs for different roles/personas.

## Files

- `system_prompts.md` - Shared system instructions for all agents
- `[agent-name]/behavior.md` - Agent's core behavior & constraints
- `[agent-name]/capabilities.json` - Metadata about agent capabilities

## When to Use

Reference agents when Claude Code needs to:
- Take on specific personas or roles
- Follow consistent behavior patterns across sessions
- Understand its scope and limitations

## Example

```
agents/
├── email_workflow_specialist/
│   ├── behavior.md
│   └── capabilities.json
└── code_analyzer/
    ├── behavior.md
    └── capabilities.json
```
EOF

cat > "$CLAUDE_DIR/rules/README.md" << 'EOF'
# Rules Directory

Explicit constraints, standards, and guidelines that Claude Code should follow.

## Files

- `coding_standards.md` - Code style & best practices
- `naming_conventions.md` - Naming schemes for consistency
- `api_contracts.md` - API/interface expectations
- `performance.md` - Performance targets & constraints
- `security.md` - Security & compliance rules

## When to Use

Define rules when you need consistent behavior:
- Across all projects
- Across team members
- Over multiple sessions

## Benefits

- Code consistency without per-session instructions
- Single source of truth for standards
- Reduced token usage (reference instead of explain)
EOF

cat > "$CLAUDE_DIR/commands/README.md" << 'EOF'
# Commands Directory

Reusable shell scripts and workflows to automate repetitive tasks.

## Files

- `setup.sh` - Project initialization
- `test.sh` - Test suite runner
- `build.sh` - Build process
- `deploy.sh` - Deployment workflow

## When to Use

Create scripts for:
- One-time setup processes
- Repetitive testing/validation
- Build and deployment workflows
- Complex multi-step operations

## Benefits

- Token efficiency (one command instead of step-by-step)
- Consistency across team members
- Easier to maintain (update script, not instructions)

## Usage

```bash
bash .claude/commands/test.sh
bash .claude/commands/build.sh
```
EOF

cat > "$CLAUDE_DIR/memory/README.md" << 'EOF'
# Memory Directory

Persistent context that carries between sessions, reducing re-explanation.

## Files

- `project_state.json` - Current project status, active features, blockers
- `decision_log.md` - Architecture decisions and rationale
- `issues_tracker.md` - Known bugs, TODOs, limitations
- `progress.md` - What's completed, what's next
- `session_context.md` - Summary from previous session

## When to Use

Store information that Claude Code needs to understand your project:
- What the project does
- Current development status
- Architecture decisions and why
- Known issues and workarounds
- Next steps & priorities

## Benefits

- Claude Code remembers context without re-reading codebase
- Faster session startup (reference instead of explain)
- Reduced token consumption
- Better continuity across team members

## Update Frequency

- `project_state.json` - Weekly or when status changes
- `decision_log.md` - When making significant decisions
- `issues_tracker.md` - As bugs/TODOs are discovered
- `progress.md` - Weekly or at sprint end
- `session_context.md` - At end of each session

## Example Flow

1. Start session → Read `session_context.md` (1 min)
2. Work on tasks
3. End session → Update `session_context.md` with summary
EOF

cat > "$CLAUDE_DIR/patterns/README.md" << 'EOF'
# Patterns Directory

Reusable code templates and architectural patterns.

## Files

- `component_template.ts` - Component boilerplate
- `api_handler.ts` - API handler pattern
- `error_handling.md` - Error handling patterns

## When to Use

Standardize how common tasks are implemented:
- Component creation
- Error handling
- API client setup
- Database query patterns

## Benefits

- Consistent code style without instructions
- Faster development (copy-paste templates)
- Single source of truth for best practices

## Process

1. Implement pattern manually once
2. Document in `patterns/` with comments
3. Use as template for future similar tasks
EOF

cat > "$CLAUDE_DIR/docs/README.md" << 'EOF'
# Docs Directory

Quick reference documentation to avoid re-explaining the project.

## Files

- `QUICK_START.md` - 2-minute project intro (what it does, how to run)
- `API.md` - API endpoints, parameters, responses
- `ARCHITECTURE.md` - System design, data flow, dependencies
- `GLOSSARY.md` - Project-specific terminology

## When to Use

Create docs to answer:
- "What does this project do?"
- "How do I run it?"
- "What APIs does it expose?"
- "How is it designed?"
- "What terminology is used?"

## Benefits

- Claude Code reads these first to understand scope
- No token waste re-explaining architecture
- New team members onboard faster

## Reading Order

1. QUICK_START.md (2 min)
2. ARCHITECTURE.md (5 min)
3. API.md (reference as needed)
4. GLOSSARY.md (reference as needed)
EOF

echo "✅ Created README files"
echo ""

# Create template files
echo "📋 Creating template files..."

cat > "$CLAUDE_DIR/memory/project_state.json" << 'EOF'
{
  "project_name": "Your Project Name",
  "description": "Brief description of what the project does",
  "current_focus": "What you're working on right now",
  "active_features": [
    "Feature 1",
    "Feature 2",
    "Feature 3"
  ],
  "completed_features": [
    "Feature A (completed date)",
    "Feature B (completed date)"
  ],
  "blockers": [
    "Issue or dependency blocking progress"
  ],
  "tech_stack": {
    "language": "TypeScript",
    "framework": "Node.js",
    "database": "PostgreSQL"
  },
  "last_updated": "2025-04-16T10:00:00Z"
}
EOF

cat > "$CLAUDE_DIR/memory/decision_log.md" << 'EOF'
# Decision Log

## Format
- **Decision:** What you decided
- **Date:** When it was decided
- **Reason:** Why you chose this option
- **Trade-offs:** What you gave up
- **Status:** Implementation status

---

## Example Decision

**Decision:** Use SendGrid for email delivery
**Date:** 2025-04-10
**Reason:** Built-in webhook event handling, cost-effective, good n8n integration
**Trade-offs:** Limited customization vs ease of use
**Status:** ✅ Implemented and working

---

## Your Decisions

(Add your decisions here)
EOF

cat > "$CLAUDE_DIR/memory/issues_tracker.md" << 'EOF'
# Issues & TODOs Tracker

## High Priority Blockers

- [ ] Issue 1: Description
- [ ] Issue 2: Description

## Medium Priority (Nice to Have)

- [ ] Feature: Description
- [ ] Improvement: Description

## Low Priority (Future)

- [ ] Polish: Description
- [ ] Optimization: Description

## Known Limitations

- Limitation 1: Workaround if available
- Limitation 2: Workaround if available

## Resolved (Archive)

- [x] Fixed issue (resolution date)
EOF

cat > "$CLAUDE_DIR/memory/session_context.md" << 'EOF'
# Session Context

Last updated: [DATE]

## What Got Done This Session

- ✅ Task 1: Description
- ✅ Task 2: Description
- ⏳ Task 3: In progress

## Next Steps (Priority Order)

1. Task: Description
2. Task: Description
3. Task: Description

## Blockers & Issues

- Issue 1: Description & impact
- Issue 2: Description & impact

## Files Modified

- `path/to/file1.ts`
- `path/to/file2.ts`
- `path/to/file3.md`

## Key Learnings

- Learning 1: What you discovered
- Learning 2: What might help next time

## Questions for Next Session

- Question 1: What to clarify
- Question 2: What to research
EOF

cat > "$CLAUDE_DIR/memory/progress.md" << 'EOF'
# Development Progress

## Completed

### Week 1
- ✅ Task completed
- ✅ Task completed

### Week 2
- ✅ Task completed

## In Progress

- 🔄 Task: Description (started [DATE])
- 🔄 Task: Description (started [DATE])

## Upcoming

- 📅 Task: Description (planned for [DATE])
- 📅 Task: Description (planned for [DATE])

## Metrics

- Test coverage: X%
- Performance: Y ms
- Code quality: Z score
EOF

echo "✅ Created template files:"
echo "   - memory/project_state.json"
echo "   - memory/decision_log.md"
echo "   - memory/issues_tracker.md"
echo "   - memory/session_context.md"
echo "   - memory/progress.md"
echo ""

# Create documentation templates
cat > "$CLAUDE_DIR/docs/QUICK_START.md" << 'EOF'
# Quick Start

## What is this?

[1-2 sentence description of your project]

## How to run it

```bash
# Step 1
npm install

# Step 2
npm run dev
```

## Key files

- `main.ts` - Entry point
- `config.json` - Configuration
- `.env.example` - Environment variables

## Useful commands

```bash
npm test          # Run tests
npm run build     # Build project
npm run lint      # Check code style
```

## Next: Read ARCHITECTURE.md for system design
EOF

cat > "$CLAUDE_DIR/docs/ARCHITECTURE.md" << 'EOF'
# Architecture

## System Overview

[Describe your system's overall design]

## Components

### Component 1
- Purpose: What it does
- Dependencies: What it depends on
- Inputs: What it receives
- Outputs: What it produces

### Component 2
- Purpose: What it does
- Dependencies: What it depends on
- Inputs: What it receives
- Outputs: What it produces

## Data Flow

```
[Source] → [Processing] → [Destination]
```

## Technology Stack

- **Language:** TypeScript
- **Runtime:** Node.js
- **Database:** PostgreSQL
- **Key Libraries:** List them here

## External Integrations

- Service 1: What it does, why we use it
- Service 2: What it does, why we use it

## Deployment

- **Environment:** Where it runs
- **Hosting:** How it's hosted
- **CI/CD:** How it's built and deployed
EOF

cat > "$CLAUDE_DIR/docs/API.md" << 'EOF'
# API Reference

## Endpoints

### GET /endpoint
- **Purpose:** What it does
- **Parameters:** What it accepts
- **Response:** What it returns

### POST /endpoint
- **Purpose:** What it does
- **Parameters:** What it accepts
- **Response:** What it returns

## Webhooks

### webhook/event
- **Triggered by:** What triggers it
- **Payload:** What data is sent
- **Response:** What should be returned

## Error Responses

All errors follow this format:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message"
  }
}
```
EOF

cat > "$CLAUDE_DIR/docs/GLOSSARY.md" << 'EOF'
# Glossary

## Project-Specific Terms

**Term 1**
Definition and context

**Term 2**
Definition and context

## Common Abbreviations

- ABC: Stands for...
- XYZ: Stands for...

## Related Concepts

- Concept 1: Explanation
- Concept 2: Explanation
EOF

echo "✅ Created documentation templates:"
echo "   - docs/QUICK_START.md"
echo "   - docs/ARCHITECTURE.md"
echo "   - docs/API.md"
echo "   - docs/GLOSSARY.md"
echo ""

# Create sample rule files
cat > "$CLAUDE_DIR/rules/coding_standards.md" << 'EOF'
# Coding Standards

## TypeScript

- Use `const` by default, `let` if needed, never `var`
- Explicit types on function parameters and returns
- 2-space indentation
- Max line length: 100 characters
- Use async/await, never `.then()` chains

## File Organization

- One class/component per file
- Group related functions together
- Imports at top, organized by: external, internal, types
- Exports at bottom of file

## Error Handling

- Always handle promise rejections
- Use custom Error types for domain-specific errors
- Log with context (what failed, why, what's being done)

## Testing

- Test file next to implementation: `file.ts` → `file.test.ts`
- Use descriptive test names: `should fail when email is invalid`
- Aim for >80% coverage
- Test happy path and error cases
EOF

cat > "$CLAUDE_DIR/rules/naming_conventions.md" << 'EOF'
# Naming Conventions

## Files

- **kebab-case** for files: `user-service.ts`, `email-handler.ts`
- **Descriptive names**: `sendgrid-integration.ts` not `sg.ts`

## Classes & Types

- **PascalCase**: `UserService`, `EmailHandler`, `CampaignZone`
- **Nouns**: Describe what the thing is

## Functions & Variables

- **camelCase**: `getUserData()`, `isValidEmail`, `campaignList`
- **Verbs for functions**: `create`, `fetch`, `validate`, `transform`
- **Descriptive names**: `calculateTotal()` not `calc()`

## Constants

- **UPPER_SNAKE_CASE**: `MAX_RETRIES`, `DEFAULT_TIMEOUT`
- **Top of file**: Global constants at module top

## Database

- **snake_case** for columns: `user_id`, `created_at`, `is_active`
- **Plural table names**: `users`, `transactions`, `email_campaigns`
- **id suffix for foreign keys**: `user_id`, `campaign_id`
EOF

cat > "$CLAUDE_DIR/rules/security.md" << 'EOF'
# Security & Compliance

## Environment Variables

- Never commit `.env` (use `.env.example`)
- All secrets: API keys, database passwords, tokens
- List all required vars in `.env.example` with descriptions
- Never log sensitive data

## CAN-SPAM Compliance

- All emails must include unsubscribe link
- Unsubscribe must be honored within 10 business days
- Sender info must be clear and accurate
- Subject line must not be misleading

## API Security

- Validate all inputs
- Use parameterized queries (never string interpolation)
- Sanitize error messages (don't leak internals)
- Rate limit endpoints
- Use HTTPS only

## Code Review

- Security review required for:
  - Anything touching database
  - Anything with external integrations
  - Anything handling user data
EOF

echo "✅ Created rules templates:"
echo "   - rules/coding_standards.md"
echo "   - rules/naming_conventions.md"
echo "   - rules/security.md"
echo ""

# Create a sample config file
cat > "$CLAUDE_DIR/config.md" << 'EOF'
# Project Configuration Reference

## Environment

```bash
NODE_ENV=development
PORT=3000
DEBUG=true
```

## Database

```bash
DATABASE_URL=postgres://user:pass@localhost:5432/dbname
DATABASE_POOL_SIZE=10
```

## External Services

```bash
SENDGRID_API_KEY=your_key_here
SENDGRID_FROM_EMAIL=noreply@example.com
WEBHOOK_SECRET=your_secret_here
```

## Feature Flags

```bash
FEATURE_NEW_DASHBOARD=false
FEATURE_BETA_API=true
```

See `.env.example` for complete list.
EOF

echo "✅ Created config reference:"
echo "   - config.md"
echo ""

echo "════════════════════════════════════════════"
echo "✨ Setup Complete!"
echo "════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo ""
echo "1. Edit these files with your project info:"
echo "   - .claude/docs/QUICK_START.md"
echo "   - .claude/docs/ARCHITECTURE.md"
echo "   - .claude/memory/project_state.json"
echo ""
echo "2. Create shell scripts in .claude/commands/ for:"
echo "   - Project setup (setup.sh)"
echo "   - Running tests (test.sh)"
echo "   - Building (build.sh)"
echo ""
echo "3. Document decisions in:"
echo "   - .claude/memory/decision_log.md"
echo ""
echo "4. Update at end of each session:"
echo "   - .claude/memory/session_context.md"
echo ""
echo "5. Add your patterns once they stabilize:"
echo "   - .claude/patterns/"
echo ""
echo "Start with: cat .claude/docs/QUICK_START.md"
echo ""
