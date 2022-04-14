import requests

url = [
        {"lieux_2015.csv" : "https://www.data.gouv.fr/fr/datasets/r/31db21ef-4328-4c5e-bf3d-66a8fe82e6a2"},
        {"caracteristiques_2015.csv" : "https://www.data.gouv.fr/fr/datasets/r/185fbdc7-d4c5-4522-888e-ac9550718f71"},
        {"lieux_2016.csv" : "https://www.data.gouv.fr/fr/datasets/r/08b77510-39c4-4761-bf02-19457264790f"},
        {"caracteristiques_2016.csv" : "https://www.data.gouv.fr/fr/datasets/r/96aadc9f-0b55-4e9a-a70e-c627ed97e6f7"},
        {"lieux_2017.csv" : "https://www.data.gouv.fr/fr/datasets/r/9b76a7b6-3eef-4864-b2da-1834417e305c"},
        {"caracteristiques_2017.csv" : "https://www.data.gouv.fr/fr/datasets/r/9a7d408b-dd72-4959-ae7d-c854ec505354"},
        {"lieux_2018.csv" : "https://www.data.gouv.fr/fr/datasets/r/d9d65ca1-16a3-4ea3-b7c8-2412c92b69d9"},
        {"caracteristiques_2018.csv" : "https://www.data.gouv.fr/fr/datasets/r/6eee0852-cbd7-447e-bd70-37c433029405"},
        {"lieux_2019.csv" : "https://www.data.gouv.fr/fr/datasets/r/2ad65965-36a1-4452-9c08-61a6c874e3e6"},
        {"caracteristiques_2019.csv" : "https://www.data.gouv.fr/fr/datasets/r/e22ba475-45a3-46ac-a0f7-9ca9ed1e283a"},
        {"lieux_2020.csv" : "https://www.data.gouv.fr/fr/datasets/r/e85c41f7-d4ea-4faf-877f-ab69a620ce21"},
        {"caracteristiques_2020.csv" : "https://www.data.gouv.fr/fr/datasets/r/07a88205-83c1-4123-a993-cba5331e8ae0"}
      ]

for item in url:
    print(item)
    for name, link in item.items():
        response = requests.get(link)
        open(name, "wb").write(response.content)
