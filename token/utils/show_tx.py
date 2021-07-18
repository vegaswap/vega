import brownie
import requests

# def write_abi():
#     response = requests.get(
#         f"https://api.bscscan.com/api?"
#         f"module=contract&"
#         f"action=getabi&"
#         f"address={contract_address}"
#     )

#     abi = response.json()["result"]
#     with open("cake.abi", "w") as f:
#         f.write(abi)

# url = "https://api.etherscan.io/api?module=proxy&action=eth_call&to=0x4CF488387F035FF08c371515562CBa712f9015d4&data=0x5c975abb&apikey=6QTQHW78K14537RUJZXJXRGGJVGKG13WBA"
url = "http://api.etherscan.io/api?module=account&action=tokentx&address=%s&startblock=0&endblock=999999999&sort=asc&apikey=%s"
apikey = "6QTQHW78K14537RUJZXJXRGGJVGKG13WBA"

private_funding = "0x0bb097042d12af8a7cb2878b30a6b04a33d4ce6b"
seed_funding = "0xf55bb51cfab743eeef69d529ea6ebd8be72163c9"


def show_address(addr):
    response = requests.get(url % (addr, apikey))
    txs = response.json()["result"]
    # print(txs)
    totalin = 0
    for tx in txs:
        # print(tx)
        # fromto = tx["from"] == seed_funding
        isto = tx["to"] == addr
        if isto:
            v = int(tx["value"]) / 10 ** 6
            totalin += v
            h = tx["hash"]
            print(tx["tokenSymbol"], ",", v, ",", h)
    print(totalin)


# show_address(seed_funding)
show_address(private_funding)

# response.json()["result"]

# txid = "0xf8dfdfe2736e51650ed53b1bf4218148f67efcebcaaf1b592039a9b900f536bc"
