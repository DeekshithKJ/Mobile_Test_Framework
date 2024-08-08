# config.py
browserstack_username = 'YOUR USER NAME'
browserstack_access_key = 'YOUR ACCESS KEY'

desired_caps = {
    'os_version': '16.0',  # iOS version
    'device': 'iPhone 14 Pro Max',  # Device name
    'app': '# Updated App URL from BrowserStack',
    'project': 'My First Project',
    'build': 'My First Build',
    'name': 'BStack-[Python] Sample Test'
}


android_desired_caps = {
    'os_version': '12.0',
    'device': 'Samsung Galaxy S22',
    'app': '# Updated App URL from BrowserStack',
    'project': 'My First Project',
    'build': 'My First Build',
    'name': 'Android Test'
}