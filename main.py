from agent.agent import run_agent
from agent.prompts import SYSTEM_PROMPT


def main():
    print("🛍️ Retail AI Assistant (CLI)")
    print("Type 'exit' to quit\n")

    # ✅ Initialize conversation memory
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        # ✅ Pass memory
        response, messages = run_agent(user_input, messages)

        print("\nAI:", response, "\n")


if __name__ == "__main__":
    main()