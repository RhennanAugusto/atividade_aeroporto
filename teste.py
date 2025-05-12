import requests

url = "http://localhost:8000/api/portoes/"

portoes = [
    {"codigo": "P01", "disponivel": True}
]

for portao in portoes:
    response = requests.post(url, json=portao)
    print(f"Status Code: {response.status_code}, Response: {response.json()}")
