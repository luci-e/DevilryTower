import json
import math
from multiprocessing import Process

files = ["common"]
copies = [3, 2, 1, 1, 1, 1, 3]

webPageHeader = """ <!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="cardsStyle.css">
</head>
<body>
"""

webPageFooter = """     </body>
</html>"""


def getIconOpeningTag(iconName):
    iconPaths = {
        "melee" : "./icons/melee.svg",
        "ranged" : "./icons/ranged.svg",
        "armour" : "./icons/armour.svg",
        "spell": "./icons/spell.svg",
        "misc": "./icons/misc.svg",
        "role_change": "./icons/shuffle.svg",
        "filler" : "./icons/misc.svg"
    }

    return f'<div class="item-icon" style="background-image:url({iconPaths[iconName]})">\n'


def generate(i):
    file = files[i]

    page = webPageHeader

    openPage = """<div class="page">\n"""
    openItem = """<div class="item">\n"""
    openTitle = """<div class="item-title">"""
    openDescription = """<div class="item-description">\n"""

    closeDiv = """</div>\n"""

    with open(f'./{file}.json', encoding='utf-8', mode='r') as cardsFileJ:
        data = json.load(cardsFileJ)

        for k,v in data.items():
            if k != "role_change":
                data[k]*= copies[i]

        itemsNo = 0
        for _k,v in data.items():
            itemsNo+=len(v)

        if( (itemsNo%4) != 0):
            data["filler"] = (4-(itemsNo%4)) * [{"name":"PlaceHolder", "description":"None", "note":"None"}]

        itemsNo = 0
        for _k,v in data.items():
            itemsNo+=len(v)

        currentItem = 0

        page += openPage

        for category, itemList in data.items():

            for item in itemList:
                page += openItem

                itemIcon = category

                if category == "weapon":
                    if "range" in item:
                        itemIcon = "ranged"
                    else:
                        itemIcon = "melee"

                page += getIconOpeningTag(itemIcon) + closeDiv
                page += openTitle + f'{item["name"]}' + closeDiv
                page += openDescription

                for k,v in item.items():
                    if (k != "name") and (k != "description") and (k != "note"):
                        page += f'{k}: {v} '
                if "description" in item.keys():
                    page += item["description"] + "<br>"
                page += item["note"] + "<br>"
                
                page += closeDiv

                page += closeDiv

                if currentItem%16 == 15 and currentItem != 0 and currentItem != itemsNo-1:
                    page += closeDiv + openPage

                currentItem += 1

        page += closeDiv
        page += webPageFooter

        with open(f'./{file}.html', encoding='utf-8', mode='w') as htmlFile:
            htmlFile.write(page)

if __name__ == '__main__':
    processes = []

    for i in range(len(files)):
        p = Process(target=generate, args=(i,))
        p.start()
        processes.append(p)
            
    for p in processes:
        p.join()