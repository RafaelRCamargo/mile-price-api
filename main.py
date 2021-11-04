import requests
import pyrebase

config = {
    "apiKey": "AIzaSyCeJTmYPQUFodrvW23tNE4mDog0V6-UjPM",
    "authDomain": "mile-price-bot.firebaseapp.com",
    "projectId": "mile-price-bot",
    "storageBucket": "mile-price-bot.appspot.com",
    "messagingSenderId": "688116496009",
    "appId": "1:688116496009:web:0fb129b25cd1d0c00f3858",
    "measurementId": "G-X6FJE0M4LN",
    "databaseURL": "https://mile-price-bot-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(config)


def get_prices():
    firebase_data = firebase.database()

    # Request Payload
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "sec-ch-ua": "\"Google Chrome\";v=\"95\", \"Chromium\";v=\"95\", \";Not A Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "Referer": "https://www.bankmilhas.com.br/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    data = "[{\"pk\":1,\"value\":16000},{\"pk\":2,\"value\":12000},{\"pk\":4,\"value\":11000},{\"pk\":5,\"value\":16000},{\"pk\":6,\"value\":79000},{\"pk\":7,\"value\":35000}]"

    # Request Response
    response = requests.post(
        "https://backend.bankmilhas.com.br/api/fidelity-program/quote/",
        headers=headers,
        data=data
    )
    response = response.json()

    all = []

    # Send/Save data
    if len(response) > 1:
        i = 0
        length = len(response)
        while i < length:
            print("Quantidade:", response[i]["points"])
            print("Vender na hora:", response[i]["prePrice"])
            print("Programar a venda:", response[i]["posPrice"], "\n")

            print("Nome:", response[i]["fidelityProgram"]["name"])
            print("Logo:", response[i]["fidelityProgram"]["logo"])
            print("Company:", response[i]["fidelityProgram"]["company"])
            print("Active:", response[i]["fidelityProgram"]["active"])

            firebase_data.child(response[i]["fidelityProgram"]["company"].lower().replace(
                " ", "-")).update({"quantity": response[i]["points"]})
            firebase_data.child(response[i]["fidelityProgram"]["company"].lower().replace(
                " ", "-")).update({"prePrice": response[i]["prePrice"]})
            firebase_data.child(response[i]["fidelityProgram"]["company"].lower().replace(
                " ", "-")).update({"posPrice": response[i]["posPrice"]})
            firebase_data.child(response[i]["fidelityProgram"]["company"].lower().replace(
                " ", "-")).update({"name": response[i]["fidelityProgram"]["name"]})
            firebase_data.child(response[i]["fidelityProgram"]["company"].lower().replace(
                " ", "-")).update({"logo": response[i]["fidelityProgram"]["logo"]})
            firebase_data.child(response[i]["fidelityProgram"]["company"].lower().replace(
                " ", "-")).update({"active": response[i]["fidelityProgram"]["active"]})
            all.append({"quantity": response[i]["points"], "prePrice": response[i]["prePrice"], "posPrice": response[i]["posPrice"], "name": response[i]
                        ["fidelityProgram"]["name"], "logo": response[i]["fidelityProgram"]["logo"], "active": response[i]["fidelityProgram"]["active"]})
            i += 1

    print(all)
    firebase_data.child("all").update({"companies": all})


if __name__ == "__main__":
    get_prices()
