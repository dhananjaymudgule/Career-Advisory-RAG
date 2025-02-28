## **Career Advisory AI**  

### **📌 Overview**  
This is a **Retrieval-Augmented Generation (RAG) Web Application** that helps users explore career options based on job descriptions. It uses:  
- **FastAPI** → Backend API for job retrieval  
- **Streamlit** → Frontend for user interaction  

---

### **📂 Project Structure**  
```
rag-career-advisor/
│── backend/               # FastAPI backend
│   ├── data/              # Data storage
│   │   ├── datasets/      # Job datasets
│   │   ├── docs/          # Documentation
│   │   ├── indexes/       # FAISS/ChromaDB indexes
│   │   ├── logs/          # Logging files
│   ├── modules/           # Core modules
│   │   ├── generator.py   # LLM-based response generation
│   │   ├── loader.py      # Data loading utilities
│   │   ├── prompts.py     # Prompt engineering
│   │   ├── retrieval.py   # Vector search logic
│   ├── main.py            # API entry point
│   ├── config.py          # Configuration settings
│   ├── logger.py          # Logging setup
│
│── frontend/              # Streamlit frontend
│   ├── pages/             # Streamlit multi-page structure
│   ├── app.py             # UI script
│   ├── config.py          # Frontend configurations
│
│── myenv/                 # Virtual environment (not included in repo)
│── .env                   # Environment variables
│── README.md              # Project documentation
│── requirements.txt       # Dependencies
|__ .gitignore             # Ignore specified files while pushing on GitHub
```

---

### **🚀 Installation & Setup**  
#### **1️⃣ Create a Virtual Environment**  
Run the following command in the project root directory:  
```bash
python -m venv myenv
```
Activate the virtual environment:
- **Windows**:  
  ```bash
  myenv\Scripts\activate
  ```
- **Mac/Linux**:  
  ```bash
  source myenv/bin/activate
  ```

#### **2️⃣ Install Dependencies**  
Run the following command:  
```bash
pip install -r requirements.txt
```

#### **3️⃣ Create a `.env` File**  
In the project root directory, create a `.env` file and insert the API keys:  
```
HUGGINGFACE_API_KEY=your_huggingface_api_key
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
```

#### **4️⃣ Start Backend (FastAPI)**  
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
📌 **API will be available at** → `http://127.0.0.1:8000`  
📌 **Swagger UI** → `http://127.0.0.1:8000/docs`

#### **5️⃣ Start Frontend (Streamlit)**  
```bash
cd frontend
streamlit run app.py
```
📌 **Streamlit UI will be available at** → `http://localhost:8501`

---

### **🛠 Technologies Used**
- **FastAPI** → Backend framework  
- **Streamlit** → UI for search queries 
- **LangChain** → To load Embeddings model 
- **FAISS** → Vector search for job retrieval  
- **Gemini** → LLM for career advice  
- **Huggingface** → Embeddings  
- **OpenAI GPT** → Evaluate  
- **RAGAS** → Evaluate  

---

### **📌 Features**
✔ Search job roles based on natural language queries  
✔ Retrieve job details from a **vector database**  
✔ Generate response/career advice using **LLM**  
✔ Simple **web UI** for user interaction  

---

