from Template.data_struct import ftp_geo_file

def buildFtpGeoFile(dictionnary) :
    try :
        for props, val in dictionnary.items() :
            if props not in ftp_geo_file._fields :
                raise KeyError("Each file properties must implements {}".format(''.join(ftp_geo_file._fields)))
        return ftp_geo_file(
            NAME=dictionnary.get('NAME'),
            GEO_TYPE=dictionnary.get('GEO_TYPE'),
            AOI=dictionnary.get('AOI'),
            FILTER_TYPE=dictionnary.get('FILTER_TYPE')
        )

    except AttributeError:
        return "Each File must implements a file properties in ftp_url.yaml, and must contains {}".format(''.join(ftp_geo_file._fields))
    except KeyError as e:
        return str(e)
