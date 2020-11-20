import fitz
from docx import Document
# import pandas as pd

word = Document("./CC Thrift Pocket Guide.docx")

word_cat = ""

for page in word.paragraphs:
    word_cat += page.text

new_word = open("extracted_word.txt", "w")

split_word = word_cat.split("p.m.")

new_word.write("p.m. \n".join(split_word))

pdf_path = "./Central County Resources.pdf"
pdf = fitz.open(pdf_path)

pdf_cat = ""

for page in pdf:
    text = page.getText()
    pdf_cat += text  # get plain text (is in UTF-8)"

new_pdf = open("extracted_pdf.txt", "w")
new_pdf.write(pdf_cat)
