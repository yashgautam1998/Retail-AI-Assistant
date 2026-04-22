# Retail AI Assistant — Architecture Document

## 1. Overview

The Retail AI Assistant is a simulation-based agentic system designed to perform two key roles:

1. **Personal Shopper (Revenue Agent)** — recommends products based on user preferences and constraints
2. **Customer Support Assistant (Operations Agent)** — evaluates return eligibility using business policies

The system is built using a **tool-calling architecture**, where the language model acts as a controller and delegates all factual operations to structured tools. This ensures high accuracy, explainability, and zero hallucination.

---

## 2. System Architecture

The system follows a modular, layered design:

```
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
LLM (Reasoning + Explanation)
```

### Components:

* **Agent Layer (`agent/`)**

  * Handles reasoning and decision-making
  * Uses system prompt to enforce rules and behavior

* **Tool Layer (`tools/`)**

  * Contains deterministic functions:

    * `search_products(filters)`
    * `get_product(product_id)`
    * `get_order(order_id)`
    * `evaluate_return(order_id)`

* **Data Layer (`data/`)**

  * CSV files for products and orders
  * Policy text for return rules

* **CLI Interface (`main.py`)**

  * Provides interactive user interface
  * Maintains conversation memory

---

## 3. Tool-Based Design

The system strictly separates **reasoning from data access**:

* The LLM **never generates product or order data**
* All factual information is retrieved via tools
* Business rules are implemented in `evaluate_return()`

### Tool Responsibilities:

| Tool            | Purpose                               |
| --------------- | ------------------------------------- |
| search_products | Filters products based on constraints |
| get_product     | Fetches product details               |
| get_order       | Retrieves order information           |
| evaluate_return | Applies return policy rules           |

---

## 4. Multi-Step Tool Execution

The agent uses a **loop-based execution model**:

* The LLM can call multiple tools in sequence
* Example (support query):

  1. `get_order(order_id)`
  2. `evaluate_return(order_id)`
  3. Final response generation

A maximum step limit is enforced to prevent infinite loops.

---

## 5. Hallucination Prevention

The system is explicitly designed to avoid hallucination:

* All factual responses depend on tool outputs
* The agent is instructed to **never guess missing data**
* If a tool returns no result:

  * The agent refuses with a clear message
* Return decisions are **rule-based**, not inferred

This ensures deterministic and trustworthy outputs.

---

## 6. Personal Shopper Logic

The recommendation system applies **multi-constraint filtering**:

* Price filtering (e.g., under $300)
* Size availability + stock validation
* Tag matching (e.g., “modest”, “evening”)
* Sale prioritization
* Ranking using `bestseller_score`

### Fallback Strategy:

If no exact match is found:

1. Relax tag constraints
2. Remove sale filter
3. Return closest matches

This mimics real-world e-commerce behavior.

---

## 7. Support Assistant Logic

Return decisions are handled using a **rule-based engine**:

### Policy Precedence:

1. Clearance items → not returnable
2. Vendor exceptions:

   * Aurelia Couture → exchange only
   * Nocturne → 21-day return window
3. Sale items → 7 days (store credit only)
4. Normal items → 14 days (refund)

The agent:

* Calls `evaluate_return()`
* Explains the applied rule
* Provides a clear decision (yes/no + type)

---

## 8. Conversation Memory

The system maintains a shared message history across turns:

* Enables multi-turn interactions
* Supports confirmations like “yes”
* Preserves context (e.g., order ID)

Example:

```
User: Can I return this?
AI: Exchange only
User: Yes
AI: Proceeding with exchange...
```

---

## 9. Tool Selection Strategy

The LLM dynamically selects tools based on intent:

| User Query             | Tool Used       |
| ---------------------- | --------------- |
| Product recommendation | search_products |
| Order lookup           | get_order       |
| Return query           | evaluate_return |

This allows flexible and intelligent behavior without hardcoding flows.

---

## 10. Design Decisions

### Why not use RAG or embeddings?

* Data is structured (CSV), not unstructured text
* Requires exact filtering and rule-based decisions
* Deterministic logic is more reliable than semantic search

### Why tool-based architecture?

* Ensures correctness and explainability
* Scales easily with additional tools
* Prevents hallucination

---

## 11. Conclusion

This system demonstrates a production-style agent architecture combining:

* Tool-based data retrieval
* Rule-based reasoning
* Multi-step execution
* Conversational memory

It achieves high accuracy, transparency, and robustness while remaining modular and extensible for future enhancements.

---
