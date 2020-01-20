from Template.data_struct import ftp_geo_file, ftp_feeder_file

def buildFtpGeoFile(dictionnary) :
    try :
        for props, val in dictionnary.items() :
            if props not in ftp_geo_file._fields and props not in 'CB':
                raise KeyError("Each file properties must implements {}".format(' , '.join(ftp_geo_file._fields)))
        return ftp_geo_file(dictionnary.get('NAME'),dictionnary.get('GEO_TYPE'),dictionnary.get('AOI'),dictionnary.get('FILTER_TYPE'),dictionnary.get('FILE_TYPE'))

    except AttributeError:
        return "Each File must implements a file properties in ftp_url.yaml, and must contains {}".format(' , '.join(ftp_geo_file._fields))
    except KeyError as e:
        return str(e)

def buildFtpFeederFile(dictionnary) :
    try :
        for props, val in dictionnary.items() :
            if props not in ftp_feeder_file._fields and props not in 'CB':
                raise KeyError("Each file properties must implements {}".format(' , '.join(ftp_feeder_file._fields)))
        return ftp_feeder_file(dictionnary.get('NAME'),dictionnary.get('JOIN_FIELD'),dictionnary.get('FOOD_FIELDS'), dictionnary.get('PATH'))

    except AttributeError:
        return "Each File must implements a file properties in ftp_url.yaml, and must contains {}".format(' , '.join(ftp_feeder_file._fields))
    except KeyError as e:
        return str(e)
