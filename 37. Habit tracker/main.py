import requests, datetime

pixela_endpoint = "https://pixe.la/v1/users"
user_params = {
    "token": "my_token",
    "username": "masicx",
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}

# response = requests.post(url=pixela_endpoint, json=user_params)
# response.raise_for_status()
# print(response.text)

graph_endpoint = f"{pixela_endpoint}/{user_params['username']}/graphs"
graph_config = {
    "id": "graph1",
    "name": "Coding Graph",
    "unit": "hours",
    "type": "float",
    "color": "ajisai"
}

headers = {
    "X-USER-TOKEN": user_params["token"]
}

# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# response.raise_for_status()
# print(response.text)

pixel_creation_endpoint = f"{graph_endpoint}/{graph_config['id']}"

today = datetime.datetime.now().strftime("%Y%m%d")
pixel_data = {
    "date": today,
    "quantity": input("How many hours did you code today? ")
}

response = requests.post(url=pixel_creation_endpoint, json=pixel_data, headers=headers)
response.raise_for_status()
print(response.text)

update_endpoint = f"{pixel_creation_endpoint}/{today}"

new_pixel_data = {
    "quantity": "10.5"
}

# response = requests.put(url=update_endpoint, json=new_pixel_data, headers=headers)
# response.raise_for_status()
# print(response.text)

delete_endpoint = f"{pixel_creation_endpoint}/{today}"

# response = requests.delete(url=delete_endpoint, headers=headers)
# response.raise_for_status()
# print(response.text)