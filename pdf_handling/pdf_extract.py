from pdf2image import convert_from_path
import tempfile
import easyocr
import traceback
import os
import uuid
import re
from exceptions import OcrFailure, TextCleaningFailure

class PDFPreProcess(object):

    def __init__(self, config) -> None:
        self.ocr = easyocr.Reader(lang_list=["en"])
        self.config = config['folder_config']
        self.block_words = ["ledger", "quotation", "timesheet", "time sheet"]

    def __get_pdf_as_text(self, pdf_path):
        output_path = self.config['temp_dir']
        try:
            ocr_results = []
            text = []
            uuid_list = []

            # Store Pdf with convert_from_path function
            images = convert_from_path(pdf_path)
            for img in images:
                img_uuid = uuid.uuid4()
                uuid_list.append(img_uuid)
                img.save(f'{output_path}/{img_uuid}.jpg', 'JPEG')

            for i in range(len(images)):
                img_path = os.path.join(output_path, f"{uuid_list[i]}.jpg")
                result = self.ocr.readtext(img_path)
                ocr_results.append(result)
                os.remove(os.path.join(output_path, f"{uuid_list[i]}.jpg"))

            for tup in ocr_results[0]:
                text.append(tup[1])

            return " ".join(text)
        except Exception as ex:
            print("Unable to perform text extraction -%s", str(ex))
            raise OcrFailure


    def __clean_text(self, text):
        """This function applies data pre processing on the provided text"""
        output = ""

        try:
            # Step -1, convert to lower case
            text = text.lower()
            # Step -2, remove extra spaces
            text = re.sub(r'\s+', ' ', text)
            # Step -3, remove special symbols except for /
            text = re.sub(r'[^\w\s,/]|_{2,}', '', text)
            # Allow / in between numbers
            text = re.sub(r'(\w)\s?/\s?(\w)', r'\1 \2', text)
            # Step -5, remove extra spaces
            text = re.sub(r'\s+', ' ', text)
            return text
            
        except Exception as ex:
            print("Unable to pre process the data -", str(ex))
            raise TextCleaningFailure
    
    def extract_text(self, pdf_path):
        skip = True
        try:
            respone = self.__get_pdf_as_text(pdf_path)
            # clean_text = self.__clean_text(respone)
            if any(word in respone for word in self.block_words):
                return "", skip
             
            return respone, False
        except:
            raise


