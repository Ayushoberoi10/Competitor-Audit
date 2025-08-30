from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def check_ecommerce(url):
    try:
        if not url.startswith("http"):
            url = "http://" + url
        response = requests.get(url, timeout=5)
        html = response.text.lower()

        # Common ecommerce indicators
        indicators = ["add to cart", "buy now", "checkout", "shop", "product", "basket"]

        for keyword in indicators:
            if keyword in html:
                return True
        return False
    except:
        return False

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        client_sites = request.form.getlist("client[]")
        competitor_sites = request.form.getlist("competitor[]")

        for client, competitor in zip(client_sites, competitor_sites):
            if check_ecommerce(competitor):
                result = "✅ PASS - Competitor is ecommerce"
            else:
                result = "❌ FAIL - Not an ecommerce store"
            results.append({
                "client": client,
                "competitor": competitor,
                "status": result
            })

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
