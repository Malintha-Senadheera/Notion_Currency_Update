import requests
import datetime

# Function to fetch the USD exchange rate
def get_usd_exchange_rate(api_key, target_currency="USD"):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad response (4xx, 5xx)
        
        data = response.json()
        
        # Check if the conversion rate for the target currency exists
        if "conversion_rates" in data and target_currency in data["conversion_rates"]:
            return data["conversion_rates"][target_currency]
        else:
            print(f"Error: Target currency {target_currency} not found.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching exchange rate: {e}")
    
    return None

# Function to update the existing Notion page
def update_notion_page(notion_token, page_id, usd_rate, currency):
    url = f"https://api.notion.com/v1/pages/{page_id}"  # Use the page ID to update the existing page
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    today = datetime.date.today().isoformat()  # Current date in ISO format
    
    # Create the request payload to update the existing page
    data = {
        "properties": {
            #"Date": {"date": {"start": today}},  # Update the date
            "Name": {"title": [{"text": {"content": f"USD {currency}"}}]},  # Optional: Change the title if needed
            "Rate": {"number": usd_rate},  # Update the exchange rate
        },
    }

    try:
        # Send the request to update the page
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()  # Will raise an error for non-2xx responses
        print("Exchange rate successfully updated in Notion!")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while updating Notion: {e}")
        if response:
            print("Response content:", response.text)  # For debugging

# Replace with your actual API keys and IDs
exchange_rate_api_key = "5d673288126b7c763f6d36c1"  # Replace with your ExchangeRate-API key
notion_token = "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"  # Replace with your Notion integration token
notion_page_id = "15e4c5d0c810802db2a0fc688eb24b8d"  # Replace with the page ID of the existing "USD" page

# Fetch the exchange rate and update the Notion page
target_currency = "LKR"  # Set the target currency code (example: "LKR")
usd_rate = get_usd_exchange_rate(exchange_rate_api_key, target_currency)

if usd_rate:
    update_notion_page(notion_token, notion_page_id, usd_rate, target_currency)
else:
    print(f"Failed to fetch exchange rate for {target_currency}.")
