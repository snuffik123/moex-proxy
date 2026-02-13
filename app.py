import requests
from flask import Flask, jsonify

app = Flask(__name__)

MOEX_URL = (
    "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json"
    "?iss.meta=off&iss.only=marketdata&marketdata.columns=SECID,LAST,BID,OFFER,LCLOSEPRICE"
)

@app.route("/prices")
def prices():
    try:
        r = requests.get(MOEX_URL, timeout=10)
        r.raise_for_status()
        data = r.json()
        rows = data["marketdata"]["data"]
        result = {}
        for row in rows:
            secid, last, bid, ask, close = row
            result[secid] = last or bid or ask or close
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
