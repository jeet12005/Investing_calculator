from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Set up your API key and endpoint
API_KEY = 'Y76v9kPel7Eu2GHJ9XiWPX3XvWsnmJNO'
BASE_URL = 'https://financialmodelingprep.com/api/v3/quote/'


def get_stock_data(symbol):
    url = f"{BASE_URL}{symbol}?apikey={API_KEY}"
    response = requests.get(url)

    # Debugging output
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")

    if response.status_code == 200:
        try:
            data = response.json()
            if data:
                return data[0]  # Assuming the API returns a list with one stock object
            else:
                return None
        except ValueError as e:
            print(f"Error parsing JSON: {e}")
            return None
    else:
        print(f"Error: Unable to fetch data for {symbol}, Status Code: {response.status_code}")
        return None



def evaluate_stock(data):
    result = ""

    if data:
        # Check for PE Ratio and set a default value if not available
        # pe_ratio = data.get("peRatio", None)
        # if pe_ratio is None:
        #     result += "PE Ratio data is not available. Proceeding with other metrics.\n"

        # Add more evaluation criteria (like price, market cap, etc.)
        price = data.get("price", None)
        if price:
            result += f"Stock price: {price}\n"

        # You can add additional checks for other financial data like market cap, volume, etc.
        market_cap = data.get("marketCap", None)
        if market_cap:
            result += f"Market Cap: {market_cap}\n"

        # Example of other evaluation criteria based on your logic
        if price and market_cap:
            if market_cap > 1000000000:
                result += "This stock has a large market cap. It's worth considering!\n"
            else:
                result += "This stock has a smaller market cap.\n"

        # Return result or additional information
        return result
    else:
        return "No data available for this stock symbol."


@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if symbol:
            stock_data = get_stock_data(symbol)
            result = evaluate_stock(stock_data)
        else:
            result = "Please enter a valid stock symbol."
    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
