# ⚖️ L.A.R.A – Legal Analysis Research Assistant

## 🧠 Overview
**L.A.R.A (Legal Analysis and Research Assistant)** is an intelligent, Python-based backend application designed to help **lawyers, researchers, and citizens** conduct deep legal research and case studies based on **Indian law**.

Inspired by the concept of **autonomous legal research agents**, L.A.R.A automates the end-to-end process — transforming user queries into precise legal search terms, retrieving authoritative data from multiple sources, and generating a **structured, citable legal analysis** that is **self-evaluated with a real-time confidence score.**

The system uses **LangGraph** for modular agent orchestration and **Retrieval-Augmented Generation (RAG)** to combine internal legal corpora with live web data. The **lawyer mode** has been upgraded to a sophisticated multi-node LangGraph workflow with issue extraction, planning, iterative retrieval, drafting, and self-critique loops, ensuring high-quality, refined legal analysis.

---

## 🚀 Features
- **Intelligent Query Rewriting:** Reformulates user-entered legal problems into precise, law-aware search queries.
- **Role-Based Agents:**
  - *Citizen Mode* – For general legal guidance and awareness using RAG with query rewriting and hybrid retrieval.
  - *Lawyer Mode* – Advanced LangGraph workflow with issue extraction, planning, iterative retrieval, drafting, and self-critique for professional legal analysis.
- **Hybrid Data Retrieval:** Combines FAISS-based local document search with live web lookups via APIs (e.g., Tavily Search).
- **Iterative Multi-Agent Reasoning:** In lawyer mode, dynamically refines queries and answers through agent loops until quality thresholds are met.
- **Structured Legal Analysis:** Synthesizes case law, acts, and judgments into clear, referenced summaries.
- **Citation System:** Each generated report contains references to primary sources and acts for validation and research traceability.
- **In-line Confidence Score:** Runs an in-line evaluator at the end of every query to provide a real-time "Confidence Score" (based on relevance, faithfulness, and clarity) directly to the user, building trust in the generated answer.
- **Iterative Refinement:** Lawyer mode includes self-critique with semantic similarity checks, allowing up to 3 iterations for answer improvement.
- **Test Endpoint:** Dedicated `/test_lawyer_agent` endpoint for direct testing of the lawyer agent workflow.
- **Evaluation System:** Automated computation of precision@5, recall@5, citation correctness, hallucination rate, and answer consistency.
- **ML Models:** Issue classifier (TF-IDF + LogisticRegression) and similarity model (Sentence-Transformers) for enhanced parsing and retrieval.

---

## 🧰 Tech Stack

| Component | Technology Used |
|------------|----------------|
| **Backend Framework** | FastAPI (Python) |
| **Agent Orchestration** | LangGraph (StateGraph with MemorySaver) |
| **Lawyer Agent Nodes** | Issue Extractor, Planner, Retriever, Drafter, Critic, Finalizer |
| **Embeddings + Search** | FAISS Vector Store |
| **Language Model** | Groq (LLaMA 3.1–8B Instant) |
| **Embeddings (Vector DB)** | HuggingFace Embeddings (all-MiniLM-L6-v2) |
| **Embeddings (Evaluation)** | Sentence-Transformers |
| **APIs Used** | Tavily Search API |
| **In-line Evaluation** | LLM-as-a-Judge (Groq) + Semantic Similarity |
| **Frontend** | React + Tailwind CSS + Clerk Auth |
| **Environment Management** | `dotenv` |

| **Evaluation Metrics** | Precision@5, Recall@5, Citation Correctness, Hallucination Rate, Answer Consistency |

| **ML Models** | TF-IDF + LogisticRegression (Classifier), Sentence-Transformers (Similarity) |

---

## 🏗️ Project Structure

```
L.A.R.A-Legal-Analysis-Research-Agent/
│
├── backend/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── citizen_agent.py
│   │   ├── lawyer_agent/
│   │   │   ├── __init__.py
│   │   │   ├── state.py
│   │   │   ├── legacy_answer.py
│   │   │   └── nodes/
│   │   │       ├── issue_extractor.py
│   │   │       ├── planner.py
│   │   │       ├── retriever.py
│   │   │       ├── drafter.py
│   │   │       └── critic.py
│   │   └── router.py
│   │
│   ├── data/
│   │   ├── faiss_index/
│   │   ├── indian_law_docs/
│   │   └── data_converter.py
│   │
│   ├── legal_rag/
│   │   ├── query_rewriter.py
│   │   ├── retrieval.py
│   │   └── summarizer.py
│   ├── raw_data/
│   │
│   ├── .env
│   ├── app.py
│   ├── db.py
│   ├── model_score_checker.py
│
├── frontend/
│   ├── src/
│   └── index.html
│
├── .gitignore
└── README.md

```


## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Rashi-Dwivedi1812/L.A.R.A-Legal-Analysis-Research-Assistant.git
    cd L.A.R.A-Legal-Analysis-Research-Assistant
    ```

2.  **Backend Setup**
    ```bash
    cd backend
    python -m venv venv
    venv\Scripts\activate  # (on Windows)
    pip install -r requirements.txt
    ```

3.  **Set Environment Variables**
   Create a .env file inside /backend:
    ```
    GROQ_API_KEY="your_grok_api_key_here"
    TAVILY_API_KEY="your_tavily_api_key_here"
    ```

4.  **Prepare Legal Data**
    * Place your legal documents (PDFs, JSONs) in the `raw_data/` directory.
    * Run the `data_converter.py` script to process them and create the FAISS index.
      
    ```bash
    python data/data_converter.py
    python data/faiss_index/faiss_indexer.py
    ```

5. **Run the Backend**
    ```
    cd backend
    python app.py
    ```
    Your FastAPI backend will now be available at:
    ```
    http://localhost:8000
    ```

6. **Test the Lawyer Agent (Optional)**
    You can test the new lawyer agent directly using the `/test_lawyer_agent` endpoint:
    ```bash
    curl -X POST "http://localhost:8000/test_lawyer_agent" \
    -H "Content-Type: application/json" \
    -d '{"user_query": "What are the legal implications of a contract breach?", "role": "lawyer", "thread_id": "test123"}'
    ```

## 💻 Frontend (React)

1. **Navigate to Frontend**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

2. **Access the UI**
    Open your browser and go to:
    ```
    http://localhost:5173
    ```

    The frontend includes user authentication via Clerk, chat history management, and role-based agent selection (Citizen or Lawyer).
---

## 📊 Example Queries
- The Securities and Exchange Board of India (SEBI) Act, 1992.
- Foreign Exchange Management Act (FEMA), 1999
- Summarize the judgment in Chunna @ Charan Singh vs State of M.P.
- Explain Section 2A introduced in the Railways Amendment Act, 2025.
- The Insolvency and Bankruptcy Code (IBC).
- Compare provisions under IPC Sections 302 and 304B with recent case law.

## 🧩 Future Enhancements
- 🧠 Multi-document synthesis for cross-case reasoning
- ⚖️ Integration with Indian Kanoon & Law Commission datasets
- 🕵️‍♀️ Named entity recognition for legal citations
- 🔗 Graph-based linking between Acts, Sections, and Cases

---

## 🏁 Contributing
Pull requests are welcome!
To contribute:
```bash
git checkout -b feature/your-feature
git commit -m "Add feature: your-feature"
git push origin feature/your-feature
```

## 👥 Collaborators  

Meet the brilliant minds behind **L.A.R.A – Legal Analysis Research Assistant** ⚖️  

| 👩‍💻 Name | 🎯 Contribution Focus | 🔗 Links |
|------------|---------|----------|
| 🧠 **Rashi Dwivedi** | Core Development • Data Engineering • Backend Systems | [![GitHub](https://img.shields.io/badge/GitHub-Rashi--Dwivedi1812-black?logo=github)](https://github.com/Rashi-Dwivedi1812) |
| ⚙️ **Sachin Mishra** | RAG Pipeline • FAISS Indexing • AI Workflow | [![GitHub](https://img.shields.io/badge/GitHub-sachin--m15-black?logo=github)](https://github.com/sachin-m15) |
| 🧩 **Janvi Gupta** | Frontend Experience • Research Support • Documentation | [![GitHub](https://img.shields.io/badge/GitHub-janviii09-black?logo=github)](https://github.com/janviii09) |

> 💡 *“Alone we can do so little; together we can do so much.” – Helen Keller*

  
