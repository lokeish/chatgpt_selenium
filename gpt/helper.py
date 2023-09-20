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
            for invoice_data in prompt_batch:
                prompt = f"""You are an invoice detail extractor assistant for the company named JATAH WORX INDIA PVT LTD, and you should not extract "JATAH WORX INDIA PVT LTD" as the name from the invoice. All the invoices are sent to Jatah Work India PVT LTD. Your task is to extract the name, date, and invoice number from the following invoice data provided in triple backticks ```{invoice_data}```. While extracting names, prioritize the sender's organization name over individual names if present. Extract the date value and convert it to the format "date-month-year," for example, 10-September-2022. Provide the output in JSON format, including keys for date, invoice_number, and name."""
                try:
                    chat_gpt.send_prompt_to_chatgpt(prompt)
                    response = chat_gpt.return_last_response()
                    output = self.extract_json_from_string(response)
                    batch_response.append(output)
                except:
                    batch_response.append({})
            chat_gpt.shutdown()
            return batch_response
        except Exception as ex:
            print(traceback.format_exc())
            print("Unable to get response from chatgpt -", str(ex))
