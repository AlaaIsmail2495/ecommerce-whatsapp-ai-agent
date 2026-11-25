from agent import process_customer_message


DEFAULT_CUSTOMER_ID = "201000000001"

DEMO_MESSAGES = [
    "Hi, what categories are available in the store?",
    "Can you search for a good laptop or product for me?",
    "Great, add one item of it to my cart.",
    "Show me what is currently in my cart."
]


def run_demo(customer_id: str) -> None:
    print(f"\n--- Running Demo Scenario for Customer: {customer_id} ---\n")
    for msg in DEMO_MESSAGES:
        print(f"Customer ({customer_id}): {msg}")
        reply = process_customer_message(customer_id, msg)
        print(f"Agent:\n{reply}\n")
        print("-" * 50)


def main() -> None:
    customer_id = DEFAULT_CUSTOMER_ID
    print("=======================================================")
    print("Store AI Agent Chat Simulator (Terminal Mode)")
    print(f"Active Customer ID: {customer_id}")
    print("Commands:")
    print("  - Type any message to chat with the agent")
    print("  - 'demo'            -> run sample shopping flow")
    print("  - 'switch <id>'     -> change active customer ID")
    print("  - 'exit' or 'quit'  -> stop simulator")
    print("=======================================================\n")

    while True:
        try:
            user_input = input(f"[{customer_id}] You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting chat simulator. Good luck!")
            break

        if not user_input:
            continue

        lower = user_input.lower()
        if lower in ("exit", "quit"):
            print("Exiting chat simulator. Good luck!")
            break

        if lower == "demo":
            run_demo(customer_id)
            continue

        if lower.startswith("switch "):
            new_id = user_input[7:].strip()
            if new_id:
                customer_id = new_id
                print(f"Switched active customer ID to: {customer_id}\n")
            else:
                print("Please provide a customer ID after 'switch', e.g.: switch 201099988877\n")
            continue

        reply = process_customer_message(customer_id, user_input)
        print(f"\nAgent:\n{reply}\n")
        print("-" * 50)


if __name__ == "__main__":
    main()