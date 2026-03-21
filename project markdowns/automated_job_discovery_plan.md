# Plan: n8n Automated Job Discovery Agent

This document provides a step-by-step guide to building an n8n workflow that automatically finds relevant job opportunities, filters them using AI based on your resume, and adds matches to your Notion tracker while notifying you on Telegram.

## Workflow Overview

**Goal:** Proactively find and filter job/internship opportunities in India.
**Source:** LinkedIn Job Search RSS Feed.
**Core Logic:**
1.  Run on a schedule.
2.  Fetch new job listings from LinkedIn.
3.  For each job, extract the full description.
4.  Use an AI agent to compare the job description against your resume.
5.  If it's a good match, add it to Notion and send a Telegram alert.

---

## Node-by-Node Implementation Guide

### Step 1: Schedule the Workflow (Cron Node)

This node will trigger your workflow automatically.

-   **Node:** `Cron`
-   **Purpose:** To run the job search process on a recurring schedule.
-   **Reference:** [Cron Node Docs](https://docs.n8n.io/nodes/n8n-nodes-base.cron/)

**Configuration:**
-   **Mode:** `Every X`
-   **Interval:** `Hours`
-   **Amount:** `4` (or your preferred frequency; every 4 hours is a good balance).

---

### Step 2: Fetch Job Listings (RSS Feed Read Node)

This node will pull the latest job postings from a LinkedIn search.

-   **Node:** `RSS Feed Read`
-   **Purpose:** To get a list of recent job postings matching your criteria.
-   **Reference:** [RSS Feed Read Node Docs](https://docs.n8n.io/nodes/n8n-nodes-base.rssFeedRead/)

**How to get the LinkedIn RSS URL:**
1.  Go to LinkedIn and perform a detailed job search. Use filters for location (e.g., "India", "Bengaluru"), title (e.g., "AI Engineer Intern", "Automation Developer"), and experience level.
2.  Copy the URL from your browser's address bar.
3.  Go to a service like [rss.app](https://rss.app/) and paste the LinkedIn URL to generate a public RSS feed URL.
4.  Copy the generated RSS feed URL.

**Configuration:**
-   **URL:** Paste the RSS feed URL you generated.

---

### Step 3: Process Each Job Individually (Split in Batches Node)

This node ensures that each job from the RSS feed is handled one at a time.

-   **Node:** `Split in Batches`
-   **Purpose:** To loop through each job listing from the RSS feed.
-   **Reference:** [Split in Batches Node Docs](https://docs.n8n.io/nodes/n8n-nodes-base.splitInBatches/)

**Configuration:**
-   **Batch Size:** `1`
-   **Options -> No Items Behavior:** Check `Continue`.

---

### Step 4: Get Full Job Description (HTTP Request Node)

This node will visit the job link from the RSS feed to get the full page content.

-   **Node:** `HTTP Request`
-   **Purpose:** To fetch the HTML content of the job posting page.
-   **Reference:** [HTTP Request Node Docs](https://docs.n8n.io/nodes/n8n-nodes-base.httpRequest/)

**Configuration:**
-   **URL:** `{{ $json.link }}` (This expression pulls the job link from the RSS item).
-   **Options -> Response Format:** `HTML`
-   **Options -> Headers -> Add Header:**
    -   **Name:** `User-Agent`
    -   **Value:** `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36` (This helps avoid being blocked).

---

### Step 5: Extract Job Description Text (HTML Extract Node)

This node will parse the HTML from the previous step to isolate the job description.

-   **Node:** `HTML Extract`
-   **Purpose:** To pull only the relevant job description text from the page's HTML.
-   **Reference:** [HTML Extract Node Docs](https://docs.n8n.io/nodes/n8n-nodes-base.htmlExtract/)

**How to find the CSS Selector:**
1.  Open a sample job page from your search in your browser.
2.  Right-click on the main job description text and select "Inspect".
3.  In the developer tools, find the `div` or `section` that contains the description. Look for a unique class name like `description__text` or `jobs-description`.
4.  Copy the CSS selector for that element.

**Configuration:**
-   **Source Data:** `Use Input from Another Node`
-   **Input Field:** `body`
-   **Extraction Values -> Add Value:**
    -   **CSS Selector:** Paste the selector you found (e.g., `.description__text` or `.jobs-description`).
    -   **Return Value:** `Text`
    -   **Key:** `jobDescription`

---

### Step 6: Store Your Resume (Code Node)

This node will hold your resume text so the AI can use it for comparison.

-   **Node:** `Code`
-   **Purpose:** To provide your resume content to the workflow.
-   **Reference:** [Code Node Docs](https://docs.n8n.io/nodes/n8n-nodes-base.code/)

**Configuration:**
-   **JavaScript:**
    ```javascript
    const resume = `
    PASTE YOUR FULL RESUME TEXT HERE.
    - Include your skills (e.g., Python, n8n, LangChain).
    - Include your experience (e.g., AI Automation Intern at Fortiv Solution).
    - Include your education and projects.
    `;
    return [{ json: { resume: resume } }];
    ```

---

### Step 7: AI-Powered Resume Matching (AI Agent Node)

This is the brain of the operation. It will decide if the job is a match.

-   **Node:** `AI Agent` (or your preferred LLM node)
-   **Purpose:** To analyze the job description against your resume and determine if it's a suitable match.
-   **Reference:** [AI Agent Node Docs](https://docs.n8n.io/nodes/n8n-nodes-langchain.agent/)

**Configuration:**
-   **Connect your preferred LLM** (e.g., Google Gemini, OpenAI, or via OpenRouter).
-   **Input:**
    -   **User Message:**
        ```
        Job Title: {{ $('Split in Batches').item.json.title }}
        Job Description: {{ $('HTML Extract').item.json.jobDescription }}
        ---
        My Resume: {{ $('Store Your Resume').item.json.resume }}
        ```
-   **System Message / Prompt:**
    ```
    You are an expert technical recruiter based in India. Your task is to evaluate if the provided job description is a strong match for the candidate's resume.

    The candidate is seeking an internship or a junior/fresher-level full-time role in AI, Automation, or Software Development.

    CRITERIA:
    1.  **Role Type:** Must be an "Internship" or a "Full-time" role suitable for a fresher or someone with less than 1 year of experience.
    2.  **Skills Match:** The required skills in the job description should significantly overlap with the skills listed on the resume (e.g., Python, n8n, AI/ML concepts).
    3.  **Domain:** The role should be in AI, Machine Learning, Automation, or a related software engineering field.

    Based on your analysis, respond with ONLY a JSON object containing three keys:
    1.  "isMatch": A boolean (true or false).
    2.  "reason": A concise, one-sentence explanation for your decision.
    3.  "jobTitle": The original job title from the RSS feed.
    ```
-   **Options:** Make sure your model is configured to output JSON if it has a specific JSON mode.

---

### Step 8: Decide if it's a Match (IF Node)

This node routes the workflow based on the AI's decision.

-   **Node:** `IF`
-   **Purpose:** To proceed only if the AI agent flags the job as a match.
-   **Reference:** [IF Node Docs](https://docs.n8n.io/nodes/n8n-nodes-base.if/)

**Configuration:**
-   **Add Condition -> Boolean:**
    -   **Value 1:** `{{ $('AI-Powered Resume Matching').item.json.isMatch }}`
    -   **Operation:** `is True`

---

### Step 9A: Add to Tracker (Notion Node)

This executes on the `true` path of the IF node.

-   **Node:** `Notion`
-   **Purpose:** To automatically log the matched job in your Notion database.
-   **Reference:** [Notion Node Docs](https://docs.n8n.io/nodes/n8n-nodes-base.notion/)

**Configuration:**
-   **Authentication:** Connect your Notion account.
-   **Resource:** `Database Page`
-   **Operation:** `Create`
-   **Database ID:** Select your "Job Applications Tracker" database.
-   **Map Fields:** Map the data from the previous nodes to your Notion columns:
    -   **Company:** `{{ $('Split in Batches').item.json.creator }}`
    -   **Position:** `{{ $('Split in Batches').item.json.title }}`
    -   **Status:** Set to `Discovered` (or your preferred initial status).
    -   **URL:** `{{ $('Split in Batches').item.json.link }}`
    -   **Notes:** `AI Analysis: {{ $('AI-Powered Resume Matching').item.json.reason }}`

---

### Step 9B: Send Telegram Alert (Telegram Node)

This also executes on the `true` path of the IF node.

-   **Node:** `Telegram`
-   **Purpose:** To send you an instant notification about the new opportunity.
-   **Reference:** [Telegram Node Docs](https://docs.n8n.io/nodes/n8n-nodes-base.telegram/)

**Configuration:**
-   **Authentication:** Connect your Telegram Bot credentials.
-   **Chat ID:** Your personal Telegram Chat ID.
-   **Text:**
    ```
    <b>🔥 New Job Match!</b>

    <b>Position:</b> {{ $('Split in Batches').item.json.title }}
    <b>Company:</b> {{ $('Split in Batches').item.json.creator }}

    <b>AI Reason:</b> <i>{{ $('AI-Powered Resume Matching').item.json.reason }}</i>

    <a href="{{ $('Split in Batches').item.json.link }}">Apply Here</a>
    ```
-   **Options -> Parse Mode:** `HTML`
