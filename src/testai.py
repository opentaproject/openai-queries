import openai
import os
import pprint
import json

from openai import OpenAI
import requests
import time

def setup_assistant() :
    model = 'gpt-4o-mini'
    client = OpenAI()
    assistant = client.beta.assistants.create(
      name="Simple Query ",
      instructions="Answer simple questions about the relevant document.",
      model=model,
      tools=[{"type": "file_search"}],
    )
    assistant_id = assistant.id
    vector_store = client.vector_stores.create(name="Simple file")
    vector_store_id = vector_store.id
    file_paths = ["./example.md"]
    file_streams = [open(path, "rb") for path in file_paths]
    file_batch = client.vector_stores.file_batches.upload_and_poll( vector_store_id=vector_store_id, files=file_streams)
    assistant = client.beta.assistants.update(
      assistant_id=assistant.id,
      tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )
    thread = client.beta.threads.create(); 
    thread_id = thread.id
    ids = {'assistant_id' : assistant_id, 'thread_id' : thread_id }
    with open('./data.json', 'w') as f:
        json.dump(ids , f)
    return ids

def main(): 
    if os.path.exists("./data.json") :
        with open('data.json', 'r') as f:
            ids = json.load(f)
    else  :
        print(f"SETUP FROM SCRATCH")
        ids = setup_assistant() 
    print(f"IDS = {ids}")
    assistant_id = ids['assistant_id'];
    thread_id = ids['thread_id']
    while True: 
        query = input("QUESTION: (or 'quit' to exit): ")
        if query.lower() == 'quit':
            print("Goodbye!")
            break
        openai.beta.threads.messages.create( thread_id=thread_id,  role="user", content=query)
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
        i = 0;
        for msg in messages.data[::-1]:  # newest last
            i = i + 1 
            if msg.role == "assistant":
                res = msg
        print(f"REPLY = { msg.content[0].text.value}")
    print(f"Bye")
    

if __name__ == "__main__":
    main()
