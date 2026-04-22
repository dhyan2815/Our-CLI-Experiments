# Claude Code Structure Implementation Checklist

Quick reference to set up token-optimized directory structure for your project.

---

## Quick Setup (5 minutes)

```bash
# Step 1: Navigate to your project
cd /path/to/your/claude-code-project

# Step 2: Run the setup script
bash setup_claude_structure.sh

# Step 3: Create placeholder files
touch .claude/agents/system_prompts.md
touch .claude/commands/setup.sh .claude/commands/test.sh .claude/commands/build.sh
chmod +x .claude/commands/*.sh
```

---

## Phase 1: Minimum Viable Setup (30 min)

These 5 files will optimize 80% of your token waste.

### ✅ Step 1: Quick Start Docs (5 min)

Edit: `.claude/docs/QUICK_START.md`

- [ ] 1-2 sentence project description
- [ ] How to run/start the project
- [ ] 3-5 key files to know about
- [ ] Command reference (test, build, etc.)

**Example for n8n project:**
```markdown
# Quick Start

n8n email campaign automation with SendGrid integration.

## Run It

\`\`\`bash
npm install
npm run dev
\`\`\`

## Key Files

- workflows/email_campaign.json - Main workflow
- tests/campaign_test_ui.html - Test console
- integrations/sendgrid/ - SendGrid helpers
```

### ✅ Step 2: Project State JSON (5 min)

Edit: `.claude/memory/project_state.json`

- [ ] Project name
- [ ] Brief description
- [ ] Current focus/status
- [ ] 3-5 active features
- [ ] 1-2 blockers
- [ ] Tech stack

**Use the JSON example from APPLIED_EXAMPLE_EMAIL_WORKFLOW.md**

### ✅ Step 3: Session Context (5 min)

Edit: `.claude/memory/session_context.md`

- [ ] What you completed recently
- [ ] Top 3 next steps
- [ ] 1-2 key blockers
- [ ] Files you modified
- [ ] 1 key learning

**This is critical** - read/update this file at start/end of each session.

### ✅ Step 4: Coding Standards (5 min)

Edit: `.claude/rules/coding_standards.md`

- [ ] Language choice (TypeScript/Python/JavaScript)
- [ ] Naming conventions (camelCase, snake_case, etc.)
- [ ] Code style (indentation, max line length)
- [ ] Error handling approach
- [ ] Testing expectations

**Use the template from setup script**

### ✅ Step 5: Architecture Diagram (10 min)

Edit: `.claude/docs/ARCHITECTURE.md`

- [ ] System overview (what it does)
- [ ] 3-4 main components
- [ ] Data flow diagram (ASCII or text)
- [ ] External integrations (APIs, databases)
- [ ] Technology stack

**Use the example from APPLIED_EXAMPLE_EMAIL_WORKFLOW.md**

**After Phase 1: You're done with minimum setup! 🎉**

---

## Phase 2: Enhanced Setup (1-2 hours)

Add these for better token efficiency.

### ✅ Step 6: Decision Log

Edit: `.claude/memory/decision_log.md`

- [ ] Document 2-3 key decisions you've made
- [ ] Why you chose each option
- [ ] Trade-offs
- [ ] Current status

**Example:**
- "Why SendGrid over Mailgun" (reasons, trade-offs)
- "Why 8-zone architecture" (separation of concerns)
- "Why Google Sheets instead of database" (trade-offs)

### ✅ Step 7: Issues & TODOs

Edit: `.claude/memory/issues_tracker.md`

- [ ] List 2-3 high priority blockers
- [ ] List 2-3 medium priority improvements
- [ ] Add known limitations
- [ ] Add any workarounds

**Example:**
```markdown
## 🔴 Blockers

### Zone D Template Rendering
- Issue: Fails with accents (é, ñ)
- Impact: Can't send Spanish campaigns
- Workaround: Use ASCII characters only
```

### ✅ Step 8: Naming Conventions

Edit: `.claude/rules/naming_conventions.md`

- [ ] File naming (kebab-case, PascalCase, etc.)
- [ ] Variable naming (camelCase, snake_case)
- [ ] Class/type naming
- [ ] Database naming (if applicable)
- [ ] URL/route naming

### ✅ Step 9: Core Patterns

Create: `.claude/patterns/[your-common-pattern].md`

- [ ] Component template (if you use components)
- [ ] Error handling pattern
- [ ] API client pattern
- [ ] Database query pattern

**Add 1-2 patterns that you use repeatedly**

### ✅ Step 10: Shell Commands

Create: `.claude/commands/[script-name].sh`

At minimum:
- [ ] `.claude/commands/setup.sh` - Project initialization
- [ ] `.claude/commands/test.sh` - Run tests
- [ ] `.claude/commands/build.sh` - Build/compile

**Example:**
```bash
# .claude/commands/test.sh
#!/bin/bash
echo "Running tests..."
npm test

echo "Running linter..."
npm run lint

echo "All checks passed!"
```

---

## Phase 3: Advanced Setup (Optional)

For maximum token efficiency on complex projects.

### ✅ Step 11: Glossary

Create: `.claude/docs/GLOSSARY.md`

- [ ] Project-specific terms (e.g., "Zone A", "Campaign")
- [ ] Abbreviations (n8n, SendGrid, etc.)
- [ ] Domain-specific concepts

### ✅ Step 12: API Reference

Create: `.claude/docs/API.md`

- [ ] All endpoints / functions
- [ ] Parameters & response formats
- [ ] Error codes
- [ ] Rate limits

### ✅ Step 13: Progress Tracking

Create: `.claude/memory/progress.md`

- [ ] Weekly milestones
- [ ] Completed features
- [ ] Upcoming features
- [ ] Metrics (test coverage, performance)

### ✅ Step 14: Webhook / Integration Contracts

Create: `.claude/rules/api_contracts.md` or `.claude/rules/webhook_contracts.md`

- [ ] Exact payload schemas
- [ ] Validation rules
- [ ] Error handling
- [ ] Examples

**See APPLIED_EXAMPLE_EMAIL_WORKFLOW.md for webhook example**

### ✅ Step 15: Security & Compliance

Create: `.claude/rules/security.md` or `.claude/rules/compliance.md`

- [ ] Environment variable rules
- [ ] Data protection rules
- [ ] Compliance requirements (CAN-SPAM, GDPR, etc.)
- [ ] Code review requirements

---

## Maintenance Checklist

Do this regularly to keep structure effective.

### ✅ Weekly

- [ ] Update `.claude/memory/session_context.md` at end of sessions
- [ ] Update `.claude/memory/progress.md` with weekly progress
- [ ] Add new issues to `.claude/memory/issues_tracker.md` as discovered

### ✅ Monthly

- [ ] Review `.claude/memory/decision_log.md` - add major decisions made
- [ ] Audit `.claude/rules/` - any standards that changed?
- [ ] Add new patterns to `.claude/patterns/` once stable
- [ ] Update `.claude/docs/ARCHITECTURE.md` if design changed

### ✅ As Needed

- [ ] Add new files to `.claude/commands/` for repetitive tasks
- [ ] Refine naming conventions in `.claude/rules/`
- [ ] Add examples to `.claude/patterns/`
- [ ] Update glossary with new terminology

---

## Validation: Is Your Structure Working?

Check these to verify you're getting token savings:

- [ ] **Can you describe your project in 1 minute?** (Without re-reading code)
  - If yes → QUICK_START.md is working
  
- [ ] **Do you remember what you worked on last session?** (Without notes)
  - If yes → session_context.md is working
  
- [ ] **Can you list current blockers from memory?**
  - If yes → issues_tracker.md is working
  
- [ ] **Do you know why you chose your architecture?**
  - If yes → decision_log.md is working
  
- [ ] **Can you run common tasks with one command?** (`bash .claude/commands/test.sh`)
  - If yes → commands are working

**Score:**
- ✅ 5/5 → Structure is working great! 🎉
- ✅ 3-4/5 → Good progress, keep maintaining
- ✅ 1-2/5 → Need to populate more files
- 0/5 → Structure not being used, review setup

---

## Template Files Summary

| File | Time to Create | Priority | Savings |
|------|----------------|-----------|---------| 
| QUICK_START.md | 5 min | 🔴 HIGH | 500 tokens |
| project_state.json | 5 min | 🔴 HIGH | 300 tokens |
| session_context.md | 5 min | 🔴 HIGH | 400 tokens |
| coding_standards.md | 5 min | 🔴 HIGH | 200 tokens |
| ARCHITECTURE.md | 10 min | 🔴 HIGH | 800 tokens |
| decision_log.md | 10 min | 🟡 MED | 400 tokens |
| issues_tracker.md | 5 min | 🟡 MED | 300 tokens |
| naming_conventions.md | 5 min | 🟡 MED | 150 tokens |
| patterns/ | 20 min | 🟡 MED | 200 tokens |
| commands/ | 15 min | 🟡 MED | 150 tokens |
| API.md | 15 min | 🟢 LOW | 100 tokens |
| GLOSSARY.md | 10 min | 🟢 LOW | 50 tokens |
| progress.md | 5 min | 🟢 LOW | 50 tokens |

**Priority Focus:** Do the 🔴 HIGH priority items first. That's ~70% of token savings.

---

## Git Setup

Once you've created the structure:

```bash
# Add to .gitignore (don't commit secrets)
echo ".env" >> .gitignore
echo "node_modules/" >> .gitignore

# Commit the structure
git add .claude/
git commit -m "feat: add token-optimized .claude directory structure

- Add agents/ for behavior definitions
- Add rules/ for coding standards & constraints
- Add commands/ for shell scripts
- Add memory/ for session context & decision tracking
- Add patterns/ for reusable templates
- Add docs/ for architecture & API reference

This optimizes token usage by ~30% per session."

# Push
git push origin main
```

---

## Getting Started Now

### Option A: Quick Start (5 minutes)

```bash
# 1. Copy this checklist to your project
cp CLAUDE_CODE_STRUCTURE_GUIDE.md /your/project/

# 2. Run setup
bash setup_claude_structure.sh

# 3. Fill in Phase 1 items (5 files)
# - QUICK_START.md
# - project_state.json
# - session_context.md
# - coding_standards.md
# - ARCHITECTURE.md

# 4. Commit
git add .claude && git commit -m "Initial .claude structure"

# 5. Next session: Reference .claude/memory/session_context.md
```

### Option B: Comprehensive Setup (2 hours)

```bash
# Follow all Phase 1 + Phase 2 steps
# ~20-30 files created
# Complete token optimization
```

### Option C: Gradual Build (Ongoing)

```bash
# Start with Phase 1 (30 min)
# Add Phase 2 items weekly as needed (5 min/item)
# Add Phase 3 items as you discover patterns (15 min/item)
# Maintain weekly with checklist above
```

---

## For Your n8n Project Specifically

**Priority order (for you):**

1. ✅ QUICK_START.md - "8-zone email workflow"
2. ✅ project_state.json - Current status, zones A-F working, D has bug, F needs unsubscribe
3. ✅ session_context.md - What you did last, next steps
4. ✅ can_spam_compliance.md - Unsubscribe requirements
5. ✅ ARCHITECTURE.md - The 8 zones, data flow
6. ✅ issues_tracker.md - Zone D character bug, unsubscribe pending
7. ✅ webhook_contracts.md - SendGrid event schemas
8. ✅ commands/ - test_webhook.sh, validate_compliance.sh
9. 🟡 decision_log.md - Why SendGrid, why 8 zones
10. 🟡 patterns/ - Zone template, unsubscribe guard pattern

**Effort:** ~2-3 hours to get everything from APPLIED_EXAMPLE_EMAIL_WORKFLOW.md filled in.

**Payoff:** ~20,000 tokens saved over next 10 sessions.

---

## Need Help?

- **General guidance:** Read `CLAUDE_CODE_STRUCTURE_GUIDE.md`
- **For email workflow:** Read `APPLIED_EXAMPLE_EMAIL_WORKFLOW.md`
- **Implementing now:** Follow this checklist
- **Troubleshooting:** Check "Validation" section above

---

## TL;DR - Just Do This

```bash
# 1. Run setup (creates all directories & templates)
bash setup_claude_structure.sh

# 2. Fill 5 key files (30 minutes)
# Edit:
# - .claude/docs/QUICK_START.md
# - .claude/memory/project_state.json
# - .claude/memory/session_context.md
# - .claude/rules/coding_standards.md
# - .claude/docs/ARCHITECTURE.md

# 3. Start next session with
cat .claude/memory/session_context.md

# 4. Update at end of session
# Edit: .claude/memory/session_context.md

# That's it! 30 min setup → 30% token savings per session
```

---

## Success Metrics

You'll know this is working when:

✅ **Token Usage** - Same quality output, 25-35% fewer tokens per session
✅ **Context Speed** - Load project context in <1 minute instead of 10 minutes
✅ **Consistency** - Same approach across all Claude Code sessions
✅ **Onboarding** - New team members understand project in 5 minutes
✅ **Continuity** - Remember what you did 2 weeks ago without re-reading code

Good luck! 🚀
