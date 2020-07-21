from selenium import webdriver

query = 'automation surface reaction mechanism workflow'
# options = Options()
# options.headless = True
# options.add_argument("--window-size=1920,1200")

DRIVER_PATH = './chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://scholar.google.com')

# find search box and enter query
driver.find_element_by_name('q').send_keys(query)
# click find button
driver.find_element_by_id('gs_hdr_tsb').click()
# click the first link with pdf
driver.find_element_by_class_name('gs_or_ggsm').click()
