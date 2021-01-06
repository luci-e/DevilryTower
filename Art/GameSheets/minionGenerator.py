import json
import math
from multiprocessing import Process

files = ["minions"]

webPageHeader = """ <!DOCTYPE html>
<html>

<head>
    <link rel="stylesheet" href="minionStyle.css">
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha256-4+XzXVhsDmqanXGHaHvgh1gMQKX40OUvDEBTu8JcmNs=" crossorigin="anonymous"></script>
</head>

<body>
    <script type="text/javascript">
    function adjustTextSize(textElement, containingElement) {
        while (textElement.height() > containingElement.height()) {
            let currentHeight = parseFloat(textElement.css("font-size"));
            console.log(currentHeight);
            textElement.css("font-size", currentHeight - 0.1);
        }
    };

    $(document).ready(function() {
        $(".minion-atk-abl-note").each(function() {
            let descriptionDiv = $(this);
            let descriptions = descriptionDiv.children("p");
            descriptions.each( function() { 
                adjustTextSize( $(this), descriptionDiv); 
                }
            );
        });
    });
    </script>
    </head>

    <body>
"""

webPageFooter = """     </body>
</html>"""


def getIconOpeningTag(iconName):
    iconPaths = {
        "Assistant Coordinator": "./icons/coordinator.svg",
        "Accountant": "./icons/accountant.svg",
        "Market Master": "./icons/market.svg",
        "Minion Resources": "./icons/minion_resources.svg",
        "Potion Seller": "./icons/cauldron.svg",
        "Information Wizard": "./icons/wizard.svg",
        "Guard": "./icons/guard.svg",
        "Janitor": "./icons/mop.svg",
        "Technical Operator": "./icons/operator.svg",
        "Intern": "./icons/intern.svg",
        "Lost Soul": "./icons/soul.svg",
        "PlaceHolder": "./icons/soul.svg"
    }

    return f'<div class="minion-icon" style="background-image:url({iconPaths[iconName]})">\n'


def generate(i):
    file = files[i]

    page = webPageHeader

    openPage = """<div class="sheet">\n"""
    openMinion = """<div class="minion">\n"""
    openTitle = """<div class="minion-title">"""
    openStats = """<div class="minion-stats">\n"""
    openDescription = """<div class="minion-description">\n"""
    openDepartment = """<div class="minion-department">\n"""
    openAtkAblNote = """<div class="minion-atk-abl-note">\n"""
    openAtkAbl = """<p class="minion-atk-abl">\n"""
    openNote = """<p class="minion-note">\n"""

    closeDiv = """</div>\n"""

    with open(f'./{file}.json', encoding='utf-8', mode='r') as cardsFileJ:
        data = json.load(cardsFileJ)

        minionNo = 0
        for _k, v in data.items():
            minionNo += len(v)

        if((minionNo % 3) != 0):
            data["filler"] = (
                3-(minionNo % 3)) * [{"name": "PlaceHolder", "stats": {"HP": "0", "MP": "0", "EP": "0", "Default stance": "Loyal to filler"}, "description": {"attacks": [{"None": "None"}]}, "note": "None"}]

        minionNo += (3-(minionNo % 3))

        currentMinion = 0

        page += openPage

        for department, minionList in data.items():

            for minion in minionList:
                page += openMinion

                page += openTitle + f'{minion["name"]}' + closeDiv

                minionIcon = minion["name"]
                page += getIconOpeningTag(minionIcon) + closeDiv

                #--------------------------------------------------#
                page += openStats

                stats = minion["stats"]

                page += f'<div class="minion-stat-item"><div class="stat-description">HP</div><div class="stat-value">{stats["HP"]}</div></div>'
                page += f'<div class="minion-stat-item"><div class="stat-description">MP</div><div class="stat-value">{stats["MP"]}</div></div>'
                page += f'<div class="minion-stat-item"><div class="stat-description">EP</div><div class="stat-value">{stats["EP"]}</div></div>'
                page += f'<div class="minion-stat-item" style="width:35mm"><div class="stat-description" >Default stance</div><div class="stat-value">{stats["Default stance"]}</div></div>'

                page += closeDiv
                #--------------------------------------------------#

                #--------------------------------------------------#
                page += openDescription

                page += openDepartment + f'Minion - {department}' + closeDiv

                description = minion["description"]

                page += openAtkAblNote
                page += openAtkAbl

                if 'attacks' in description:
                    page += '<b style="font-variant: small-caps;">Attacks</b><br>'
                    for attack in description['attacks']:
                        for name, desc in attack.items():
                            page += f'<b>{name}: </b>{desc}<br>'

                if 'abilities' in description:
                    page += '<b style="font-variant: small-caps;">Abilities</b><br>'
                    for ability in description['abilities']:
                        for name, desc in ability.items():
                            page += f'<b>{name}: </b>{desc}<br>'

                if 'equipment' in description:
                    page += f'<b style="font-variant: small-caps;">Equipment</b><br>{description["equipment"]}<br>'

                page += '</p>'

                page += openNote + f'{minion["note"]}</p>'

                page += closeDiv

                page += closeDiv
                #--------------------------------------------------#

                page += closeDiv

                if currentMinion % 3 == 2 and currentMinion != 0 and currentMinion != minionNo-1:
                    page += closeDiv + openPage

                currentMinion += 1

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
