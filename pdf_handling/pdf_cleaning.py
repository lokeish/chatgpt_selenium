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
                    shutil.copy(pdf_path, destination_path)
                    total_no_files_moved += 1
                # For Docx format
                elif filename.endswith('.docx'):
                    docx_path = os.path.join(source_folder, filename)
                    pdf_filename = os.path.splitext(filename)[0] + ".pdf"
                    pdf_path = os.path.join(destination_folder, pdf_filename)
                    # Convert docx to pdf format
                    libreoffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"
                    command = [
                                libreoffice_path,
                                "--headless",
                                "--convert-to", "pdf",
                                "--outdir", destination_folder,
                                docx_path
                              ]
                    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()
                    total_no_files_moved += 1
                else:
                    total_no_files_skipped += 1
                    print("Skipping file -", filename)
            print("Total no of files moved -", total_no_files_moved)
            print("Total no of files skipped -", total_no_files_skipped)
            print("Required Files are moved to the temp folder for processing")
        except Exception as ex:
            print("Data moving to destination folder failed -%s", str(ex))
            self.logger.error("Data moving to destination folder failed -%s", str(ex))
            raise FilesFilterFailure

        return total_no_files_moved

    def start_cleaning(self, input_dir, output_dir):
        """main function that start files cleaning on pdf source folder"""
        no_of_files = 0
        try:
            no_of_files = self.__filter_files(input_dir, output_dir)
        except:
            raise
        return no_of_files

# For individual class testing purpose
# if __name__ == "__main__":
#     import toml 
#     config = toml.load("config.toml")
#     dc = DataCleaning(config)
#     dc.start_cleaning(config['folder_config']['input_dir'], config['folder_config']['output_dir'])
