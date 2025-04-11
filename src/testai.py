import openai
import os
import pprint
import json
import chardet
import fitz
import shutil
import string
import random

from openai import OpenAI
import requests
import time
import tiktoken

model = 'gpt-4o-mini'

def nuke() :
    return
    print(f"GETTING_RID_OF_EVERYTHING")
    client = OpenAI()
    vector_stores = client.vector_stores.list()
    for vector_store in [] : # vector_stores :
        print(f"SOON DELETING {vector_store}")
        vector_store_id = vector_store.id
        vector_store_files = client.vector_stores.files.list( vector_store_id=vector_store.id)
        for vector_store_file in vector_store_files :
            file_id = vector_store_file.id
            print(f"DELETING {vector_store_file} {vector_store_id} {file_id}")
            try :
                client.vector_stores.files.delete( vector_store_id=vector_store_id, file_id=file_id)
            except :
                print(f"FILE ERROR {file_id}")
        print(f"DELETING {vector_store} {vector_store_id}")
        try :
            client.vector_stores.delete( vector_store_id=vector_store_id)
        except :
            print(f"VECTOR_STORE_ERROR {vector_store_id}")

    assistants = openai.beta.assistants.list()
    for assistant in assistants:
        assistant_id = assistant.id
        print(f"\n🧹 Deleting assistant: {assistant_id} ({assistant.name})")
        time.sleep(0.5)
        try :
            client.beta.assistants.delete(assistant_id)
        except :
            print(f"ASSISTANT ERROR {assistant}")

    files = client.files.list()
    for file in files :
        file_id = file.id
        print(f"DELETE FILE {file_id}")
        client.files.delete(file_id)

    print("\n✅ All assistants and assistant-related files deleted.")

def get_token_count( file_paths ):
    encoding = tiktoken.encoding_for_model(model)

    def extract_text_from_pdf(file_path):
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    ntokens = 0
    for p in file_paths :
        if p.split('.')[-1] == 'pdf' :
            text =   extract_text_from_pdf( p )
        else :
            with open(p , "r" , encoding='utf-8') as f:
                text = f.read()
        tokens = encoding.encode(text)
        ntokens = ntokens + len(tokens)
    return ntokens



def setup_assistant() :
    nuke()
    # 
    # Basic parameters for the assistant
    #
    # Give instructions to the model
    instructions="Answer simple questions about the relevant document."
    #
    # files to upload
    file_paths = ["../README.md","example.md","example.pdf"] # You can try some example files instead in the repo
    ntokens = get_token_count( file_paths )
    encoding = tiktoken.encoding_for_model(model)

    #
    # provide persistence to thread and file uploads
    json_file = './data.json' # IMPORTANT DELETE THIS FILE TO TRIGGER NEW UPLOAD
    #
    #
    client = OpenAI()
    max_tokens = ntokens // 6  ## KEEP THE RESPONSE CONCISE
    instructions = instructions + f"\n Respond with less than {max_tokens} tokens"
    print(f"INSTRUCTIONS = {instructions}")
    assistant = client.beta.assistants.create(
      name="Simple Query ",
      instructions=instructions,
      model=model,
      tools=[{"type": "file_search"}],
    )
    assistant_id = assistant.id
    vector_store = client.vector_stores.create(name="Simple file")
    vector_store_id = vector_store.id
    # 
    # Make sure to hide the files so that nobody tries to search for the source files
    #
    file_paths_hidden = [];
    i = 0;
    for p in file_paths :
        hash = ''.join(random.choices(string.ascii_lowercase, k=6))
        ftype = p.split('.')[-1]
        filename = f"/tmp/{hash}.{ftype}"
        shutil.copy(p,filename)
        file_paths_hidden.append(filename)
        i = i + 1
    print(f"HIDDEN = {file_paths_hidden}")

    file_streams = [open(path, "rb") for path in file_paths_hidden]
    file_batch = client.vector_stores.file_batches.upload_and_poll( vector_store_id=vector_store_id, files=file_streams)
    assistant = client.beta.assistants.update(
      assistant_id=assistant.id,
      tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )
    thread = client.beta.threads.create(); 
    thread_id = thread.id
    for p in file_paths_hidden :
        os.remove(p)
    ids = {'assistant_id' : assistant_id, 'thread_id' : thread_id ,'max_tokens' : max_tokens }
    with open(json_file, 'w') as f:
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
    max_tokens = ids['max_tokens']
    assistant_id = ids['assistant_id'];
    thread_id = ids['thread_id']
    encoding = tiktoken.encoding_for_model(model)
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
        txt =   str( msg.content[0].text.value )
        tokens = encoding.encode(txt)
        print(f"MAX_TOKENS = {max_tokens} NTOKENS = {len(tokens)} REPLY = {txt}")
    print(f"Bye")
    

if __name__ == "__main__":
    main()
