# 🛍️ Retail AI Assistant

An agentic AI system that simulates a real-world e-commerce assistant with two core capabilities:

- 🛒 **Personal Shopper (Revenue Agent)** — recommends products based on user preferences
- 📦 **Customer Support Assistant (Operations Agent)** — evaluates return eligibility using business rules

Built using a **tool-calling architecture**, ensuring high accuracy, zero hallucination, and explainable outputs.

---

## 🚀 Features

- ✅ AI-powered product recommendations
- ✅ Rule-based return eligibility decisions
- ✅ Multi-step tool execution
- ✅ Conversation memory support
- ✅ No hallucination (strict tool-based data access)
- ✅ CLI-based interactive interface

---

## 🧠 Architecture Overview


User Input
↓
LLM Agent (Decision Layer)
↓
Tool Selection (Function Calling)
↓
Tool Execution (Data Layer)
↓
Structured Output
↓
LLM (Final Response)


### 🔹 Key Design Principles

- LLM handles **reasoning only**
- Tools handle **all factual data**
- No direct data generation by the model
- Deterministic and explainable outputs

---

## 📁 Project Structure


Retail-AI-Assistant/
│
├── agent/
│ ├── agent.py # Core agent logic
│ ├── prompts.py # System prompt
│
├── tools/
│ ├── order_tools.py
│ ├── product_tools.py
│ ├── product_tools.py
│ 
│
├── data/
│ ├── products_inventory.csv
│ ├── orders.csv
│ ├── policy.txt
│
├── main.py # CLI interface
├── requirements.txt
├── .env.example
└── README.md


---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yashgautam1998/Retail-AI-Assistant.git
cd Retail-AI-Assistant
2️⃣ Create virtual environment
python -m venv venv
3️⃣ Activate virtual environment

Windows (PowerShell):

.\venv\Scripts\Activate

Mac/Linux:

source venv/bin/activate
4️⃣ Install dependencies
pip install -r requirements.txt
5️⃣ Setup environment variables
Copy .env.example → .env
Add your OpenAI API key:
OPENAI_API_KEY=your_openai_key_here
6️⃣ Run the application
python main.py
💬 Example Usage
🛍️ Retail AI Assistant (CLI)
Type 'exit' to quit

You: Show me dresses under $200 in size M
AI: Here are some great options...

You: Can I return order #1234?
AI: This item is eligible for exchange only...
🛠️ Tools
Tool	Description
search_products	Filters products based on constraints
get_product	Fetches product details
get_order	Retrieves order information
evaluate_return	Applies return policy rules
🔄 Multi-Step Execution

The agent can call multiple tools in sequence:

Example flow:

get_order(order_id)
evaluate_return(order_id)
Generate final response
🛡️ Hallucination Prevention
❌ Model never generates product/order data
✅ All data comes from tools
✅ Strict refusal if data not found
✅ Rule-based return decisions
🛍️ Personal Shopper Logic
Price filtering
Size + stock validation
Tag-based matching
Bestseller ranking
Sale prioritization

Fallback strategy:

Relax filters if no exact match found
📦 Return Policy Logic

Policy precedence:

Clearance → Not returnable
Vendor rules:
Aurelia Couture → Exchange only
Nocturne → 21-day return window
Sale items → 7 days (store credit)
Regular items → 14 days (refund)
💡 Why Tool-Based Architecture?
✔ High accuracy
✔ No hallucination
✔ Easy to scale
✔ Clear separation of concerns