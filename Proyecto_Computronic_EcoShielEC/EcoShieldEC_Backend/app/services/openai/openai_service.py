from openai import *

class OpenAIService:
    def __init__(self, api_key: str, base_url: str, system_prompt: str, model: str = "openai/gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.messages = [{"role": "system", "content": system_prompt}]
        
    def get_response(self, user_text: str, max_tokens: int = 100, temperature: float = 0.2, response_format = "json_object"):
        self.messages.append({"role": "user", "content": user_text})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            max_completion_tokens=max_tokens,
            temperature=temperature,
            response_format=response_format
        )

        answer = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": answer})
        return answer