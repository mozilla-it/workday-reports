import requests
import sys
import logging

logger = logging.getLogger(__name__)


class RawReports():

    def __init__(self, report_url: str, username: str = None, password: str = None, proxies: dict = {}):
        self.report_url = report_url
        self.username = username
        self.password = password
        self.proxies = proxies

    def get_report(self) -> str:
        try:
            if self.username and self.password:
                r = requests.get(self.report_url, auth=(self.username, self.password), proxies=self.proxies)
            else:
                r = requests.get(self.report_url, proxies=self.proxies)
            r.encoding = "utf-8"  # otherwise requests thinks it's ISO-8859-1
            return r.text
        except:
            logger.critical(sys.exc_info()[0])
            raise

