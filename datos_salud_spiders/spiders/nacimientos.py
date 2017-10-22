# -*- coding: utf-8 -*-
import logging
from io import BytesIO

import pandas
import rarfile
from scrapy import Request
from scrapy.http import Response
from scrapy.spiders import Spider


class NacimientosSpider(Spider):
    name = 'nacimientos'

    urls = {
        'listado_excel': 'http://www.msp.gub.uy/EstVitales/nacimientos.html'
    }

    def __init__(self, *args, **kwargs):
        super(NacimientosSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        return [Request(self.urls['listado_excel'], callback=self.get_csv_files)]

    def get_csv_files(self, response: Response):
        # get all <a> items with 'Descargar CSV'
        a_buttons = response.xpath('//table[@class="table-fill"]//a[contains(@title, "Descargar CSV")]')
        for btn in a_buttons:
            href = btn.xpath('@href').extract_first()
            # join url to download csv
            url = response.urljoin(href)
            # yield request to process
            yield Request(url=url, callback=self.decompress)

    def decompress(self, response: Response):
        with rarfile.RarFile(BytesIO(response.body)) as rf:
            try:
                # open rar and then csv
                rarinfo = rf.infolist().pop()
                with rf.open(rarinfo) as csv_file:
                    # open csv in chunks of 10000 elements
                    for chunk in pandas.read_csv(csv_file, chunksize=10**4, sep=';'):
                        count = 0
                        for row in chunk.iterrows():
                            count += 1
                            # yield item
                            yield row[1].to_dict()
            except ValueError as e:
                logging.error(e)
            return None
