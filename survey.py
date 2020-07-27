from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, InvalidArgumentException


class LiteratureSurvey():
    ''' A class for scraping Google Scholar for a given query

    Usage:
    ______

    >>> query = 'put_your_query_here'
    e.g. query = 'Cr silica dft mechanism'
    >>> ls = LiteratureSurvay(query)
    >>> ls.run()

    '''

    def __init__(self, query):
        ''' Initialize the class with the user defined options

        Parameters:
        ___________
        query : str
            a phrase to look for - what you want to use to search Google Scholar

        '''
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('headless')
        options.add_argument('--test-type')
        DRIVER_PATH = './chromedriver'

        self.query = query
        self.driver = webdriver.Chrome(
            executable_path=DRIVER_PATH, options=options)

    def run(self):
        ''' Main method to run the workflow '''
        # search Google Scholar for a given query
        print('Searching for a query {}'.format(self.query))
        self.search()
        # get links to papers, convert to dois and download pdfs
        # for a given search page
        print('Page: 1')
        self.run_page()
        next_pages = self.get_next_pages()
        # open next page and do everything to download .pdf files
        for i, page in enumerate(next_pages):
            # check validity of the links
            if page is not None:
                page_number = i + 1
                print('Page: {}'.format(page_number))
                try:
                    self.driver.get(page)
                    self.run_page()
                # if the links are inalid, handle the error
                except InvalidArgumentException:
                    print('error')
                    pass

    def run_page(self):
        ''' For a given Google Scholar search page, get links to the papers,
        transforms it to DOI and use SciHub to download .pdf files'''
        # get links to all papers on the 1st page
        links_to_papers = self.get_links_to_papers()
        # convert these links to doi
        dois = self.get_dois(links_to_papers)
        # download pdf files
        for doi in dois:
            print('Getting .pdf file for {}'.format(doi))
            try:
                self.get_pdf(doi)
                print('Done!')
            except NoSuchElementException as exception:
                print('Cannot download {}. Check doi'.format(doi))
                pass

    def search(self):
        ''' Searching Google Scholar for a given query '''
        self.driver.get('https://scholar.google.com')
        # find search box and enter query
        self.driver.find_element_by_name('q').send_keys(query)
        # click find button
        self.driver.find_element_by_id('gs_hdr_tsb').click()

    def get_next_pages(self):
        ''' Get a list with links_to_papers to Google Scholar pages 2-9

        Return:
        _______
        next_pages : list(str)
            a list with Google Scholar pages 1-9

        '''
        next_pages = []
        # find id of the page changing bar
        element = self.driver.find_element_by_id('gs_nml')
        # get links_to_papers to all pages 2-9
        for el in self.driver.find_elements_by_class_name('gs_nma'):
            next_pages.append(el.get_attribute('href'))
        return next_pages

    # def click_next_page(self):
    #     self.driver.get(
    #         'https://scholar.google.pl/scholar?hl=en&as_sdt=0%2C5&q=surface&btnG=')
    #     element = self.driver.find_element_by_id('gs_nm')
    #     button_list = []
    #     for el in element.find_elements_by_xpath('./button'):
    #         button_list.append(el)
    #     for button in button_list:
    #         try:
    #             button.click()
    #         except ElementNotInteractableException:
    #             print('sth wrong')
    #             pass

        # for el in element.find_elements_by_xpath(
        #         ".//button[@class='gs_btnPR gs_in_ib gs_btn_lrge gs_btn_half gs_btn_lsu']"):
        #     print(el)

    def get_links_to_papers(self):
        ''' Get all links_to_papers to the research papers

        Returns:
        _______
        all_links_to_papers : list(str)
            a list with links_to_papers to papers

        '''
        all_links_to_papers = []
        # find class name handling links_to_papers to the articles
        links_to_papers = self.driver.find_elements_by_class_name('gs_rt a')
        # loop through all elements of that class and get links_to_papers to research articles
        for link in links_to_papers:
            all_links_to_papers.append(link.get_attribute('href'))
        return all_links_to_papers

    def get_dois(self, links_to_papers):
        ''' Get DOIs of papers from links to the papers

        Parameters:
        __________
        links_to_papers : list(str)
            a list of links to the original papers

        For many articles doi can be successfully composed from link to the paper
        e.g. https://onlinelibrary.wiley.com/doi/abs/10.1002/jcc.25871
        Fragment '10.1002/jcc.25871' is good enough for SciHub.

        '''
        dois = []
        for links_to_paper in links_to_papers:
            create_doi = links_to_paper.split('/')[-2:]
            doi = create_doi[0] + '/' + create_doi[1]
            dois.append(doi)
        return dois

    def get_doi_wiley(self, link_to_paper):
        ''' Return DOI of the articles published by Wiley

        Parameters:
        ___________

        link_to_paper : str
            link to the Wiley article
            e.g. 'https://onlinelibrary.wiley.com/doi/full/10.1002/jcc.25871'

        Returns:
        doi : str
            doi of the paper to be downloaded
            e.g. 'https://doi.org/10.1002/jcc.25871'
        '''
        # open page with the article
        self.driver.get(link_to_paper)
        element = self.driver.find_element_by_class_name('epub-doi')
        doi = element.get_attribute('href')
        return doi

    def get_pdf(self, doi):
        ''' Use Scihub to download .pdf files

        Parameters:
        ___________
        doi : str
            a doi of the paper to be downloaded (with https:/doi.org/)
            e.g. 'https://doi.org/10.1002/jcc.25871'

        '''
        # open the scihub page for a given doi
        self.driver.get('https://sci-hub.tw/' + doi)
        # find 'Save' button element and imitate clicking it
        element = self.driver.find_element_by_id('buttons')
        element.find_elements_by_xpath(".//a")


query = 'reaction mechanism dft chromium silica'
ls = LiteratureSurvey(query)
ls.run()
