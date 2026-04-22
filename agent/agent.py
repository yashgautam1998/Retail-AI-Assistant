import json
from openai import OpenAI

from tools.product_tools import search_products, get_product
from tools.order_tools import get_order
from tools.return_tools import evaluate_return
from agent.prompts import SYSTEM_PROMPT
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_tool(name, args):
    if name == "search_products":
        return search_products(args)
    if name == "get_product":
        return get_product(args["product_id"])
    if name == "get_order":
        return get_order(args["order_id"])
    if name == "evaluate_return":
        return evaluate_return(args["order_id"])
    return {"error": "Unknown tool"}


tools = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "parameters": {
                "type": "object",
                "properties": {
                    "max_price": {"type": "number"},
                    "size": {"type": "string"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "is_sale": {"type": "boolean"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_order",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"}
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "evaluate_return",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"}
                },
                "required": ["order_id"]
            }
        }
    }
]
def run_agent(user_input, messages):

    # ✅ Add user message to existing conversation
    messages.append({"role": "user", "content": user_input})

    MAX_STEPS = 5
    step = 0

    while step < MAX_STEPS:
        step += 1

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        msg = response.choices[0].message

        # ✅ Final response
        if not msg.tool_calls:
            print("\n================ FINAL RESPONSE ================\n")
            messages.append({"role": "assistant", "content": msg.content})
            return msg.content, messages

        messages.append(msg)

        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            print(f"\n🔧 Step {step} → Tool Called: {name} | Args: {args}")

            result = call_tool(name, args)

            # ✅ Early exit on error
            if isinstance(result, dict) and "error" in result:
                return result["error"], messages

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

    return "Sorry, I couldn't complete the request.", messages