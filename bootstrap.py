#-*- coding: UTF-8 -*-
from Configuration.Config import Config
import logging
import os
from Controller.GeoFilter import GeoFilter
from logger.boot import setupLogging
from Controller.FtpLoader import FtpLoader
from utils.builders import InterfaceBuilder
import zipfile
from Store.main import Store

def execute(instance, arg=None, cb=[]) :
    if len(cb) > 0:
        return instance.exec(arg, cb)
    return instance.exec(arg)

if __name__ == '__main__' :

    setupLogging()
    store = Store()
    mainStore = store.get_instance()
    logger = logging.getLogger(__name__)
    config = Config()
    urls = config.get_property("URL")
    for domain in urls :
        for dom, url in domain.items() :
            dict_files = config.get_property("FILES").get(dom)
            if dict_files is not None :
                download_dir = config.get_property("WS").get("DOWNLOAD").get(dom)
                extract_dir = config.get_property("WS").get("EXTRACT").get(dom)
                is_zip = False
                ftp = FtpLoader(url, outDir=download_dir)
                for file, props in dict_files.items() :
                    downloaded = ftp.downloadFileItem(file)
                    if downloaded :
                        if zipfile.is_zipfile(os.path.join(download_dir, file)) :
                            is_zip = True
                            with zipfile.ZipFile(os.path.join(download_dir, file), 'r') as zip_ref:
                                zip_ref.extractall(extract_dir)
                        for f in props :
                            fType = f.get('ITYPE')
                            if fType is not None :
                                if fType == 'GEO' :
                                    target_dir = extract_dir if is_zip else download_dir
                                    fileConfig = InterfaceBuilder(f, f.get('ITYPE'))
                                    geo_filter = GeoFilter(fileConfig, target_dir)
                                    execute(geo_filter, cb=f.get('CB', []))


                    else :
                        logger.error("Error occured while downloadind the file {}. Check logs".format(file))
                        continue
            else :
                logger.error("Error occured while trying to access the file list of domain {}. Check if you wrote a file list for this domain in the ftp_url.yaml config file".format(dom))
                continue


