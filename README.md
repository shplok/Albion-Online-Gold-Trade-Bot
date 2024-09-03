Albion Online Trading Bot


Overview:


This Python-based trading bot is designed for Albion Online. It automates the process of buying and selling gold based on real-time market data. The bot monitors the game's gold prices, calculates thresholds for buying and selling, and automatically places orders in the game's market. It also includes a feature for random mouse movements to simulate human behavior, reducing the likelihood of detection by anti-bot systems.


Features
    • Automated Trading: Automatically buys or sells gold based on threshold prices.
    • Market Data Fetching: Retrieves historical gold prices to determine optimal   buy/sell points.
    • OCR Integration: Uses Tesseract OCR to read in-game data like current gold and silver quantities.
    • Random Movements: Periodically moves the mouse to simulate human interaction and avoid detection.
    • Customizable Intervals: Set the time interval for checking and placing market orders.


Requirements
Python 3.11 and up
requests, schedule, pyautogui, cv2, pytesseract, numpy, Pillow
Tesseract OCR installed and correctly configured.


Usage
    • Clone the repository.
    • Install the required packages via pip.
    • Ensure Tesseract OCR is installed and the path is set in the script.
    • Run the script and follow the prompts to start trading in Albion Online.
    • Ensure that you keep the game in fullscreen and that it is the focused window.
    • If you have a different window resolution than 1920x1080, you need to find the factor in which the monitor is     
      different in size and use the provided "MONITOR_RESOLUTION_FACTOR_X and MONITOR_RESOLUTION_FACTOR_Y".
        
        For Example: 
            if you had a monitor with the resolution 3840x2160, the factor change for the x and y would be as follows

            3840/1980 = 2, 2160/1080 = 2 so instead of 1, MONITOR_RESOLUTION x and y would both be 2.
    
