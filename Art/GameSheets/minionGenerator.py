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

    function totalHeight(elements){
        let elementsHeight = 0;
        elements.each(function(){
            elementsHeight += $(this).height();
        });

        return elementsHeight;
    }

    function adjustTextSize(textElements, containingElement) {
        while (totalHeight(textElements) > containingElement.height()-15) {
            textElements.each( function(){
                let textElement = $(this);
                let currentHeight = parseFloat(textElement.css("font-size"));
                textElement.css("font-size", currentHeight - 0.1);        
            });
        }
    };

    $(document).ready(function() {
        $(".minion-atk-abl-note").each(function() {
            let descriptionDiv = $(this);
            let descriptions = descriptionDiv.children("p");
            adjustTextSize( descriptions, descriptionDiv); 
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
        "Boss delegate": "./icons/coordinator.svg",
        "Floor responsible": "./icons/responsible.svg",
        "Lawyer": "./icons/law-book.svg",
        "Public relations": "./icons/public-relation.svg",
        "Accountant": "./icons/accountant.svg",
        "Market master": "./icons/market.svg",
        "Minion resources": "./icons/minion-resources.svg",
        "Potion seller": "./icons/cauldron.svg",
        "Information wizard": "./icons/wizard.svg",
        "Guard": "./icons/guard.svg",
        "Security officer": "./icons/badge.svg",
        "Janitor": "./icons/mop.svg",
        "Technical operator": "./icons/operator.svg",
        "Intern": "./icons/intern.svg",
        "Lost soul": "./icons/soul.svg",
        "Right hand man": "./icons/broccoli.svg",
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
    openDepXp = """<div class="minion-dep-xp">\n"""
    openDepartment = """<div class="minion-department">\n"""
    openXp = """<div class="minion-xp">\n"""
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
                3-(minionNo % 3)) * [{"name": "PlaceHolder", "stats": {"HP": "0", "MP": "0", "EP": "0", "XP":"0", "Default stance": "Loyal to filler"}, "description": {"attacks": [{"None": "None"}]}, "note": "None"}]

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

                #--------------------------------------------------#
                page += openDepXp
                page += openDepartment + f'Minion - {department}' + closeDiv
                page += openXp + f'XP: {stats["XP"]}' + closeDiv
                page += closeDiv
                #--------------------------------------------------#

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

                page += '<hr class="description-separator">'

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
