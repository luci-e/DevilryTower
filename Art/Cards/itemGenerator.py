import json
import math
from multiprocessing import Process

files = ["common", "uncommon", "rare", "epic", "legendary"]
copies = [3, 2, 1, 1, 1, 4]

webPageHeader = """ <!DOCTYPE html>
<html>
<head>
    <style>

        @page{
            size: A4 portrait;
        }

        .page{
            display: flex;
            flex-direction: column;
            justify-content: space-evenly;
            page-break-after : always;
        }

        .item-row{
            display: flex;
            justify-content: space-evenly;
            width: 210mm;
            background-color: green;
            border: 1px solid black;
        }


        .item{
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
            justify-content: space-around;
            height: 67mm;
            width: 47mm;
            background-color: red;
            border: 1px solid black;
        }

        .item-title{
            width: 85%;
            flex-grow: 0;
            margin: 1mm;
            border: 1px solid black;
            padding: 1mm;
        }

        .item-description{
            font-size: 3.5mm;
            width: 85%;
            margin: 1mm;
            border: 1px solid black;
            flex-grow: 2;
            padding: 1mm;
        }

        body {
            background-color: linen;
        }

    </style>
</head>
<body>
"""

webPageFooter = """     </body>
</html>"""

def generate(i):
    processes = []
    file = files[i]

    page = webPageHeader

    openPage = """<div class="page">\n"""
    openRow = """<div class="item-row">\n"""
    openItem = """<div class="item">\n"""
    openTitle = """<div class="item-title">"""
    openDescription = """<div class="item-description">\n"""

    closeDiv = """</div>\n"""

    with open(f'./{file}.json', encoding='utf-8', mode='r') as cardsFileJ:
        data = json.load(cardsFileJ)
        items = data["items"]*copies[i]

        if(i == 0):
            with open(f'./role_change.json', encoding='utf-8', mode='r') as role_changeJ:
                roles = json.load(role_changeJ)
                items += roles["items"]

        itemsNo = len(items)

        if( (itemsNo%4) != 0):
            items += (4-(itemsNo%4)) * [{"name":"PlaceHolder", "description":"None", "note":"None"}]

        itemsNo = len(items)

        pagesNo = math.ceil(itemsNo/16)
        rowsNo = math.ceil(itemsNo/4)

        currentItem = 0
        currentRow = 0

        for _pageno in range(pagesNo):
            page += openPage
            for r in range(4):
                if currentRow+1 <= rowsNo and currentItem+1 < itemsNo:
                    page += openRow
                    currentRow += 1
                    for i in range(4):
                        if currentItem+1 <= itemsNo:
                            item = items[currentItem]
                            page += openItem + openTitle
                            page += f'{item["name"]}' + closeDiv
                            page += openDescription

                            for k,v in item.items():
                                if (k != "name") and (k != "description") and (k != "note"):
                                    page += f'{k}: {v} '
                            if "description" in item.keys():
                                page += item["description"] + "<br>"
                            page += item["note"] + "<br>"

                            currentItem += 1
                            page += closeDiv + closeDiv
                    page += closeDiv
            currentRow = 0
            page += closeDiv
        page += webPageFooter

        with open(f'./{file}.html', encoding='utf-8', mode='w') as htmlFile:
            htmlFile.write(page)
            
    for p in processes:
        p.join()

if __name__ == '__main__':
    processes = []

    for i in range(len(files)):
        p = Process(target=generate, args=(i,))
        p.start()
        processes.append(p)
            
    for p in processes:
        p.join()