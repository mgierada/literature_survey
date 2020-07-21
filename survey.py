from selenium import webdriver


class LiteratureSurvay():
    ''' A class for scraping Google Scholar for a given query '''

    def __init__(self, query):
        ''' Initialize class '''
        DRIVER_PATH = './chromedriver'
        self.query = query
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH)

    def search(self):
        ''' Click on the first .pdf file to open it '''
        self.driver.get('https://scholar.google.com')
        # find search box and enter query
        self.driver.find_element_by_name('q').send_keys(query)
        # click find button
        self.driver.find_element_by_id('gs_hdr_tsb').click()
        # click the first link with pdf
        self.driver.find_element_by_class_name('gs_or_ggsm').click()


query = 'automation surface reaction mechanism workflow'
ls = LiteratureSurvay(query)
ls.search()
