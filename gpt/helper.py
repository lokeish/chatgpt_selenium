import logging
from .chatgpt import ChatGpt
import traceback

class GPTHelper(object):
    def __init__(self, config) -> None:
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.project_config = config['project_settings']


    def extract_json_from_string(self, input: str):
        try:
            start = input.find('{')
            end = input.find('}')
            js = eval(input[start:end+2])
            return js 
        except:
            pass

    def get_response(self, prompt_batch: str):
        """gets response for prompt"""
        try:
            batch_response = []
            chat_gpt = ChatGpt(self.project_config['chrome_path'], self.project_config['chromer_driver_path'])
            for prompt in prompt_batch:
                prompt = f"{self.config['chatgpt_config']['prompt']} ```{prompt}```"
                chat_gpt.send_prompt_to_chatgpt(prompt)
                response = chat_gpt.return_last_response()
                output = self.extract_json_from_string(response)
                batch_response.append(output)
            chat_gpt.shutdown()
            return batch_response
        except Exception as ex:
            print(traceback.format_exc())
            print("Unable to get response from chatgpt -", str(ex))
