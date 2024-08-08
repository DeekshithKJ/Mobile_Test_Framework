# test_android.py
from appium import webdriver
from appium.options.android import UiAutomator2Options
import config
import time


def initialize_driver():
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.platform_version = config.android_desired_caps['os_version']
    options.device_name = config.android_desired_caps['device']
    options.app = config.android_desired_caps['app']

    bstack_options = {
        "projectName": config.android_desired_caps['project'],
        "buildName": config.android_desired_caps['build'],
        "sessionName": config.android_desired_caps['name'],
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
    driver.implicitly_wait(30)
    return driver


def handle_error_message(driver):
    try:
        error_message = driver.find_element("xpath",
                                            '//android.widget.TextView[@text="Oops, something went wrong. Please try again. Code: E101"]')
        ok_button = driver.find_element("id", 'android:id/button1')
        if error_message and ok_button:
            print("Error message displayed. Clicking Ok button.")
            ok_button.click()
            time.sleep(2)  # Wait for the screen to refresh
            return True
    except Exception as e:
        print(f"No error message displayed. Exception: {e}")
    return False


def run_test():
    driver = initialize_driver()

    try:
        # Validate home screen is displayed
        try:
            home_screen = driver.find_element("xpath",
                                              '//android.widget.TextView[@text="Please enter your Ident-ID to start"]')
            assert home_screen, "Home screen not displayed"
            print("Home screen is displayed.")
        except Exception as e:
            print(f"Error finding home screen: {e}")
            return

        # Find the edit box and start button
        try:
            ident_input = driver.find_element("id", 'io.idnow.autoident:id/editTextCode')
            start_button = driver.find_element("id", 'io.idnow.autoident:id/start_ident')
            assert ident_input is not None, "Edit box not found"
            assert start_button is not None, "Start button not found"
            print("Ident input and Start button found.")
        except Exception as e:
            print(f"Error finding Ident input or Start button: {e}")
            return

        ident_ids = ["SG1-DIKYN", "SG1-PRVEN", "SG1-WMFFG", "SG1-QVMYP", "SG1-UPXPW"]

        retry_attempts = len(ident_ids)
        for attempt in range(retry_attempts):
            try:
                ident_input.clear()
                time.sleep(1)

                ident_id = ident_ids[attempt]
                print(f"Entering Ident ID: {ident_id}")

                # Debugging logs
                print(f"Ident Input: {ident_input}")
                print(f"Start Button: {start_button}")

                ident_input.click()  # Ensure the field is focused
                ident_input.send_keys(ident_id)
                time.sleep(2)  # Give some time to send keys
                start_button.click()
                print(f"Attempt {attempt + 1}: Entered Ident ID '{ident_id}' and clicked Start.")
            except Exception as e:
                print(f"Error interacting with Ident input or Start button: {e}")

            if not handle_error_message(driver):
                break
            print("Retrying...")

        # Validate terms and conditions screen
        try:
            terms_conditions = driver.find_element("xpath", '//android.widget.TextView[@text="Terms and Conditions"]')
            assert terms_conditions, "Terms and conditions screen not displayed"
            print("Terms and conditions screen is displayed.")
        except Exception as e:
            print(f"Error finding terms and conditions screen: {e}")

        time.sleep(5)

        # Click on the close icon
        try:
            close_icon = driver.find_element("id", 'io.idnow.autoident:id/btn_close')
            close_icon.click()
            print("Clicked on the close icon.")
        except Exception as e:
            print(f"Error finding or clicking close icon: {e}")

        # Validate options with reasons are displayed
        try:
            options_reasons = driver.find_element("xpath", '//android.widget.TextView[@text="Options with Reasons"]')
            assert options_reasons is not None, "Options with reasons not displayed"
            print("Options with reasons are displayed.")
        except Exception as e:
            print(f"Error finding options with reasons: {e}")

        # Choose an option and click Quit session
        try:
            reason_option = driver.find_element("id", 'io.idnow.autoident:id/reason_radio')
            quit_button = driver.find_element("id", 'io.idnow.autoident:id/finish_button')
            reason_option.click()
            quit_button.click()
            print("Chose an option and clicked Quit session.")
        except Exception as e:
            print(f"Error finding or clicking option or quit session button: {e}")

        # Validate the intermediate screen before redirecting to the home screen
        try:
            intermediate_screen = driver.find_element("xpath", '//android.widget.TextView[contains(@text,"Ident-ID")]')
            assert intermediate_screen, "Intermediate screen not displayed"
            print(f"Intermediate screen with Ident-ID is displayed: {intermediate_screen.text}")
        except Exception as e:
            print(f"Error finding intermediate screen: {e}")

        # Final assertion to ensure the home screen is displayed again
        try:
            home_screen_again = driver.find_element("xpath",
                                                    '//android.widget.TextView[@text="Please enter your Ident-ID to start"]')
            assert home_screen_again, "Home screen not displayed after quitting session"
            print("Home screen is displayed again.")
        except Exception as e:
            print(f"Error finding home screen again: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    run_test()
