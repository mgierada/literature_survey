from selenium import webdriver


class LiteratureSurvay():
    ''' A class for scraping Google Scholar for a given query '''

    def __init__(self, query):
        ''' Initialize class '''
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        # options.add_argument('headless')
        options.add_argument('--test-type')
        DRIVER_PATH = './chromedriver'

        self.query = query
        self.driver = webdriver.Chrome(
            executable_path=DRIVER_PATH, options=options)

    def run(self):
        ''' Main run method '''
        LiteratureSurvay.search(self)
        links = LiteratureSurvay.get_links(self)
        # print(links)
        LiteratureSurvay.next_page(self)

    def search(self):
        ''' Click on the first .pdf file to open it '''
        self.driver.get('https://scholar.google.com')
        # find search box and enter query
        self.driver.find_element_by_name('q').send_keys(query)
        # click find button
        self.driver.find_element_by_id('gs_hdr_tsb').click()
        # click the first link with pdf
        # self.driver.find_element_by_class_name('gs_or_ggsm').click()

    def next_page(self):
        element = self.driver.find_element_by_id('gs_nml')
        # print(element.find_element_by_xpath(
        #     ".//a[@class='gs_nma']").get_attribute('href'))
        new = []
        for el in element.find_elements_by_xpath(
                ".//a[@class='gs_nma']"):
            print(el.get_attribute('href'))
        # print(page.get_attribute('href'))

    def get_links(self):
        ''' Get all links to the research papers 

        Returns:
        _______
        all_links : list(str)
            a list with links to papers

        '''
        all_links = []
        links = self.driver.find_elements_by_class_name('gs_rt a')
        for link in links:
            all_links.append(link.get_attribute('href'))
        return all_links


query = 'automation surface reaction mechanism workflow'
ls = LiteratureSurvay(query)
ls.run()
