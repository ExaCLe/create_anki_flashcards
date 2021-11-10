import csv

from bs4 import BeautifulSoup
import os
import uuid
from highlight import highlight_script, get_styles

PATH_TO_MEDIA = os.path.join(
    "/",
    "Users",
    "leonbiermann",
    "Library",
    "Application Support",
    "Anki2",
    "Benutzer 1",
    "collection.media",
)


def extractCards(file, target, path_to_file):
    path_parts = path_to_file.split("/")
    if len(path_parts) > 1: 
        path_parts = path_parts[0:-1]
        path = "/".join(path_parts)
    else: 
        path = ""
    print("Extracting")
    soup = BeautifulSoup(file, "html.parser")
    writer = csv.writer(target, delimiter=";")

    # find all the toggle elements
    uls = soup.find_all("ul", class_="toggle")

    for ul in uls:
        details = ul.find("details")

        # extract the front side
        summary = details.find("summary")
        front = summary.text

        # extract the back side
        lists = details.findAll("ul")
        codes = details.findAll("pre")
        images = details.findAll("img")
        back = get_styles() + "<ul>"
        for list in lists:
            for li in list.contents:
                back = back + "<li>" + escape_for_anki(li.text) + "</li>"
        back = back + "</ul>"
        back += "<pre class='code code-wrap'>"
        for code in codes:
            back = (
                back
                + "<code class='code code-wrap'>"
                + escape_for_anki(code.text)
                + "</code>"
            )
        back += "</pre>"
        for image in images:
            current_path = os.path.abspath(os.path.join(path, clear_spaces(image["src"])))
            id = str(uuid.uuid4())
            os.rename(current_path, os.path.join(PATH_TO_MEDIA, id + ".png"))
            back = back + "<img src='" + id + ".png'" + "/>"
        # write the result to the file
        back = back + highlight_script()
        writer.writerow([front, back])
        print("Finished")


def clear_spaces(text):
    return text.replace("%20", " ")


def escape_for_anki(text):
    result = ""
    for char in text:
        if char == "<":
            result = result + "&lt;"
        elif char == ">":
            result = result + "&gt;"
        elif char == "&":
            result = result + "&amp;"
        else:
            result = result + char
    return result


def read_in_cards(path_to_file):
    print("File Choosen")
    with open(path_to_file) as file:
        with open("/Users/leonbiermann/Desktop/Personal Projects/createFlashCards/cards.csv", "w") as target:
            extractCards(file, target, path_to_file)
            print("Finished")


def main():
    read_in_cards("page.html")


if __name__ == "__main__":
    main()
