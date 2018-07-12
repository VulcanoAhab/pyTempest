import os
import re
import requests
from lxml import html
from streamparse import Bolt


class Fetch(Bolt):
    """
    """
    outputs = [ "president_name", "date",
                "speech_title", "speech_url"]
    _reTitle=re.compile(r"(?P<date>\d{2}-\d{2}-\d{4})\s+-\s+(?P<title>[\w\s\d]+)")

    def initialize(self, conf, ctx):
        self.pid = os.getpid()
        self.total = 0

    def process(self, tup):
        """
        tup:("president_name", "page_url", "page_number", "page_source")
        """
        #set vars
        page_source = tup.values[-1]
        page_object=html.fromstring(page_source)
        xpath="//*[@id='content-core']/div/div/h2/a"
        elements=page_object.xpath(xpath)
        headers={
            "User-Agent":"Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus "\
            "Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18."\
            "0.1025.133 Mobile Safari/535.19",
            "Connection":"keep-alive"
        }
        for el in elements:
            dateTitle=el.text
            speech_url=el.attrib["href"].strip("/view")
            rexDateTitle=self._reTitle.search(dateTitle)
            if not rexDateTitle:
                msg="Could not extract from title: [{}]".format(dateTitle)
                self.logger.info(msg)
                continue
            else:
                #get metadata
                date=rexDateTitle.group("date")
                title=rexDateTitle.group("title")
                msg="RUNNING Date [{}] | Title [{}]| PID[{}]".format(date,title,self.pid)
                self.logger.info(msg)
                #get speech pdf
                r=requests.get(speech_url)
                pdf_content=r.pdf_content
                fd=open("/tmp/pdf_test.pdf", "wb")
                fd.write(pdf_content)
                fd.close()
                self.emit([tup.values[0], date, title, speech_url])
