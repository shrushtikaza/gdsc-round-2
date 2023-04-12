from dotenv import load_dotenv 
import openai 
import os 

load_dotenv()

openai.api_key = os.getenv('CHATGPT_API_KEY')

def chatgpt_response(prompt) : 
    response = openai.Completion.create(
        model = "text-babbage-001",
        prompt = prompt,
        temperature = 0.3,
        max_tokens = 250
    )
    response_dict = response.get("choices")
    if response_dict and len(response_dict) > 0 :
        prompt_response = response_dict[0]["text"]
    return prompt_response 
