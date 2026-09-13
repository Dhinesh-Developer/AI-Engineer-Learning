
import ollama
import sys
from openai import OpenAI

def simple_chat_without_memory(user_input:str, use_ollama: bool = True) -> str :

    if use_ollama:
        client = OpenAI(base_url="http://localhost:11434/v1/",api_key="ollama")
        model_name = "llama3.2"
    else:
        client = OpenAI()   
        model_name = "gpt-4o-mini" 

    # Each call only includes the current message
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages= [
                {
                    "role":"user",
                    "content":user_input
                }
            ]
        )    
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    # Model selection
    print("Simple chatbot without memory")
    print("Notice how the bot won't remember anything from previous message!")
    print("select the model type: ")
    print("1. OpenAI GPT-4")
    print("2. Ollama (Local - llama3.2)")

    while True:
        choice = input("Enter choice (1 or 2): ").strip()
        if choice in ["1","2"]:
            break
        print("Please enter either 1 or 2")

    use_ollama = choice == "2"

    #print instructions
    print("=== Chat session started===")
    print("Type 'quit' or 'exit' to end the conversation")
    print("Type 'clear' to clear the screen")
    print("Each message is independent - the bot has no memory of previous messages")

    # Main chat loop

    while True:
        # get the user input
        user_input = input("\nYou:").strip()

        # check for exit commands
        if user_input.lower() in ["quit","exit"]:
            print("\nGoodbye!")
            sys.exit()

        # check for clear command
        if user_input.lower() == "clear":
            continue

        if not user_input:
            continue

        # Get and print messages
        response = simple_chat_without_memory(user_input=user_input,use_ollama=True)
        print(f"Bot: {response}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("chat session ended by user.")
        sys.exit()    

"""
Simple chatbot without memory
Notice how the bot won't remember anything from previous message!
select the model type: 
1. OpenAI GPT-4
2. Ollama (Local - llama3.2)
Enter choice (1 or 2): 2
=== Chat session started===
Type 'quit' or 'exit' to end the conversation
Type 'clear' to clear the screen
Each message is independent - the bot has no memory of previous messages

You:My name is kumar.
Bot: Hello Kumar! It's nice to meet you. Is there anything I can help you with or would you like to chat?

You:what is my name
Bot: I don't have any information about your name. I'm a large language model, 
I don't have personal knowledge or access to your identity information. 
Each time you interact with me, it's a new conversation and I don't retain any information from previous conversations.

If you'd like to share your name, I'd be happy to chat with you about it!


"""