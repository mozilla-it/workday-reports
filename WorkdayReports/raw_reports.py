import requests
import sys
import logging

logger = logging.getLogger(__name__)


class RawReports:
    def __init__(
        self,
        report_url: str = None,
        username: str = None,
        password: str = None,
        proxies: dict = {},
    ):
        self.report_url = report_url
        self.username = username
        self.password = password
        self.proxies = proxies

    def get_report(
        self, report_url: str = None, username: str = None, password: str = None
    ) -> str:

        report_url = report_url if report_url else self.report_url
        username = username if username else self.username
        password = password if password else self.password

        try:
            if username and password:
                r = requests.get(
                    report_url, auth=(username, password), proxies=self.proxies,
                )
            else:
                r = requests.get(report_url, proxies=self.proxies)
            r.encoding = "utf-8"  # otherwise requests thinks it's ISO-8859-1
            return r.text
        except:
            logger.critical(sys.exc_info()[0])
            raise
