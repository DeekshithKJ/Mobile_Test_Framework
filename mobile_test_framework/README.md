# Mobile Test Automation Framework

This repository contains a mobile test automation framework designed to automate testing scenarios for both iOS and Android apps. The framework utilizes BrowserStack for device and browser testing.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [BrowserStack Setup](#browserstack-setup)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
  - [iOS](#ios)
  - [Android](#android)

## Prerequisites

- Python 3.11 or higher
- Appium-Python-Client
- Selenium
- BrowserStack account

## Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/mobile_test_framework.git
   cd mobile_test_framework
   
2. To Activate virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. pip install -r requirements.txt

4. BrowserStack Setup
Sign up for a BrowserStack account.

Get your BrowserStack credentials (username and access key) from the BrowserStack dashboard.

Upload your iOS and Android app to BrowserStack:

Go to App Automate.
Click on "Upload" and upload your app file (.ipa for iOS, .apk for Android).
Note the app URL provided by BrowserStack after uploading.

5. Running tests:

ios : python test_app.py
android : python test_android.py
