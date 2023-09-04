# ChatGPT Selenium Invoice Extractor

This project utilizes ChatGPT and Selenium to extract invoice information, including the invoice number, date, and name of the person, from a given input. Users can customize the prompt by modifying the `config.toml` file to suit their needs.

## Getting Started

Follow these steps to set up and run the project:

### Prerequisites

1. Python 3.x installed on your system.
2. Chrome web browser installed.
3. ChromeDriver installed for Selenium. You can download it from [here](https://sites.google.com/chromium.org/driver/).
4. Clone this repository to your local machine.

### Installation

1. Navigate to the project directory:

   ```bash
   cd chatgpt_selenium
   ```
 
 2. Install required packages
    ```bash
    pip install -r requirements.txt
    ```
    
### Usage

1. Place the files you want to process in the source folder.
2. Customize the ChatGPT prompt in the config.toml file according to your requirements. 
3. Currently it extracts invoice number, date and name of the person, and the each file present in source folder will be placed in destination folder with pdf file name as <name_of_the_person>_<invoice_number>_<date>.
4. If any customization is required for your own usecase feel free to modify and raise the pr to merge as a feature.

    ```bash
    python main.py
    ```
    
### Note: 
If you need to add/update any extra details to the prompt please go to the `config.toml` and modify the prompt under project_settings.