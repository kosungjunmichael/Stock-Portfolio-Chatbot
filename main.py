# main.py
from dotenv import load_dotenv
load_dotenv()  # loads .env into environment variables

from llm_agent.agent import create_agent


def login():
    print("=== Portfolio Bot Login ===")
    username = input("Enter a username: ").strip()
    if not username:
        username = "default"
    return username


def main():
    user_id = login()
    agent = create_agent(user_id)

    print(f"\nPortfolio chatbot ready for user: {user_id}")
    print("Examples:")
    print("  - I bought 10 NVDA at 120")
    print("  - I sold 3 NVDA at 150")
    print("  - What's my profit on NVDA?")
    print("  - What's my total profit?")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("> ").strip()
        if user_input.lower() in ("quit", "exit"):
            break

        try:
            response = agent.run(user_input)
            print(response)
        except Exception as e:
            print(f"[Error] {e}")


if __name__ == "__main__":
    main()
