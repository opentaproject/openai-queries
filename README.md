
## Demo using  openai assistants to query a file source.




### Prerequisites

* Clone the repo and work in the src directory
   ```
   git clone https://github.com/opentaproject/openai-queries.git
   ```
* Install the libraries
  * cd openta-queryies/src
  ```
  python3.11 -m venv env
  source env/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
  ```
* You need to have a paid account with OpenAI 
* Then go to https://auth.openai.com/log-in to authorize your account to use the API
    - Add some funds to the credit balance and get your API key; copy it down
* Add a .envrc file with the API key like this:  
   ```
   #.envrc
   export OPENAI_API_KEY=sk-proj-T0.....
   ```
 * Make sure your .envrc is loaded and your key works
``` 
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "Tell me a joke?"}]
  }'
  ```

<!-- USAGE EXAMPLES -->
## Usage

#### Run the demo
  ```
  python aitest.py
  ```
### Use other files to upload
* See aitest.py for easliy modified parameters.
 
## Sample output
  *Note a potential security issue that the name of the file can be obtained by the user. See last question below*
```
python testai.py
SETUP FROM SCRATCH
IDS = {'assistant_id': 'asst_XXXXX', 'thread_id': 'thread_XXXXX'}
QUESTION: (or 'quit' to exit): Summarize the document. 
Waiting for completion...
Waiting for completion...
Waiting for completion...
REPLY = The document is a README file for a demo project that illustrates how to use OpenAI's API for querying a file source. It provides steps to set up the project, including cloning the repository, installing required libraries, and configuring the API key. 

Key components include:
- Prerequisites for running the demo.
- Instructions on cloning the repository and installing necessary libraries using Python.
- Details on obtaining API credentials and setting up the environment to work with the OpenAI API.
- A simple usage example demonstrating how to run a demo script for interacting with the OpenAI model.

Overall, it serves as a guide for users interested in integrating OpenAI's capabilities into their applications【4:0†source】.
QUESTION: (or 'quit' to exit): How many words are there in the readme file
Waiting for completion...
Waiting for completion...
REPLY = The README file contains a total of 892 words【8:0†source】.
QUESTION: (or 'quit' to exit): What is the name of the file.
Waiting for completion...
Waiting for completion...
Waiting for completion...
REPLY = The name of the file is `README.md`【12:0†source】.
QUESTION: (or 'quit' to exit): 
```





<p align="right">(<a href="#readme-top">back to top</a>)</p>
