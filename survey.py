from selenium import webdriver


class LiteratureSurvay():
    ''' A class for scraping Google Scholar for a given query '''

    def __init__(self, query):
        ''' Initialize class '''
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('headless')
        options.add_argument('--test-type')
        DRIVER_PATH = './chromedriver'

        self.query = query
        self.driver = webdriver.Chrome(
            executable_path=DRIVER_PATH, options=options)

    def run(self):
        ''' Main run method '''
        # LiteratureSurvay.search(self)
        # links = LiteratureSurvay.get_links(self)
        # np = LiteratureSurvay.get_next_pages(self)
        # print(np)
        link_to_paper = 'https://onlinelibrary.wiley.com/doi/full/10.1002/jcc.25871'
        # doi = LiteratureSurvay.get_doi_wiley(self, link_to_paper)
        doi = 'https://doi.org/10.1002/jcc.25871'
        LiteratureSurvay.get_pdf(self, doi)

    def search(self):
        ''' Click on the first .pdf file to open it '''
        self.driver.get('https://scholar.google.com')
        # find search box and enter query
        self.driver.find_element_by_name('q').send_keys(query)
        # click find button
        self.driver.find_element_by_id('gs_hdr_tsb').click()
        # click the first link with pdf
        # self.driver.find_element_by_class_name('gs_or_ggsm').click()

    def get_next_pages(self):
        ''' Get a list with links to Google Scholar pages 2-9 

        Return:
        _______
        next_pages : list(str)
            a list with Google Scholar pages 1-9

        '''
        next_pages = []
        element = self.driver.find_element_by_id('gs_nml')
        for el in element.find_elements_by_xpath(
                ".//a[@class='gs_nma']"):
            next_pages.append(el.get_attribute('href'))
        return next_pages

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

    def get_doi_wiley(self, link_to_paper):
        ''' Return DOI of the articles published by Wiley '''
        # open page with the article
        self.driver.get(link_to_paper)
        element = self.driver.find_element_by_class_name('epub-doi')
        doi = element.get_attribute('href')
        return doi

    def get_pdf(self, doi):
        self.driver.get('https://sci-hub.tw/' + doi)
        element = self.driver.find_element_by_id('buttons')
        for el in element.find_elements_by_xpath(
                ".//a"):
            el.click()


query = 'automation surface reaction mechanism workflow'
ls = LiteratureSurvay(query)
ls.run()
