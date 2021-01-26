from typing import List, Dict
from functools import reduce
from re import split as regsplit

from fitz import open as fopen, Document


def find_from_word_to_word(strt_str: str, fin_str: str, lst_to_search: List) -> str:
    start_index: int = lst_to_search.index(strt_str)
    search_index: int = [lst_to_search.index(
        string) for string in lst_to_search if string.startswith(fin_str)][0]
    search_word_cat: str = ",".join(
        lst_to_search[start_index:search_index]).replace(",", " ")
    return search_word_cat


def extract_location_info(location_info: List) -> Dict:
    location_object: Dict = {}
    for string in location_info:
        try:
            if(string.upper().startswith("PO Box")):
                location_object["address"] = string
            else:
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
        if(string.upper().startswith("PHONE")):
            phone_fax_info: str = string.lower()
            if(phone_fax_info.find("fax") != -1):
                fax_text: str = find_from_word_to_word(
                    string, "Website", location_info)
                if(len(fax_text)):
                    phone_fax_arr: List[str] = fax_text.lower().split(
                        "fa")
                    phone_num: str = phone_fax_arr[0].split(":")[1]
                    fax_num: str = phone_fax_arr[1].split(":")[1]
                    location_object["phone"] = phone_num.strip()
                    location_object["fax"] = fax_num.strip()
            else:
                phone_fax_arr: List[str] = phone_fax_info.split(":")
                location_object["phone"] = phone_fax_arr[1].strip()
        elif(string.find(":") != -1):
            string_to_test: str = string.lower()

            if(string_to_test.startswith("website")):
                string_to_test: str = find_from_word_to_word(
                    string, "Contact", location_info)
            elif(string_to_test.startswith("contact")):
                string_to_test: str = find_from_word_to_word(
                    string, "Email", location_info)
            elif(string_to_test.startswith("email")):
                string_to_test: str = find_from_word_to_word(
                    string, "Population", location_info)
            elif(string_to_test.startswith("population")):
                string_to_test: str = find_from_word_to_word(
                    string, "Service", location_info)
            elif(string_to_test.startswith("service")):
                string_to_test: str = find_from_word_to_word(
                    string, "Special", location_info)
            elif(string_to_test.startswith("special")):
                string_to_test: str = find_from_word_to_word(
                    string, "Accept", location_info)
            elif(string_to_test.startswith("accept")):
                string_to_test: str = find_from_word_to_word(
                    string, "Cultural", location_info)
            elif(string_to_test.startswith("cultural")):
                string_to_test: str = find_from_word_to_word(
                    string, "ADA", location_info)
            elif(string_to_test.startswith("ada")):
                string_to_test: str = find_from_word_to_word(
                    string, "Linguistic", location_info)
            elif(string_to_test.startswith("linguistic")):
                string_to_test: str = find_from_word_to_word(
                    string, "NPI", location_info)
            splitter: List[str] = string_to_test.split(":", 1)
            if(len(splitter) == 2):
                location_object[splitter[0].lower().strip().replace(" ", "_")
                                ] = splitter[1].strip()
    return location_object


final_location_arr: List[Dict] = []

pdf: Document = fopen(
    "./current_english_directory.pdf")

for page in pdf:
    text: str = page.getText().strip()
    if(text.startswith("SUBSTANCE USE DISORDER")):
        continue
    elif (text.find("TTY") != -1):
        continue

    location_info: List[str] = []
    provider_info: List[str] = []

    splitter_word = "RENDERING"

    if(text.find(splitter_word) != -1):
        page_with_table: List[str] = text.splitlines()

        for line in page_with_table:
            if(line.find(splitter_word) != -1):
                line_splitter_index: int = page_with_table.index(
                    line)

                location_info: List[str] = page_with_table[:line_splitter_index]
                provider_info: List[str] = page_with_table[line_splitter_index:]

        if(len(location_info)):
            final_location_arr.append(extract_location_info(location_info))
    else:
        multi_org_split: List[str] = regsplit(r"NPI.*", text)
        filter_org_split: List[str] = list(filter(
            lambda item: item, multi_org_split))

        org_lines_split: List[List[str]] = list(map(
            lambda string: string.split("\n"), multi_org_split))

        cleaned_arrs: List[List[str]] = []

        for org_info in org_lines_split:
            cleaned_arrs.append(
                list(filter(lambda string: string.strip() != "", org_info)))

        # If there are more pages with titles, put them in list below
        list_of_page_titles: List[str] = [
            "PRIMARY PREVENTION", "DUI PROGRAMS", "PC 1000 PROGRAMS"]

        for title in list_of_page_titles:
            if(cleaned_arrs[0][0].startswith(title)):
                del cleaned_arrs[0][0]
                break

        for cleaned_list in cleaned_arrs:
            if(len(cleaned_list)):
                cleaned_list.append("NPI: N/A")
                final_location_arr.append(
                    extract_location_info(cleaned_list))

new_pdf = open("./extracted_pdf.txt", "w")
new_pdf.write(str(final_location_arr))
