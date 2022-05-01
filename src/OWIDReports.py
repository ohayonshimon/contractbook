#!/usr/bin/env python3
"""This script will Fetch the latest OWID Covid data in JSON fromat.
and extract the desired information from the dataset"""


import os
import datetime
from csv import reader
import requests

from generator import Generator
import config

from log import logger
import OWID


def get_countries(selected_countries_input_file):
    with open(selected_countries_input_file, 'r') as read_obj:
        csv_reader = reader(read_obj)
        row = next(csv_reader)
    return row


class OWIDReports:
    """Creating reports From the latest OWID dataset."""

    def __init__(self, config, dataset, selected_countries):
        self.config = config
        self.selected_countries = selected_countries
        self.dataset = dataset
        self.today = datetime.date.today()
        self.selected_report_file = config.SELECTED_COUNTRIES_REPORT
        self.oldest_report_file = config.OLDEST_COUNTRIES_REPORT

    def run(self):
        self.selected_countries_report()
        self.oldest_countries_report()

    def selected_countries_report(self):

        selected_countries_report = \
            self.render_report(self.create_selected_report(),
                               self.selected_report_file)

        return FileHandler.write_report(selected_countries_report,
                                        self.selected_report_file)

    def oldest_countries_report(self):

        oldest_countries_report = \
            self.render_report(self.create_oldest_report(),
                               self.oldest_report_file)

        return FileHandler.write_report(oldest_countries_report,
                                        self.oldest_report_file)

    def render_report(self, report, template_file):
        content = {'report': report,
                   'time': self.today}

        return Generator(template_file).render_file(content)

    def create_selected_report(self):
        report = {}
        for country in self.dataset:
            if self.dataset[country]["location"] in self.selected_countries:
                report.setdefault(country, {})
                report[country]["name"] = \
                    self.dataset[country]["location"]
                report[country]["new_cases"] = \
                    self.dataset[country]["new_cases"]
                report[country]["total_cases"] = \
                    self.dataset[country]["total_cases"]
                report[country]["new_vaccinations"] = \
                    self.dataset[country]["new_vaccinations"]
                report[country]["total_vaccinations"] \
                    = self.dataset[country]["total_vaccinations"]

        return report

    def create_oldest_report(self):
        report = {}
        countries = sorted(self.dataset.items(),
                           key=lambda d: d[1]['last_updated_date'])

        for country in countries[:config.NUMBER_OF_COUNTRIES]:
            report[country[1]["location"]] = country[1]["last_updated_date"]
        return report


class FileHandler(object):
    """Handling files"""

    @staticmethod
    def write_report(report_data, file_path):
        current = os.path.dirname(__file__)
        report_path = os.path.join(current, config.REPORT_DIR, file_path)
        with open(report_path, 'w', encoding='UTF-8') as report:
            report.write(report_data)


def main():
    selected_countries = get_countries(config.SELECTED_COUNTRIES_INPUT_FILE)
    dataset = OWID.get()
    OWIDReports(config, dataset, selected_countries).run()


if __name__ == "__main__":
    main()
