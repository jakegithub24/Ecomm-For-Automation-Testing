import sys
import time
import random
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from webdriver_manager.firefox import GeckoDriverManager

def get_args():
    parser = argparse.ArgumentParser(description="Simulate real-world product price and state changes via Selenium.")
    parser.add_argument("-u", "--url", help="Target hosted URL of the TechPrice app (e.g. http://localhost:5000)")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode.")
    return parser.parse_args()

def prompt_for_url():
    print("=" * 60)
    print("           TECHPRICE AUTOMATION CLI")
    print("=" * 60)
    try:
        url = input("Enter the hosted URL of the TechPrice app (e.g. http://localhost:5000): ").strip()
        if not url:
            print("URL cannot be empty!")
            sys.exit(1)
        if not url.startswith("http"):
            url = "http://" + url
        return url
    except (KeyboardInterrupt, EOFError):
        print("\nOperation cancelled.")
        sys.exit(0)

def main():
    args = get_args()
    url = args.url
    if not url:
        url = prompt_for_url()

    # Set up Firefox options
    options = Options()
    if args.headless:
        options.add_argument("-headless")

    print(f"\n[INFO] Starting Firefox (Gecko) driver...")
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)

    try:
        change_count = 0
        print("\n[INFO] Press Ctrl+C at any time in the console to stop the simulation.")
        
        while True:
            change_count += 1
            print(f"\n--- Change #{change_count} ---")
            
            # Step 1: Visit Login Page
            login_url = f"{url.rstrip('/')}/login"
            print(f"[INFO] Visiting Login page: {login_url}")
            driver.get(login_url)

            # Step 2: Login as Admin
            print("[INFO] Logging in as admin...")
            username_field = wait.until(EC.element_to_be_clickable((By.ID, "username")))
            password_field = driver.find_element(By.ID, "password")
            submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

            username_field.clear()
            username_field.send_keys("admin")
            password_field.clear()
            password_field.send_keys("Admin@123")
            submit_btn.click()

            # Wait for admin table to load
            wait.until(EC.presence_of_element_located((By.ID, "admin-table-body")))
            print("[SUCCESS] Logged in successfully!")

            # Step 3: Select a random product row
            rows = driver.find_elements(By.CSS_SELECTOR, "#admin-table-body tr")
            if not rows:
                print("[WARNING] No products found in the admin table! Skipping.")
                continue

            target_row = random.choice(rows)
            product_id = target_row.get_attribute("data-id")
            product_name = target_row.find_element(By.CLASS_NAME, "td-name").text
            print(f"[INFO] Target Product Selected: {product_name} (ID: {product_id})")

            # Step 4: Click the Edit button
            edit_btn = target_row.find_element(By.CLASS_NAME, "edit-btn")
            edit_btn.click()

            # Step 5: Wait for Edit Modal inputs to load
            wait.until(EC.element_to_be_clickable((By.ID, "p-name")))
            time.sleep(0.5) # Wait for modal open animation transition

            # Step 6: Perform Random Changes
            price_field = driver.find_element(By.ID, "p-price")
            state_select = Select(driver.find_element(By.ID, "p-state"))

            current_price_str = price_field.get_attribute("value")
            try:
                current_price = float(current_price_str)
            except ValueError:
                current_price = 100.0

            # Randomize Price: change by +/- 5% to 20%
            change_percent = random.uniform(0.05, 0.20)
            direction = random.choice([1, -1])
            new_price = round(current_price * (1 + direction * change_percent), 2)
            if new_price < 5: # prevent negative/free products
                new_price = round(current_price * 1.10, 2)

            # Randomize State
            states = ["In Stock", "coming soon", "out of stock", "discontinued"]
            new_state = random.choice(states)

            # Fill Inputs
            print(f"[ACTION] Updating price from ${current_price} -> ${new_price}")
            price_field.clear()
            price_field.send_keys(str(new_price))

            print(f"[ACTION] Updating state to: {new_state}")
            state_select.select_by_value(new_state)

            # Step 7: Click Save
            save_btn = driver.find_element(By.CSS_SELECTOR, "#product-form button[type='submit']")
            save_btn.click()

            # Wait for saving to complete (modal closes)
            wait.until(EC.invisibility_of_element_located((By.ID, "product-modal")))
            print("[SUCCESS] Product details updated and saved successfully!")
            time.sleep(1) # Wait for table/toast transition effects

            # Step 8: Logout
            print("[INFO] Logging out...")
            logout_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/logout')]")))
            logout_link.click()

            # Wait to load landing page
            wait.until(EC.presence_of_element_located((By.ID, "products-grid")))
            print("[SUCCESS] Logged out successfully. Ready for next session.")

            # Sleep between cycles to mimic human interaction
            sleep_time = random.randint(3, 8)
            print(f"[INFO] Sleeping for {sleep_time} seconds (Press Ctrl+C to stop)...")
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\n[INFO] Simulation stopped by user (Ctrl+C). Exiting gracefully...")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")
    finally:
        print("[INFO] Closing Firefox browser...")
        driver.quit()

if __name__ == '__main__':
    main()
