from gpt.chatgpt import ChatGpt
import os
import toml
import shutil
import logging
from pdf_handling import pdf_cleaning, pdf_extract, pdf_helper
from gpt import helper
from logging.config import fileConfig
import sys

# load configuration file
config = toml.load('config.toml')
project_config = config['project_settings']
folder_config = config['folder_config']

# logging configuration
fileConfig('logging.conf', disable_existing_loggers=False)


# Required objects
pdf_clean = pdf_cleaning.DataCleaning(config)
pdf_ext = pdf_extract.PDFPreProcess(config)
gpt_helper = helper.GPTHelper(config)
pdf_help = pdf_helper.PDFHelper()


def main(input_dir: str, output_dir: str):
    """Main Function that does 3 things, data cleaning, data extraction, and getting resposne from chatgpt"""
    
    failed_conversion_count = 0
    failed_files_names = []
    
    # Step -1, Data cleaning
    logging.info("Performing the data/pdf cleaning")
    os.makedirs('temp_extract', exist_ok=True)
    pdf_clean.start_cleaning(input_dir, output_dir='temp_extract')

    # Step -2, Extract
    pdf_files = [f for f in os.listdir('temp_extract') if os.path.isfile(os.path.join('temp_extract', f))]

    # Step -3, prepare batches
    file_batches = [pdf_files[i:i + project_config['batch_size']] for i in range(0, len(pdf_files), project_config['batch_size'])]

    # Step -4, save pdf to target folder with required changes.
    for fb in file_batches:
        prompt_batch = []
        source_pdf_path_list = []
        for ind, pdf in enumerate(fb):
            source_pdf_path = os.path.join('temp_extract', pdf)
            # Extract text from pdf
            prompt, skip = pdf_ext.extract_text(source_pdf_path)
            if not skip:
                prompt_batch.append(prompt)
                source_pdf_path_list.append(source_pdf_path)

        # send prompt in batches to gpt to get invoice details
        batch_response = gpt_helper.get_response(prompt_batch)

        # Save pdf to the target folder
        failed_count, failed_files = pdf_help.save_pdf(batch_response=batch_response, output_dir=output_dir, source_file_path_list=source_pdf_path_list)

        failed_conversion_count += failed_count
        failed_files_names.append(failed_files)

    logging.info("All files are placed in target folder with required changes")
    print("All files are placed in target folder with required changes")

    if len(failed_files) > 0:
        print("For these files unable to extract details ->", failed_files)

    # Step -5, moved failed files to input dir
    for file in failed_files:
        shutil.move(file, input_dir)

    # Step-5, Clean the temp folder
    shutil.rmtree('temp_extract')


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
        sys.exit()

    # Ensure the output directory exists or create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    main(input_dir, output_dir)