from pathlib import Path
import requests
import fitz

# Scraping directory URL
provider_directory_url = "http://countyofsb.org/behavioral-wellness/asset.c/6074"
response = requests.get(provider_directory_url)

# Saving scraped data as PDF
# provider_directory_document = Path("./current_english_directory.pdf")
# provider_directory_document.write_bytes(response.content)

# Opening scraped data and turning into string
# current_directory_pdf = fitz.open("./current_english_directory.pdf")
current_directory_pdf = fitz.open(None, response.content, "pdf")
# current_directory_pdf_cat = ""

print(current_directory_pdf.metadata["modDate"])


# for page in current_directory_pdf:
#     text = page.getText()
#     current_directory_pdf_cat += text

# # Comparing newly scraped PDF with previously scraped PDF
# previous_directory_pdf = fitz.open("./previous_english_directory.pdf")
# previous_directory_pdf_cat = ""

# for page in previous_directory_pdf:
#     text = page.getText()
#     previous_directory_pdf_cat += text

# if(current_directory_pdf_cat != previous_directory_pdf_cat):
#     print("no!")
# else:
#     print("yes!")

# print(current_directory_pdf[3].getText("words"))
