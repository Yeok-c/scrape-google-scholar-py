from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selectolax.lexbor import LexborHTMLParser
from typing import List, Union, Dict
from pathlib import Path        
from urllib.request import urlretrieve
import numpy as np

class CustomGoogleScholarArticleDownload:
    def __init__(self, 
                gscholar_url:str, 
                pdf_location:str) -> None:
        
        self.gscholar_url = gscholar_url
        self.pdf_location = pdf_location
        self.pdf_url = self._get_pdf_url()
        self.download_success_counter = 0
        self.download_total_counter = 0
        self._download()
        
    def _get_pdf_url(
            self,
        ) -> Dict[str, List[Union[str, int, None]]]:

        # selenium stealth
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        
        service = Service() #ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        stealth(driver,
            languages=['en-US', 'en'],
            vendor='Google Inc.',
            platform='Win32',
            webgl_vendor='Intel Inc.',
            renderer='Intel Iris OpenGL Engine',
            fix_hairline=True,
        )
        
        driver.get(self.gscholar_url)
        parser = LexborHTMLParser(driver.page_source)
        try:
            url = parser.css(".gsc_oci_title_ggi")[0].child.attrs['href']
        except:
            url = None
        return url
    
    def _download(self):
        self.download_total_counter += 1
        try:
            urlretrieve(self.pdf_url, self.pdf_location)
            # print(f"PDF successfully saved to {self.pdf_location}")
            self.download_success_counter += 1
            return True
        except Exception as e:
            # print(f'Error downloading pdf: {e}')
            return False
        