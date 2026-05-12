# ML Intern Setup & Usage Guide

**ml-intern** is an open-source ML engineer agent from Hugging Face that can autonomously research, write, and ship high-quality machine learning code.

---

## Table of Contents

1. [Installation](#installation)
2. [Initial Setup](#initial-setup)
3. [Usage Modes](#usage-modes)
4. [Command Reference](#command-reference)
5. [Configuration](#configuration)
6. [Using with Claude Code](#using-with-claude-code)
7. [Troubleshooting](#troubleshooting)

---

## Installation

### Method 1: Direct Install (Recommended for Claude Code)

Install ml-intern directly from GitHub using pip:

```bash
pip install git+https://github.com/huggingface/ml-intern.git
```

This installs the package globally and creates the `ml-intern` CLI command.

### Method 2: Via uvx (Portable, No Install)

Run ml-intern without installing it:

```bash
uvx --from git+https://github.com/huggingface/ml-intern.git ml-intern --help
```

### Method 3: Clone and Develop

```bash
git clone https://github.com/huggingface/ml-intern.git
cd ml-intern
uv pip install -e .
```

---

## Initial Setup

### Step 1: Create Environment File

Create a `.env` file in your project root (or home directory) with your API keys:

```bash
# Required: At least one LLM provider
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxx

# Optional: OpenAI as backup
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Location:** Place `.env` in the directory where you'll run `ml-intern`, or in your home directory (`~/.env` on Linux/Mac, `%USERPROFILE%\.env` on Windows).

### Step 2: Verify Installation

```bash
ml-intern --help
```

You should see:

```
usage: ml-intern [-h] [--model MODEL] [--max-iterations MAX_ITERATIONS]
                 [--no-stream] [--sandbox-tools]
                 [prompt]

Hugging Face Agent CLI
```

---

## Usage Modes

### Mode 1: Interactive Chat Mode

Start an interactive session:

```bash
ml-intern
```

This opens a REPL where you can chat with the agent about ML tasks.

### Mode 2: Headless Single Prompt

Run a single task without interactive mode:

```bash
ml-intern "Train a sentiment analysis model on the IMDB dataset"
```

### Mode 3: With Sandbox Tools

Use Hugging Face Spaces sandbox for code execution (GPU access available):

```bash
ml-intern --sandbox-tools "Fine-tune a LLaMA model on my custom dataset"
```

---

## Command Reference

```bash
# Show help
ml-intern --help

# Run headless with a prompt
ml-intern "your ML task here"

# Specify model
ml-intern -m anthropic/claude-3-5-sonnet "train a classifier"

# Set max iterations (default: 50)
ml-intern --max-iterations 100 "complex task"

# Disable streaming output
ml-intern --no-stream "non-streaming task"

# Use HF Space sandbox for GPU
ml-intern --sandbox-tools "train on GPU"
```

---

## Configuration

### Project-Level Config

ml-intern looks for configuration in:

1. `./configs/cli_agent_config.json`
2. `~/.config/ml-intern/config.json`

### Sample Configuration

```json
{
  "model": "anthropic/claude-3-5-sonnet-20241022",
  "max_iterations": 50,
  "stream": true
}
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key for Claude models |
| `OPENAI_API_KEY` | No | OpenAI API key as fallback |
| `HF_TOKEN` | No | Hugging Face token for private models/datasets |

---

## Using with Claude Code

### Integration Pattern

Since ml-intern is installed globally, you can invoke it from Claude Code:

```bash
# Example: Ask ml-intern to analyze or modify ML code
ml-intern "Review the model.py file and suggest improvements for training speed"

# Example: Generate ML code
ml-intern "Create a training script for a CNN on CIFAR-10"
```

### Workflow with Claude Code

1. **Use Claude Code** for:
   - General project management
   - File operations
   - Code review
   - Multi-step software engineering tasks

2. **Use ml-intern** for:
   - ML-specific code generation
   - Model training scripts
   - Dataset preprocessing
   - Research paper implementation

### Example Workflow

```bash
# 1. Claude Code creates the project structure
mkdir my-ml-project && cd my-ml-project

# 2. Ask ml-intern to create a training script
ml-intern "Create a PyTorch training script for image classification"

# 3. Claude Code integrates and modifies as needed
# 4. ml-intern can review and improve the ML code
ml-intern "Optimize the training loop for better GPU utilization"
```

---

## Troubleshooting

### Issue: Command Not Found

**Symptom:** `ml-intern: command not found`

**Fix:** Ensure pip install completed successfully:

```bash
pip install git+https://github.com/huggingface/ml-intern.git

# Verify
pip show ml-intern
```

### Issue: API Key Not Found

**Symptom:** Error about missing API key

**Fix:** Ensure `.env` file exists and contains:

```
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

The file must be in the current directory or home directory.

### Issue: Dependency Conflicts

**Symptom:** Warnings about incompatible packages

**Fix:** Create a dedicated virtual environment:

```bash
# Create new environment
python -m venv ml-intern-env
source ml-intern-env/bin/activate  # Linux/Mac
# OR
ml-intern-env\Scripts\activate  # Windows

# Install
pip install git+https://github.com/huggingface/ml-intern.git
```

### Issue: Model Not Available

**Symptom:** "Model not found" or "Invalid model"

**Fix:** Use a valid model identifier:

```bash
# Use Claude
ml-intern -m anthropic/claude-3-5-sonnet-20241022 "task"

# Use GPT-4
ml-intern -m openai/gpt-4o "task"
```

---

## Project Structure Reference

ml-intern expects this structure when working:

```
project/
├── .env                 # API keys (DO NOT COMMIT)
├── configs/
│   └── cli_agent_config.json  # Agent configuration
├── data/                # Datasets
├── models/              # Saved models
├── outputs/             # Training outputs
└── [your ML files]
```

---

## Dependencies Installed

When you install ml-intern, these key packages are included:

| Package | Purpose |
|---------|---------|
| `litellm` | Unified LLM interface |
| `fastapi` | Backend API |
| `fastmcp` | MCP server integration |
| `datasets` | Hugging Face datasets |
| `transformers` | Pre-trained models |
| `huggingface-hub` | HF model/dataset access |

---

## Next Steps

1. **Get an API key** from [Anthropic](https://console.anthropic.com/) or [OpenAI](https://platform.openai.com/)

2. **Create your `.env` file** with the key

3. **Test with a simple prompt:**
   ```bash
   ml-intern "Write a simple PyTorch classifier"
   ```

4. **Explore the ml-intern repository:**
   - [https://github.com/huggingface/ml-intern](https://github.com/huggingface/ml-intern)
   - Read `AGENTS.md` for contribution guidelines
   - Read `REVIEW.md` for code review process

---

## Quick Reference Card

```bash
# Install
pip install git+https://github.com/huggingface/ml-intern.git

# Setup
echo "ANTHROPIC_API_KEY=sk-ant-xxxxx" > .env

# Use
ml-intern "your ML task"
ml-intern -m anthropic/claude-3-5-sonnet "task"
ml-intern --sandbox-tools "GPU task"
ml-intern --max-iterations 100 "long task"
ml-intern --no-stream "no streaming"
```

---

*Last Updated: 2026-05-12*
