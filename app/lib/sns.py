from app.config.cplog import CPLog
import cherrypy
import json
import urllib
import urllib2

log = CPLog(__name__)

class SNS:

    key = ''

    def __init__(self):
        self.enabled = self.conf('enabled')
        self.key = self.conf('key')
        pass

    def conf(self, options):
        return cherrypy.config['config'].get('Notifo', options)

    def send(self, message, status):

        url = 'http://sns.burst-dev.com/notification'

        try:
            message = message.strip()
            data = urllib.urlencode({
                'key': self.key,
                'subject': status,
                'message': message.encode('utf-8')
            })

            req = urllib2.Request(url)
            handle = urllib2.urlopen(req, data)
            json.load(handle)
        except Exception, e:
            log.info(e)
            log.error('SNS notification failed.')
            return False

        log.info('SNS notification success.')
        return

    def notify(self, message, status):
        if not self.enabled:
            return

        self.send(message, status)

    def test(self, key):

        self.enabled = True
        self.key = key

        self.notify('This is a test notification from Couch Potato', "Testing")
