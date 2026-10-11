import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


try:

    # -----------------------------
    # LOGIN
    # -----------------------------

    print("\nTEST 1: Login")

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

    # Brief pause so the user can visibly see inputs typed
    time.sleep(1)

    # Original locator (will fail because HTML button ID is loginBtn)
    login_button = driver.find_element(
        By.ID,
        "loginButton"
    )

    login_button.click()

    wait.until(
        EC.url_contains("/dashboard")
    )

    print("PASS: Login successful")


    # -----------------------------
    # PROFILE
    # -----------------------------

    print("\nTEST 2: Profile")
    time.sleep(1)

    profile_link = driver.find_element(
        By.ID,
        "profileLink"
    )

    profile_link.click()

    wait.until(
        EC.url_contains("/profile")
    )

    print("PASS: Profile page opened")


    # -----------------------------
    # PRODUCTS
    # -----------------------------

    print("\nTEST 3: Products")
    time.sleep(1)

    products_link = driver.find_element(
        By.ID,
        "productsLink"
    )

    products_link.click()

    wait.until(
        EC.url_contains("/products")
    )

    print("PASS: Products page opened")


    # -----------------------------
    # SETTINGS
    # -----------------------------

    print("\nTEST 4: Settings")
    time.sleep(1)

    settings_link = driver.find_element(
        By.ID,
        "settingsLink"
    )

    settings_link.click()

    wait.until(
        EC.url_contains("/settings")
    )

    print("PASS: Settings page opened")


    # -----------------------------
    # LOGOUT
    # -----------------------------

    print("\nTEST 5: Logout")
    time.sleep(1)

    logout_link = driver.find_element(
        By.ID,
        "logoutLink"
    )

    logout_link.click()

    wait.until(
        EC.url_contains("/login")
    )

    print("PASS: Logout successful")


    print("\n========================================")
    print("ALL TESTS PASSED")
    print("========================================")


except Exception as e:

    print("\n========================================")
    print("TEST FAILED")
    print("========================================")

    print("Error:", e)
    # Pause so user can see failure state on screen before quitting
    time.sleep(2)


finally:

    driver.quit()