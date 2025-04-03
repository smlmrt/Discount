# 🛍️ Koton Price Tracker

An automated tool that monitors price changes on Koton's men's clothing section and sends email notifications when items go on sale.

## 📋 Features

- 🔍 Automatically scrapes product information from Koton's website
- 💾 Tracks and stores product prices locally
- 📊 Compares new prices with previously recorded prices
- 📩 Sends email notifications when price drops are detected
- 🤖 Can be configured to run automatically on a schedule

## 🛠️ Requirements

- Python 3.6+
- Chrome browser
- ChromeDriver (matching your Chrome version)
- Internet connection
- Gmail account for sending notifications

## 📦 Dependencies

- selenium: For web scraping
- smtplib: For sending emails
- json: For storing price data
- time: For managing delays during scraping
- csv: For potential data export (prepared for future use)

## ⚙️ Installation

1. Clone or download this repository:
```bash
git clone https://github.com/yourusername/koton-price-tracker.git
cd koton-price-tracker
```

2. Install required packages:
```bash
pip install selenium
```

3. Download ChromeDriver from [here](https://sites.google.com/chromium.org/driver/) that matches your Chrome browser version.

4. Place the ChromeDriver executable in your project directory or specify its path in the code.

## 🔧 Configuration

Before running the script, you need to configure your email settings:

1. Open the script in a text editor
2. Update the following variables with your information:
   - `EMAIL_SENDER`: Your Gmail address
   - `EMAIL_PASSWORD`: Your Gmail app password (see note below)
   - `EMAIL_RECEIVER`: Email address to receive notifications
   - `url`: Update with the correct Koton men's section URL

**Important Note on Gmail App Passwords:**
For security reasons, Gmail requires an "App Password" instead of your regular password. To create one:
1. Enable 2-Step Verification on your Google Account
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Select "Mail" and "Other (Custom name)"
4. Enter "Koton Price Tracker" and click "Generate"
5. Use the 16-character password generated

## 🚀 Usage

Run the script manually:
```bash
python koton_price_tracker.py
```

## 📊 How It Works

1. The script launches a headless Chrome browser (runs in the background)
2. It navigates to the Koton men's section and scrapes product information
3. The script compares current prices with previously saved prices
4. If any products have price reductions, it sends an email notification
5. All prices are saved to `previous_prices.json` for future comparisons

## 🔄 Output

When price drops are detected, you'll receive an email with:
- Product name
- Previous price
- New discounted price

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
