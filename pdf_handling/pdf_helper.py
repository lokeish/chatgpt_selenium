import os  
import shutil
import re
import traceback

class PDFHelper(object):
    def __init__(self) -> None:
        pass 

    def save_pdf(self, batch_response, output_dir, source_file_path_list):
        """Save pdf file in targer folder with invoice id, name of person and date as file name"""
        failed_count = 0
        failed_files = []
        try:
            for ind, response in enumerate(batch_response):
                try:
                    dt = self.check_keys(response)
                    destination_file_name = f"{dt['name']}_{dt['invoice']}_{dt['date']}.pdf"
                    clean_name = self.clean_string(destination_file_name)
                    destination_file_path = os.path.join(output_dir, clean_name)
                    shutil.copy(source_file_path_list[ind], destination_file_path)
                except Exception as ex:
                    failed_count += 1
                    failed_files.append(source_file_path_list[ind])
                    print(f"Unable to save pdf - {source_file_path_list[ind]}")

        except Exception as ex:
            print(traceback.format_exc())
            print("Unable to save pdf in target folder -", str(ex))

        return failed_count, failed_files

    def check_keys(self, details):
        s1 = {}
        sd = ['name', 'date', 'invoice']
        for key, val in details.items():
            for k in sd:
                if k in key:
                    s1[k] = val
        return s1
    
    def clean_string(self, input_string):
        # Define a regular expression pattern to match special characters and spaces
        pattern = r'[~`!@#$%^&*()+=<>?:"{}|/\\\[\],;\'\s]'
        
        # Use re.sub to replace matched characters with an empty string
        cleaned_string = re.sub(pattern, '', input_string)
        
        return cleaned_string
    


# For testing purpose
# if __name__ == "__main__":
#     pd = PDFHelper()
#     details = {'invoice_number': '005/2022-2023', 'name': 'AnupRameshChandVarma', 'date': 'O1stSeptember    2022'}
#     pd.save_pdf(details, '/data/classifier_data/testing', 'temp_extract/AnupVarmaSeptemberinvoice.pdf')