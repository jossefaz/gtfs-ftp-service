#-*- coding: UTF-8 -*-
from Configuration.Config import Config
import logging

from Controller.GeoFilter import GeoFilter
from logger.boot import setupLogging
from Controller.FtpLoader import FtpLoader
from Model.geoCsv import *
import zipfile

if __name__ == '__main__' :

    setupLogging()
    logger = logging.getLogger(__name__)
    config = Config()
    urls = config.get_property("URL")
    for domain in urls :
        for dom, url in domain.items() :
            download_dir = config.get_property("WS").get("DOWNLOAD").get(dom)
            ftp = FtpLoader(url, outDir=download_dir)
            dict_files = config.get_property("FILES").get(dom)
            for file, props in dict_files.items() :
                downloaded = ftp.downloadFileItem(file)
                if downloaded :
                    if file.endswith('.zip') :
                        with zipfile.ZipFile(os.path.join(download_dir, file), 'r') as zip_ref:
                            zip_ref.extractall(download_dir)
                    for f in props :
                        geofilter = GeoFilter(f.get('GEO_MASK'), download_dir, f.get('NAME'), f.get('GEO_TYPE'), f.get('FILTER_TYPE'))
                        results = geofilter.exec()
                        print(len(results))

                else :
                    logger.error("Error occured while downloadind the file {}. Check logs".format(file))
                    continue


