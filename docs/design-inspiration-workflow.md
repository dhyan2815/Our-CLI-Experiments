**WORKFLOW**

**Stop Wasting Tokens on Raw HTML**

Set up [TinyFish](https://www.tinyfish.ai/?utm_source=instagram&utm_medium=paid-social&utm_campaign=newapis-developer-2026q2&utm_term=sukhad) to give your AI agent clean web context in under 5 minutes.

by techie007

# **The Problem**

If you’re using Cursor, Claude Code, or OpenClaw to interact with the live web, the native fetch tools dump thousands of lines of useless markup — CSS, navbars, ads, cookie banners — directly into your context window.

The result: blown token budgets, hallucinated outputs, and agents that fail halfway through complex web workflows.

And the second a site throws a Cloudflare challenge or bot detection? Your Playwright scripts are dead.

# **The Fix: [TinyFish](https://www.tinyfish.ai/?utm_source=instagram&utm_medium=paid-social&utm_campaign=newapis-developer-2026q2&utm_term=sukhad)**

TinyFish is a unified infrastructure platform for AI agents that handles web access properly. Instead of dumping raw HTML, it:

* Spins up a stealth cloud browser (sub-250ms cold start)

* Bypasses anti-bot systems automatically

* Strips the garbage and pipes clean Markdown/JSON straight to your filesystem

**⚡**  87% fewer tokens per operation. Clean context. Agents that actually complete.

# **Step-by-Step Setup**

**Step 1 —-** Go To [TinyFish](https://www.tinyfish.ai/?utm_source=instagram&utm_medium=paid-social&utm_campaign=newapis-developer-2026q2&utm_term=sukhad) and create an account.

## **Step 2 — Install the CLI**

```
npm install \-g @tiny-fish/cli
```

Verify the installation:

```
tinyfish \--version
```

## **Step 2 — Authenticate**

tinyfish auth login

This opens the API keys page in your browser. Paste your key when prompted. The key gets saved to \~/.tinyfish/config.json.

For CI/CD environments, pipe the key directly:

```
echo $TINYFISH\_API\_KEY | tinyfish auth set
```

Check your auth status anytime:

```
tinyfish auth status
```

## **Step 3 — Add the Skill to Your Agent**

If you’re using Claude Code or any agent that supports Skills, grab the TinyFish Skill file:

**Skill file:** github.com/tinyfish-io/tinyfish-cookbook/blob/main/skills/use-tinyfish/SKILL.md

Drop this into your project’s skills directory. Your agent now knows when and how to call TinyFish.

# **Pick the Right Tool**

TinyFish has four tools. Start with the lightest one that gets the job done, and escalate only when needed:

**search  →  fetch  →  agent  →  browser**

lightest                                                          heaviest

| Tool | When to Use | Speed |
| :---- | :---- | :---- |
| **search** | Find URLs or get quick answers about a topic | Fastest |
| **fetch** | You have URLs and need their clean content (articles, docs, product pages) | Fast |
| **agent** | Interact with a page — click, fill forms, navigate, extract structured data | Slower |
| **browser** | Raw programmatic browser control via CDP when agent isn’t enough | Slowest |

# **Common Patterns**

## **Pattern 1: Research (search → fetch)**

Search for a topic, then fetch the best results to read full content.

```
tinyfish search query "best React state management libraries 2026"

tinyfish fetch content get \--format markdown "https://result1.com" "https://result2.com"
```

## **Pattern 2: Deep Extraction (search → agent)**

Search to find the right site, then use agent to interact and extract structured data.

```
tinyfish search query "Nike running shoes official store"

tinyfish agent run \--url "https://nike.com/running" "Extract all running shoes as JSON: \[{\\"name\\": str, \\"price\\": str}\]"
```

## **Pattern 3: Escalation (fetch → agent)**

Try fetch first. If the page is dynamic/JS-heavy and returns empty or incomplete content, escalate to agent.

## **Pattern 4: Parallel Extraction**

When hitting multiple independent sites, make separate calls — don’t combine into one goal.

**⚠️**  Never combine multiple sites into a single agent goal. Run them as parallel independent calls for reliability.

# **Bonus: Find Reddit Posts for Marketing**

Reddit is a goldmine for distribution — people actively ask for tool recommendations in subreddits like r/SaaS, r/startups, r/webdev, r/artificial, and niche communities. TinyFish lets you systematically find these high-intent threads so you can engage authentically.

## **Step 1 — Search for Relevant Reddit Threads**

Use the search tool to find Reddit threads where people are asking for exactly the kind of tool you’re building:

```
tinyfish search query "site:reddit.com best web scraping tool for AI agents"
```

```
tinyfish search query "site:reddit.com how to scrape websites with Cursor Claude Code"
```

```
tinyfish search query "site:reddit.com bypass Cloudflare bot detection scraping"
```

This gives you a list of URLs with titles and snippets. Pick the threads that have high engagement and genuine “looking for a tool” intent.

## **Step 2 — Fetch the Full Thread Content**

Now fetch the actual thread content as clean Markdown — no Reddit UI garbage, no sidebar, no ads:

```
tinyfish fetch content get \--format markdown "https://reddit.com/r/webdev/comments/abc123/..."
```

You get the original post, all comments, upvote context — clean text your AI agent can reason over.

## **Step 3 — Extract Structured Data with Agent**

For deeper extraction — like pulling all comments that mention a competitor, or finding threads with unanswered questions — use the agent:

```
tinyfish agent run \--url "https://reddit.com/r/SaaS/comments/xyz789/..." \\

  "Extract all comments as JSON: \[{\\"author\\": str, \\"text\\": str, \\"upvotes\\": int, \\"mentions\_tool\\": bool}\]"
```

## **Step 4 — Scale It: Batch Reddit Mining**

Create a CSV file with your target Reddit URLs and goals, then run them all in batch:

tinyfish agent batch run \--input reddit\_threads.csv

Your CSV has two columns: url and goal. TinyFish processes them in parallel and returns structured JSON for each.

## **Example Search Queries to Try**

```
* "site:reddit.com looking for AI web scraping tool 2026"

* "site:reddit.com alternative to Playwright for scraping"

* "site:reddit.com how to give AI agent browser access"

* "site:reddit.com best tool to extract website content for LLM context"

* "site:reddit.com token limit problem with web scraping AI coding"
```

**💡**  Pro tip: Pipe the search results into your AI agent and let it decide which threads are highest-intent. Then fetch only those threads and draft personalized, value-first replies — not spam.

# **Links**

[**TinyFish**](https://www.tinyfish.ai/?utm_source=instagram&utm_medium=paid-social&utm_campaign=newapis-developer-2026q2&utm_term=sukhad) **CLI Docs:** https://docs.tinyfish.ai/cli

[**TinyFish**](https://www.tinyfish.ai/?utm_source=instagram&utm_medium=paid-social&utm_campaign=newapis-developer-2026q2&utm_term=sukhad) **Skill:** https://github.com/tinyfish-io/tinyfish-cookbook/blob/main/skills/use-tinyfish/SKILL.md

**Get API Key:** https://agent.tinyfish.ai/api-keys