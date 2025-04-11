
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
  See line 21 n aitest.py
### Give other instructions
 







<p align="right">(<a href="#readme-top">back to top</a>)</p>
