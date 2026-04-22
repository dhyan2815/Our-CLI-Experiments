# Applied Example: Your n8n Email Campaign Structure

This shows exactly how to organize your existing Fortiv n8n email workflow project using the token-optimized structure.

---

## Your Current State (from memory)

You're rebuilding a broken n8n email marketing workflow with:
- **8 zones** (A–H) that process different email campaign stages
- **Google Spreadsheet** backing with 4 sheets
- **SendGrid integration** with API, sender auth, event webhooks
- **Compliance gap**: Unsubscribe guards needed in Zones C, D, F
- **Test infrastructure**: Interactive HTML console for webhook payload testing

---

## Recommended Directory Structure for Your Project

```
fortiv-ai-automation/
├── .claude/
│   ├── agents/
│   │   ├── README.md
│   │   └── email_workflow_specialist/
│   │       ├── behavior.md
│   │       └── capabilities.json
│   │
│   ├── rules/
│   │   ├── README.md
│   │   ├── can_spam_compliance.md
│   │   ├── webhook_contracts.md
│   │   ├── sendgrid_standards.md
│   │   └── n8n_node_patterns.md
│   │
│   ├── commands/
│   │   ├── README.md
│   │   ├── test_webhook.sh
│   │   ├── validate_compliance.sh
│   │   └── deploy_workflow.sh
│   │
│   ├── memory/
│   │   ├── README.md
│   │   ├── project_state.json
│   │   ├── decision_log.md
│   │   ├── issues_tracker.md
│   │   ├── progress.md
│   │   └── session_context.md
│   │
│   ├── patterns/
│   │   ├── README.md
│   │   ├── zone_node_template.md
│   │   ├── sendgrid_event_handler.js
│   │   ├── webhook_payload_schema.json
│   │   └── error_handling.md
│   │
│   ├── docs/
│   │   ├── README.md
│   │   ├── QUICK_START.md
│   │   ├── ARCHITECTURE.md
│   │   ├── API.md
│   │   └── GLOSSARY.md
│   │
│   └── config.md
│
├── workflows/                  # Your existing folder
│   ├── email_campaign.json    # Main n8n workflow
│   ├── zone_a_initial_processing.json
│   ├── zone_b_validation.json
│   ├── ... (zones C-H)
│   └── README.md
│
├── tests/                     # Your existing folder structure
│   ├── campaign_test_ui.html  # Interactive test console
│   ├── webhook_payloads.json
│   └── sendgrid_events.json
│
├── integrations/              # Your existing folder
│   ├── sendgrid/
│   │   ├── config.json
│   │   ├── api_wrapper.js
│   │   └── event_handlers.js
│   └── google_sheets/
│       └── client.js
│
├── docs/                      # Your existing folder
│   ├── n8n_workflow_guide.md
│   └── sendgrid_setup.md
│
├── .env.example
├── .gitignore
└── README.md
```

---

## File-by-File: What to Write

### 1. `.claude/memory/project_state.json`

```json
{
  "project_name": "Fortiv AI Email Campaign Automation",
  "description": "n8n-based email marketing workflow with SendGrid integration, 8 processing zones, Google Sheets sync",
  "current_focus": "Implementing CAN-SPAM unsubscribe guards in Zones C, D, F",
  "status": "Rebuilding after intern transition (broken workflow being fixed)",
  "active_features": [
    "Zone A: Initial payload processing",
    "Zone B: Email validation & enrichment",
    "Zone C: Personalization (UNSUBSCRIBE GUARD PENDING)",
    "Zone D: Template rendering (VALIDATION ISSUE BLOCKING)",
    "Zone E: Segmentation & filtering",
    "Zone F: Send queue (UNSUBSCRIBE GUARD PENDING)",
    "Zone G: SendGrid webhook intake & logging",
    "Zone H: Event processing & analytics",
    "Google Sheets sync (4 sheets: contacts, templates, campaigns, results)",
    "SendGrid integration (API, webhooks, event tracking)"
  ],
  "completed_features": [
    "SendGrid API authentication & configuration",
    "Webhook endpoint setup for events",
    "Interactive test console (campaign_test_ui.html)",
    "Zone A-B basic flow (date: 2025-04-14)",
    "Database schema for campaigns (date: 2025-04-10)"
  ],
  "blockers": [
    "Zone D template validation failing on certain characters - needs debugging",
    "Unsubscribe guard not yet implemented in Zones C, D, F (CAN-SPAM compliance)",
    "Zone H analytics aggregation needs performance optimization"
  ],
  "tech_stack": {
    "orchestration": "n8n (self-hosted)",
    "email_service": "SendGrid",
    "spreadsheet": "Google Sheets",
    "backend": "Node.js with n8n nodes",
    "testing": "HTML console + JSON payloads",
    "database": "None (spreadsheet-based)"
  },
  "team_context": "Intern (you) inherited broken workflow from previous intern. Full rebuild required.",
  "last_updated": "2025-04-16T10:30:00Z"
}
```

### 2. `.claude/memory/decision_log.md`

```markdown
# Decision Log: Email Campaign Workflow

## Decision: Use SendGrid Instead of Alternatives
**Date:** 2025-04-08 (inherited decision, validated)
**Options Considered:**
- Mailgun (better parsing, complex setup)
- AWS SES (cheaper, requires IAM setup)
- SendGrid (chosen)
**Reason:** Built-in webhook event handling, cost-effective (~$14/month), native n8n integration
**Trade-offs:** Limited customization vs ease of integration with n8n
**Status:** ✅ Implemented, webhooks working, no regrets

## Decision: 8-Zone Architecture
**Date:** 2025-04-08 (inherited design)
**Rationale:** Separate concerns
- Zone A: Parsing
- Zone B: Validation
- Zone C: Personalization
- Zone D: Rendering
- Zone E: Segmentation
- Zone F: Sending
- Zone G: Webhook intake
- Zone H: Analytics
**Benefit:** Clear responsibility boundaries, easy to debug/modify per zone
**Status:** ✅ Proven design, working well

## Decision: Google Sheets as Backend
**Date:** 2025-04-08 (inherited)
**Reason:** No database needed, easy to view/debug data live, client can edit templates directly
**Trade-off:** Not scalable beyond ~10K campaigns/month, slower than DB queries
**Status:** ✅ Working for current volume, revisit if scale changes

## Decision: Interactive HTML Test Console
**Date:** 2025-04-14 (your decision)
**Reason:** Manual webhook testing was tedious, needed reliable way to test all 4 endpoints
**Result:** campaign_test_ui.html reduces test feedback cycle from 5 min to 30 sec
**Status:** ✅ Deployed, saved significant time

## Decision Pending: CAN-SPAM Unsubscribe Implementation
**Status:** ⏳ Needs decision
**Options:**
1. Add guard in Zone C (before personalization) - simple but wastes compute
2. Add guard in Zone F (before sending) - optimal but requires different logic
3. Add in both C and F - safe but duplicates work
**Recommendation:** Option 2 (Zone F) - check unsubscribe list immediately before send
**Decision:** [Awaiting your approval]
```

### 3. `.claude/memory/issues_tracker.md`

```markdown
# Issues & TODOs

## 🔴 High Priority Blockers

### Zone D Template Rendering Fails on Special Characters
- **Status:** 🔴 BLOCKING
- **Issue:** Templates with accents (é, ñ) or quotes (" ") failing validation
- **Impact:** Can't send campaigns with non-ASCII characters (affects Spanish campaigns)
- **Root Cause:** Likely character encoding in SendGrid API call
- **Workaround:** Escape quotes manually, avoid accents (temporary)
- **Next:** Debug Zone D node, check SendGrid charset settings

### CAN-SPAM Unsubscribe Not Implemented
- **Status:** 🔴 COMPLIANCE RISK
- **Issue:** Zones C, D, F missing unsubscribe guards
- **Impact:** Cannot legally send emails (violates CAN-SPAM Act)
- **Required Fix:** Add unsubscribe check in Zone F before SendGrid call
- **Effort:** 2-3 hours to implement + test
- **Timeline:** URGENT - before next campaign send

## 🟡 Medium Priority (Nice to Have)

### Zone H Analytics Aggregation Performance
- **Status:** 🟡 SLOW (60 sec to aggregate 1K events)
- **Issue:** Google Sheets writes are sequential
- **Fix:** Batch writes or use intermediate cache
- **Effort:** 4 hours
- **Timeline:** Next sprint if volume increases

### Webhook Retry Logic
- **Status:** 🟡 MISSING
- **Issue:** If webhook fails, event is lost
- **Fix:** Add retry queue in Zone G
- **Effort:** 3 hours

## 🟢 Low Priority (Polish)

### Test Console UI Polish
- **Issue:** campaign_test_ui.html works but UI is plain
- **Fix:** Add visual feedback, status indicators
- **Timeline:** Nice to have, low impact

## ✅ Resolved (Archive)

- [x] SendGrid authentication (2025-04-10)
- [x] Webhook endpoint creation (2025-04-10)
- [x] Zone A-B basic flow (2025-04-14)
- [x] Test console MVP (2025-04-14)
```

### 4. `.claude/memory/session_context.md`

```markdown
# Session Context - Last Session

**Last updated:** 2025-04-16 10:30 AM

## ✅ What Got Done This Session

- ✅ Rebuilt Zone A payload parsing (fixed JSON parsing bug from previous intern)
- ✅ Fixed Zone B email validation (regex was too strict)
- ✅ Debugged SendGrid webhook integration
- ✅ Created interactive test console (campaign_test_ui.html)
- ✅ Tested all 4 webhook endpoints (DELIVERY, BOUNCE, OPEN, CLICK)
- ⏳ Started Zone D debugging (template rendering issue with accents - 50% done)

## 🚀 Next Steps (Priority Order)

1. **URGENT:** Implement CAN-SPAM unsubscribe guard in Zone F
   - Fetch unsubscribe list from SendGrid
   - Add conditional check before send
   - Test with real unsubscribe scenario
   - Estimated: 2 hours

2. **DEBUG:** Fix Zone D template character encoding
   - Check SendGrid API charset settings
   - Test with Spanish/accent characters
   - Update test_payloads.json with accent test cases
   - Estimated: 1.5 hours

3. **OPTIMIZE:** Zone H analytics aggregation
   - Add batch write logic
   - Measure before/after performance
   - Update architecture doc
   - Estimated: 4 hours (lower priority)

## 🚧 Blockers & Issues

### Zone D Character Encoding
- **Status:** 🔴 BLOCKING 2nd campaign send
- **Error:** Template with "José" fails validation
- **Last action:** Checked SendGrid API docs, found charset param
- **Next action:** Test with charset=utf-8 in Zone D node

### Missing Unsubscribe Check
- **Status:** 🔴 COMPLIANCE RISK
- **Required:** Cannot send emails without this
- **Next action:** Start implementation in Zone F

## 📝 Files Modified This Session

- `workflows/email_campaign.json` - Updated Zone A-B
- `workflows/zone_d_rendering.json` - Debugging in progress
- `tests/campaign_test_ui.html` - Created from scratch
- `tests/sendgrid_events.json` - Added test cases
- `.env.example` - Added SENDGRID_WEBHOOK_SECRET

## 💡 Key Learnings

1. **Webhook testing slows iteration** - Created test console to make feedback instant
2. **Character encoding matters in SendGrid** - Different API endpoints may have different charset defaults
3. **n8n debugging is easier with separate test files** - Don't embed test data, keep external for reuse

## ❓ Questions for Next Session

- Should unsubscribe check go in Zone C (early) or Zone F (late)?
- Should we implement retry logic for Zone G webhooks?
- Do we need to optimize Zone H before next campaign?

## 🎯 Session Summary (TL;DR)

Made good progress rebuilding workflow. Zones A-B stable. Zone D needs charset fix for international emails. Unsubscribe guard is high-priority blocker for compliance. Test infrastructure now makes iteration fast.
```

### 5. `.claude/rules/can_spam_compliance.md`

```markdown
# CAN-SPAM Compliance Rules

All email campaigns must follow these rules or they are non-compliant.

## Requirements (Legal Mandate)

### 1. Unsubscribe Link
- **Requirement:** Every email must have a working unsubscribe link
- **Where:** Must be in Zone F (before SendGrid call)
- **Implementation:** Check against SendGrid suppression list
- **Timeframe:** Unsubscribe must be honored within 10 business days

### 2. Sender Information
- **Requirement:** Sender address must be accurate and verifiable
- **Config:** Set in SendGrid from_email (currently: noreply@example.com)
- **Check:** Domain must have SPF/DKIM records (use SendGrid sender auth)

### 3. Subject Line
- **Requirement:** Must not be misleading or deceptive
- **Check:** No clickbait, no fake subject lines
- **Implementation:** No automated check needed, human review required

### 4. Physical Address
- **Requirement:** Must include business physical address
- **Where:** Email footer (Zone F template)
- **Example:** Fortiv Solutions Inc., [address], [city], [state] [zip]

### 5. Commercial vs Transactional
- **Transactional:** Password reset, order confirmation, receipts
- **Commercial:** Marketing, promotions, newsletters
- **Rule:** Only commercial emails need unsubscribe (transactional exempt)

## Implementation in n8n

### Zone F: Pre-Send Unsubscribe Check

```
Zone F Unsubscribe Guard Logic:
├─ Get recipient email
├─ Query SendGrid suppression list (unsubscribed)
├─ If email is unsubscribed:
│  └─ Log as skipped, add to results
├─ If email is NOT unsubscribed:
│  └─ Send via SendGrid
└─ Always: Log disposition (sent/skipped)
```

### Zone C: Double-Check (Optional)
Early validation to fail fast:
- Skip personalization work for known unsubscribed users
- Reduces compute cost

## Testing Unsubscribe

1. **Create test email:** test-unsubscribe@example.com
2. **Send 1st campaign:** Should succeed, email received
3. **Unsubscribe:** Click unsubscribe link (Zone H processes it)
4. **Send 2nd campaign:** Should skip (check Zone H logged unsubscribe)
5. **Verify:** Check SendGrid suppression list

## SendGrid Integration Points

- **Suppression List:** GET /v3/suppression/unsubscribes
- **Add to Suppression:** POST /v3/suppression/unsubscribes
- **Remove from Suppression:** DELETE /v3/suppression/unsubscribes/{email}

## Documentation

See:
- `integrations/sendgrid/api_wrapper.js` - Helper functions
- `patterns/zone_f_presend_guard.md` - Implementation pattern
- `tests/can_spam_validation.json` - Test cases
```

### 6. `.claude/rules/webhook_contracts.md`

```markdown
# Webhook Payload Contracts

All webhooks must follow these schemas exactly.

## Zone G: Event Webhook Intake

**Endpoint:** POST /n8n/webhook/email-events
**Source:** SendGrid Event Webhook

### Supported Event Types

#### DELIVERY
```json
{
  "event": "delivered",
  "email": "user@example.com",
  "timestamp": 1234567890,
  "campaign_id": "campaign_123"
}
```

#### BOUNCE
```json
{
  "event": "bounce",
  "email": "invalid@example.com",
  "bounce_type": "hard", // hard or soft
  "reason": "550 user unknown",
  "timestamp": 1234567890
}
```

#### OPEN
```json
{
  "event": "open",
  "email": "user@example.com",
  "timestamp": 1234567890,
  "user_agent": "Mozilla/5.0..."
}
```

#### CLICK
```json
{
  "event": "click",
  "email": "user@example.com",
  "url": "https://example.com/link?utm_source=email",
  "timestamp": 1234567890
}
```

#### UNSUBSCRIBE
```json
{
  "event": "unsubscribe",
  "email": "user@example.com",
  "timestamp": 1234567890,
  "reason": "user"  // or "bounce", "complaint"
}
```

## Validation Rules

- `email` must be valid email format
- `timestamp` must be valid Unix epoch
- `event` must be one of: delivered, bounce, open, click, unsubscribe
- If `bounce_type` present, must be: hard, soft
- All required fields must be present

## Error Responses

If validation fails:
```json
{
  "success": false,
  "error": "Invalid email format",
  "event_type": "open"
}
```

If processing succeeds:
```json
{
  "success": true,
  "event_id": "evt_123",
  "processed_at": "2025-04-16T10:30:00Z"
}
```
```

### 7. `.claude/docs/QUICK_START.md`

```markdown
# Quick Start: Email Campaign Workflow

## What is This?

n8n-based email marketing automation platform that sends bulk campaigns via SendGrid with full event tracking (opens, clicks, bounces) and Google Sheets integration.

## How to Run It

### Prerequisites
- n8n instance (self-hosted or cloud)
- SendGrid account with API key
- Google Sheets with template credentials
- Node.js 18+ (for local testing)

### Setup (One Time)

1. **Configure SendGrid**
   ```bash
   # Set in n8n environment:
   SENDGRID_API_KEY=your_key_here
   SENDGRID_FROM_EMAIL=noreply@yourcompany.com
   ```

2. **Import Workflow**
   - Copy `workflows/email_campaign.json` into n8n
   - Update credentials (SendGrid API, Google Sheets)
   - Enable webhook: http://your-n8n/webhook/email-events

3. **Test**
   - Open `tests/campaign_test_ui.html` in browser
   - Send test payload to Zone G (webhook intake)
   - Verify event appears in Google Sheets

### Running a Campaign

```bash
# 1. Prepare data in Google Sheets (contacts, templates, campaign config)
# 2. Trigger workflow (manual in n8n UI)
# 3. Monitor progress in Zones A-F
# 4. View results in Zone H (Google Sheets)
# 5. Check event webhooks in Zone G logs
```

## Key Files

| File | Purpose |
|------|---------|
| `workflows/email_campaign.json` | Main n8n workflow |
| `.claude/docs/ARCHITECTURE.md` | How the 8 zones work |
| `tests/campaign_test_ui.html` | Interactive webhook testing |
| `integrations/sendgrid/` | SendGrid API helpers |
| `.claude/memory/issues_tracker.md` | Known issues |

## Quick Reference

| Zone | Purpose | Status |
|------|---------|--------|
| A | Parse payload | ✅ Working |
| B | Validate email | ✅ Working |
| C | Personalize | ⏳ Missing unsubscribe |
| D | Render template | 🔴 Character encoding bug |
| E | Segment/filter | ✅ Working |
| F | Send queue | ⏳ Missing unsubscribe guard |
| G | Webhook intake | ✅ Working |
| H | Analytics | ✅ Slow, needs optimization |

## Useful Commands

```bash
# Test webhook locally
bash .claude/commands/test_webhook.sh

# Validate CAN-SPAM compliance
bash .claude/commands/validate_compliance.sh

# Deploy workflow
bash .claude/commands/deploy_workflow.sh
```

## Next Steps

1. Read `.claude/docs/ARCHITECTURE.md` for system design
2. Check `.claude/memory/issues_tracker.md` for what's broken
3. See `.claude/memory/session_context.md` for where we left off

## Getting Help

- Zone A-E questions? See `workflows/zone_[letter].json`
- SendGrid questions? See `integrations/sendgrid/`
- CAN-SPAM questions? See `.claude/rules/can_spam_compliance.md`
```

### 8. `.claude/docs/ARCHITECTURE.md`

```markdown
# Email Campaign Workflow Architecture

## System Overview

8-zone n8n workflow that processes email campaigns end-to-end:

```
Input Data → [Zones A-F] → SendGrid → [Zone G] ← Webhooks
                                          ↓
                                      [Zone H] → Results/Analytics
                                          ↓
                                    Google Sheets
```

## Zone Breakdown

### Zone A: Payload Parsing
- **Input:** Raw campaign request (JSON)
- **Process:** Parse contacts, templates, campaign metadata
- **Output:** Structured campaign object
- **Error Handling:** Validate JSON schema, fail if malformed

### Zone B: Email Validation & Enrichment
- **Input:** Contact list from Zone A
- **Process:** Validate email format, remove duplicates, enrich data
- **Output:** Clean contact list
- **Validation Rules:** Standard email regex, no system emails

### Zone C: Personalization
- **Input:** Clean contacts + templates
- **Process:** Replace {{variables}} with user data ({{name}}, {{company}})
- **Output:** Personalized email content
- **⚠️ TODO:** Add unsubscribe guard here (optional)

### Zone D: Template Rendering
- **Input:** Personalized content
- **Process:** Render markdown/HTML, apply formatting
- **Output:** HTML-ready email body
- **🔴 BUG:** Fails on non-ASCII characters (é, ñ, etc.)

### Zone E: Segmentation & Filtering
- **Input:** Rendered emails
- **Process:** Apply filters (geography, engagement, preferences)
- **Output:** Final send list
- **Example:** "Only send to US contacts", "Skip opted-out"

### Zone F: Send Queue & Pre-Send Guard
- **Input:** Filtered send list
- **Process:**
  1. Check SendGrid suppression list (unsubscribe guard)
  2. If unsubscribed: log as skipped, move to Zone H
  3. If subscribed: send via SendGrid API
- **Output:** Sent emails + failed sends
- **⚠️ TODO:** Implement unsubscribe check

### Zone G: Webhook Event Intake
- **Trigger:** SendGrid event webhook (delivered, bounce, open, click)
- **Process:** Validate event schema, log to database
- **Output:** Event logged, webhook acknowledged
- **Events:** delivery, bounce, open, click, unsubscribe

### Zone H: Analytics & Results Aggregation
- **Input:** Campaign results + events from Zone G
- **Process:** Aggregate stats (sent, delivered, opened, clicked, bounced)
- **Output:** Campaign report in Google Sheets
- **Metrics:** Send rate, open rate, click rate, bounce rate

## Data Flow

```
Google Sheets (Inputs)
├─ contacts sheet: email, name, company, location
├─ templates sheet: subject, body, unsubscribe_url
├─ campaigns sheet: campaign_id, name, status
└─ events sheet: (written by workflow)

              ↓

n8n Workflow (Zones A-H)
├─ Zone A: Parse & validate inputs
├─ Zone B: Email validation, deduplication
├─ Zone C: Variable substitution
├─ Zone D: HTML rendering
├─ Zone E: Apply filters
├─ Zone F: Unsubscribe check + SendGrid send
├─ Zone G: Receive webhooks
└─ Zone H: Aggregate results

              ↓

SendGrid (Email Service)
├─ Accepts email via API
├─ Sends email to recipient
└─ Fires webhooks (delivered, opened, clicked, etc.)

              ↓

Google Sheets (Outputs)
└─ events sheet: Updated with sent/delivery/open/click events
```

## Key Integration Points

### SendGrid API
- **Authentication:** API Key in env var `SENDGRID_API_KEY`
- **Send Endpoint:** POST /v3/mail/send
- **Suppress List:** GET /v3/suppression/unsubscribes
- **Event Webhook:** Configured in SendGrid dashboard

### Google Sheets
- **Credentials:** OAuth2 token in n8n
- **Input Sheets:** contacts, templates, campaigns
- **Output Sheet:** events, results

### n8n Webhook
- **URL:** POST /n8n/webhook/email-events
- **Source:** SendGrid Event Webhook (configured in SendGrid UI)
- **Auth:** Optional (webhook token in URL)

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Orchestration | n8n | Workflow engine |
| Email Service | SendGrid | Sending + event webhooks |
| Data Store | Google Sheets | Contacts, templates, results |
| Testing | HTML + JavaScript | Local webhook testing |
| Deployment | Docker (n8n) | Self-hosted instance |

## Performance Targets

| Zone | Target | Current | Notes |
|------|--------|---------|-------|
| A | <1 sec | <0.5s | Simple parse |
| B | <0.1 sec/email | Variable | Depends on size |
| C | <0.1 sec/email | <0.3s | Variable replacement |
| D | <0.2 sec/email | 🔴 Variable | Character encoding issue |
| E | <0.1 sec/email | <0.2s | Filter application |
| F | 0.5 sec/email | Variable | SendGrid API call |
| G | <1 sec | <0.5s | Webhook intake |
| H | <2 sec/100 events | 60s | Batch Google Sheets writes |

Zone H needs optimization for large event volumes.

## Deployment Diagram

```
┌─────────────────────────────────────────────────────────┐
│ n8n Instance (Docker Container)                         │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Email Campaign Workflow                          │   │
│  │ ├─ Zones A-F (Send Pipeline)                     │   │
│  │ ├─ Zone G (Webhook Intake)                       │   │
│  │ └─ Zone H (Analytics)                            │   │
│  └──────────────────────────────────────────────────┘   │
│           ↓              ↓              ↓                │
└──────────────────────────────────────────────────────────┘
         │              │              │
         ↓              ↓              ↓
    SendGrid      Google Sheets     (Webhooks ← SendGrid)
    API Keys      OAuth2 Creds      Configured in SendGrid UI
```

## Security Considerations

- **API Keys:** Stored in n8n secrets (not in repo)
- **Google Sheets:** OAuth2 authenticated
- **Webhooks:** Optional webhook token in URL path
- **Unsubscribe:** Must check SendGrid suppression before send (legal requirement)
```

### 9. `.claude/patterns/zone_f_unsubscribe_guard.md`

```markdown
# Pattern: Zone F Unsubscribe Guard

Implements CAN-SPAM-compliant unsubscribe check before sending.

## Problem

Without this guard, we:
- Violate CAN-SPAM Act
- Send emails to people who opted out
- Risk sending complaints to SendGrid
- Damage sender reputation

## Solution

Add validation node in Zone F that:
1. Fetches SendGrid suppression list
2. Checks if email is in suppressed/unsubscribed list
3. If unsubscribed: skip send, log as skipped
4. If subscribed: proceed to send

## Implementation (n8n)

```yaml
Zone F Node: HTTP Request
├─ Method: GET
├─ URL: https://api.sendgrid.com/v3/suppression/unsubscribes
├─ Headers:
│  └─ Authorization: Bearer {{ $env.SENDGRID_API_KEY }}
├─ Query:
│  └─ email={{ $json.email }}
└─ Authentication: None (using header)

Next Node: Condition
├─ If response.result[0] exists (email is suppressed):
│  └─ → Skip send, log as "unsubscribed"
└─ Else:
   └─ → Proceed to SendGrid send
```

## Code Example (JavaScript)

```javascript
// Check if email is in SendGrid suppression list
async function isUnsubscribed(email, apiKey) {
  const response = await fetch(
    `https://api.sendgrid.com/v3/suppression/unsubscribes?email=${email}`,
    {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${apiKey}`
      }
    }
  );
  
  const data = await response.json();
  return data.result && data.result.length > 0;
}

// Usage in send logic
if (await isUnsubscribed(email, apiKey)) {
  console.log(`Skipping ${email}: unsubscribed`);
  return { sent: false, reason: 'unsubscribed' };
} else {
  // Send email
  return sendViaAPI(email, ...);
}
```

## Testing

1. **Create test email:** testuser@example.com
2. **Send campaign:** Should succeed
3. **Unsubscribe:** Click unsubscribe link (or use SendGrid API)
4. **Add to suppression:** Verify in SendGrid UI
5. **Send 2nd campaign:** Should skip with reason="unsubscribed"
6. **Verify:** Check logs show skipped, not sent

## Performance

- **API call:** ~100-200ms per email
- **Optimization:** Batch check with batch endpoint (slower to implement)
- **Recommendation:** Current per-email is fine for <100 emails/sec

## References

- SendGrid API: https://docs.sendgrid.com/api-reference/suppressions/retrieve-a-global-suppression
- CAN-SPAM: https://www.ftc.gov/business-guidance/pages/can-spam-act-compliance-guide
```

---

## How to Use This Structure

### Before Your Next Session

```bash
# 1. Run setup script (one time)
bash setup_claude_structure.sh

# 2. Populate key files with content above
cp .claude/docs/QUICK_START.md .claude/docs/QUICK_START.md  # Edit with your content
cp .claude/memory/project_state.json .claude/memory/project_state.json  # Use JSON above
# ... etc for other files

# 3. Commit to git
git add .claude/
git commit -m "feat: add token-optimized .claude structure"
```

### Start of Next Claude Code Session

```
Good morning! Here's where we left off:

Reference context:
- QUICK_START: .claude/docs/QUICK_START.md
- Project state: .claude/memory/project_state.json
- Last session: .claude/memory/session_context.md
- Known issues: .claude/memory/issues_tracker.md

Today's focus: [Task]

Blockers: See .claude/memory/issues_tracker.md
```

### End of Session

Update `.claude/memory/session_context.md`:
- ✅ What you completed
- 🚀 Next steps (priority order)
- 🚧 Any blockers
- 📝 Files you modified
- 💡 Key learnings

---

## Expected Token Savings

| Without Structure | With Structure | Savings |
|-------------------|----------------|---------|
| Re-explain workflow | Reference QUICK_START.md | 500 tokens |
| Re-explain architecture | Reference ARCHITECTURE.md | 800 tokens |
| Repeat "what's broken?" | Reference issues_tracker.md | 300 tokens |
| Repeat decisions | Reference decision_log.md | 400 tokens |
| **Total per session** | **2000 token reduction** | **~30% savings** |

Over 10 sessions = 20,000 tokens saved.

---

## Next: Create These Files

1. Copy the JSON/markdown content above into actual files
2. Run `bash setup_claude_structure.sh` to create the directory structure
3. Edit the template files with your project info
4. Commit to git: `git add .claude && git commit`
5. Update this guide in your Claude Code next session reference

---

## Questions?

- **Structure unclear?** Read `CLAUDE_CODE_STRUCTURE_GUIDE.md` (comprehensive)
- **Practical example?** You're reading it (email workflow example)
- **Implementation help?** Use the setup script, it creates everything

Good luck optimizing your token usage! 🚀
```

