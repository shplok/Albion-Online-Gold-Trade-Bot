import requests
from datetime import datetime, timedelta
import schedule
import time
import pyautogui
import cv2
import pytesseract
import numpy as np
from PIL import ImageGrab
import sys
import keyboard
import random


pytesseract.pytesseract.tesseract_cmd = r'YOUR PATH TO TESSERACT HERE INCLUDING "tesseract.exe"'

# Constants


MONITOR_RESOLUTION_FACTOR_X = 1
MONITOR_RESOLUTION_FACTOR_Y = 1

INTERVAL = 0.15  # Interval in minutes
MARKET_COORDINATES_X, MARKET_COORDINATES_Y = 1694 * MONITOR_RESOLUTION_FACTOR_X, 30 * MONITOR_RESOLUTION_FACTOR_Y
SELECT_ORDERS_X, SELECT_ORDERS_Y = 812 * MONITOR_RESOLUTION_FACTOR_X, 977 * MONITOR_RESOLUTION_FACTOR_Y
CHECK_X, CHECK_Y, CHECK_WIDTH, CHECK_HEIGHT = 568 * MONITOR_RESOLUTION_FACTOR_X, 521 * MONITOR_RESOLUTION_FACTOR_Y, 50, 30
SILVER_CHECK_X, SILVER_CHECK_Y, SILVER_CHECK_WIDTH, SILVER_CHECK_HEIGHT = 570 * MONITOR_RESOLUTION_FACTOR_X, 559 * MONITOR_RESOLUTION_FACTOR_Y, 200, 30

BUY_GOLD_INPUT_COORDINATES_X, BUY_GOLD_INPUT_COORDINATES_Y = 596 * MONITOR_RESOLUTION_FACTOR_X, 708 * MONITOR_RESOLUTION_FACTOR_Y
SELL_GOLD_INPUT_COORDINATES_X, SELL_GOLD_INPUT_COORDINATES_Y = 607 * MONITOR_RESOLUTION_FACTOR_X, 861 * MONITOR_RESOLUTION_FACTOR_Y

BUY_SILVER_INPUT_COORDINATES_X, BUY_SILVER_INPUT_COORDINATES_Y = 777 * MONITOR_RESOLUTION_FACTOR_X, 712 * MONITOR_RESOLUTION_FACTOR_Y
SELL_SILVER_INPUT_COORDINATES_X, SELL_SILVER_INPUT_COORDINATES_Y = 761 * MONITOR_RESOLUTION_FACTOR_X, 855 * MONITOR_RESOLUTION_FACTOR_Y

BUY_ORDER_COORDINATES_X, BUY_ORDER_COORDINATES_Y = 1399 * MONITOR_RESOLUTION_FACTOR_X, 716 * MONITOR_RESOLUTION_FACTOR_Y
SELL_ORDER_COORDINATES_X, SELL_ORDER_COORDINATES_Y = 1410 * MONITOR_RESOLUTION_FACTOR_X, 858 * MONITOR_RESOLUTION_FACTOR_Y

CONFIRM_BUY_ORDER_X, CONFIRM_BUY_ORDER_Y = 1158 * MONITOR_RESOLUTION_FACTOR_X, 641 * MONITOR_RESOLUTION_FACTOR_Y
CONFIRM_SUBMITTED_X, CONFIRM_SUBMITTED_Y = 963 * MONITOR_RESOLUTION_FACTOR_X, 520 * MONITOR_RESOLUTION_FACTOR_Y

CONFIRM_SELL_ORDER_X, CONFIRM_SELL_ORDER_Y = 930 * MONITOR_RESOLUTION_FACTOR_X, 614 * MONITOR_RESOLUTION_FACTOR_Y


CLOSE_MARKET_X, CLOSE_MARKET_Y = 1458 * MONITOR_RESOLUTION_FACTOR_X, 168 * MONITOR_RESOLUTION_FACTOR_Y

RANDOM_MOVEMENT_INTERVAL = random.randint(3, 10)

skip_next_run_until = None  # Global flag for skip timing
last_movement_time = datetime.now()  # Initialize the last movement time


while True:
    try:
        print("running...")
        print(r"""
     ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___  ___     
    /  /\/  /\/  /\/  /\/  /\/  /\/  /\/  /\/  /\/  /\/  /\/  /\/  /\    
   /  /:/  /:/  /:/  /:/  /:/  /:/  /:/  /:/  /:/  /:/  /:/  /:/  /::\   
  /  /:/  /:/  /:/  /:/  /:/  /:/  /:/  /:/  /:/  /:/  /:/  /:/  /:/\:\  
 /  /:/  /:/  /:/  /:/  /:/  /:/  /:/  /:/  /:/  /:/  /:/  /:/  /:/  \:\ 
/__/:/__/:/__/:/__/:/__/:/__/:/__/:/__/:/__/:/__/:/__/:/__/:/__/:/ \__\:\
            """)
        print(r"""
                      _                 _ _             _           _   
                     | |               | (_)           | |         | |  
 ___  ___  _   _ _ __| |_ _ __ __ _  __| |_ _ __   __ _| |__   ___ | |_ 
/ __|/ _ \| | | | '__| __| '__/ _` |/ _` | | '_ \ / _` | '_ \ / _ \| __|
\__ | (_) | |_| | |  | |_| | | (_| | (_| | | | | | (_| | |_) | (_) | |_ 
|___/\___/ \__, |_|   \__|_|  \__,_|\__,_|_|_| |_|\__, |_.__/ \___/ \__|
            __/ |                                  __/ |                
           |___/                                  |___/                 
             """)
        print(r"""
___   __   __   __   __   __   __   __   __   __   __   __   __     ___              
\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\ /  /:/
 \  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  /:/ 
  \  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\/:/  
   \  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \:\  \::/   
    \__\/\__\/\__\/\__\/\__\/\__\/\__\/\__\/\__\/\__\/\__\/\__\/\__\/    

            """)

        relevant_hours = int(input("Enter the number of past hours to fetch data for: "))
        if relevant_hours <= 0:
            print("Please enter a positive number.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a valid integer.")


def focus_game_window():
    pyautogui.getWindowsWithTitle("Albion Online Client")[0].activate()


def select_order_mode():
    pyautogui.moveTo(SELECT_ORDERS_X, SELECT_ORDERS_Y)
    pyautogui.click()


def capture_screen(x, y, width, height):
    screen = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    screen_np = np.array(screen)
    return screen_np

def extract_numbers(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 60, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(binary_image, config='--psm 7')
    print(f"Extracted text: {text}")  # Debug output
    
    # Remove any non-digit characters except 'k' and '.'
    cleaned_text = ''.join(char for char in text if char.isdigit() or char in 'k.')
    
    try:
        if 'k' in cleaned_text:
            # Remove 'k' and convert to float, then multiply by 1000
            number = float(cleaned_text.replace('k', '')) * 1000
        else:
            # Convert to float
            number = float(cleaned_text)
        
        # Round to nearest integer
        return round(number)
    except ValueError:
        print(f"Error parsing number from text: {cleaned_text}")
        return None

def check_number():
    screen = capture_screen(CHECK_X, CHECK_Y, CHECK_WIDTH, CHECK_HEIGHT)
    number = extract_numbers(screen)
    print(f"Extracted number: {number}")
    return number if number is not None else 0

def check_silver_quantity():
    screen = capture_screen(SILVER_CHECK_X, SILVER_CHECK_Y, SILVER_CHECK_WIDTH, SILVER_CHECK_HEIGHT)
    quantity = extract_numbers(screen)
    print(f"Extracted silver quantity: {quantity}")
    return quantity if quantity is not None else 0

def contained_random_movement():
    random_x = random.randint(350, 1920)
    random_y = random.randint(41, 900)
    pyautogui.moveTo(random_x, random_y)
    time.sleep(random.randint(1, 3))
    pyautogui.click(button="right")

def fetch_gold_data():
    end_date = datetime.now()
    start_date = end_date - timedelta(hours=12)
    
    start_date_str = start_date.strftime('%m-%d-%Y')
    end_date_str = end_date.strftime('%m-%d-%Y')

    url = f'https://west.albion-online-data.com/api/v2/stats/gold?date={start_date_str}&end_date={end_date_str}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def process_gold_prices(data):
    return [entry['price'] for entry in data if 'price' in entry]

def calculate_thresholds(prices):
    if not prices:
        return None, None
    
    min_price = min(prices)
    max_price = max(prices)
    
    buy_threshold = min_price + 1
    sell_threshold = max_price - 1
    
    return buy_threshold, sell_threshold

def input_gold_price(extracted_number, x, y):
    if extracted_number is not None:
        pyautogui.moveTo(x, y)
        pyautogui.click()
        pyautogui.typewrite(str(round(extracted_number)))
        print(f"Input number {round(extracted_number)} at coordinates ({x}, {y})")
    else:
        print("No valid number to input.")

def input_silver_price(threshold, x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()
    pyautogui.typewrite(str(round(threshold)))
    print(f"Input number {round(threshold)} at coordinates ({x}, {y})")

def open_market():
    pyautogui.moveTo(MARKET_COORDINATES_X, MARKET_COORDINATES_Y)
    time.sleep(0.55)  # Small delay before clicking
    pyautogui.click()

def buy_gold(buy_threshold, extracted_number, silver_quantity):
    if extracted_number == 0:
        print(f"Buying gold at price: {buy_threshold}")
        silver_input = silver_quantity // buy_threshold
        input_gold_price(silver_input, BUY_GOLD_INPUT_COORDINATES_X, BUY_GOLD_INPUT_COORDINATES_Y)
        time.sleep(0.69)
        
        input_silver_price(buy_threshold, BUY_SILVER_INPUT_COORDINATES_X, BUY_SILVER_INPUT_COORDINATES_Y)
        time.sleep(0.46)
        pyautogui.moveTo(BUY_ORDER_COORDINATES_X, BUY_ORDER_COORDINATES_Y)
        pyautogui.click()
        time.sleep(0.53)
        pyautogui.moveTo(CONFIRM_BUY_ORDER_X, CONFIRM_BUY_ORDER_Y)
        time.sleep(0.2)
        pyautogui.click()
        time.sleep(0.55)
        pyautogui.moveTo(CONFIRM_SELL_ORDER_X, CONFIRM_SELL_ORDER_Y)
        time.sleep(0.78) 
        pyautogui.click()
        print("Proceeding with gold purchase.")
        time.sleep(0.64)
        pyautogui.moveTo(CONFIRM_SUBMITTED_X, CONFIRM_SUBMITTED_Y)
        time.sleep(1.13)
        pyautogui.click()
        time.sleep(0.78) 
        
        pyautogui.moveTo(CLOSE_MARKET_X, CLOSE_MARKET_Y)
        pyautogui.click()

def sell_gold(sell_threshold, extracted_number):
    print(f"Selling gold at price: {sell_threshold}")
    input_gold_price(extracted_number, SELL_GOLD_INPUT_COORDINATES_X, SELL_GOLD_INPUT_COORDINATES_Y)
    time.sleep(0.59)
    input_silver_price(sell_threshold, SELL_SILVER_INPUT_COORDINATES_X, SELL_SILVER_INPUT_COORDINATES_Y)
    time.sleep(0.55)
    pyautogui.moveTo(SELL_ORDER_COORDINATES_X, SELL_ORDER_COORDINATES_Y)
    pyautogui.click()
    print("Proceeding with gold sale.")
    time.sleep(0.3)
    pyautogui.moveTo(CONFIRM_SELL_ORDER_X, CONFIRM_SELL_ORDER_Y)
    time.sleep(0.55)
    pyautogui.click()
    time.sleep(0.55)
    pyautogui.moveTo(CONFIRM_SUBMITTED_X, CONFIRM_SUBMITTED_Y)
    time.sleep(0.78) 
    pyautogui.click()
    time.sleep(0.78) 
    pyautogui.moveTo(CLOSE_MARKET_X, CLOSE_MARKET_Y)
    time.sleep(1.08)
    pyautogui.click()
    

def run_trading_bot():
    global skip_next_run_until
    
    current_time = datetime.now()
    
    if skip_next_run_until and current_time < skip_next_run_until:
        print(f"Skipping run. Next check will be at {skip_next_run_until}")
        return
    
    print(f"Running trading bot at {current_time}")
    focus_game_window()  # Ensure the game window is focused
    open_market()
    select_order_mode()
    
    data = fetch_gold_data()
    
    if data:
        prices = process_gold_prices(data)
        if prices:
            relevant_prices = prices[-(relevant_hours):] # do -12: for past 12 hours -6: for past 6 you get the point
            print(f"Gold Price {relevant_hours}hr Delta: {relevant_prices}")
            
            buy_threshold, sell_threshold = calculate_thresholds(relevant_prices)
            
            if buy_threshold is not None and sell_threshold is not None:
                print(f"Buy threshold: {buy_threshold}")
                print(f"Sell threshold: {sell_threshold}")
                
                extracted_number = check_number()
                silver_quantity = check_silver_quantity()  # Get the silver quantity
                
                if extracted_number is not None and silver_quantity is not None:
                    if extracted_number == 0 and silver_quantity < buy_threshold:
                        print("Detected owned gold quantity is zero and owned silver is below the threshold. Skipping check")
                        pyautogui.moveTo(CLOSE_MARKET_X, CLOSE_MARKET_Y)
                        pyautogui.click()
                        time.sleep(random.randint(6, 25))
                        
                        skip_next_run_until = current_time + timedelta(minutes=INTERVAL)
                    elif extracted_number == 0:
                        print("Detected quantity is zero, buying gold at threshold price.")
                        buy_gold(buy_threshold, extracted_number, silver_quantity)
                        time.sleep(random.randint(1, 15))                        
                    else:
                        sell_gold(sell_threshold, extracted_number)
                        time.sleep(random.randint(1, 15))
                else:
                    print("Unable to read gold or silver quantities")
                    pyautogui.moveTo(CLOSE_MARKET_X, CLOSE_MARKET_Y)
                    pyautogui.click()
            else:
                print("Unable to calculate thresholds")
                sys.exit()  # Exit if thresholds are not calculable.
        else:
            print("No gold prices found")
            sys.exit()  # Exit if no gold prices are available.
    else:
        print("No data fetched")
        sys.exit()  # Exit if no data is fetched.
             
def main_loop():
    global last_movement_time
    
    while True:
        curr_time = datetime.now()
        
        if (curr_time - last_movement_time).total_seconds() >= RANDOM_MOVEMENT_INTERVAL * 60:
            print("mooovinnnng :)")
            contained_random_movement()
            last_movement_time = curr_time

        if keyboard.is_pressed('q'):  # Check if 'q' is pressed to stop the main loop
            print("Stopping script as 'q' key is pressed.")
            sys.exit()

        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    schedule.every(INTERVAL).minutes.do(run_trading_bot)
    main_loop()
