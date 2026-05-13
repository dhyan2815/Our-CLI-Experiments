# AI/ML Portfolio Project Analysis

> Last updated: May 13, 2026
> Based on Dhyan Patel's profile and 2026 market demand

---

## Profile Summary

**Stack:** Python, JavaScript/TypeScript, React, Node.js, TensorFlow, Scikit-Learn, n8n, LangChain, Docker

**Strongest Assets:**
- Deployed CNN project (SmokeSignal - 72% false positive reduction, 36k images)
- Production RAG pipelines from Fortiv internship
- Live demos (rare for freshers)
- 9.05 CGPA

**Current Upskilling:** LLM fine-tuning → RAG pipelines → MLOps → ML System Design

---

## Three Recommended Projects

---

# Project 1: RAG-based Document QA Chatbot

## Why It Works

Builds directly on your Fortiv RAG experience. Every company wants this. Differentiator: you can say "I built production RAG pipelines" - most freshers can't.

## Target Niches

| Niche | Documents | Pain Point |
|-------|-----------|------------|
| **Legal Document Analyzer** | Contracts, NDAs, agreements | Lawyers spend hours searching for clauses |
| **HR Policy Chatbot** | Employee handbooks, benefits docs | New hires can't find answers |
| **Research Paper Assistant** | PDFs, arXiv papers | Researchers summarize papers manually |
| **Real Estate Doc Processor** | Property docs, agreements, permits | Agents sift through paperwork |
| **Financial Report Analyzer** | Annual reports, filings, prospectuses | Analysts manually extract metrics |

## Technical Implementation

### Data Pipeline

```
1. File Upload → Text Extraction
   - PDF: pdfplumber or PyMuPDF (preserves tables)
   - DOCX: python-docx
   - CSV: pandas read

2. Chunking Strategy (Critical)
   - Semantic chunking: Use sentence-transformers to find natural breaks
   - Window size: 512 tokens with 50 token overlap
   - Add metadata: page_number, section_header, document_id

3. Vector Store Options
   - ChromaDB (easiest for demo)
   - Qdrant (better for production, has cloud tier)
   - Weaviate (if you want GraphQL later)

4. Retrieval: Hybrid search = BM25 (keyword) + semantic (embedding)
   - Use reranking (BAAI/bge-reranker-v1-m1) for better results
```

### UI Features That Impress

- Source highlighting (click to see exact paragraph)
- "Ask follow-up" (uses conversation history)
- File comparison (ask "What's different between doc A and B?")
- Export citations to Markdown/PDF
- Chat history with search

### Evaluation Metrics

- Retrieval precision@k (measure what % of top-k results relevant)
- Answer accuracy (human eval or LLM-as-judge)
- Response latency (<2s for 10k doc corpus)

### Time to Build

2-3 weeks

---

# Project 2: Fine-tuned Domain LLM

## Why It Works

Shows real model training ability - not just API calling. Rare for fresher portfolios.

## Specific Domains + Datasets

| Domain | Dataset | Model to Fine-tune | Evaluation |
|--------|---------|-------------------|------------|
| **Medical QA** | PubMedQA (1k train), MedQA (USMLE) | Llama-3-8B-Instruct | Accuracy on test set |
| **Legal Contract Analysis** | ContractNLI (10k pairs) | Mistral-7B | F1 on NLI tasks |
| **Financial Sentiment** | FinQA, ConvFinQA | TinyLlama-1.1B | Exact match on numerical reasoning |
| **Technical Support** | StackOverflow Q&A subset | Phi-3-mini | ROUGE-L on answers |

## Technical Stack for Fine-tuning

### Infrastructure Options (2026)

- **Free Tier:** Google Colab Pro (~$10/month), Kaggle (15GB GPU)
- **Paid:** RunPod (~$0.40/hr for A100), Lambda Labs (~$0.50/hr)
- **HuggingFace Spaces:** Free A100 for 2hrs/week

### Fine-tuning Approach

```
1. Base Model:
   - Phi-3-mini (4B params) - runs on single GPU
   - Llama-3-8B - needs 24GB VRAM
   - Mistral-7B - needs 16GB VRAM

2. Technique:
   - QLoRA (quantized LoRA) - reduces memory 70%
   - 4-bit quantization with bitsandbytes
   - Target: 8-16GB GPU requirement

3. Training Config:
   - Learning rate: 2e-4
   - Epochs: 3-5 (early stopping)
   - Batch size: 4-8 (gradient accumulation)
   - Warmup: 10% of steps

4. Frameworks:
   - TRL (Transformers Reinforcement Learning) - easiest
   - Axolotl - pre-configured configs for popular models
```

## Demo UI to Build

- Split screen: base model vs fine-tuned model
- Temperature slider (show how fine-tuned handles better)
- Domain-specific examples only

## Differentiation Points

- Show exact prompt templates used
- Show training loss curve
- Show evaluation results on held-out set
- Quantify: "Fine-tuned model scores 23% higher on medical reasoning"

### Time to Build

3-4 weeks

---

# Project 3: End-to-End ML Pipeline (MLOps Showcase)

## Why It Works

Your current upskilling focus. Shows you understand production ML, not just Jupyter notebooks.

## Architecture Overview

```
                      PIPELINE OVERVIEW

  [Data] ──► [Preprocess] ──► [Train] ──► [Evaluate]
    │              │              │            │
    ▼              ▼              ▼            ▼
  S3/GCS       DVC           MLflow       Comet/
  bucket       tracking       registry    W&B

       [Model] ──► [Package] ──► [Deploy] ──► [Monitor]
          │              │            │            │
          ▼              ▼            ▼            ▼
       MLflow      FastAPI       Railway/    Prometheus
       registry     + Docker     Render      + Grafana
```

## Implementation Levels

### Level 1 - Basic (2 weeks)

- GitHub Actions workflow: on push to main → train → test → build Docker → deploy
- FastAPI wrapper around your model
- Basic health check endpoint

### Level 2 - Intermediate (add 1 week)

- Model versioning in MLflow
- A/B testing (deploy two versions, route % traffic)
- Basic metrics logging (prediction count, latency p50/p99)

### Level 3 - Pro (add 1 week)

- Data drift detection (compare input distribution)
- Retraining trigger (auto-trigger when drift detected)
- Custom metrics dashboard

## Monitoring Dashboard Metrics

| Metric | Why It Matters | Tool |
|--------|-----------------|------|
| Latency p50/p99 | Shows performance | Prometheus |
| Prediction confidence distribution | Detects model uncertainty | Custom |
| Request volume | Demand spike detection | Prometheus |
| Error rate | Model breaking | Prometheus |
| Data drift (KL divergence) | Input distribution shift | Great Expectations |

## Deployment Targets Comparison

| Platform | Pros | Cons | Cost |
|----------|------|------|------|
| **Railway** | Easy, auto-scaling | Cold starts | $5-20/mo |
| **Render** | Free tier, good docs | Limited GPU | Free tier |
| **HuggingFace Spaces** | Free GPU, easy | Limited control | Free |
| **Render + GPU** | GPU inference | Slow | $15/mo |
| **Fly.io** | Global edge | Complex setup | $5/mo |

### Time to Build

2-3 weeks

---

## Differentiation Strategy

| Project | What Makes Yours Different |
|---------|---------------------------|
| RAG Chatbot | Multi-document, hybrid search, follow-up questions |
| Fine-tuned LLM | Show side-by-side eval, quantified improvement |
| MLOps Pipeline | Full lifecycle visibility, monitoring dashboard |

---

## Recommended Build Order

Based on your current upskilling + existing experience:

1. **RAG Chatbot** (Week 1-2) - Leverages Fortiv RAG work directly
2. **MLOps Pipeline** (Week 3-4) - Your current MLOps rotation
3. **Fine-tuned LLM** (Week 5-7) - After you've leveled up on fine-tuning

---

## Resources

- **SmokeSignal AI (Reference):** https://smokkesignal-ai.streamlit.app/
- **Yield Metrics (Reference):** https://yieldmetrics.streamlit.app/
- **GitHub:** https://github.com/dhyan2815
- **Portfolio:** https://dhyan-patel.onrender.com/

---

*Generated from AI/ML career analysis session*