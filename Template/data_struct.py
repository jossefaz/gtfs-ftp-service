from collections import namedtuple

propLists = ['NAME', 'GEO_TYPE', 'AOI', 'FILTER_TYPE']
ftp_file = namedtuple('Ftp_file', propLists)

def buildFtpFile(dictionnary) :
    try :
        for props, val in dictionnary.items() :
            if props not in ['NAME', 'GEO_TYPE', 'AOI', 'FILTER_TYPE'] :
                raise KeyError("Each file properties must implements {}".format(''.join(propLists)))
        return ftp_file(
            NAME=dictionnary.get('NAME'),
            GEO_TYPE=dictionnary.get('GEO_TYPE'),
            AOI=dictionnary.get('AOI'),
            FILTER_TYPE=dictionnary.get('FILTER_TYPE')
        )

    except AttributeError:
        return "Each File must implements a file properties in ftp_url.yaml, and must contains {}".format(''.join(propLists))
    except KeyError as e:
        return str(e)

