# MCP Exploration - Day 2

**Date:** 2026-05-17
**Session:** Day 2 of 30-Day AI CLI Experimentation
**Focus:** HuggingFace MCP server exploration

---

## MCP Server Status

`.mcp.json` configured with:
```json
{
  "mcpServers": {
    "hf-mcp-server": {
      "type": "http",
      "url": "https://huggingface.co/mcp?login"
    }
  }
}
```

---

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `hf_hub_query` | Search/query HF hub |
| `hub_repo_search` | Search repositories |
| `hub_repo_details` | Get repo metadata |
| `gr1_z_image_turbo_generate` | Image generation |
| `hf_doc_search` | Search documentation |
| `hf_doc_fetch` | Fetch docs |
| `paper_search` | Find ML papers |
| `space_search` | Find Spaces |
| `hf_whoami` | Current user info |

---

## Test Results

### Model Search: "small language model"

```bash
mcp__hf-mcp-server__hub_repo_search(
  query="small language model",
  repo_types=["model"],
  limit=5
)
```

**Result:** 5 models found, including:
- snarktank/small-language-model (MIT license)
- lingea/fasttext_language_detection
- a1Kingleo/SmallLanguageModelCollection

---

## Capabilities Observed

1. **Model Discovery** - Search 100K+ models on HuggingFace
2. **Image Generation** - Z-Image Turbo model available
3. **Documentation** - Access to HF/Gradio docs
4. **Paper Search** - Research paper lookup
5. **Spaces Discovery** - Find demo applications

---

## Next Steps

- Explore image generation tool
- Test paper search for ML topics
- Document Notion MCP capabilities (if configured)
- Plan custom MCP server build

---

**Commit:** Day 2 - MCP exploration (hf-mcp-server tested)