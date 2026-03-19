# LoanEase WhatsApp Loan Bot — Full Architectural Design

> **Workflow ID:** `ADJrQP70qXaX2VlS`
> **Workflow Name:** Main Workflow
> **Platform:** n8n
> **AI Engine:** Google Gemini (2.5 Pro / 2.5 Flash / embedding-001)
> **Database:** Supabase
> **Storage:** Google Drive
> **Communication Channel:** WhatsApp Business API (Meta Graph API)
> **Vector Store:** Pinecone

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [High-Level Architecture](#2-high-level-architecture)
3. [Database Schema (Supabase Tables)](#3-database-schema-supabase-tables)
4. [Pipeline Breakdown](#4-pipeline-breakdown)
   - [Pipeline 0 — Entry & Session Management](#pipeline-0--entry--session-management)
   - [Pipeline 1 — Phase Detection & Routing](#pipeline-1--phase-detection--routing)
   - [Pipeline 2 — Customer Data Collection (AI Conversation Agent)](#pipeline-2--customer-data-collection-ai-conversation-agent)
   - [Pipeline 3 — Document Intake & Verification](#pipeline-3--document-intake--verification)
   - [Pipeline 4 — Lender Matching (RAG)](#pipeline-4--lender-matching-rag)
   - [Pipeline 5 — Post-Match & Advisor Notification](#pipeline-5--post-match--advisor-notification)
5. [Node-by-Node Reference](#5-node-by-node-reference)
6. [AI Agent Architecture](#6-ai-agent-architecture)
7. [Phase State Machine](#7-phase-state-machine)
8. [Data Flow Diagrams](#8-data-flow-diagrams)
9. [Error Handling & Fallback Strategy](#9-error-handling--fallback-strategy)
10. [Security & Credential Map](#10-security--credential-map)
11. [Complete Node Inventory](#11-complete-node-inventory)

---

## 1. System Overview

LoanEase is a **fully automated WhatsApp-first loan origination bot** built on n8n. It guides a customer from first contact through to a ranked lender match, entirely over WhatsApp — no human intervention is required until the customer explicitly requests an advisor.

### Core Capabilities

| Capability | Description |
|---|---|
| **Onboarding** | Greets new users, collects name and loan type |
| **Data Collection** | Collects all loan-specific financial details conversationally |
| **Document Intake** | Accepts document images/files via WhatsApp, verifies them with Gemini Vision |
| **Lender Matching** | Performs RAG-based vector search against a Pinecone lender policy database |
| **Advisor Escalation** | Notifies a DSA (Direct Selling Agent) via rich HTML email when requested |
| **Full Audit Trail** | All inbound and outbound messages are logged to Supabase |

### Loan Types Supported

| Code | Name |
|---|---|
| `business` | Business Loan |
| `personal` | Personal Loan |
| `home` | Home Loan |
| `lap` | Loan Against Property |
| `od_cc` | Overdraft / Cash Credit |

---

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        WHATSAPP (Meta Cloud API)                        │
│              Customer sends text / image / document / button reply      │
└────────────────────────────┬────────────────────────────────────────────┘
                             │ Webhook POST
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PIPELINE 0 — ENTRY & SESSION MANAGEMENT                                │
│  Parse payload → Log message → Check/Create session → Fetch context     │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  PIPELINE 1 — PHASE DETECTION & ROUTING                                 │
│  Map session_state → phase (1/2/3/4/5)                                  │
└──────┬──────────────┬───────────────────┬───────────────────┬───────────┘
       │              │                   │                   │
    Phase 1        Phase 2            Phase 3            Phase 4/5
  Onboarding   Data Collection    Doc Collection     Lender Match /
                                                      Post-Match
       │              │                   │                   │
       ▼              ▼                   ▼                   ▼
┌──────────┐  ┌──────────────┐  ┌──────────────────┐  ┌─────────────────┐
│ AI Agent │  │  AI Agent    │  │ Gemini Vision    │  │  RAG Lender     │
│ Phase 1  │  │  Phase 2     │  │ Doc Verifier +   │  │  Matching Agent │
│(Onboard) │  │ (Collect)    │  │ AI Doc Analyst   │  │  (Pinecone)     │
└────┬─────┘  └──────┬───────┘  └────────┬─────────┘  └───────┬─────────┘
     │               │                   │                     │
     ▼               ▼                   ▼                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  RESPONSE LAYER                                                         │
│  Parse AI JSON → Update Supabase → Send WhatsApp message → Log reply    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Database Schema (Supabase Tables)

The workflow reads from and writes to **six Supabase tables**:

### `customers`
Stores customer identity data.

| Field | Type | Description |
|---|---|---|
| `id` | UUID (PK) | Auto-generated |
| `phone_number` | string | WhatsApp number (unique) |
| `full_name` | string | Collected during onboarding |
| `source` | string | Always `whatsapp_bot` |
| `is_active` | boolean | Always `true` on creation |

### `loan_applications`
Stores all loan-related fields for a customer's active application.

| Field | Type | Description |
|---|---|---|
| `id` | UUID (PK) | Auto-generated |
| `customer_id` | UUID (FK) | References `customers.id` |
| `loan_type` | string | business / personal / home / lap / od_cc |
| `loan_amount` | number | In rupees |
| `employment_type` | string | salaried / self_employed / business |
| `monthly_income` | number | In rupees |
| `business_vintage` | string | e.g. "3 years" |
| `annual_turnover` | number | In rupees |
| `property_value` | number | In rupees |
| `property_type` | string | residential / commercial / plot |
| `property_ownership` | string | self / family / joint |
| `existing_bank` | string | For OD/CC loan type |
| `cibil_score` | number | 300–900 |
| `city` | string | Normalised Indian city name |
| `status` | string | `collecting_info` on creation |

### `conversation_sessions`
Tracks the live state machine for each customer's conversation.

| Field | Type | Description |
|---|---|---|
| `id` | UUID (PK) | Auto-generated |
| `phone_number` | string | Customer phone (FK to customers) |
| `session_state` | string | Current state (see State Machine) |
| `application_id` | UUID | FK to `loan_applications.id` |
| `last_message` | string | Last message received |
| `retry_count` | integer | Incremented on invalid responses |
| `expires_at` | timestamp | Set to `now + 24 hours` on each update |

### `conversation_logs`
Append-only log of all messages (inbound + outbound).

| Field | Type | Description |
|---|---|---|
| `id` | UUID (PK) | Auto-generated |
| `phone_number` | string | Customer phone |
| `direction` | string | `inbound` or `outbound` |
| `message_type` | string | text / image / document / audio / video |
| `message_content` | string | Text body or description |
| `whatsapp_msg_id` | string | Meta's message ID |

### `documents`
Metadata for every verified document received.

| Field | Type | Description |
|---|---|---|
| `id` | UUID (PK) | Auto-generated |
| `application_id` | UUID | FK to `loan_applications.id` |
| `customer_id` | UUID | FK to `customers.id` |
| `document_type` | string | Canonical type (e.g. `pan_card`, `aadhaar`) |
| `original_filename` | string | As received |
| `stored_filename` | string | As saved in Google Drive |
| `google_drive_url` | string | Direct download link |
| `google_drive_file_id` | string | Drive file ID |
| `google_drive_folder_id` | string | Customer folder ID |
| `mime_type` | string | e.g. `application/pdf` |
| `file_size_bytes` | number | File size |
| `is_verified` | boolean | Always `true` when saved here |

### `lender_matches`
Stores ranked lender results for each application.

| Field | Type | Description |
|---|---|---|
| `id` | UUID (PK) | Auto-generated |
| `application_id` | UUID | FK to `loan_applications.id` |
| `lender_name` | string | Lender name from Pinecone result |
| `match_score` | float | 0.00–1.00 |
| `rank` | integer | 1 = best match |
| `reasons` | array | List of match reason strings |
| `presented_to_customer` | boolean | Always `true` when saved |

---

## 4. Pipeline Breakdown

---

### Pipeline 0 — Entry & Session Management

**Purpose:** Receive every WhatsApp message, parse it, log it, and either load an existing conversation session or bootstrap a brand-new customer with all required records.

#### Nodes in this pipeline:

```
Webhook_RecieveMessage
    └─► Code_ParseInput
            └─► Supabase_LogConversation
                    └─► Supabase_GetConversationState
                            └─► IF_SessionExists?
                                    ├─► [YES] Merge1
                                    └─► [NO]  Supabase_CreateCustomer
                                                  └─► Supabase_CreateLoanApplication
                                                          └─► Supabase_CreateSession
                                                                  └─► GoogleDrive_CreateACustomerFolder
                                                                              └─► Merge1
```

#### Step-by-step logic:

**1. `Webhook_RecieveMessage`**
- Type: Webhook trigger
- Path: `c82e412e-58b9-42cd-b871-f68912841ed0`
- Receives raw WhatsApp webhook payload from Meta Cloud API
- Passes raw JSON to the next node

**2. `Code_ParseInput`**
- Type: Code (JavaScript)
- Extracts and normalises all fields from the raw WhatsApp payload
- Handles all message types: text, image, document, audio, video, button_reply, list_reply
- Skips execution if there are no messages (e.g. status update events) by returning `{ skip: true }`
- **Output fields:**
  - `phone` — sender's phone number
  - `customer_name` — from WhatsApp profile
  - `message_id` — Meta message ID
  - `timestamp` — Unix timestamp
  - `message_type` — text / image / document / audio / video / interactive
  - `text` — text body (empty string if not text)
  - `media_id` — for image/document/audio/video
  - `media_type` — document / image / video / audio
  - `media_mime_type` — MIME type of media
  - `media_filename` — original filename for documents
  - `media_caption` — caption on media
  - `button_reply` / `button_reply_id` — for interactive button messages
  - `list_reply` / `list_reply_id` — for list reply messages
  - `business_phone_id` — WhatsApp Business phone ID
  - `display_phone` — display phone number

**3. `Supabase_LogConversation`**
- Table: `conversation_logs`
- Direction: `inbound`
- Logs: phone, message_type, whatsapp_msg_id, message_content (text body)
- Runs on every message regardless of what follows

**4. `Supabase_GetConversationState`**
- Table: `conversation_sessions`
- Filter: `phone_number = parsed phone`
- Fetches existing session if it exists
- `alwaysOutputData: true` — never stops the flow even if no session found

**5. `IF_SessionExists?`**
- Checks if `$json.id` exists (i.e. a session record was returned)
- **TRUE path → `Merge1`** (returning customer)
- **FALSE path → New customer bootstrap**

#### New Customer Bootstrap (FALSE path):

**6. `Supabase_CreateCustomer`**
- Table: `customers`
- Creates record with: phone_number, source=`whatsapp_bot`, is_active=`true`

**7. `Supabase_CreateLoanApplication`**
- Table: `loan_applications`
- Creates skeleton application with: customer_id, loan_type=`pending`, status=`collecting_info`

**8. `Supabase_CreateSession`**
- Table: `conversation_sessions`
- Creates session with: phone_number, session_state=`new_user`, application_id

**9. `GoogleDrive_CreateACustomerFolder`**
- Creates a named folder inside `LoanApplications/` on Google Drive
- Folder name = customer's WhatsApp phone number
- This folder will later store all verified document uploads

**10. `Merge1`**
- Merges both paths (returning customer and newly created customer) back into a single stream
- Ensures downstream nodes always receive a consistent session object

---

After `Merge1`, the flow retrieves all context needed for AI processing:

```
Merge1
  └─► Supabase_Get10RecentMessages
          └─► Code_Fetch_Latest_10_MSG
                  └─► Aggregate
                          └─► Supabase_GetCustomerDetails
                                  └─► Supabase_GetLoanApplication
                                          └─► Supabase_GetSessionState
                                                  └─► Set_SessionState
                                                          └─► Code_DetectPhase
```

**11. `Supabase_Get10RecentMessages`**
- Table: `conversation_logs`
- Fetches ALL messages for the phone number (returnAll: true)
- Used for conversation history context

**12. `Code_Fetch_Latest_10_MSG`**
- Sorts messages by `created_at` descending
- Slices to the latest 10 items
- Ensures the AI only gets a bounded context window

**13. `Aggregate`**
- Aggregates all 10 message items into a single array field `recent_messages`
- Makes it easy to pass as a single JSON object downstream

**14. `Supabase_GetCustomerDetails`**
- Table: `customers`
- Filter: phone_number
- Fetches full_name and customer ID

**15. `Supabase_GetLoanApplication`**
- Table: `loan_applications`
- Filter: `customer_id = customer.id`
- Fetches current loan type and all collected application fields

**16. `Supabase_GetSessionState`**
- Table: `conversation_sessions`
- Filter: phone_number
- Fetches: session_state, retry_count, expires_at, last_message, application_id

**17. `Set_SessionState`**
- Simple assignment node
- Passes `session_state` forward as a clean top-level field

---

### Pipeline 1 — Phase Detection & Routing

**Purpose:** Map the current `session_state` string to a numeric phase (1–5) and decide which pipeline branch to execute.

```
Set_SessionState
    └─► Code_DetectPhase
            └─► IF_SkipAgent?
                    ├─► [skip=true / Phase 4] → (no agent, RAG pipeline runs separately)
                    └─► [skip=false] → IF_Document Phase+MediaReceived?
                                            ├─► [Phase 3 + media] → Document Pipeline
                                            └─► [otherwise]       → Conversation Pipeline
```

**18. `Code_DetectPhase`**
- JavaScript node that maps every known `session_state` to a numeric phase:

| States | Phase | Pipeline |
|---|---|---|
| `new_user`, `awaiting_fullname`, `awaiting_loan_type` | 1 | Onboarding |
| `awaiting_loan_amount`, `awaiting_employment_type`, `awaiting_monthly_income`, `awaiting_business_vintage`, `awaiting_annual_turnover`, `awaiting_property_value`, `awaiting_property_type`, `awaiting_property_ownership`, `awaiting_existing_bank`, `awaiting_cibil_score`, `awaiting_city` | 2 | Data Collection |
| `awaiting_documents`, `collecting_documents`, `doc_type_clarification` | 3 | Document Collection |
| `matching_in_progress` | 4 | RAG (skips AI agent) |
| `results_sent`, `advisor_requested`, `human_handoff`, `escalated_to_human`, `application_complete` | 5 | Post-Match |

- Also builds `conversation_history` from the last 6 recent messages formatted as `[{role, content}]`
- Sets `required_docs` based on loan type from a hardcoded map
- Sets `skip_agent = true` when `phase === 4`
- Passes all fields forward unchanged

**19. `IF_SkipAgent?`**
- Checks if `skip_agent === true`
- **TRUE (Phase 4):** Exits this branch — RAG pipeline is triggered separately
- **FALSE:** Proceeds to `IF_Document Phase+MediaReceived?`

**20. `IF_Document Phase+MediaReceived?`**
- Two conditions combined with AND:
  - `current_phase === 3`
  - `media_id` is not empty
- **TRUE:** Routes to Document Pipeline (file has been sent in document collection phase)
- **FALSE:** Routes to Conversation Pipeline (text message or non-document phase)

---

### Pipeline 2 — Customer Data Collection (AI Conversation Agent)

**Purpose:** All text-based conversation — onboarding (Phase 1), data collection (Phase 2), post-match follow-up (Phase 5) — flows through a single AI agent that uses phase-specific system prompts.

```
IF_Document Phase+MediaReceived? [FALSE]
    └─► Set_InternalParams
            └─► Code_SystemPromptSelector
                    └─► AI Agent for Conversations
                            └─► Code_ParseAIResponse
                                    └─► IF_EscalatetoHuman?
                                            ├─► [TRUE escalate] → (stop / human handoff)
                                            └─► [FALSE] → Code_DynamicFieldSaver
                                                              └─► IF_WriteNeeded?
                                                                      ├─► [write needed] → IF_DB_Id Exist?
                                                                      │                         ├─► Supabase_UpdateField → Supabase_UpdateConversationSessions1 → Whatsapp_SendMessage1
                                                                      │                         └─► Supabase_UpdateField1 → Supabase_UpdateConversationSessions2 → Whatsapp_SendMessage2
                                                                      └─► [no write] → IF_IsValid?
                                                                                            ├─► [valid] → Supabase_UpdateConversationSessions → Whatsapp_SendMessage
                                                                                            └─► [invalid] → Supabase_UpdateConversationSession (with retry++) → Merge2 → Whatsapp_SendMessage
```

#### Node Details:

**21. `Set_InternalParams`**
- Selects and surfaces the key fields needed throughout the conversation pipeline:
  - `session_state`, `current_phase`, `conversation_history`, `required_docs`, `skip_agent`
  - `user_message` — extracted from `Whatsapp_RecieveMessage` node
  - `phone` — from `Code_ParseInput`

**22. `Code_SystemPromptSelector`**
- Selects the correct **system prompt** based on `current_phase`
- Builds the **user prompt** with all runtime context
- Contains four static system prompts (one per conversational phase):

##### System Prompt — Phase 1 (Onboarding)
- Handles `new_user` → greet, ask for name
- Handles `awaiting_fullname` → extract name, present loan type options
- Handles `awaiting_loan_type` → map to standard loan code
- Returns structured JSON with `extracted_field`, `extracted_value`, `next_state`, `response_message`

##### System Prompt — Phase 2 (Data Collection)
- Field-by-field collection based on loan type flow:
  - **Business:** loan_amount → business_vintage → annual_turnover → cibil → city
  - **Personal:** loan_amount → employment_type → monthly_income → cibil → city
  - **Home:** loan_amount → employment_type → monthly_income → property_value → property_type → cibil → city
  - **LAP:** loan_amount → employment_type → monthly_income → property_value → property_ownership → cibil → city
  - **OD/CC:** loan_amount → business_vintage → annual_turnover → existing_bank → cibil → city
- Flexible Indian number format parsing (lakhs, crores, k notation)
- Retry logic: rephrase (0-1), simplify (2), escalate_to_human (3+)
- Sets `next_state = "awaiting_documents"` when all fields collected

##### System Prompt — Phase 3 (Document Collection — text only)
- Handles text questions about documents
- Lists what is still missing for the customer's loan type
- Does NOT process actual file uploads (those go to the Document Pipeline)

##### System Prompt — Phase 5 (Post-Match / Closing)
- Handles `results_sent` state: advisor YES/NO/questions
- Handles `advisor_requested`: confirm callback
- Handles `human_handoff`: empathy + confirm human assist

##### User Prompt Builder
Each phase gets a different context block injected:
- Phase 1: `CURRENT STATE` + `CUSTOMER MESSAGE`
- Phase 2: `CURRENT STATE` + `LOAN TYPE` + `CUSTOMER NAME` + `RETRY COUNT` + `FIELDS ALREADY COLLECTED` + `CUSTOMER MESSAGE`
- Phase 3: `LOAN TYPE` + `DOCUMENTS REQUIRED` + `DOCUMENTS RECEIVED` + `MESSAGE TYPE` + `FILENAME` + `CUSTOMER MESSAGE/CAPTION`
- Phase 5: `CURRENT STATE` + `CUSTOMER NAME` + `CUSTOMER MESSAGE`

**23. `AI Agent for Conversations`**
- n8n AI Agent node
- LLM: **Google Gemini 2.5 Pro** (temperature 0.3)
- System message: `$json.system_prompt`
- User message: `$json.user_prompt` + appended JSON of session state, customer details, loan application, recent messages
- Returns raw text output containing a JSON object

**24. `Code_ParseAIResponse`**
- Strips markdown code fences (` ```json `, ` ``` `)
- Extracts JSON using regex `{[\s\S]*}`
- Falls back to safe defaults if parsing fails
- Enforces schema with `enforceSchema()`:

```json
{
  "is_valid": boolean,
  "extracted_value": string | number | null,
  "extracted_field": string | null,
  "next_state": string,
  "response_message": string,
  "needs_clarification": boolean,
  "escalate_to_human": boolean,
  "confidence": "high" | "medium" | "low"
}
```

**25. `IF_EscalatetoHuman?`**
- Checks `escalate_to_human === true`
- **TRUE:** Stops main flow (human handoff — no further automated processing)
- **FALSE:** Continues to field saving

**26. `Code_DynamicFieldSaver`**
- Reads `extracted_field` and `extracted_value` from AI response
- Validates field against whitelist of 13 allowed fields:
  `loan_type`, `loan_amount`, `employment_type`, `monthly_income`, `business_vintage`, `annual_turnover`, `property_value`, `property_type`, `property_ownership`, `existing_bank`, `cibil_score`, `city`, `full_name`
- Determines target table:
  - `full_name` → `customers` table
  - All others → `loan_applications` table
- Sets `db_table`, `db_field`, `db_value`, `db_id`, `write_skipped` flag
- Skips write if field is invalid, value is null, or no application ID

**27. `IF_WriteNeeded?`**
- Checks `write_skipped === false`
- **TRUE (write needed) → `IF_DB_Id Exist?`**
- **FALSE (no write) → `IF_IsValid?`**

**28. `IF_DB_Id Exist?`**
- Checks if `db_id` field exists (i.e. we have a record to update)
- **TRUE → `Supabase_UpdateField`** (updates `loan_applications` table dynamically)
- **FALSE → `Supabase_UpdateField1`** (updates `customers` table dynamically)

**29. `Supabase_UpdateField` / `Supabase_UpdateField1`**
- Dynamic Supabase update using `$json.db_table`, `$json.db_field`, `$json.db_value`, `$json.db_id`
- Writes exactly one field per AI turn
- After writing:
  - `UpdateField` → `Supabase_UpdateConversationSessions1` → `Whatsapp_SendMessage1`
  - `UpdateField1` → `Supabase_UpdateConversationSessions2` → `Whatsapp_SendMessage2`

**30. `IF_IsValid?` (for no-write path)**
- Checks `is_valid === true` from AI response
- **TRUE (valid response, no write needed) → `Supabase_UpdateConversationSessions`** → `Whatsapp_SendMessage`
- **FALSE (invalid/clarification needed) → `Supabase_UpdateConversationSession`** (with retry count increment) → `Merge2` → `Whatsapp_SendMessage`

#### Session Update Nodes (all three variants update the same fields):

**`Supabase_UpdateConversationSessions` / `...Sessions1` / `...Sessions2`**
- Updates: `session_state = next_state`, `expires_at = now + 24h`, `last_message = user_message`
- The retry-count variant also increments `retry_count += 1`

#### WhatsApp Send & Log Nodes:

**`Whatsapp_SendMessage` / `...Message1` / `...Message2`**
- Phone ID: `1018956984633375`
- Recipient: customer phone
- Body: `Code_ParseAIResponse.first().json.response_message`

**`Supabase_LogOutboundMessage` / `...Message1` / `...Message2`**
- Direction: `outbound`
- Logs the AI-generated response message

---

### Pipeline 3 — Document Intake & Verification

**Purpose:** When a customer sends a file (image or document) during the document collection phase, download it, analyse it with Gemini Vision for type detection and authenticity verification, store it in Google Drive, record metadata in Supabase, and inform the customer of what is still needed.

```
IF_Document Phase+MediaReceived? [TRUE]
    └─► HTTP_GetFile (fetch media URL from Meta Graph API)
            └─► HTTP_DownloadFile (download binary file)
                    └─► Gemini_AnalyzeDocument (Gemini Vision — document verification)
                            └─► Code_ParseAIResponse1
                                    └─► IF_IsValid?1
                                            ├─► [INVALID] → WhatsApp_InvalidDocumentRecieved
                                            └─► [VALID]   → GoogleDrive_SearchFolder
                                                                └─► Set_DocumentDetails
                                                                        └─► GoogleDrive_UploadFile
                                                                                └─► Supabase_SaveDocumentMetaData
                                                                                        └─► Supabase_GetRecievedDocuments
                                                                                                └─► Aggregate_ReceivedDocuments
                                                                                                        └─► AIAgent_AnalysePendingDocument
                                                                                                                └─► Code_ParseAIAgent
                                                                                                                        └─► IF_AllDocumentRecieved?
                                                                                                                                ├─► [ALL DONE] → Send message1 (congrats)
                                                                                                                                │                   → Supabase_LogOutboundMessage4
                                                                                                                                │                       → Supabase_UpdateSessionState (matching_in_progress)
                                                                                                                                │                           → WhatsApp_SendLenderWaitMSG
                                                                                                                                │                               → [Lender Matching Pipeline]
                                                                                                                                └─► [MISSING] → WhatApp_DocumentsMSG
                                                                                                                                                    → Supabase_LogOutboundMessage3
```

#### Node Details:

**31. `HTTP_GetFile`**
- URL: `https://graph.facebook.com/v19.0/{media_id}`
- Authorization: Bearer token (WhatsApp Business API token)
- Returns JSON with a `url` field pointing to the actual file

**32. `HTTP_DownloadFile`**
- URL: `$json.url` (from previous node)
- Authorization: Same Bearer token
- Response format: `file` (binary)
- Downloads the actual document/image as binary data

**33. `Gemini_AnalyzeDocument`**
- Type: `@n8n/n8n-nodes-langchain.googleGemini`
- Model: `models/gemini-2.5-pro`
- Input type: `binary` (the downloaded file)
- Input metadata passed in prompt: `media_mime_type`, `media_filename`
- Performs comprehensive document analysis:
  - **Document Type Detection** — 16 canonical types (aadhaar_card, pan_card_applicant, pan_card_business, bank_statement, salary_slip, form_16, itr, gst_registration_certificate, ca_audited_financials, business_existence_proof, property_agreement, property_documents, property_photos, stock_statement, loan_application_form, other)
  - **Authenticity Validation** — checks for: blurred/pixelated fonts, misaligned text, missing mandatory fields, signs of digital editing, placeholder data, wrong document type
  - **Confidence Assessment** — high / medium / low
- Returns structured JSON:
```json
{
  "isValid": boolean,
  "document_type": "canonical_type",
  "confidence": "high|medium|low",
  "reason": "one sentence",
  "flags": ["array of specific issues"]
}
```

**34. `Code_ParseAIResponse1`**
- Safely parses Gemini's response from `candidates[0].content.parts[0].text`
- Strips markdown fences
- Falls back to `{ isValid: false, document_type: "unknown", ... }` on failure
- Enforces all required fields exist

**35. `IF_IsValid?1`**
- Checks `$json.isValid === true`
- **FALSE → `WhatsApp_InvalidDocumentRecieved`**: Sends "document received is invalid ❌ Kindly upload the correct document" and stops
- **TRUE → `GoogleDrive_SearchFolder`**: Proceeds to storage

**36. `GoogleDrive_SearchFolder`**
- Searches Google Drive for the customer's folder
- Query: `{customer_name}_{phone}`
- Limit: 1 result
- Returns folder `id`

**37. `Set_DocumentDetails`**
- Prepares upload parameters:
  - `fileName` = `{document_type}_{customer_name}`
  - `file` = binary data from `HTTP_DownloadFile`
  - `folderID` = Drive folder ID from search

**38. `GoogleDrive_UploadFile`**
- Uploads the binary file to the customer's Drive folder
- Input field: `file`
- Folder: dynamic `folderID`

**39. `Supabase_SaveDocumentMetaData`**
- Table: `documents`
- Saves: application_id, customer_id, document_type, original_filename, stored_filename, google_drive_url, google_drive_file_id, google_drive_folder_id, mime_type, file_size_bytes, is_verified=`true`

**40. `Supabase_GetRecievedDocuments`**
- Table: `documents`
- Fetches ALL documents for this customer_id (returnAll: true)

**41. `Aggregate_ReceivedDocuments`**
- Aggregates the `document_type` field from all received document records into a single array field `Recieved Document`

**42. `AIAgent_AnalysePendingDocument`**
- Type: n8n AI Agent
- LLM: **Google Gemini 2.5 Pro**
- Prompt includes: total received documents, loan type, customer name, current document received
- System prompt contains the full required document list for all 5 loan types
- Compares received vs required documents
- Returns JSON with:

```json
{
  "loan_type": "",
  "customer_phone": "",
  "received_documents": [],
  "missing_documents": [],
  "all_documents_completed": false,
  "verification_status": "pending_documents",
  "next_state": "collecting_documents",
  "whatsapp_reply": "",
  "confidence": "high"
}
```

**43. `Code_ParseAIAgent`**
- Strips markdown, parses JSON
- Normalises all fields using type-safe helpers (`ensureArray`, `ensureBoolean`, `cleanString`)
- Adds `total_received_documents` and `total_missing_documents` count fields
- Adds `processed_at` timestamp

**44. `IF_AllDocumentRecieved?`**
- Checks `all_documents_completed === true`
- **TRUE (all docs received):**
  - `Send message1` — WhatsApp congratulations message
  - `Supabase_LogOutboundMessage4` — logs outbound
  - `Supabase_UpdateSessionState` — sets `session_state = matching_in_progress`
  - `WhatsApp_SendLenderWaitMSG` — "Hang tight, matching your profile with suitable lenders ✅ Your results will be ready in a few seconds!"
  - → **Lender Matching Pipeline begins**
- **FALSE (docs still missing):**
  - `WhatApp_DocumentsMSG` — sends the `whatsapp_reply` from AI (lists what's still needed)
  - `Supabase_LogOutboundMessage3` — logs outbound

---

### Pipeline 4 — Lender Matching (RAG)

**Purpose:** Once all documents are collected, perform a Retrieval-Augmented Generation search against a Pinecone vector database of lender policies to rank the best matching lenders for the customer's specific profile.

```
WhatsApp_SendLenderWaitMSG
    └─► Set_BuildQuery (assemble full customer profile)
            └─► Lender Matching Agent (RAG with Pinecone + Gemini 2.5 Pro)
                    └─► Code_ParseAIAgentOutput
                            └─► IF_MatchFound?
                                    ├─► [NO MATCH] → WhatsApp_MatchNotFoundMSG
                                    └─► [MATCH]    → Split_RankedLenders
                                                        └─► Supabase_StoreLenderMatches (per lender)
                                                                └─► Aggregate2
                                                                        └─► WhatsApp_SendLenderMatchingMSG
                                                                                └─► Supabase_LogOutboundMessage5
                                                                                        └─► Supabase_UpdateSessionState1 (results_sent)
```

#### Node Details:

**45. `Set_BuildQuery`**
- Assembles all customer and application fields into a clean flat object for the AI agent prompt:
  - `full_name`, `phone_number`, `loan_type`, `loan_amount`, `monthly_income`, `employment_type`, `cibil_score`, `city`, `business_vintage`, `annual_turnover`, `property_value`, `property_type`, `property_ownership`, `existing_bank`
- All fields default to `'null'` string if not present

**46. `Lender Matching Agent`**
- Type: n8n AI Agent with tool access
- Primary LLM: **Google Gemini 2.5 Pro**
- Fallback LLM: **Google Gemini 2.5 Flash**
- **Tool:** `lender_policy_search` (Pinecone vector store)
  - Index: `lender-documents`
  - Namespace: `$json.loan_type` (searches only within the relevant loan type namespace)
  - Embedding model: `models/gemini-embedding-001`
  - Mode: `retrieve-as-tool`
- **Agent behaviour:**
  1. Uses `lender_policy_search` tool with a full natural language query describing the customer's entire profile
  2. Retrieves lender policy documents from Pinecone
  3. Evaluates each lender against: loan type, loan amount range, CIBIL minimum, city coverage, employment type, income/turnover minimums, business vintage minimums
  4. Disqualifies non-matching lenders (explains why in `disqualified_summary`)
  5. Ranks qualifying lenders by: interest rate (lower = better), processing time (faster = better), profile headroom, special benefits
  6. Caps results at 5 lenders maximum
- **Output:**
```json
{
  "matches_found": true,
  "total_matches": 3,
  "ranked_lenders": [
    {
      "rank": 1,
      "lender_name": "...",
      "lender_id": "uuid",
      "match_score": 0.95,
      "interest_rate_range": "10.5% - 14%",
      "max_loan_eligible": "₹XX lakhs",
      "processing_time": "3-5 days",
      "reasons": ["...", "..."],
      "special_notes": "..."
    }
  ],
  "customer_friendly_message": "WhatsApp formatted message with *bold* and emojis",
  "disqualified_summary": "HDFC excluded: minimum CIBIL 750..."
}
```

**47. `Code_ParseAIAgentOutput`**
- Strips markdown, extracts JSON block
- Recursively converts `\\n` escape sequences to real newlines (important for WhatsApp formatting)
- Falls back to `{ error: true }` on parse failure

**48. `IF_MatchFound?`**
- Checks `matches_found === true`
- **FALSE → `WhatsApp_MatchNotFoundMSG`**: "No Matching Lenders were found ❌"
- **TRUE → `Split_RankedLenders`**

**49. `Split_RankedLenders`**
- Splits the `ranked_lenders` array so each lender becomes its own item
- Enables one Supabase insert per lender

**50. `Supabase_StoreLenderMatches`**
- Table: `lender_matches`
- Saves per lender: application_id, lender_name, match_score, rank, reasons, presented_to_customer=`true`

**51. `Aggregate2`**
- Re-aggregates all lender items back into a single item after saving
- Needed to send a single WhatsApp message (not one per lender)

**52. `WhatsApp_SendLenderMatchingMSG`**
- Sends the `customer_friendly_message` to the customer
- This message contains the ranked lender results in WhatsApp-friendly format

**53. `Supabase_LogOutboundMessage5`**
- Logs the lender matching message as outbound

**54. `Supabase_UpdateSessionState1`**
- Updates `session_state = results_sent`
- Future messages from this customer will now be handled by Phase 5

---

### Pipeline 5 — Post-Match & Advisor Notification

**Purpose:** After lender results are sent, handle the customer's follow-up (yes/no for advisor, questions), and if they request an advisor, send a rich HTML notification email to the DSA team.

```
Supabase_LogOutboundMessage (from Phase 2 output)
    └─► IF_AdvisorRequested?
            ├─► [NO - session != advisor_requested] → No Operation, do nothing
            └─► [YES - session == advisor_requested]
                    └─► Supabase_GetLenderMatches
                            └─► Aggregate_MatchedLenders
                                    └─► Set_RequiredParams
                                            └─► Agent_Prepare_Agent_Mail
                                                    └─► Code_ParseAgentOutput
                                                            └─► Gmail_SendMail
```

#### Node Details:

**55. `IF_AdvisorRequested?`**
- Checks if `Merge2.first().json.session_state === "advisor_requested"`
- This state is set by the Phase 5 AI agent when customer says YES to advisor
- **FALSE → `No Operation, do nothing`** (conversation continues normally)
- **TRUE → Advisor notification pipeline**

**56. `Supabase_GetLenderMatches`**
- Table: `lender_matches`
- Filter: `application_id = current application id`
- Fetches all matched lenders that were presented to the customer

**57. `Aggregate_MatchedLenders`**
- Aggregates all lender rows into a single `data` array

**58. `Set_RequiredParams`**
- Packages three objects together:
  - `customer_details` — from `Supabase_GetCustomerDetails`
  - `Loan_Application` — from `Supabase_GetLoanApplication`
  - `matched_lender` — the aggregated lenders array

**59. `Agent_Prepare_Agent_Mail`**
- Type: n8n AI Agent
- LLM: **Google Gemini 2.5 Pro**
- Generates a **rich HTML email** for the DSA/advisor team
- Email structure:
  - **Header** (navy #0D1B2A): eyebrow text, "Lender Match Notification" title, lender count badge
  - **Alert bar** (gold gradient): "New loan application ready for review — N lenders matched"
  - **Application Summary**: Application ID, Customer Name, Phone, Requested Amount, Purpose (2-column table)
  - **Matched Lenders section**: One card per lender with rank badge, lender name, match score (colour-coded badge + progress bar), notes
  - **Footer** (navy): workflow attribution
- Match score badge colours: green (≥90%), amber (70-89%), red (<70%)
- Output:
```json
{
  "subject": "Loan ₹X,XX,XXX – Application #ID – N Lenders Matched",
  "htmlBody": "<complete HTML string>"
}
```

**60. `Code_ParseAgentOutput`**
- Strips markdown, extracts JSON
- Returns `{ subject, htmlBody }`

**61. `Gmail_SendMail`**
- Sends to: `shreyashinde0926@gmail.com` (DSA/advisor team inbox)
- Subject: from `$json.subject`
- Message: from `$json.htmlBody` (full HTML)
- Attribution appended: false

---

## 5. Node-by-Node Reference

Complete inventory of all 70 nodes with their types and positions:

| # | Node Name | Type | Purpose |
|---|---|---|---|
| 1 | `Webhook_RecieveMessage` | Webhook | Entry point — receives WhatsApp webhook |
| 2 | `Code_ParseInput` | Code | Parse raw WhatsApp payload |
| 3 | `Supabase_LogConversation` | Supabase | Log inbound message |
| 4 | `Supabase_GetConversationState` | Supabase | Fetch existing session |
| 5 | `IF_SessionExists?` | IF | New vs returning customer |
| 6 | `Supabase_CreateCustomer` | Supabase | Create new customer record |
| 7 | `Supabase_CreateLoanApplication` | Supabase | Create skeleton loan application |
| 8 | `Supabase_CreateSession` | Supabase | Create conversation session |
| 9 | `GoogleDrive_CreateACustomerFolder` | Google Drive | Create customer document folder |
| 10 | `Merge1` | Merge | Reunite new + returning customer paths |
| 11 | `Supabase_Get10RecentMessages` | Supabase | Fetch conversation history |
| 12 | `Code_Fetch_Latest_10_MSG` | Code | Sort and slice to 10 most recent |
| 13 | `Aggregate` | Aggregate | Bundle messages into array |
| 14 | `Supabase_GetCustomerDetails` | Supabase | Fetch customer profile |
| 15 | `Supabase_GetLoanApplication` | Supabase | Fetch loan application data |
| 16 | `Supabase_GetSessionState` | Supabase | Fetch current session state |
| 17 | `Set_SessionState` | Set | Surface session_state field |
| 18 | `Code_DetectPhase` | Code | Map state → phase number |
| 19 | `IF_SkipAgent?` | IF | Skip agent for Phase 4 (RAG) |
| 20 | `IF_Document Phase+MediaReceived?` | IF | Route to doc pipeline |
| 21 | `Set_InternalParams` | Set | Prepare conversation pipeline params |
| 22 | `Code_SystemPromptSelector` | Code | Select phase system prompt + user prompt |
| 23 | `AI Agent for Conversations` | AI Agent | Main conversational AI |
| 24 | `Google Gemini Chat Model1` | Gemini LM | LLM for conversation agent |
| 25 | `Code_ParseAIResponse` | Code | Parse + clean AI JSON response |
| 26 | `IF_EscalatetoHuman?` | IF | Check escalation flag |
| 27 | `Code_DynamicFieldSaver` | Code | Determine which DB field to write |
| 28 | `IF_WriteNeeded?` | IF | Skip DB write if nothing extracted |
| 29 | `IF_DB_Id Exist?` | IF | Route to correct table |
| 30 | `Supabase_UpdateField` | Supabase | Dynamic update to loan_applications |
| 31 | `Supabase_UpdateField1` | Supabase | Dynamic update to customers |
| 32 | `Supabase_UpdateConversationSessions` | Supabase | Update state (valid path) |
| 33 | `Supabase_UpdateConversationSession` | Supabase | Update state + retry count (invalid) |
| 34 | `Supabase_UpdateConversationSessions1` | Supabase | Update state (write path 1) |
| 35 | `Supabase_UpdateConversationSessions2` | Supabase | Update state (write path 2) |
| 36 | `Merge2` | Merge | Reunite valid/invalid session update paths |
| 37 | `Whatsapp_SendMessage` | WhatsApp | Send reply (no-write valid path) |
| 38 | `Whatsapp_SendMessage1` | WhatsApp | Send reply (write path 1) |
| 39 | `Whatsapp_SendMessage2` | WhatsApp | Send reply (write path 2) |
| 40 | `Supabase_LogOutboundMessage` | Supabase | Log outbound (path 1) |
| 41 | `Supabase_LogOutboundMessage1` | Supabase | Log outbound (path 2) |
| 42 | `Supabase_LogOutboundMessage2` | Supabase | Log outbound (path 3) |
| 43 | `IF_AdvisorRequested?` | IF | Check if advisor was requested |
| 44 | `HTTP_GetFile` | HTTP Request | Get media URL from Meta API |
| 45 | `HTTP_DownloadFile` | HTTP Request | Download binary file |
| 46 | `Gemini_AnalyzeDocument` | Google Gemini | Vision-based document analysis |
| 47 | `Code_ParseAIResponse1` | Code | Parse Gemini document analysis |
| 48 | `IF_IsValid?1` | IF | Valid vs invalid document |
| 49 | `WhatsApp_InvalidDocumentRecieved` | WhatsApp | Notify invalid document |
| 50 | `GoogleDrive_SearchFolder` | Google Drive | Find customer folder |
| 51 | `Set_DocumentDetails` | Set | Prepare upload params |
| 52 | `GoogleDrive_UploadFile` | Google Drive | Upload document file |
| 53 | `Supabase_SaveDocumentMetaData` | Supabase | Save document metadata |
| 54 | `Supabase_GetRecievedDocuments` | Supabase | Fetch all received documents |
| 55 | `Aggregate_ReceivedDocuments` | Aggregate | Bundle received doc types |
| 56 | `AIAgent_AnalysePendingDocument` | AI Agent | Analyse pending vs required docs |
| 57 | `2.5-pro1` | Gemini LM | LLM for document analysis agent |
| 58 | `Code_ParseAIAgent` | Code | Parse document analysis response |
| 59 | `IF_AllDocumentRecieved?` | IF | All docs complete check |
| 60 | `Send message1` | WhatsApp | Congrats — all docs received |
| 61 | `Supabase_LogOutboundMessage4` | Supabase | Log outbound (docs complete) |
| 62 | `WhatApp_DocumentsMSG` | WhatsApp | Send missing docs reminder |
| 63 | `Supabase_LogOutboundMessage3` | Supabase | Log outbound (docs missing) |
| 64 | `Supabase_UpdateSessionState` | Supabase | Set state to matching_in_progress |
| 65 | `WhatsApp_SendLenderWaitMSG` | WhatsApp | "Matching in progress" message |
| 66 | `Set_BuildQuery` | Set | Assemble full customer profile |
| 67 | `Lender Matching Agent` | AI Agent | RAG lender matching |
| 68 | `2.5-pro` | Gemini LM | Primary LLM for lender agent |
| 69 | `2.5-flash` | Gemini LM | Fallback LLM for lender agent |
| 70 | `lender_policy_search tool` | Pinecone | Vector search tool |
| 71 | `gemini-embedding-001` | Gemini Embedding | Embedding model for Pinecone |
| 72 | `Code_ParseAIAgentOutput` | Code | Parse lender matching output |
| 73 | `IF_MatchFound?` | IF | Check if any lenders matched |
| 74 | `Split_RankedLenders` | Split Out | One item per matched lender |
| 75 | `Supabase_StoreLenderMatches` | Supabase | Save each lender match |
| 76 | `Aggregate2` | Aggregate | Re-aggregate for single message |
| 77 | `WhatsApp_SendLenderMatchingMSG` | WhatsApp | Send ranked lender results |
| 78 | `Supabase_LogOutboundMessage5` | Supabase | Log outbound (lender results) |
| 79 | `Supabase_UpdateSessionState1` | Supabase | Set state to results_sent |
| 80 | `Supabase_GetLenderMatches` | Supabase | Fetch lender matches for email |
| 81 | `Aggregate_MatchedLenders` | Aggregate | Bundle lender matches |
| 82 | `Set_RequiredParams` | Set | Package email input data |
| 83 | `Agent_Prepare_Agent_Mail` | AI Agent | Generate HTML email |
| 84 | `Google Gemini Chat Model` | Gemini LM | LLM for email agent |
| 85 | `Code_ParseAgentOutput` | Code | Parse email agent output |
| 86 | `Gmail_SendMail` | Gmail | Send advisor notification email |
| 87 | `No Operation, do nothing` | NoOp | Skip advisor path if not requested |
| 88 | `IF_IsValid?` | IF | Route valid vs invalid AI response |

---

## 6. AI Agent Architecture

The workflow uses **four distinct AI agents**, each with a specific scope:

### Agent 1: `AI Agent for Conversations`
- **Scope:** Phases 1, 2, and 5 — all text-based dialogue
- **Model:** Gemini 2.5 Pro (temperature 0.3)
- **Input:** system_prompt (phase-selected) + user_prompt (runtime context)
- **Output Schema:** `{ is_valid, extracted_field, extracted_value, next_state, response_message, needs_clarification, escalate_to_human, confidence }`
- **Responsibilities:** Greeting, name extraction, loan type mapping, financial data collection, field validation, post-match follow-up

### Agent 2: `Gemini_AnalyzeDocument`
- **Scope:** Single document visual analysis
- **Model:** Gemini 2.5 Pro (vision/multimodal)
- **Input:** Binary file + metadata (mime_type, filename)
- **Output Schema:** `{ isValid, document_type, confidence, reason, flags[] }`
- **Responsibilities:** Document type detection, authenticity verification, red flag identification

### Agent 3: `AIAgent_AnalysePendingDocument`
- **Scope:** Post-document-upload tracking
- **Model:** Gemini 2.5 Pro
- **Input:** Received documents list, loan type, customer name, current document
- **Output Schema:** `{ loan_type, customer_phone, received_documents[], missing_documents[], all_documents_completed, verification_status, next_state, whatsapp_reply, confidence }`
- **Responsibilities:** Comparing received vs required docs, generating WhatsApp reply, determining completion state

### Agent 4: `Lender Matching Agent`
- **Scope:** RAG-based lender selection
- **Model:** Gemini 2.5 Pro (primary) / Gemini 2.5 Flash (fallback)
- **Tool:** `lender_policy_search` (Pinecone vector store, loan_type namespace)
- **Embedding:** `gemini-embedding-001`
- **Input:** Full customer profile (all loan application fields)
- **Output Schema:** `{ matches_found, total_matches, ranked_lenders[], customer_friendly_message, disqualified_summary }`
- **Responsibilities:** Semantic policy search, eligibility filtering, ranking, WhatsApp message generation

### Agent 5: `Agent_Prepare_Agent_Mail`
- **Scope:** DSA advisor email generation
- **Model:** Gemini 2.5 Pro
- **Input:** customer_details + loan_application + matched_lenders[]
- **Output Schema:** `{ subject, htmlBody }`
- **Responsibilities:** Generating a professional, fully styled HTML email for the advisor team

---

## 7. Phase State Machine

The entire conversation is driven by a state machine stored in `conversation_sessions.session_state`.

```
                    ┌──────────────┐
  New Customer ────►│  new_user    │ (Phase 1)
                    └──────┬───────┘
                           │ name collected
                    ┌──────▼───────────┐
                    │awaiting_fullname  │ (Phase 1)
                    └──────┬────────────┘
                           │ loan type collected
                    ┌──────▼───────────┐
                    │awaiting_loan_type │ (Phase 1)
                    └──────┬────────────┘
                           │
                    ┌──────▼───────────────┐
                    │awaiting_loan_amount   │ (Phase 2)
                    └──────┬────────────────┘
                           │
                    ┌──────▼──────────────────────────────────────────────┐
                    │  [Loan-type-specific fields collected in sequence]   │ (Phase 2)
                    │  employment_type, monthly_income, business_vintage,  │
                    │  annual_turnover, property_value, property_type,     │
                    │  property_ownership, existing_bank, cibil_score      │
                    └──────┬──────────────────────────────────────────────┘
                           │ all fields collected
                    ┌──────▼───────────┐
                    │  awaiting_city   │ (Phase 2 — always last field)
                    └──────┬────────────┘
                           │
                    ┌──────▼──────────────────┐
                    │  awaiting_documents      │ (Phase 3)
                    └──────┬────────────────────┘
                           │
                    ┌──────▼──────────────────┐
                    │  collecting_documents    │ (Phase 3 — loops until complete)
                    └──────┬────────────────────┘
                           │ ambiguous doc
                    ┌──────▼────────────────────┐
                    │  doc_type_clarification   │ (Phase 3)
                    └──────┬─────────────────────┘
                           │
                           │ all mandatory docs received
                    ┌──────▼──────────────────────┐
                    │  matching_in_progress        │ (Phase 4 — RAG, no agent)
                    └──────┬───────────────────────┘
                           │ lender results sent
                    ┌──────▼──────────────────┐
                    │  results_sent            │ (Phase 5)
                    └──────┬────────────────────┘
                           │ customer says YES to advisor
                    ┌──────▼──────────────────┐
                    │  advisor_requested       │ (Phase 5 → triggers DSA email)
                    └──────┬────────────────────┘
                           │
                    ┌──────▼──────────────────┐
                    │  application_complete    │ (Phase 5 — terminal)
                    └─────────────────────────┘

  At any point if escalate_to_human = true:
                    ┌──────────────────────────┐
                    │  human_handoff /          │ (Phase 5)
                    │  escalated_to_human       │
                    └──────────────────────────┘
```

---

## 8. Data Flow Diagrams

### 8.1 — New Customer First Message Flow

```
WhatsApp message arrives
         │
         ▼
Code_ParseInput → extract phone, text, media
         │
         ▼
Supabase_LogConversation (inbound)
         │
         ▼
Supabase_GetConversationState → [no record returned]
         │
         ▼ (FALSE branch)
Supabase_CreateCustomer → {phone, source, is_active}
         │
         ▼
Supabase_CreateLoanApplication → {customer_id, loan_type=pending}
         │
         ▼
Supabase_CreateSession → {phone, state=new_user, application_id}
         │
         ▼
GoogleDrive_CreateACustomerFolder → /LoanApplications/{phone}/
         │
         ▼
Merge1 → [continues to context fetch]
         │
         ▼
[Fetch recent messages → Aggregate]
         │
         ▼
[Fetch customer → loan app → session state]
         │
         ▼
Code_DetectPhase → phase=1, skip_agent=false
         │
         ▼
IF_SkipAgent? → FALSE
         │
         ▼
IF_Document Phase+MediaReceived? → FALSE (text message)
         │
         ▼
Set_InternalParams
         │
         ▼
Code_SystemPromptSelector → Phase 1 system prompt + user prompt
         │
         ▼
AI Agent → "Hi [name based on time]! Welcome to LoanEase. What's your name?"
         │
         ▼
Code_ParseAIResponse → { next_state: "awaiting_fullname", response_message: ... }
         │
         ▼
IF_EscalatetoHuman? → FALSE
         │
         ▼
Code_DynamicFieldSaver → write_skipped=true (first message, no extraction yet)
         │
         ▼
IF_WriteNeeded? → FALSE
         │
         ▼
IF_IsValid? → TRUE
         │
         ▼
Supabase_UpdateConversationSessions → state=awaiting_fullname
         │
         ▼
Merge2 → Whatsapp_SendMessage → Supabase_LogOutboundMessage
```

### 8.2 — Document Upload Flow

```
Customer sends document image
         │
         ▼
Code_ParseInput → { media_id: "xxx", media_type: "image", message_type: "image" }
         │
         ▼
[Log, session fetch, context fetch, phase detect]
         │
         ▼
Code_DetectPhase → phase=3, skip_agent=false
         │
         ▼
IF_Document Phase+MediaReceived? → TRUE (phase=3 AND media_id not empty)
         │
         ▼
HTTP_GetFile → GET graph.facebook.com/v19.0/{media_id}
         │        Response: { url: "https://lookaside.fbsbx.com/..." }
         ▼
HTTP_DownloadFile → binary file data
         │
         ▼
Gemini_AnalyzeDocument (vision)
         │        → { isValid: true, document_type: "aadhaar_card", confidence: "high", ... }
         ▼
Code_ParseAIResponse1 → normalised JSON
         │
         ▼
IF_IsValid?1 → TRUE
         │
         ▼
GoogleDrive_SearchFolder → find /LoanApplications/{name}_{phone}/
         │
         ▼
Set_DocumentDetails → { fileName: "aadhaar_card_Rahul", file: <binary>, folderID: "abc" }
         │
         ▼
GoogleDrive_UploadFile → uploaded file object
         │
         ▼
Supabase_SaveDocumentMetaData → documents table record
         │
         ▼
Supabase_GetRecievedDocuments → [all docs for this customer]
         │
         ▼
Aggregate_ReceivedDocuments → { "Recieved Document": ["aadhaar_card", "pan_card"] }
         │
         ▼
AIAgent_AnalysePendingDocument
         │        → { missing_documents: ["salary_slip_3months", "bank_statement_6months"], all_documents_completed: false }
         ▼
Code_ParseAIAgent → normalised
         │
         ▼
IF_AllDocumentRecieved? → FALSE
         │
         ▼
WhatApp_DocumentsMSG → "Got your *Aadhaar Card* ✅\n\nStill need:\n1. Salary Slips\n2. Bank Statement"
         │
         ▼
Supabase_LogOutboundMessage3
```

### 8.3 — Lender Matching Flow

```
All documents received → IF_AllDocumentRecieved? TRUE
         │
         ▼
Send message1 → "Great! All documents received 🎉"
         │
         ▼
Supabase_UpdateSessionState → state=matching_in_progress
         │
         ▼
WhatsApp_SendLenderWaitMSG → "Hang tight, matching your profile with suitable lenders ✅"
         │
         ▼
Set_BuildQuery → { full_name, phone, loan_type, loan_amount, cibil_score, city, ... }
         │
         ▼
Lender Matching Agent
   ├── Calls lender_policy_search("business loan, ₹50L, CIBIL 750, Mumbai, 5yr vintage, ₹2Cr turnover")
   ├── Pinecone returns 10 policy documents from "business" namespace
   ├── Agent evaluates eligibility for each lender
   ├── Ranks top 5 by rate + processing time + fit
   └── Returns { ranked_lenders: [...], customer_friendly_message: "...", matches_found: true }
         │
         ▼
Code_ParseAIAgentOutput → clean JSON with real newlines
         │
         ▼
IF_MatchFound? → TRUE
         │
         ▼
Split_RankedLenders → [lender1, lender2, lender3] as separate items
         │
         ▼
Supabase_StoreLenderMatches → save each (loops per lender)
         │
         ▼
Aggregate2 → back to single item
         │
         ▼
WhatsApp_SendLenderMatchingMSG → rich ranked results to customer
         │
         ▼
Supabase_LogOutboundMessage5
         │
         ▼
Supabase_UpdateSessionState1 → state=results_sent
```

---

## 9. Error Handling & Fallback Strategy

### AI Output Parsing
Every AI node output is followed by a dedicated `Code_Parse*` node that:
1. Handles null/empty output
2. Strips markdown code fences
3. Extracts JSON using regex
4. Validates all required fields exist
5. Returns safe defaults on any failure

### Retry Logic (Phase 2)
- `retry_count` is stored in `conversation_sessions` and incremented by `Supabase_UpdateConversationSession`
- AI system prompt instructs:
  - retry 0-1: rephrase question differently, give an example
  - retry 2: simplify drastically, offer to skip with a default
  - retry 3+: set `escalate_to_human = true`

### Session Timeout
- Every session update sets `expires_at = now + 24 hours`
- Sessions are effectively kept alive indefinitely as long as the customer messages within 24 hours

### Invalid Documents
- `Gemini_AnalyzeDocument` returns `isValid: false` with detailed flags
- `WhatsApp_InvalidDocumentRecieved` immediately notifies the customer
- The session state remains in `collecting_documents` — the customer can retry

### No Lender Match
- `IF_MatchFound?` routes to `WhatsApp_MatchNotFoundMSG` with a friendly message
- No crash — flow terminates gracefully

### Human Escalation
- If `escalate_to_human === true` from any AI agent turn:
  - `IF_EscalatetoHuman?` exits the write/send pipeline silently
  - The Phase 5 system prompt for `human_handoff` state will pick up the next message

---

## 10. Security & Credential Map

| Credential | Type | Used By |
|---|---|---|
| `Whatsapp Lender Matching System` | Supabase API | All Supabase nodes |
| `GDrive: fortiv.test03` | Google Drive OAuth2 | GoogleDrive_CreateACustomerFolder, GoogleDrive_SearchFolder, GoogleDrive_UploadFile |
| `Google Gemini(PaLM) Api account 3` | Google PaLM API | All Gemini models (chat, vision, embedding) |
| `WhatsApp account` | WhatsApp Business API | All WhatsApp send nodes |
| `lender-documents API` | Pinecone API | lender_policy_search tool |
| `fortiv.test03 Proj: fortiv-test-1` | Gmail OAuth2 | Gmail_SendMail |
| *(Hardcoded in HTTP nodes)* | Bearer Token | HTTP_GetFile, HTTP_DownloadFile (Meta Graph API) |

> ⚠️ **Note:** The Meta Graph API Bearer token is hardcoded directly in the `HTTP_GetFile` and `HTTP_DownloadFile` nodes. This should be moved to an n8n credential for production security.

---

## 11. Complete Node Inventory

### Trigger Nodes (1)
| Node | Webhook Path |
|---|---|
| `Webhook_RecieveMessage` | `c82e412e-58b9-42cd-b871-f68912841ed0` |

### Code Nodes (10)
| Node | Purpose |
|---|---|
| `Code_ParseInput` | WhatsApp payload normalisation |
| `Code_Fetch_Latest_10_MSG` | Sort + slice message history |
| `Code_DetectPhase` | State → phase mapping |
| `Code_SystemPromptSelector` | AI prompt builder |
| `Code_ParseAIResponse` | Parse conversation AI JSON |
| `Code_ParseAIResponse1` | Parse document vision AI JSON |
| `Code_DynamicFieldSaver` | Determine DB write target |
| `Code_ParseAIAgent` | Parse document tracking AI JSON |
| `Code_ParseAIAgentOutput` | Parse lender matching AI JSON |
| `Code_ParseAgentOutput` | Parse email generation AI JSON |

### IF (Conditional) Nodes (10)
| Node | Condition |
|---|---|
| `IF_SessionExists?` | `$json.id` exists |
| `IF_SkipAgent?` | `skip_agent === true` |
| `IF_Document Phase+MediaReceived?` | `phase===3 AND media_id not empty` |
| `IF_EscalatetoHuman?` | `escalate_to_human === true` |
| `IF_WriteNeeded?` | `write_skipped === false` |
| `IF_DB_Id Exist?` | `db_id` exists |
| `IF_IsValid?` | `is_valid === true` |
| `IF_IsValid?1` | `isValid === true` |
| `IF_AllDocumentRecieved?` | `all_documents_completed === true` |
| `IF_MatchFound?` | `matches_found === true` |
| `IF_AdvisorRequested?` | `session_state === advisor_requested` |

### Supabase Nodes (22)
| Node | Table | Operation |
|---|---|---|
| `Supabase_LogConversation` | conversation_logs | Create |
| `Supabase_GetConversationState` | conversation_sessions | Get |
| `Supabase_CreateCustomer` | customers | Create |
| `Supabase_CreateLoanApplication` | loan_applications | Create |
| `Supabase_CreateSession` | conversation_sessions | Create |
| `Supabase_Get10RecentMessages` | conversation_logs | Get All |
| `Supabase_GetCustomerDetails` | customers | Get |
| `Supabase_GetLoanApplication` | loan_applications | Get |
| `Supabase_GetSessionState` | conversation_sessions | Get |
| `Supabase_UpdateConversationSessions` | conversation_sessions | Update |
| `Supabase_UpdateConversationSession` | conversation_sessions | Update (+ retry) |
| `Supabase_UpdateConversationSessions1` | conversation_sessions | Update |
| `Supabase_UpdateConversationSessions2` | conversation_sessions | Update |
| `Supabase_UpdateField` | loan_applications | Update (dynamic) |
| `Supabase_UpdateField1` | customers | Update (dynamic) |
| `Supabase_LogOutboundMessage` | conversation_logs | Create |
| `Supabase_LogOutboundMessage1` | conversation_logs | Create |
| `Supabase_LogOutboundMessage2` | conversation_logs | Create |
| `Supabase_LogOutboundMessage3` | conversation_logs | Create |
| `Supabase_LogOutboundMessage4` | conversation_logs | Create |
| `Supabase_LogOutboundMessage5` | conversation_logs | Create |
| `Supabase_SaveDocumentMetaData` | documents | Create |
| `Supabase_GetRecievedDocuments` | documents | Get All |
| `Supabase_GetLenderMatches` | lender_matches | Get All |
| `Supabase_StoreLenderMatches` | lender_matches | Create |
| `Supabase_UpdateSessionState` | conversation_sessions | Update |
| `Supabase_UpdateSessionState1` | conversation_sessions | Update |

### WhatsApp Nodes (9)
| Node | Purpose |
|---|---|
| `Whatsapp_SendMessage` | Conversational reply (no-write valid) |
| `Whatsapp_SendMessage1` | Conversational reply (write path 1) |
| `Whatsapp_SendMessage2` | Conversational reply (write path 2) |
| `WhatsApp_InvalidDocumentRecieved` | Invalid document notification |
| `Send message1` | All documents received congrats |
| `WhatApp_DocumentsMSG` | Missing documents reminder |
| `WhatsApp_SendLenderWaitMSG` | "Matching in progress" notification |
| `WhatsApp_SendLenderMatchingMSG` | Ranked lender results |
| `WhatsApp_MatchNotFoundMSG` | No match found notification |

### AI / LLM Nodes (8)
| Node | Model | Role |
|---|---|---|
| `AI Agent for Conversations` | Gemini 2.5 Pro | Conversational phases 1, 2, 5 |
| `Google Gemini Chat Model1` | Gemini 2.5 Pro | LLM sub-node for conversation agent |
| `Gemini_AnalyzeDocument` | Gemini 2.5 Pro (Vision) | Document verification |
| `AIAgent_AnalysePendingDocument` | Gemini 2.5 Pro | Document tracking |
| `2.5-pro1` | Gemini 2.5 Pro | LLM for doc tracking agent |
| `Lender Matching Agent` | Gemini 2.5 Pro / Flash | RAG lender matching |
| `2.5-pro` | Gemini 2.5 Pro | Primary LLM for lender agent |
| `2.5-flash` | Gemini 2.5 Flash | Fallback LLM for lender agent |
| `Agent_Prepare_Agent_Mail` | Gemini 2.5 Pro | HTML email generation |
| `Google Gemini Chat Model` | Gemini 2.5 Pro | LLM for email agent |

### Google Drive Nodes (3)
| Node | Operation |
|---|---|
| `GoogleDrive_CreateACustomerFolder` | Create folder |
| `GoogleDrive_SearchFolder` | Search folder |
| `GoogleDrive_UploadFile` | Upload file |

### HTTP Request Nodes (2)
| Node | URL |
|---|---|
| `HTTP_GetFile` | `graph.facebook.com/v19.0/{media_id}` |
| `HTTP_DownloadFile` | Dynamic URL from GetFile response |

### Utility Nodes
| Node | Type | Purpose |
|---|---|---|
| `Merge1` | Merge | Reunite session paths |
| `Merge2` | Merge | Reunite valid/invalid AI paths |
| `Aggregate` | Aggregate | Bundle recent messages |
| `Aggregate_ReceivedDocuments` | Aggregate | Bundle received doc types |
| `Aggregate_MatchedLenders` | Aggregate | Bundle matched lenders |
| `Aggregate2` | Aggregate | Re-aggregate after per-lender saves |
| `Set_SessionState` | Set | Surface session_state |
| `Set_InternalParams` | Set | Prepare conversation params |
| `Set_DocumentDetails` | Set | Prepare upload params |
| `Set_BuildQuery` | Set | Assemble customer profile |
| `Set_RequiredParams` | Set | Package email inputs |
| `Split_RankedLenders` | Split Out | One item per lender |
| `No Operation, do nothing` | NoOp | Skip advisor path |
| `lender_policy_search tool` | Pinecone Vector Store | RAG tool |
| `gemini-embedding-001` | Gemini Embedding | Pinecone embeddings |
| `Gmail_SendMail` | Gmail | DSA advisor email |

---

*Document generated from n8n workflow JSON — LoanEase Customer Bot*
*Workflow Version ID: `b9089ddf-7026-4d06-a1f9-76b49fae3366`*