import json

new_text = open("extracted_word.txt", "r").read()
text_to_arr = new_text.split("\n")

name_and_address = []
hours = []

for page in text_to_arr:
    if page[-1] == " ":
        hours.append(page)
    else:
        to_append = page.replace("(L)", ", Lompoc").replace(
            "(B)", ", Buellton").replace("(SY)", ", Santa Ynez").replace("(S)", ", Solvang")
        name_and_address.append(to_append)

while len(name_and_address) != len(hours):
    for i, hour in enumerate(hours):
        if hour[0] == ",":
            hours[i - 1] += hour
            del hours[i]

# print(hours)

cleaned_hours = list(
    map(lambda hour: hour.replace("-", "", 1).strip(" "), hours))

mapped_name_and_address = list(
    map(lambda name: name.split(","), name_and_address))

for i, entry in enumerate(mapped_name_and_address):
    entry.append(cleaned_hours[i])

final_txt = open("final_food_resources.py", "w")
final_txt.write(json.dumps(mapped_name_and_address))

# for entry in mapped_name_and_address:
#     entry = list(map(lambda ent: ent.strip(" "), entry))

# for final in mapped_name_and_address:
#     print(final)

# print(mapped_name_and_address)
# print(hours)

# L == Lompoc, B == Buellton, S == Solvang, SY == Santa Ynez
