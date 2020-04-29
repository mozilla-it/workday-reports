import requests
import sys
import logging
import io
import csv

logger = logging.getLogger(__name__)


class Report:
    """
    This class can download a report based on URI from workday (or read it from file), 
    and optionally parse the report, store it, or return it raw.
    Parameters:
    * report_url, base_url, report_uri can be used to define where the report is retrieved from. 
      report_url takes precedent over base_url+report_uri. A sane base_url is provided. 
      Either report_url or report_uri are required unless using input_filename, which will forego hitting workday.
    * username, password: workday credentials (required)
    * proxies: http proxy for hitting workday (optional)
    * input_filename, output_filename: can be used for reading and writing reports. 
      Using input_filename will prevent hitting workday and should only be used for testing/debugging. 
      output_filename is used for writing a report to file.

    Example usage:

    >>> from WorkdayReports.raw_reports import Report
    >>> report = Report(username="test",password="redacted",report_uri="/ccx/service/customreport/thing/ANOTHER_THING/report_name")
    >>> print(len(list(report)))
    >>> report.write("/tmp/report.csv")
    >>> 
    >>> new_report = Report(input_filename="/tmp/report.csv")
    >>> print(len(list(new_report)))

    """

    def __init__(
        self,
        report_url: str = "",
        username: str = None,
        password: str = None,
        proxies: dict = {},
        base_url: str = "https://services1.myworkday.com",
        report_uri: str = None,
        input_filename: str = None,
        output_filename: str = None,
    ):
        self.report_url = report_url
        self.username = username
        self.password = password
        self.proxies = proxies
        self._report_bytes = bytes()
        self._report = ""
        self._report_parsed = []
        self._input_filename = input_filename
        self._output_filename = output_filename

        if self._input_filename:
            self.read()
            self.parse()
            # if we're just reading a file we can stop here.
            return None

        if not self.report_url and base_url and report_uri:
            self.report_url = f"{base_url}/{report_uri}"
        if "?" not in self.report_url:
            self.report_url += "?format=csv&bom=true"
        if "format=csv" not in self.report_url:
            logger.warning(
                "format=csv was not found in the URL arguments to Workday, this may not work."
            )

        assert (
            self.report_url
        ), "report_url or report_uri or input_filename must be specified."
        assert (
            self.username and self.password
        ), "Must provide username and password credentials to workday"

        self.get()
        self.parse()

    @property
    def report(self) -> str:
        return self._report

    @property
    def report_parsed(self) -> list:
        return self._report_parsed

    def __iter__(self):
        return iter(self._report_parsed)

    def read(self, filename: str = None) -> bool:
        if filename:
            self._input_filename = filename
        if not self._input_filename:
            raise Exception("Must specify an input filename")
        txt = open(self._input_filename, "r").read()
        self._report = txt
        self._report_bytes = bytes(txt, "utf-8")
        return True

    def get(self) -> bool:
        try:
            if self.username and self.password:
                r = requests.get(
                    self.report_url,
                    auth=(self.username, self.password),
                    proxies=self.proxies,
                )
            else:
                r = requests.get(self.report_url, proxies=self.proxies)
            r.encoding = "utf-8"  # otherwise requests thinks it's ISO-8859-1
            self._report_bytes = r.content
            self._report = r.text
            return True
        except:
            logger.critical(sys.exc_info()[0])
            raise

    def write(self, filename: str = None) -> bool:
        if filename:
            self._output_filename = filename
        if not self._output_filename:
            raise Exception("Must specify an output filename")
        f = open(self._output_filename, "wb")
        f.write(self._report_bytes)
        f.close()
        return True

    def parse(self) -> bool:
        report_parsed = []
        rows = csv.DictReader(self._report.splitlines())
        for row in rows:
            # a row is an OrderedDict
            report_parsed += [row]
        self._report_parsed = report_parsed
        return True
