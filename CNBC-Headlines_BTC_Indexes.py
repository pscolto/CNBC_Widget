import tkinter as tk
from tkinter import ttk
import webbrowser
import requests
from lxml import html
import yfinance as yf


def get_bitcoin_price():
    btc_data = yf.download("BTC-USD", period="2d", interval="1d")
    btc_data = btc_data.tail(2)
    price = btc_data["Close"][-1]
    change = btc_data["Close"].pct_change()[-1]
    return price, change


def get_market_data():
    symbols = ["^DJI", "^GSPC", "^IXIC"]
    market_data = yf.download(symbols, period="2d", interval="1d")
    market_data = market_data.tail(2)

    data = {}
    for symbol in symbols:
        price = market_data["Close"][symbol][-1]
        change = market_data["Close"][symbol].pct_change()[-1]
        change_percent = change * 100
        data[symbol] = (price, change, change_percent)
    return data


def get_cnbc_headlines():
    url = "https://www.cnbc.com/"
    response = requests.get(url)
    tree = html.fromstring(response.content)
    headlines = []
    for article in tree.xpath('//div[contains(@class, "LatestNews-headline")]//a'):
        headline_text = article.text_content().strip()
        if headline_text:  # Check if headline text is not empty
            headlines.append((headline_text, article.get("href")))
    return headlines[:10]



def open_link(url, label):
    webbrowser.open(url)
    label.config(foreground="purple")


def update_widget():
    bitcoin_price, bitcoin_change = get_bitcoin_price()
    bitcoin_change_percent = bitcoin_change * 100
    bitcoin_var.set(f"Bitcoin Price: ${bitcoin_price:,.2f} ({bitcoin_change_percent:+.2f}%)")
    bitcoin_label.config(foreground="green" if bitcoin_change > 0 else "red" if bitcoin_change < 0 else "black")

    market_data = get_market_data()
    display_symbols = ["DOW", "S&P", "NASDAQ"]
    for symbol, display_symbol, (price_label, price_var) in zip(["^DJI", "^GSPC", "^IXIC"], display_symbols, [(dow_label, dow_var), (sp500_label, sp500_var), (nasdaq_label, nasdaq_var)]):
        price, change, change_percent = market_data[symbol]
        price_var.set(f"{display_symbol}: {price:,.2f} ({change_percent:+.2f}%)")
        price_label.config(foreground="green" if change > 0 else "red" if change < 0 else "black")

    headlines = get_cnbc_headlines()
    for i, (headline, url) in enumerate(headlines):
        label = ttk.Label(headlines_frame, text=f"\u2022 {headline}", font=("Arial", 12, "bold"), cursor="hand2", wraplength=400)
        label.grid(column=0, row=i, sticky="w")
        label.bind("<Button-1>", lambda e, u=url, l=label: open_link(u, l))

    root.after(60000, update_widget)


root = tk.Tk()
root.title("Coltrain's Potato Widget")
root.configure(background="black")

frame = ttk.Frame(root, padding="10")
frame.grid(column=0, row=0, sticky="wens")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

bitcoin_var = tk.StringVar()
bitcoin_label = ttk.Label(frame, textvariable=bitcoin_var, background="black", font=("Arial", 12))
bitcoin_label.grid(column=0, row=0, sticky="we")

dow_var = tk.StringVar()
dow_label = ttk.Label(frame, textvariable=dow_var, background="black", font=("Arial", 12))
dow_label.grid(column=0, row=1, sticky="we")

sp500_var = tk.StringVar()
sp500_label = ttk.Label(frame, textvariable=sp500_var, background="black", font=("Arial", 12))
sp500_label.grid(column=0, row=2, sticky="we")

nasdaq_var = tk.StringVar()
nasdaq_label = ttk.Label(frame, textvariable=nasdaq_var, background="black", font=("Arial", 12))
nasdaq_label.grid(column=0, row=3, sticky="we")

headlines_frame = ttk.Frame(frame, padding="10")
headlines_frame.grid(column=0, row=4, sticky="wens")

update_widget()

root.mainloop()
