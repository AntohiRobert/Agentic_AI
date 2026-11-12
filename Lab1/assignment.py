import sys
from openai import OpenAI

def run_chat_loop():
    client = OpenAI()

    # 1. Maintain in-memory history initialized with a system prompt
    messages = [
        {
            "role": "system",
            "content": "You are a concise academic mentor. Remember details shared by the user."
        }
    ]

    print("Chat session started. Type 'exit' or 'quit' to end.\n" + "-" * 50)

    while True:
        try:
            # 2. Read user input from stdin
            user_input = input("User: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting session.")
            break

        # 3. Check for exit command
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Session ended.")
            break

        # 4. Append user message to history
        messages.append({"role": "user", "content": user_input})

        try:
            # 5. Dispatch full history to the model
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )

            assistant_reply = response.choices[0].message.content

            # 6. Print response
            print(f"Assistant: {assistant_reply}\n")

            # 7. Crucial: Append assistant reply back into history
            messages.append({"role": "assistant", "content": assistant_reply})

        except Exception as e:
            print(f"Error during API call: {e}", file=sys.stderr)
            # Remove the last user message if the call failed so state remains consistent
            messages.pop()

if __name__ == "__main__":
    run_chat_loop()