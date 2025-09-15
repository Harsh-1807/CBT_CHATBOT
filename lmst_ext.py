import openai

# Configuration for LM Studio (OpenAI-compatible API)
class OpenAIConfig:
    def __init__(self):
        self.base_url = "http://localhost:1234/v1"  # LM Studio local server
        self.api_type = "open_ai"
        self.api_key = "not-needed"  # LM Studio ignores API keys

# Function to read file content (system prompt)
def read_file_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"⚠️ File not found: {file_path}")
        return None

# Function to send messages to LM Studio
def initiate_conversation(input_text, system_message):
    response = openai.ChatCompletion.create(
        model="local-model",   # use "local-model" or the model you loaded in LM Studio
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": input_text}
        ],
        temperature=0.7,
    )
    return response.choices[0].message["content"].strip()

def main():
    # Instantiate configuration
    config = OpenAIConfig()
    openai.api_base = config.base_url
    openai.api_key = config.api_key

    # Read system message
    system_message = read_file_content("system_message.txt")
    if system_message is None:
        return

    print("✅ Connected to LM Studio at", config.base_url)
    print("Type 'exit' to quit.\n")

    # Conversation loop
    while True:
        user_input = input("User: ")
        if user_input.lower() in ['exit', 'bye', 'end']:
            print("👋 Exiting the conversation.")
            break

        model_response = initiate_conversation(user_input, system_message)
        print("Model:", model_response)

if __name__ == "__main__":
    main()
