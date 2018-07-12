
import time
from pyBrows.seleniumChrome import Headless
from streamparse import Spout


class PredsMapSpout(Spout):
    outputs = ["president_name", "page_url", "page_number", "page_source"]
    _targets=[
        "http://www.biblioteca.presidencia.gov.br/presidencia/ex-presidentes/fernando-henrique-cardoso/discursos/1o-mandato/1995-1",
    ]
    def initialize(self, stormconf, context):
        """
        """
        #init vars
        self._pages=[]
        president_name="Fernado Henrique Cardoso"
        #init browser
        wd=Headless()
        self.logger.info("TARGET PRESIDENT: [{}]".format(president_name))
        for target_url in self._targets:
            page_number=0 #starting paging
            wd.get(target_url)
            source_page=wd.pageSource
            self.logger.info("GET: [{}] ".format(target_url))
            self._pages.append((president_name,target_url,
                               page_number,source_page))
        wd.close()
        #add iterator
        self.pages=iter(self._pages)

    def next_tuple(self):
        try:
            predsPageMap = next(self.pages)
            self.emit(predsPageMap)
        except StopIteration:
            self.logger.info("[-] No more URLS to process. Waiting...")
            time.sleep(10)
