<div align="center">

<img src="yellowdotai_logo.jpg" alt="Yellow.ai Logo" width="180" />

# AI Banking Agent – Yellow.ai (Gen AI)

**A next-generation conversational banking assistant powered by Generative AI, intelligent intent routing, and real-time backend API integrations.**

[![CI Tests](https://img.shields.io/github/actions/workflow/status/vachan18/Gen-AI-banking-agent/ci.yml?branch=main&style=for-the-badge&logo=githubactions&logoColor=white&label=CI%20Tests)](https://github.com/vachan18/Gen-AI-banking-agent/actions/workflows/ci.yml)
[![Live Bot Demo](https://img.shields.io/badge/Live_Bot-Yellow.ai-FFC72C?style=for-the-badge&logo=probot&logoColor=black)](https://cloud.yellow.ai/liveBot/x1774959469287?region=r0)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Generative AI](https://img.shields.io/badge/Generative_AI-Yellow.ai_LLM-4285F4?style=for-the-badge)](https://yellow.ai)
[![Webhook](https://img.shields.io/badge/Integration-REST_Webhooks-2ea44f?style=for-the-badge)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

---

### 🌐 [Click Here to Test the Live Banking Assistant](https://cloud.yellow.ai/liveBot/x1774959469287?region=r0)

</div>

---

## 📌 Executive Summary

Modern banking customers expect instant, 24/7 self-service across accounts, loans, and transaction services without wait times. This project implements a **production-ready conversational AI banking agent** built on **Yellow.ai's Generative AI platform**, coupled with Python webhook integrations and banking core APIs.

### Key Highlights
- **GenAI-Powered Live Banking Assistant**: Built using Yellow.ai, automating end-to-end customer interactions including account assistance, transaction support, and zero-latency FAQ resolution.
- **Intelligent Conversational Workflows**: Designed structured flows with intent handling, dynamic slot filling, AI Agents, and AI-driven flow optimization to enhance real-time conversational UX.
- **Robust API & Webhook Integrations**: Engineered webhook integrations, structured JSON data pipelines, and Python scripting for seamless, secure API communication between banking backends and the conversational agent.
- **Sub-Second Response Times**: Delivers rich interactive UI components (interactive cards, carousels, quick replies) paired with LLM fallback for conversational questions.

---

## 📸 Interface & System Visuals

### 1. Live Banking AI Assistant Deployment
Automated resolution of complex banking queries, multi-step automation workflows, and sub-second real-time conversational responses.

<div align="center">
  <img src="Picture3.png" alt="Yellow.ai Banking App Interface" width="85%" />
</div>

---

### 2. Intelligent Routing & Workflow Architecture
End-to-end workflow highlighting `User Input` $\rightarrow$ `AI Routing` $\rightarrow$ `Automation Workflow` $\rightarrow$ `Response`, powered by `getLoanAccounts` API endpoints and conditional branching.

<div align="center">
  <img src="Picture2.png" alt="Routing Logic for Yellow.ai Banking App" width="85%" />
</div>

---

## 🏗️ Technical Architecture

```mermaid
flowchart TD
    A["👤 User Chat / Voice Input"] --> B["🤖 Yellow.ai Orchestrator & GenAI LLM"]
    
    subgraph YellowAI ["Yellow.ai Cognitive Engine"]
        B --> C{"Intent Recognition & Routing"}
        C -->|"FAQ / Information"| D["Dynamic GenAI Answer Engine"]
        C -->|"Loan Inquiries"| E["Loan Account Flow"]
        C -->|"Account / Balance"| F["Account Service Flow"]
        C -->|"Transactions"| G["Transaction History Flow"]
    end

    subgraph BackendIntegration ["Integration Layer (Python Webhook)"]
        E -->|"Webhook GET /api/loans"| H["getLoanAccounts API"]
        H --> I["Dynamic Carousel Cards (LN001 / LN002)"]
        I -->|"User Selects Loan ID"| J["GET /api/loans/{loan_id}"]
        F -->|"Webhook GET /api/accounts"| K["Account Balance Service"]
        G -->|"Webhook GET /api/transactions"| L["Transaction Service"]
    end

    subgraph DataStore ["Core Banking Mock Data"]
        H -.-> M[("mock_banking_data.json")]
        J -.-> M
        K -.-> M
        L -.-> M
    end

    D --> N["💬 Natural Language Response"]
    J --> N
    K --> N
    L --> N
    N --> O["📱 User Interface (Web / Mobile)"]
```

---

## ⚡ Core Functionalities

### 1. Dynamic Loan Accounts & Carousel Rendering
- Queries the `getLoanAccounts` endpoint in real-time.
- Dynamically renders interactive loan cards (e.g., **Home Loan | LN001** and **Personal Loan | LN002**).
- Triggers contextual conditional logic based on customer selection:
  ```
  IF [selected_loan_id] == 'LN001' -> Fetch Home Loan Outstanding & Next EMI Date
  ELSE IF [selected_loan_id] == 'LN002' -> Fetch Personal Loan Outstanding & Interest Rate
  ```

### 2. Account Assistance & Balance Check
- Authenticated account inquiries delivering current available balance, account tier, and branch details.
- Secure data masking for customer identification.

### 3. Transaction Support & Statement Retrieval
- Instant lookup for recent debits, credits, UPI payments, and automated EMI debits.

### 4. GenAI FAQ & Fallback Resolution
- Handles open-ended banking inquiries (interest rate policies, branch timings, KYC verification steps) using generative responses grounded in verified banking knowledge bases.

---

## 🛠️ Tech Stack & Skills

| Domain | Technology / Tool |
| :--- | :--- |
| **Conversational AI Platform** | [Yellow.ai](https://yellow.ai) (Dynamic Flow Builder, Gen AI Bot Engine) |
| **Backend Integration** | Python 3.9+, Flask, REST APIs, Webhook Handlers |
| **Data Format** | JSON (JavaScript Object Notation), Schema Validation |
| **AI & Automation** | Intent Handling, Slot Extraction, Generative AI, Prompt Engineering |
| **Deployment & Testing** | Yellow.ai Cloud Console, Local Webhook Server, Postman |

---

## 📂 Project Repository Structure

```
├── Picture2.png                 # Architectural routing diagram & workflow logic
├── Picture3.png                 # Mobile UI spotlight & deployment overview
├── yellowdotai_logo.jpg         # Yellow.ai platform branding asset
├── webhook_server.py            # Python Flask webhook & banking API microservice
├── requirements.txt             # Python dependencies
├── data/
│   └── mock_banking_data.json   # Mock banking datasets (loans, accounts, transactions)
├── .gitignore                   # Standard ignore rules
└── README.md                    # Project documentation
```

---

## 🚀 Running the Webhook Backend Locally

### 1. Clone the Repository
```bash
git clone https://github.com/vachan18/Gen-AI-banking-agent.git
cd Gen-AI-banking-agent
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the Service
```bash
python webhook_server.py
```
*The server will start on `http://127.0.0.1:5000`.*

### 5. Test Endpoints
```bash
# Fetch Loan Accounts
curl http://127.0.0.1:5000/api/loans

# Fetch Specific Loan (LN001)
curl http://127.0.0.1:5000/api/loans/LN001

# Fetch Account Details
curl http://127.0.0.1:5000/api/accounts
```

---

## 🔗 Live Yellow.ai Project Link

Test the interactive bot directly in the Yellow.ai cloud environment:  
👉 **[Launch Yellow.ai Live Banking Bot](https://cloud.yellow.ai/liveBot/x1774959469287?region=r0)**

---

## 👨‍💻 Author

**Vachan U S**  
- **GitHub**: [@vachan18](https://github.com/vachan18)  
- **Portfolio**: [devfolio.co/@Vachanus](https://devfolio.co/@Vachanus)  
- **Email**: vachanus@gmail.com

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
