# Required imports
import os
import subprocess
import shutil
import logging
from exceptions import FilesFilterFailure

class DataCleaning(object):
    def __init__(self, config) -> None:
        self.logger = logging.getLogger(__name__)
        self.config = config


    def __filter_files(self, source_folder, destination_folder):
        """filters required files and moves to destination folder
           * Ignores the xlsx format files
           * Converts docx to pdf format
        """
        total_no_files_moved = 0
        total_no_files_skipped = 0
        try:
            for filename in os.listdir(source_folder):
                filepath = os.path.join(source_folder, filename)
                # Exclude directories
                if os.path.isdir(filepath):
                    pass
                # For pdf format
                elif filename.endswith(".pdf"):
                    pdf_path = os.path.join(source_folder, filename)
                    destination_path = os.path.join(destination_folder, filename)
                    shutil.move(pdf_path, destination_path)
                    total_no_files_moved += 1
                # For Docx format
                elif filename.endswith('.docx'):
                    docx_path = os.path.join(source_folder, filename)
                    pdf_filename = os.path.splitext(filename)[0] + ".pdf"
                    pdf_path = os.path.join(destination_folder, pdf_filename)
                    # Convert docx to pdf format
                    command = [
                                "libreoffice",
                                "--headless",
                                "--convert-to", "pdf",
                                "--outdir", destination_folder,
                                docx_path
                              ]
                    subprocess.run(command)
                    os.remove(docx_path)
                    total_no_files_moved += 1
                else:
                    total_no_files_skipped += 1
                    print("Skipping file -", filename)
            print("Total no of files moved -", total_no_files_moved)
            print("Total no of files skipped -", total_no_files_skipped)
            print("Required Files are moved to destination file")
        except Exception as ex:
            print("Data moving to destination folder failed -%s", str(ex))
            self.logger.error("Data moving to destination folder failed -%s", str(ex))
            raise FilesFilterFailure

    def start_cleaning(self, input_dir, output_dir):
        """main function that start files cleaning on pdf source folder"""
        try:
            self.__filter_files(input_dir, output_dir)
        except:
            raise

# For individual class testing purpose
# if __name__ == "__main__":
#     import toml 
#     config = toml.load("config.toml")
#     dc = DataCleaning(config)
#     dc.start_cleaning(config['folder_config']['input_dir'], config['folder_config']['output_dir'])
