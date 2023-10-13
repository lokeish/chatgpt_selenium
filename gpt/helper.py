import logging
from .chatgpt import ChatGpt
import traceback
import json
from exceptions import IncorrectExtraction

class GPTHelper(object):
    def __init__(self, config) -> None:
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.project_config = config['project_settings']


    def extract_json_from_string(self, input: str):
        try:
            input = str(input)
            start = input.find('{')
            positions = []
            end_pos = input.find('}')
            while end_pos != -1:
                positions.append(end_pos)
                end_pos = input.find('}', end_pos+1)
            max_end_pos = max(positions)
            json_string = input[start:max_end_pos+2]
            output = json.loads(json_string)
            return output
        except:
            pass

    def get_response(self, prompt_batch: str):
        """gets response for prompt"""
        try:
            batch_response = []
            chat_gpt = ChatGpt(self.project_config['chrome_path'], self.project_config['chromer_driver_path'], self.project_config)
            for invoice_data in prompt_batch:
                curr_count = 0
                retry_count = self.project_config['retry_count']
                success_flag = False
                while curr_count < retry_count:
                    prompt = f"""You are an invoice detail extractor assistant for the company named JATAH WORX INDIA PVT LTD, and you should not extract "JATAH WORX INDIA PVT LTD" or "NEUTRINOS Technologies" as the name from the invoice. All the invoices are sent to Jatah Work India PVT LTD. Your task is to extract the name, date, and invoice number from the following invoice data provided in triple backticks ```{invoice_data}```. {"While extracting names, prioritize the sender's organization name over individual names if present." if retry_count > 1 else ""}. Extract the date value and convert it to the format "date-month-year," for example, 10-September-2022. Provide the output in JSON format only without being verbose, including keys for date, invoice_number, and name."""
                    try:
                        chat_gpt.send_prompt_to_chatgpt(prompt)
                        response = chat_gpt.return_last_response()
                        output = self.extract_json_from_string(response)
                        if "jatah"  in output.get('name','').lower() or "neutrinos" in output.get('name', '').lower():
                            raise IncorrectExtraction
                        curr_count = retry_count
                        success_flag = True
                        batch_response.append(output)
                    except:
                        curr_count += 1
                        pass
            if not success_flag:
                batch_response.append({})
                
            chat_gpt.shutdown()
            return batch_response
        except Exception as ex:
            print(traceback.format_exc())
            print("Unable to get response from chatgpt -", str(ex))

# # test chatgpt
# if __name__ == "__main__":
#     import toml 
#     config = toml.load("config.toml")
#     project_config =  config['project_settings']
#     chat_gpt = ChatGpt(project_config['chrome_path'], project_config['chromer_driver_path'], project_config)
#     chat_gpt.send_prompt_to_chatgpt("hi how are you?")
#     response = chat_gpt.return_last_response()
#     print(response)
#     chat_gpt.shutdown()