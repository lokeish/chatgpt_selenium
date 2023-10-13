import traceback
import time 
import socket
import os
import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ChatGpt(object):
    login_xq    = '//button[//div[text()="Log in"]]'
    continue_xq = '//button[text()="Continue"]'
    tutorial_iq = 'radix-:ri:'
    button_tq   = 'button'
    done_xq     = '//button[//div[text()="Done"]]'

    chatbox_cq  = 'text-base'
    wait_cq     = 'text-2xl'
    reset_xq    = '//a[//span[text()="New chat"]]'
    regen_xq    = '//div[text()="Regenerate"]'
    textarea_tq = 'textarea'
    textarea_iq = 'prompt-textarea'
    gpt_xq    = '//span[text()="{}"]'
    def __init__(self, chrome_path, chrome_driver_path, project_config) -> None:
        self.chrome_path = chrome_path
        self.chrome_driver_path = chrome_driver_path
        self.project_config = project_config
        chatgpt_url = "https://chat.openai.com"
        # Get free port
        port = self.find_available_port()
        self.launch_chrome_with_remote_debugging(port=port, url=chatgpt_url)
        self.wait_for_human_verification()
        self.driver = self.setup_webdriver(port=port)


    def send_prompt_to_chatgpt(self, prompt):
        """ Sends a message to ChatGPT and waits for 20 seconds for the response """
        try:
            input_box = self.driver.find_element(by=By.XPATH, value='//textarea[contains(@placeholder, "Send a message")]')
            input_box.send_keys(prompt)
            time.sleep(5)
            input_box.send_keys(Keys.RETURN)
            time.sleep(10)
        except:
            print(traceback.format_exc())

    def wait_for_human_verification(self):
        print("You need to manually complete the log-in or the human verification if required.")

        while True:
            user_input = input(
                "Enter 'y' if you have completed the log-in or the human verification, or 'n' to check again: ").lower()
            if user_input == 'y':
                print("Continuing with the automation process...")
                break
            elif user_input == 'n':
                print("Waiting for you to complete the human verification...")
                time.sleep(5)  # You can adjust the waiting time as needed
            else:
                print("Invalid input. Please enter 'y' or 'n'.")


    def return_last_response(self):
        """Return the text of the last ChatGPT response"""
        try:
            response_elements = self.driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')
            if response_elements:
                last_response_text = response_elements[-1].text
                return last_response_text
            else:
                print("No response elements found.")
                return None
        except Exception as e:
            print("An error occurred while getting the last response:")
            print(e)
            traceback.print_exc()
            return None

    

    def return_chatgpt_conversation(self):
        """
        :return: returns a list of items, even items are the submitted questions (prompts) and odd items are chatgpt response
        """

        return self.driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')



    def setup_webdriver(self, port):
        """  Initializes a Selenium WebDriver instance, connected to an existing Chrome browser
             with remote debugging enabled on the specified port"""

        service = Service(executable_path=self.chrome_driver_path)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver


    def launch_chrome_with_remote_debugging(self, port, url):
        """ Launches a new Chrome instance with remote debugging enabled on the specified port and navigates to the
            provided url """

        def open_chrome():
            data_path = self.project_config['chrome_data_dir']
            chrome_cmd = f"{self.chrome_path} --remote-debugging-port={port} --user-data-dir={data_path} {url}"
            os.system(chrome_cmd)

        chrome_thread = threading.Thread(target=open_chrome)
        chrome_thread.start()


    def find_available_port(self):
        """ This function finds and returns an available port number on the local machine by creating a temporary
            socket, binding it to an ephemeral port, and then closing the socket. """

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]
        

    def shutdown(self):
        """ Closes the browser and terminates the WebDriver session."""
        print("Closing the browser...")
        self.driver.close()
        self.driver.quit()
    
    def wait_until_disappear(self, by, query, timeout_duration=15):
        '''
        Waits until the specified web element disappears from the page.

        This function continuously checks for the presence of a web element.
        It waits until the element is no longer present on the page.
        Once the element has disappeared, the function returns.

        Args:
            by (selenium.webdriver.common.by.By): The method used to locate the element.
            query (str): The query string to locate the element.
            timeout_duration (int, optional): The total wait time before the timeout exception. Default: 15.

        Returns:
            None
        '''
        print(f'Waiting element {query} to disappear.')
        try:
            WebDriverWait(
                self.driver,
                timeout_duration
            ).until_not(
                EC.presence_of_element_located((by, query))
            )
            print(f'Element {query} disappeared.')
        except:
            print(f'Element {query} still here, something is wrong.')
        return

    def interact(self, question : str):
        '''
        Sends a question and retrieves the answer from the ChatGPT system.

        This function interacts with the ChatGPT.
        It takes the question as input and sends it to the system.
        The question may contain multiple lines separated by '\n'. 
        In this case, the function simulates pressing SHIFT+ENTER for each line.

        After sending the question, the function waits for the answer.
        Once the response is ready, the response is returned.

        Args:
            question (str): The interaction text.

        Returns:
            str: The generated answer.
        '''

        text_area = self.driver.find_elements(By.TAG_NAME, self.textarea_tq)
        if not text_area:
            print('Unable to locate text area tag. Switching to ID search')
            text_area = self.driver.find_elements(By.ID, self.textarea_iq)
        if not text_area:
            raise RuntimeError('Unable to find the text prompt area. Please raise an issue with verbose=True')

        text_area = text_area[0]

        for each_line in question.split('\n'):
            text_area.send_keys(each_line)
            text_area.send_keys(Keys.SHIFT + Keys.ENTER)
        text_area.send_keys(Keys.RETURN)
        print('Message sent, waiting for response')
        self.wait_until_disappear(By.CLASS_NAME, self.wait_cq)
        answer = self.driver.find_elements(By.CLASS_NAME, self.chatbox_cq)[-1]
        print('Answer is ready', answer.text)
        return answer.text