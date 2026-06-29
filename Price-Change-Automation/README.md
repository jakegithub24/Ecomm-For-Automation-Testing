# TechPrice — Price Change Automation Script

This directory contains a Selenium-based automation script that simulates real-world product price fluctuations and inventory status updates. It logs into the administrative console, picks a random product, randomizes its price and state, and repeats this cycle at set intervals.

---

## 🚀 How it Works

The [price_change_script.py](file:///home/parrot/Downloads/price_tracker_app/Price-Change-Automation/price_change_script.py) performs the following cycle:
1. **Admin Login**: Navigates to `/login` and signs in using the configured admin credentials.
2. **Product Selection**: Accesses the administrative dashboard and selects a random product row from the table.
3. **Random Update**:
   - Randomizes the price by +/- 5% to 20%.
   - Randomizes the inventory state among `In Stock`, `Coming Soon`, `Out of Stock`, and `Discontinued`.
4. **Save & Apply**: Saves the changes to update the database, generating a new data point in the product's price history.
5. **Admin Logout**: Safely logs out and returns to the home page.
6. **Cycle Sleep**: Sleeps for a random interval (between 1 and 5 minutes) before running the next update cycle.

---

## 🛠️ Setup & Running

### 1. Prerequisites
Ensure you have the Firefox web browser installed on your machine. The script uses Python's Selenium bindings and automatically handles GeckoDriver installation via `webdriver-manager`.

### 2. Install Dependencies
Navigate to this directory and install the required Python packages:
```bash
pip install -r requirements.txt
```
*(Dependencies specified in [requirements.txt](file:///home/parrot/Downloads/price_tracker_app/Price-Change-Automation/requirements.txt) include `selenium` and `webdriver-manager`.)*

### 3. Run the Automation
Run the script by passing the target URL of your hosted TechPrice application (local or production):
```bash
python price_change_script.py --url http://localhost:5000
```
Or run the script without any parameters to be prompted for the URL in the terminal.

#### Running in Headless Mode
To run the browser in the background without opening a physical window, use the `--headless` flag:
```bash
python price_change_script.py --url http://localhost:5000 --headless
```

To stop the simulation at any time, press `Ctrl+C` in the console.
