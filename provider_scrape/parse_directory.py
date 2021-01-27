from typing import List, Dict
from functools import reduce
from re import split as regsplit, search

from fitz import open as fopen, Document

final_location_arr: List[Dict] = []
final_provider_arr: List[Dict] = []


def location_string_extract_and_cat(strt_str: str, fin_str: str, lst_to_search: List) -> str:
    start_index: int = lst_to_search.index(strt_str)
    search_index: int = [lst_to_search.index(
        string) for string in lst_to_search if string.startswith(fin_str)][0]
    search_word_cat: str = ",".join(
        lst_to_search[start_index:search_index]).replace(",", " ")
    return search_word_cat


def location_info_extract(location_info_list: List) -> Dict:
    location_object: Dict = {}
    for string in location_info_list:
        try:
            if(string.upper().startswith("PO Box")):
                location_object["address"] = string
            else:
                address_index: int = location_info_list.index(string)
                location_arr: List[str] = location_info_list[0:address_index]
                location_string: str = reduce(
                    lambda first_string, next_string: first_string+next_string, location_arr)
                location_object["location_name"] = location_string.strip()
                location_object["address"] = location_info_list[address_index].strip(
                )
                break
        except:
            continue

    for string in location_info:
        if(string.upper().startswith("PHONE")):
            phone_fax_info: str = string.lower()
            if(phone_fax_info.find("fax") != -1):
                fax_text: str = location_string_extract_and_cat(
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
                string_to_test: str = location_string_extract_and_cat(
                    string, "Contact", location_info)
            elif(string_to_test.startswith("contact")):
                string_to_test: str = location_string_extract_and_cat(
                    string, "Email", location_info)
            elif(string_to_test.startswith("email")):
                string_to_test: str = location_string_extract_and_cat(
                    string, "Population", location_info)
            elif(string_to_test.startswith("population")):
                string_to_test: str = location_string_extract_and_cat(
                    string, "Service", location_info)
            elif(string_to_test.startswith("service")):
                string_to_test: str = location_string_extract_and_cat(
                    string, "Special", location_info)
            elif(string_to_test.startswith("special")):
                string_to_test: str = location_string_extract_and_cat(
                    string, "Accept", location_info)
            elif(string_to_test.startswith("accept")):
                string_to_test: str = location_string_extract_and_cat(
                    string, "Cultural", location_info)
            elif(string_to_test.startswith("cultural")):
                string_to_test: str = location_string_extract_and_cat(
                    string, "ADA", location_info)
            elif(string_to_test.startswith("ada")):
                string_to_test: str = location_string_extract_and_cat(
                    string, "Linguistic", location_info)
            elif(string_to_test.startswith("linguistic")):
                string_to_test: str = location_string_extract_and_cat(
                    string, "NPI", location_info)
            splitter: List[str] = string_to_test.split(":", 1)
            if(len(splitter) == 2):
                location_object[splitter[0].lower().strip().replace(" ", "_")
                                ] = splitter[1].strip()
    return location_object


def provider_string_extract_and_cat(starting_index: int, end_index: int, arr_to_search: List, cat: Dict = {"concat": True}) -> str:
    search_word_cat: str = ",".join(
        arr_to_search[starting_index:end_index])
    if(cat["concat"]):
        search_word_cat: str = search_word_cat.replace(",", " ")
    return search_word_cat


def provider_info_extract(provider_info_list: List) -> Dict:
    provider_info_dict: Dict = {
        "provider_list_name": provider_info_list[0], "provider_list": []}

    provider_info_arr: List[str] = list(map(
        lambda string: string.strip(), provider_info_list[1:]))

    npi_num_indexes: List[int] = [index for index, string in enumerate(
        provider_info_arr) if search(r'^\d{9,10}$', string)]
    npi_len: int = len(npi_num_indexes)

    training_indexes: List[int] = [index for index, string in enumerate(
        provider_info_arr) if search(r'^yes$|^no$|^pending$', string.lower())]
    train_len: int = len(training_indexes)

    first_last_name_index: int = 0
    for string in provider_info_arr:
        if(string.lower().endswith("training")):
            first_last_name_index: int = provider_info_arr.index(
                string) + 1
            break

    training_indexes_plus_one: List[int] = list(
        map(lambda num: num + 1, training_indexes))

    last_name_indexes: List[int] = [
        first_last_name_index, *training_indexes_plus_one[:-1]]
    last_len: int = len(last_name_indexes)

    # There is a weird thing where two pages are not matching up on the NPI number column and Cultural Competency Training column. I don't understand it but this seems necessary for now.
    if(sum([npi_len, train_len, last_len]) / 3 == last_len):
        for index, element in enumerate(last_name_indexes):
            single_provider_info: Dict = {}

            name_index: int = last_name_indexes[index]
            npi_index: int = npi_num_indexes[index]
            train_index: int = training_indexes[index]

            full_name: str = provider_string_extract_and_cat(
                name_index, npi_index, provider_info_arr)
            name_split: List[str] = full_name.rsplit(" ", 1)

            single_provider_info["first_name"] = name_split[1]
            single_provider_info["last_name"] = name_split[0]

            single_provider_info["npi_number_type_1"] = provider_info_arr[npi_index]

            certification_type_and_number: str = provider_string_extract_and_cat(
                npi_index + 1, train_index, provider_info_arr, {"concat": False})

            cert_split: List[str] = []

            if(certification_type_and_number.find(",") != -1):
                cert_split: List[str] = certification_type_and_number.rsplit(
                    ",", 1)
            else:
                cert_split: List[str] = certification_type_and_number.rsplit(
                    " ", 1)

            single_provider_info["license_certification_registration_type"] = cert_split[0].replace(
                ",", " ")
            single_provider_info["license_certification_registration_number"] = cert_split[1]

            single_provider_info["completed_cultural_competency_training"] = provider_info_arr[train_index].lower(
            )

            provider_info_dict["provider_list"].append(single_provider_info)
    return provider_info_dict


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
            final_location_arr.append(location_info_extract(location_info))

        if(len(provider_info)):
            final_provider_arr.append(provider_info_extract(provider_info))

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
                    location_info_extract(cleaned_list))

new_pdf = open("./extracted_pdf.txt", "w")
new_pdf.write(str([*final_location_arr, *final_provider_arr]))
