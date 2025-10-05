import os
import requests
from dotenv import load_dotenv

load_dotenv()


class CloudflareLLM:
    def __init__(self):
        self.token = os.getenv("CLOUDFLARE_AUTH_TOKEN")
        self.account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")

        if not self.token or not self.account_id:
            raise ValueError("CLOUDFLARE_AUTH_TOKEN или CLOUDFLARE_ACCOUNT_ID не заданы в .env")

        self.url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/@hf/google/gemma-7b-it"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def get_solution(self, task_text: str) -> str:
        """Отправляем текст задачи в Cloudflare LLM и получаем ответ"""
        payload = {
            "messages": [
                {"role": "system", "content": "You are a friendly assistant"},
                {"role": "user", "content": f"Объясни, как решить эту задачу:\n{task_text}"}
            ]
        }

        try:
            response = requests.post(self.url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()

            if "result" in data and "response" in data["result"]:
                return data["result"]["response"]

            return "Нет ответа от LLM"
        except requests.exceptions.RequestException as e:
            return f"Ошибка при запросе к Cloudflare: {e}"

