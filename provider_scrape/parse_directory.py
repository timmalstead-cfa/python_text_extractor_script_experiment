from typing import List, Dict
import re
from functools import reduce
from fitz import fitz, Document

pdf: Document = fitz.open(
    "./current_english_directory.pdf")

pdf_cat: str = ""

for page in pdf:
    text: str = page.getText().strip()
    if(text.startswith("SUBSTANCE USE DISORDER")):
        continue
    elif (text.find("TTY") != -1):
        continue

    splitter_word = "RENDERING"
    if(text.find(splitter_word) != -1):
        location_info: List[str] = []
        provider_info: List[str] = []

        page_with_table: List[str] = text.splitlines()

        for line in page_with_table:
            if(line.find(splitter_word) != -1):
                line_splitter_index: int = page_with_table.index(
                    line)

                location_info: List[str] = page_with_table[:line_splitter_index]
                provider_info: List[str] = page_with_table[line_splitter_index:]

        if(len(location_info)):
            location_object: Dict = {}
            for string in location_info:
                try:
                    first_word: str = string.split()[0]
                    number: int = int(first_word)
                    address_index: int = location_info.index(string)
                    location_arr: List[str] = location_info[0:address_index]
                    location_string: str = reduce(
                        lambda first_string, next_string: first_string+next_string, location_arr)
                    location_object["location_name"] = location_string.strip()
                    location_object["address"] = location_info[address_index].strip(
                    )
                    break
                except:
                    continue
            for string in location_info:
                if(string.startswith("PHONE") or string.startswith("Phone") or string.startswith("phone")):
                    phone_fax_info: str = string.lower()
                    if(phone_fax_info.find("fax") != -1):
                        phone_fax_arr: List[str] = phone_fax_info.split("fa")
                        phone_num: str = phone_fax_arr[0].split(":")[1]
                        fax_num: str = phone_fax_arr[1].split(":")[1]
                        location_object["phone"] = phone_num.strip()
                        location_object["fax"] = fax_num.strip()
                    else:
                        phone_fax_arr: List[str] = phone_fax_info.split(":")
                        location_object["phone"] = phone_fax_arr[1].strip()
                elif(string.startswith("FAX") or string.startswith("Fax") or string.startswith("fax")):
                    fax_number: str = string.split(":")[1]
                    location_object["fax"] = fax_number.strip()
                elif(string.find(":") != -1):
                    splitter: List[str] = string.split(":")
                    location_object[splitter[0].lower().strip()
                                    ] = splitter[1].strip()
            print(location_object)

        text: str = str(location_info)
        pdf_cat += text


new_pdf = open("./extracted_pdf.txt", "w")
new_pdf.write(pdf_cat)
