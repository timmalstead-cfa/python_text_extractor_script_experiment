from io import TextIOWrapper
from datetime import datetime

import requests
import fitz


def format_pdf_time(date_string: str) -> datetime:
    return datetime.strptime(date_string, "%Y%m%d%H%M%S")


provider_directory_url: str = "http://countyofsb.org/behavioral-wellness/asset.c/6074"
response: bytes = requests.get(provider_directory_url).content
fetched_directory_pdf: fitz.Document = fitz.open("pdf", response)

# html_to_save = fetched_directory_pdf[4].getText("words")
# html_file = open("./example.txt", "w")
# html_file.write(str(html_to_save))

fetched_mod_date_string: str = fetched_directory_pdf.metadata["modDate"][2:-7]
fetched_mod_date_datetime_object: datetime = format_pdf_time(
    fetched_mod_date_string)

saved_mod_date_file: TextIOWrapper = open("./saved_mod_date.txt")
saved_mod_date_datetime_object: datetime = format_pdf_time(
    saved_mod_date_file.read())

fetched_directory_is_newer: bool = fetched_mod_date_datetime_object > saved_mod_date_datetime_object

if(fetched_directory_is_newer):
    saved_mod_date_file: TextIOWrapper = open("./saved_mod_date.txt", "w")
    saved_mod_date_file.write(fetched_mod_date_string)
