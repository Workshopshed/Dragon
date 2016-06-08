from StringIO import StringIO
import pycurl


def get_key():
    with open('IFTTTKey.conf', 'r') as f:
        key = f.readline()
    f.close()
    return key


def get_notifyURL(numDragons):
    return "https://maker.ifttt.com/trigger/DragonDetected/with/key/" + get_key() + "?value1=" + str(numDragons)


def call_api(url):
    r = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.CONNECTTIMEOUT, 10)
    c.setopt(c.TIMEOUT, 60)
    c.setopt(c.WRITEFUNCTION, r.write)
    c.perform()
    c.close()
    return r.getvalue()


print call_api(get_notifyURL(2))

