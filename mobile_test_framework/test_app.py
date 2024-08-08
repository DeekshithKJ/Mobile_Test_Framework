from appium import webdriver
from appium.options.ios import XCUITestOptions
import config
import time

# Initialize the options
options = XCUITestOptions()
options.platform_name = 'iOS'
options.platform_version = '16.0'
options.device_name = 'iPhone 14 Pro Max'
options.app = config.desired_caps['app']

# Set BrowserStack options directly into the capabilities dictionary
bstack_options = {
    "projectName": config.desired_caps['project'],
    "buildName": config.desired_caps['build'],
    "sessionName": config.desired_caps['name'],
    "userName": config.browserstack_username,
    "accessKey": config.browserstack_access_key
}

options.load_capabilities({
    "bstack:options": bstack_options
})

driver = webdriver.Remote(
    command_executor='http://hub-cloud.browserstack.com/wd/hub',
    options=options
)

# Add implicit wait
driver.implicitly_wait(30)


def handle_error_message():
    try:
        error_message = driver.find_element("xpath",
                                            '//XCUIElementTypeStaticText[@name="Oops, something went wrong. Please try again. Code: E101"]')
        ok_button = driver.find_element("xpath", '//XCUIElementTypeButton[@name="Ok"]')
        if error_message and ok_button:
            print("Error message displayed. Clicking Ok button.")
            ok_button.click()
            time.sleep(2)  # Wait for the screen to refresh
            return True
    except Exception as e:
        print(f"No error message displayed. Exception: {e}")
    return False


try:
    # Validate home screen is displayed
    home_screen = driver.find_element("xpath",
                                      '//XCUIElementTypeStaticText[@name="Please enter your Ident-ID to start"]')
    assert home_screen, "Home screen not displayed"
    print("Home screen is displayed.")

    # Find the edit box and start button
    ident_input = driver.find_element("xpath", '//XCUIElementTypeTextField[@value="Ident-ID"]')
    start_button = driver.find_element("xpath", '//XCUIElementTypeButton[@name="Start"]')

    # Ensure the elements are not None
    assert ident_input is not None, "Edit box not found"
    assert start_button is not None, "Start button not found"
    print("Ident input and Start button found.")

    # Ident IDs list
    ident_ids = [
        "SG1-DIKYN", "SG1-PRVEN", "SG1-WMFFG", "SG1-QVMYP", "SG1-UPXPW"
    ]

    # Retry mechanism to handle error message
    for ident_id in ident_ids:
        # Clear the ident input field
        ident_input.clear()
        time.sleep(1)

        # Enter an ident ID and click start
        ident_input.send_keys(ident_id)
        start_button.click()
        print(f"Attempting with Ident ID '{ident_id}'.")

        if handle_error_message():
            print("Retrying with the next Ident ID...")
            continue  # Try the next Ident ID
        else:
            print("Proceeding as no error message displayed.")
            break  # Exit the loop if no error message is displayed

    # Validate the terms and conditions screen is displayed
    terms_conditions = driver.find_element("xpath",
                                           '//XCUIElementTypeStaticText[@name="Terms and Conditions"]')  # Update this with the correct ID from Inspector
    assert terms_conditions, "Terms and conditions screen not displayed"
    print("Terms and conditions screen is displayed.")

    # Add a wait to ensure elements are fully loaded
    time.sleep(5)

    # Click on the close icon
    try:
        close_icon = driver.find_element("xpath",
                                         '//XCUIElementTypeButton[@name="Close"]')  # Verify this ID using Appium Inspector
        close_icon.click()
        print("Clicked on the close icon.")
    except Exception as e:
        print(f"Error finding or clicking close icon: {e}")

    # Validate options with reasons are displayed
    try:
        options_reasons = driver.find_element("xpath",
                                              '//XCUIElementTypeStaticText[@name="Quit identification session"]')  # Verify this ID using Appium Inspector
        assert options_reasons is not None, "Options with reasons not displayed"
        print("Options with reasons are displayed.")
    except Exception as e:
        print(f"Error finding options with reasons: {e}")

    # Choose an option and click Quit session
    try:
        option = driver.find_element("xpath",
                                     '//XCUIElementTypeTable/XCUIElementTypeCell[1]/XCUIElementTypeOther')  # Verify this ID using Appium Inspector
        quit_button = driver.find_element("xpath",
                                          '//XCUIElementTypeButton[@name="Quit session"]')  # Verify this ID using Appium Inspector
        option.click()
        quit_button.click()
        print("Chose an option and clicked Quit session.")
    except Exception as e:
        print(f"Error finding or clicking option or quit session button: {e}")

    # Validate the intermediate screen before redirecting to the home screen
    try:
        intermediate_screen = driver.find_element("xpath",
                                                  '//XCUIElementTypeStaticText[contains(@name, "SG1-")]')  # Verify this ID using Appium Inspector
        assert intermediate_screen, "Intermediate screen not displayed"
        print(f"Intermediate screen with Ident-ID is displayed: {intermediate_screen.text}")
    except Exception as e:
        print(f"Error finding intermediate screen: {e}")

    # Final assertion to ensure the home screen is displayed again
    try:
        home_screen_again = driver.find_element("xpath",
                                                '//XCUIElementTypeStaticText[@name="Please enter your Ident-ID to start"]')  # Verify this ID using Appium Inspector
        assert home_screen_again, "Home screen not displayed after quitting session"
        print("Home screen is displayed again.")
    except Exception as e:
        print(f"Error finding home screen again: {e}")

finally:
    # Quit the driver
    driver.quit()
