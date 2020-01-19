#-*- coding: UTF-8 -*-
from Configuration.Config import Config
import logging
import os
from Controller.GeoFilter import GeoFilter
from logger.boot import setupLogging
from Controller.FtpLoader import FtpLoader
from Template.data_struct import buildFtpFile, ftp_file
import zipfile


if __name__ == '__main__' :

    setupLogging()
    logger = logging.getLogger(__name__)
    config = Config()
    urls = config.get_property("URL")
    for domain in urls :
        for dom, url in domain.items() :
            dict_files = config.get_property("FILES").get(dom)
            if dict_files is not None :
                download_dir = config.get_property("WS").get("DOWNLOAD").get(dom)
                ftp = FtpLoader(url, outDir=download_dir)
                for file, props in dict_files.items() :

                    downloaded = ftp.downloadFileItem(file)
                    if downloaded :
                        if file.endswith('.zip') :
                            with zipfile.ZipFile(os.path.join(download_dir, file), 'r') as zip_ref:
                                zip_ref.extractall(download_dir)
                        for f in props :
                            fileConfig = buildFtpFile(f)
                            if isinstance( fileConfig, ftp_file):
                                geofilter = GeoFilter(f.get('GEO_MASK'), download_dir, f.get('NAME'), f.get('GEO_TYPE'), f.get('FILTER_TYPE'))
                                results = geofilter.exec()
                                if results is not None :
                                    print(len(results))
                                else :
                                    logger.error("an error occured, check logs")
                                    continue
                            else :
                                logger.error(fileConfig)
                                continue

                    else :
                        logger.error("Error occured while downloadind the file {}. Check logs".format(file))
                        continue
            else :
                logger.error("Error occured while trying to access the file list of domain {}. Check if you wrote a file list for this domain in the ftp_url.yaml config file".format(dom))
                continue


