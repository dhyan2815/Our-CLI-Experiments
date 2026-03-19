# Comprehensive Guide: Connecting n8n Instance-Level MCP to AI CLIs

This guide explains how to connect your n8n instance-level MCP server to AI CLI tools like **Claude Code** and **Gemini CLI**.

---

## 1. Prerequisites

- **n8n Version:** Ensure you are running n8n version `1.72.0` or later.
- **Admin Access:** You must have Owner or Admin permissions on your n8n instance.
- **Node.js:** Installed on your local machine (required for `npx`).

---

## 2. Enable MCP in n8n

Before connecting, you must enable the MCP server at the instance level.

1.  **Open n8n:** Go to your n8n dashboard.
2.  **Navigate to Settings:** Go to **Settings > Instance-level MCP**.
3.  **Toggle Enable:** Turn on the **Enable MCP access** toggle.
4.  **Expose Workflows:** 
    - Workflows are **not** exposed by default.
    - Go to your workflow list or individual workflow settings.
    - Look for the **MCP Access** toggle and enable it for each workflow you want the AI to see.
    - *Note:* Workflows must be **published** and have a supported trigger (Webhook, Schedule, Chat, or Form).

---

## 3. Get Connection Details

1.  Go back to **Settings > Instance-level MCP**.
2.  Click on **Connection Details**.
3.  **Access Token:** Select the **Access Token** tab.
    - Copy your **Personal MCP Access Token**. 
    - *Warning:* This is only shown once. Save it securely.
4.  **Server URL:** Note your instance's MCP endpoint:
    - `https://<your-n8n-domain>/mcp-server/http`

---

## 4. Connecting to Claude Code CLI

Claude Code uses a built-in command to add MCP servers.

### Command Syntax:
Run the following in your terminal:

```bash
claude mcp add n8n-mcp --transport http https://<your-n8n-domain>/mcp-server/http --header "Authorization: Bearer <YOUR_N8N_MCP_TOKEN>"
```

### Verification:
After adding, you can verify it's active by running:
```bash
claude mcp list
```

---

## 5. Connecting to Gemini CLI

Gemini CLI uses a `settings.json` or equivalent configuration (check your local `~/.gemini/config.json` or use the CLI flags).

### Using `npx supergateway` (Recommended)
Gemini CLI often interacts with MCP servers via a proxy if direct HTTP support is not native for all versions.

1.  **Configuration:**
    Add the following to your MCP server configuration:

    ```json
    {
      "mcpServers": {
        "n8n": {
          "command": "npx",
          "args": [
            "-y", "supergateway",
            "--streamableHttp", "https://<your-n8n-domain>/mcp-server/http",
            "--header", "authorization:Bearer <YOUR_N8N_MCP_TOKEN>"
          ]
        }
      }
    }
    ```

2.  **Interactive Addition:**
    If using the Gemini interactive mode, you can often pass the server as a flag:
    ```bash
    gemini --mcp-server "npx -y supergateway --streamableHttp https://<your-n8n-domain>/mcp-server/http --header 'authorization:Bearer <YOUR_N8N_MCP_TOKEN>'"
    ```

---

## 6. Security Best Practices

- **Token Rotation:** If your token is compromised, rotate it immediately in n8n under **Settings > Instance-level MCP > Connection Details**.
- **Granular Access:** Only enable MCP access for workflows that are necessary for the AI's tasks.
- **Environment Variables:** For self-hosted instances, you can use `N8N_DISABLED_MODULES=mcp` to completely hide the feature if not in use.

---

## 7. Troubleshooting

- **401 Unauthorized:** Double-check your Bearer Token and ensure it has no extra spaces.
- **Workflow Not Found:** Ensure the workflow is **Published** and the **MCP Access** toggle is ON for that specific workflow.
- **SSE Connection Timeout:** Ensure your n8n instance is publicly accessible or reachable from your CLI's network environment.

---

## 8. Starter Guide: Using n8n MCP for Productivity

This section walks you from basic usage to intermediate automation patterns.

### 8.1 Understanding What You Can Do

The n8n MCP allows AI assistants to:
- **List & discover** workflows in your n8n instance
- **Execute** workflows on-demand (with triggers: webhook, schedule, chat, form)
- **Create** new workflows programmatically
- **Update** existing workflows
- **Manage** executions and versions

### 8.2 Basic Usage Patterns

#### Pattern 1: Trigger Workflows On-Demand

The most common use case: ask AI to run a workflow for you.

**Example prompts:**
- "Run my 'Daily Report' workflow"
- "Execute the Slack notification workflow with input: {data}"
- "Trigger the data sync workflow"

**Prerequisites:**
- Workflow must have a supported trigger: Webhook, Chat, Form, or Schedule
- Workflow must be **Published**
- Workflow must have **MCP Access** enabled

#### Pattern 2: Discover Existing Workflows

**Example prompts:**
- "List all my n8n workflows"
- "Find workflows related to Slack"
- "Show me workflows that have webhooks"

#### Pattern 3: Check Execution Status

**Example prompts:**
- "What's the status of my last workflow execution?"
- "Show me recent failed executions"
- "Get execution details for workflow ID XYZ"

### 8.3 Intermediate Workflows for Productivity

#### Workflow 1: Automated Status Reports

**Setup:**
1. Create a workflow with a Chat trigger
2. Add nodes to gather data (HTTP Request, HTTP Call to Self)
3. Format response and send via Slack/Email

**Usage:**
```
User: "Give me today's sales report"
AI executes: Your workflow → gathers data → returns formatted report
```

#### Workflow 2: One-Click Data Operations

**Setup:**
1. Create workflows that accept webhook data
2. Include CRUD operations: create records, update sheets, etc.

**Usage:**
```
User: "Create a new row in my tracking spreadsheet with: task=X, priority=high"
AI executes: Your webhook workflow with the data
```

#### Workflow 3: Scheduled Monitoring

**Setup:**
1. Keep schedule-triggered workflows for monitoring
2. Use MCP to check their status or manually trigger them

**Usage:**
```
User: "Run the hourly health check now"
AI executes: Your monitoring workflow immediately
```

#### Workflow 4: Multi-Step Automation Chains

**Setup:**
1. Create modular workflows (workflow A → calls workflow B)
2. Use HTTP Request node to call other workflows via webhooks
3. Chain multiple operations together

**Usage:**
```
User: "Process this lead: {email}"
AI executes: Workflow A (validate) → Workflow B (enrich) → Workflow C (notify)
```

### 8.4 Professional Productivity Tips

#### Tip 1: Design Workflows for MCP

- **Chat-trigger workflows** are best for interactive AI usage
- **Webhook workflows** accept structured data from AI
- Keep workflows **single-purpose** (easier to invoke and debug)
- Use **consistent naming** (e.g., `mcp:report:daily`, `mcp:lead:process`)

#### Tip 2: Use Parameters Effectively

Pass data to workflows via:

| Method | How | Use Case |
|--------|-----|----------|
| Webhook body | Pass JSON in request | Structured data |
| Chat input | Use Chat trigger fields | Interactive prompts |
| Form fields | Form trigger fields | Structured forms |

**Example webhook payload:**
```json
{
  "action": "create_task",
  "data": {
    "title": "Review PR",
    "priority": "high",
    "assignee": "dhyan"
  }
}
```

#### Tip 3: Error Handling & Monitoring

- Enable **error workflows** in n8n settings
- Use MCP to quickly check: "Show me recent errors"
- Keep execution history for debugging

#### Tip 4: Version Management

- MCP can manage workflow versions
- Use version rollback for safe changes
- Check: "Show me previous versions of workflow X"

### 8.5 Example Prompt Library

Here are productivity prompts you can use:

**Quick Actions:**
- "Execute my daily standup workflow"
- "Run the backup workflow now"
- "Trigger the weekly report generation"

**Data Operations:**
- "Send this data to my tracking spreadsheet"
- "Create a new item in my CRM"
- "Update the status in my project tracker"

**Monitoring & Status:**
- "What's the current status of my automation workflows?"
- "Show me execution history for today"
- "Any failed workflows in the last hour?"

**Discovery:**
- "What workflows do I have for Slack integration?"
- "Find workflows that process webhooks"
- "List all active workflows"

**Management:**
- "Enable MCP access on workflow X"
- "Update workflow Y with new webhook URL"
- "Show me the structure of workflow Z"

### 8.6 Building Your Automation Stack

**Recommended workflow categories for productivity:**

1. **Reporting** - Daily/weekly automated reports
2. **Notifications** - Alerts, reminders, updates
3. **Data Sync** - Keep systems in sync
4. **Processing** - Data transformation, enrichment
5. **Monitoring** - Health checks, uptime monitoring
6. **On-demand Actions** - Triggered by AI requests

**Tips for stacking:**
- Start with 3-5 core workflows
- Add more as you discover needs
- Keep a "meta-workflow" that lists all your MCP-enabled workflows

### 8.7 Security & Best Practices

- **Least Privilege:** Only enable MCP on workflows the AI needs
- **Input Validation:** Validate all AI-provided inputs in workflows
- **Rate Limiting:** Be mindful of workflow execution limits
- **Audit Logs:** Review execution history regularly
- **Token Management:** Rotate tokens periodically

---

## 9. Quick Reference Card

| Task | MCP Tool | Example Prompt |
|------|----------|----------------|
| List workflows | `n8n_list_workflows` | "List my workflows" |
| Execute workflow | `execute_workflow` | "Run workflow X" |
| Search nodes | `search_nodes` | "Find email nodes" |
| Find templates | `search_templates` | "Find Slack templates" |
| Check health | `n8n_health_check` | "Is n8n connected?" |
| Validate workflow | `validate_workflow` | "Check workflow for errors" |

---

*Reference: [Official n8n Documentation](https://docs.n8n.io/advanced-ai/accessing-n8n-mcp-server/)*
