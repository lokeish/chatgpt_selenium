from gpt.chatgpt import ChatGpt
import os
import toml
import logging
from pdf_handling import pdf_cleaning, pdf_extract, pdf_helper
from gpt import helper

# load configuration file
config = toml.load('config.toml')
project_config = config['project_settings']
folder_config = config['folder_config']

# logging configuration
# logging.config.fileConfig('logging.conf', disable_existing_loggers=False)


# Required objects
pdf_clean = pdf_cleaning.DataCleaning(config)
pdf_ext = pdf_extract.PDFPreProcess(config)
gpt_helper = helper.GPTHelper(config)
pdf_helper = pdf_helper.PDFHelper()


def main(input_dir: str, output_dir: str):
    # Step -1, Data cleaning
    logging.info("Performing the data/pdf cleaning")
    # pdf_clean.start_cleaning(input_dir, output_dir='temp_extract')
    # Step -2, Extract
    pdf_files = [f for f in os.listdir('temp_extract') if os.path.isfile(os.path.join('temp_extract', f))]
    # Step -3, prepare batches
    file_batches = [pdf_files[i:i + project_config['batch_size']] for i in range(0, len(pdf_files), project_config['batch_size'])]

    for fb in file_batches:
        prompt_batch = []
        source_pdf_path_list = []
        for ind, pdf in enumerate(fb):
            source_pdf_path = os.path.join('temp_extract', pdf)
            # Extract text from pdf
            prompt = pdf_ext.extract_text(source_pdf_path)
            prompt_batch.append(prompt)
            source_pdf_path_list.append(source_pdf_path)

        # send prompt in batches to gpt to get invoice details
        batch_response = gpt_helper.get_response(prompt) if ind%5 == 0 else gpt_helper.get_response(prompt_batch)
        # Save pdf to the target folder
        pdf_helper.save_pdf(batch_response=batch_response, output_dir=output_dir, source_file_path_list=source_pdf_path_list)
    print("All files are placed in target folder with required names")

if __name__ == "__main__":
    # Prompt the user for source folder path
    print("Welcome to invoice extract!!!")
    input_dir = input("Enter source folder path (press Enter to use default location): ").strip()
    if not input_dir:
        input_dir = folder_config['input_dir']

    # Prompt the user for output directory path
    output_dir = input("Enter output directory path (press Enter to use default location): ").strip()
    if not output_dir:
        output_dir = folder_config['output_dir']

    # Validate if the paths exist
    if not os.path.exists(input_dir):
        print(f"Source folder '{input_dir}' does not exist.")
        os._exit()

    # Ensure the output directory exists or create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    main(input_dir, output_dir)