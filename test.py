from gpt import chatgpt
import toml
import logging
from pdf_handling import pdf_cleaning, pdf_extract

# load configuration file
config = toml.load('config.toml')
project_config = config['project_settings']

chatgpt = chatgpt.ChatGpt(project_config['chrome_path'], project_config['chromer_driver_path'])

# Define a prompt and send it to chatGPT
prompt = "EXtract invoice number, name of the person and date from the text provided in triple backticks. Make sure your response is in json format only. You will be penalised for being verbose so avoid being verbose. Hence simply return json response, which will be further consumed by python program"
prompt = f"{prompt} ```worldxplorer overseas consultancy shop no 03 1st floor site no 11 khata no 393 east taluk tc palya main road krishnarajapuram bangalore 560049 phone 9535372315 gstin 29airpa8024b1zf pan airpa8024b tax invoice m s, jatah worx india pvt ltd j000 invoice no is000156 no342, krishna nilayam, flat no302, invoice date 31 07 2022 3rd floor,2nd cross, 8th main btm layout 2nd stage,bangalore 560 076 gst no 29aadcj7448m1zv state code 29 airline malaysia airlines state name karnataka passengers ticket no sectors flight details travel fare k3 tax tax total date sac code 998551 vijaya battu 2323908326499 bnekulhyd mh 134 u 02 09 2022 3,16000 11,20700 14,36700 rs fourteen thousand three hundred sixtyseven only total 14,36700 e oeterms conditions for worldxplorer overseas consultancy cash payment to be made to the cashier official receipt must be obtained cheque all cheques demand drafts in payment of bill must be crossed a c payee only and drawn in favour of worldxplorer overseas consultancy late payment interest 24 per annum will be charged on all outstanding bills after due date very imp kindly check all details carefully to avoid unnecessary complications authorized signatory this is a system generated invoice, hence does not require any signature bank icici bank branch battarahalli account no 369805001443 ifsc code icic0003698```"
print("sending prompt to chatgpt")

# Prompt 1
chatgpt.send_prompt_to_chatgpt(prompt)
response = chatgpt.return_last_response()
print("first resonse --->", response)


prompt2 = "hello im lokeish, how are you"
chatgpt.send_prompt_to_chatgpt(prompt2)
r2 = chatgpt.return_last_response()
print("second respnose --->", r2)



# Close the browser and terminate the WebDriver session
chatgpt.shutdown()