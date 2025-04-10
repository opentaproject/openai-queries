import openai
import pprint

from openai import OpenAI
import requests
import time

def setup_assistant() :
    model = 'gpt-4o-mini'
    client = OpenAI()
    assistant = client.beta.assistants.create(
      name="Simple student",
      instructions="Answer simple questions about the relevant document.",
      model=model,
      tools=[{"type": "file_search"}],
    )
    print(f"A2, {assistant}")
    assistant_id = assistant.id
    vector_store = client.vector_stores.create(name="Simple file")
    vector_store_id = vector_store.id
    file_paths = ["./example.pdf"]
    file_streams = [open(path, "rb") for path in file_paths]
    file_batch = client.vector_stores.file_batches.upload_and_poll( vector_store_id=vector_store_id, files=file_streams)
    print(file_batch.file_counts)
    response = client.responses.create(
        model=model,
        input="What does the uploaded file say?",
        tools=[{
            "type": "file_search",
            "vector_store_ids": [vector_store_id]
        }],
    )
    assistant = client.beta.assistants.update(
      assistant_id=assistant.id,
      tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )
    #thread = client.beta.threads.create(
    #  messages=[
    #    {
    #      "role": "user",
    #      "content": "What does the file say?",
    #    }
    #  ]
    #)
    thread = client.beta.threads.create(); 
    thread_id = thread.id
    print(f"THREAD = {thread}")
    print(thread.tool_resources.file_search)
    # Add user message (no need to include file_ids)
    return assistant_id, thread_id, 

def setup() :
    assistant_id, thread_id = setup_assistant() 
    openai.beta.threads.messages.create( thread_id=thread_id,  role="user", content="Summarize the uploaded PDF.")
    print(f"A6")
    #thread_id = thread.id
    run = openai.beta.threads.runs.create( thread_id=thread_id, assistant_id=assistant_id)
    while True:
        run_status = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status == "completed":
            break
        elif run_status.status == "failed":
            raise Exception("Run failed.")
        else:
            print("Waiting for completion...")
            time.sleep(1)
    messages = openai.beta.threads.messages.list(thread_id=thread_id)
    print("\nAssistant Response:")
    i = 0;
    for msg in messages.data[::-1]:  # newest last
        print(f"I = {i} msg={msg} ")
        i = i + 1 
        if msg.role == "assistant":
            res = msg
            print(msg.content[0].text.value)
    print(f"MSG ={msg}")
    return assistant_id
    


def main():
    assistant_id = setup() 
    print(f"ASSISTANT_ID = {assistant_id}")
    while True:
        user_input = input("Enter something (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        print(f"You said: {user_input}")

if __name__ == "__main__":
    main()
