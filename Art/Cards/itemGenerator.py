import json
import math
from multiprocessing import Process

file = "items.json"
copies = {
        "Common Items": 3,
         "Uncommon Items": 2,
         "Rare Items": 1,
         "Epic Items": 1,
         "Legendary Items": 1,
         "Special Items": 3}

webPageHeader = """ <!DOCTYPE html>
<html>
<head>
<script
  src="https://code.jquery.com/jquery-3.5.1.slim.min.js"
  integrity="sha256-4+XzXVhsDmqanXGHaHvgh1gMQKX40OUvDEBTu8JcmNs="
  crossorigin="anonymous"></script>
<link rel="stylesheet" href="cardsStyle.css">
</head>
<body>
<script type="text/javascript">

$(document).ready( function() {
    $(".item-description").each( function(){
        let descriptionDiv = $(this);
        let descriptionText = descriptionDiv.children("p").first();

        while( descriptionText.height() > descriptionDiv.height() ){
            let currentHeight = parseFloat(descriptionText.css("font-size"));
            descriptionText.css("font-size", currentHeight - 0.5);
        }
    } )
});
</script>
"""

webPageFooter = """     </body>
</html>"""


def getIconOpeningTag(iconName):
    iconPaths = {
        "melee": "./icons/melee.svg",
        "ranged": "./icons/ranged.svg",
        "armour": "./icons/armour.svg",
        "spells": "./icons/spell.svg",
        "miscellaneous": "./icons/misc.svg",
        "role change": "./icons/shuffle.svg",
        "filler": "./icons/misc.svg"
    }

    return f'<div class="item-icon" style="background-image:url({iconPaths[iconName]})">\n'


def getStatIcon(statName, statValue):
    iconPaths = {
        "slots": "./icons/slots.svg",
        "uses": "./icons/uses.svg",
        "hits": "./icons/hits.svg",
        "ticks": "./icons/ticks.svg",
        "range": "./icons/range.svg",
        "mana": "./icons/mana.svg",
        "damage": "./icons/damage.svg",
        "resistance": "./icons/resistance.svg"
    }

    if statValue == "Infinity":
        statValue = "&infin;"

    if statName in iconPaths:
        return f'<div class="stat"><img class="stat-icon" src="{iconPaths[statName]}">:{statValue}&nbsp;</div>\n'


def generate(itemCategory, data):
    page = webPageHeader

    openPage = """<div class="page">\n"""
    openItem = """<div class="item">\n"""
    openTitle = """<div class="item-title">"""
    openDescription = """<div class="item-description"><p>"""
    openStats = """<div class="item-stats">\n"""

    closeDiv = """</div>\n"""


    for k, v in data.items():
        if k != "role change":
            data[k] *= copies[itemCategory]

    itemsNo = 0
    for _k, v in data.items():
        itemsNo += len(v)

    if((itemsNo % 4) != 0):
        data["filler"] = (
            4-(itemsNo % 4)) * [{"name": "PlaceHolder", "description": "None", "note": "None"}]

    itemsNo += (4-(itemsNo % 4))

    currentItem = 0

    page += openPage

    for category, itemList in data.items():

        for item in itemList:
            page += openItem

            itemIcon = category

            if category == "weapons":
                if "range" in item:
                    itemIcon = "ranged"
                else:
                    itemIcon = "melee"

            page += getIconOpeningTag(itemIcon) + closeDiv
            page += openTitle + f'{item["name"]}' + closeDiv

            page += openDescription
            if "description" in item:
                page += item["description"] + "<br><br>"

            page += f'<i style="font-weight: lighter; color: lightslategrey;">{item["note"]}</i></p>'
            page += closeDiv

            page += openStats

            if "slots" in item:
                page += getStatIcon("slots", item["slots"])
            if "uses" in item:
                page += getStatIcon("uses", item["uses"])
            if "hits" in item:
                page += getStatIcon("hits", item["hits"])
            if "ticks" in item:
                page += getStatIcon("ticks", item["ticks"])
            if "range" in item:
                page += getStatIcon("range", item["range"])
            if "mana" in item:
                page += getStatIcon("mana", item["mana"])
            if "damage" in item:
                page += getStatIcon("damage", item["damage"])
            if "resistance" in item:
                page += getStatIcon("resistance", item["resistance"])

            page += closeDiv

            page += closeDiv

            if currentItem % 16 == 15 and currentItem != 0 and currentItem != itemsNo-1:
                page += closeDiv + openPage

            currentItem += 1

    page += closeDiv
    page += webPageFooter

    with open(f'./{itemCategory}.html', encoding='utf-8', mode='w') as htmlFile:
        htmlFile.write(page)


if __name__ == '__main__':
    processes = []

    with open(f'./{file}', encoding='utf-8', mode='r') as cardsFileJ:
        data = json.load(cardsFileJ)

        for k,v in data.items():
            p = Process(target=generate, args=(k,v,))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()
