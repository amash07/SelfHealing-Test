import sys
import os
import time

# ==========================================
# ADD PROJECT ROOT TO PYTHON PATH
# ==========================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, PROJECT_ROOT)


# ==========================================
# IMPORTS
# ==========================================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from self_healing.healer import SelfHealing


# ==========================================
# START BROWSER
# ==========================================

options = webdriver.ChromeOptions()
if "--headless" in sys.argv:
    options.add_argument("--headless=new")
else:
    options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

try:
    # Bring Chrome window to front on Windows
    driver.switch_to.window(driver.current_window_handle)
    driver.maximize_window()
    import ctypes
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    ctypes.windll.user32.SetForegroundWindow(hwnd)
except Exception:
    pass

driver.get("http://127.0.0.1:5000")
wait = WebDriverWait(driver, 10)
healer = SelfHealing(driver)


try:

    print()
    print("========================================")
    print("SELF-HEALING SELENIUM TEST")
    print("========================================")


    # ======================================
    # TEST 1 - LOGIN
    # ======================================

    print()
    print("TEST 1: Login")

    username = wait.until(
        EC.presence_of_element_located(
            (By.ID, "username")
        )
    )

    password = driver.find_element(
        By.ID,
        "password"
    )

    username.send_keys("admin")
    password.send_keys("admin123")

    # Visible pause so user can see credentials filled
    time.sleep(1)

    # Website has loginBtn
    # Test expects loginButton
    login_button = healer.find_element(
        By.ID,
        "loginButton"
    )

    login_button.click()

    wait.until(
        EC.url_contains("/dashboard")
    )

    print("PASS: Login successful")


    # ======================================
    # TEST 2 - DASHBOARD
    # ======================================

    print()
    print("TEST 2: Dashboard")
    time.sleep(1)

    dashboard_link = healer.find_element(
        By.ID,
        "dashboardLink"
    )

    print("PASS: Dashboard loaded")


    # ======================================
    # TEST 3 - PROFILE
    # ======================================

    print()
    print("TEST 3: Profile")
    time.sleep(1)

    # Expected: profileLink
    # Actual: profileBtn
    profile_link = healer.find_element(
        By.ID,
        "profileLink"
    )

    profile_link.click()

    wait.until(
        EC.url_contains("/profile")
    )

    print("PASS: Profile page opened")


    # ======================================
    # TEST 4 - PRODUCTS
    # ======================================

    print()
    print("TEST 4: Products")
    time.sleep(1)

    products_link = healer.find_element(
        By.ID,
        "productsLink"
    )

    products_link.click()

    wait.until(
        EC.url_contains("/products")
    )

    print("PASS: Products page opened")


    # ======================================
    # TEST 5 - SETTINGS
    # ======================================

    print()
    print("TEST 5: Settings")
    time.sleep(1)

    # Expected: settingsLink
    # Actual: settingsbtn
    settings_link = healer.find_element(
        By.ID,
        "settingsLink"
    )

    settings_link.click()

    wait.until(
        EC.url_contains("/settings")
    )

    print("PASS: Settings page opened")


    # ======================================
    # TEST 6 - LOGOUT
    # ======================================

    print()
    print("TEST 6: Logout")
    time.sleep(1)

    logout_link = healer.find_element(
        By.ID,
        "logoutLink"
    )

    logout_link.click()

    wait.until(
        EC.url_contains("/login")
    )

    print("PASS: Logout successful")


    # ======================================
    # FINAL RESULT
    # ======================================

    print()
    print("========================================")
    print("ALL TESTS PASSED")
    print("SELF-HEALING SUCCESSFUL")
    print("========================================")

    # Pause so user can see final success screen
    time.sleep(2)


except Exception as e:

    print()
    print("========================================")
    print("TEST FAILED")
    print("========================================")

    print("Error:", e)
    time.sleep(2)


finally:

    driver.quit()