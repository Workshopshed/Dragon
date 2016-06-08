from StringIO import StringIO
import pycurl
import signal,sys

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

def main():
    r = call_api("http://csb.stanford.edu/class/public/pages/sykes_webdesign/05_simple.html")
    print r

# Handle exit and kill from OS
def set_exit_handler(func):
    signal.signal(signal.SIGTERM, func)
def on_exit(sig, func=None):
    print "exit handler triggered"
    sys.exit(1)


# Run program
if __name__ == '__main__':
     set_exit_handler(on_exit)
     sys.exit(main())

