from selenium import webdriver


class LiteratureSurvay():
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
        ''' Main run method '''
        LiteratureSurvay.search(self)
        links_to_papers = LiteratureSurvay.get_links_to_papers(self)
        dois = self.get_dois(links_to_papers)
        print(dois)
        # np = LiteratureSurvay.get_next_pages(self)
        # print(np)
        # link_to_paper = 'https://onlinelibrary.wiley.com/doi/full/10.1002/jcc.25871'
        # doi = LiteratureSurvay.get_doi_wiley(self, link_to_paper)
        # doi = 'https://doi.org/10.1002/jcc.25871'
        # LiteratureSurvay.get_pdf(self, doi)

    def search(self):
        ''' Searching Google Scholar for a given query '''
        self.driver.get('https://scholar.google.com')
        # find search box and enter query
        self.driver.find_element_by_name('q').send_keys(query)
        # click find button
        self.driver.find_element_by_id('gs_hdr_tsb').click()
        # click the first link with pdf
        # self.driver.find_element_by_class_name('gs_or_ggsm').click()

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
        for el in element.find_elements_by_xpath(
                ".//a[@class='gs_nma']"):
            next_pages.append(el.get_attribute('href'))
        return next_pages

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


query = 'automation surface reaction mechanism workflow'
ls = LiteratureSurvay(query)
ls.run()
