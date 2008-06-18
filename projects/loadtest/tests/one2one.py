# The Grinder 3.0.1
# HTTP script recorded by TCPProxy at 09.Haz.2008 01:32:23

from net.grinder.script import Test
from net.grinder.script.Grinder import grinder
from net.grinder.plugin.http import HTTPPluginControl, HTTPRequest
from HTTPClient import NVPair, Codecs
from java.util import Random
from org.xml.sax import InputSource
from org.apache.xerces.parsers import DOMParser

# A shorter alias for the grinder.logger.output() method.
log = grinder.logger.output

connectionDefaults = HTTPPluginControl.getConnectionDefaults()
httpUtilities = HTTPPluginControl.getHTTPUtilities()

# To use a proxy server, uncomment the next line and set the host and port.
# connectionDefaults.setProxyServer("localhost", 8001)

# These definitions at the top level of the file are evaluated once,
# when the worker process is started.

connectionDefaults.defaultHeaders = \
  ( NVPair('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; tr; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'),
    NVPair('Accept-Encoding', 'gzip,deflate'),
    NVPair('Accept-Language', 'tr-TR,tr;q=0.8,en-us;q=0.5,en;q=0.3'),
    NVPair('Accept-Charset', 'ISO-8859-9,utf-8;q=0.7,*;q=0.7'),
    NVPair('Cache-Control', 'no-cache'),
    NVPair('Accept', 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5'), )

agentID = int(grinder.properties["grinder.agentID"])
processID = int(grinder.processName.split("-").pop())
host = '192.168.1.200'
domain = 'openf.ath.cx'
boshUrl = 'http://' + host + ':7070/http-bind/'
boshWait = 1
userPrefix = 'user'
numThreads = 1

# Create an HTTPRequest for each request, then replace the
# reference to the HTTPRequest with an instrumented version.
# You can access the unadorned instance using request101.__target__.

request101 = Test(101, 'Initiate a BOSH session').wrap(HTTPRequest(url=boshUrl))
request201 = Test(201, 'Authenticate').wrap(HTTPRequest(url=boshUrl))
request301 = Test(301, 'Bind resource').wrap(HTTPRequest(url=boshUrl))
request401 = Test(401, 'Request a session from the server').wrap(HTTPRequest(url=boshUrl))
request501 = Test(501, 'Get roster').wrap(HTTPRequest(url=boshUrl))
request601 = Test(601, 'Change presence').wrap(HTTPRequest(url=boshUrl))
request701 = Test(701, 'Send one to one message').wrap(HTTPRequest(url=boshUrl))
request801 = Test(801, 'Make an empty request to the server').wrap(HTTPRequest(url=boshUrl))
request901 = Test(901, 'Terminate the session').wrap(HTTPRequest(url=boshUrl))

class TestRunner:
  """A TestRunner instance is created for each worker thread."""
  
  def __init__(self):
    log("agentID %s, processID %s, threadID %s" % (agentID, processID, grinder.threadID))
    self.userID = (agentID * 100000) + (processID * numThreads) + grinder.threadID
    self.targetUserID = (agentID * 100000) + (processID * numThreads) + (grinder.threadID + 1) % numThreads
    log("userID %s, targetUserID %s" % (self.userID, self.targetUserID))
    self.username = userPrefix + str(self.userID)
    self.password = userPrefix + str(self.userID)
    self.targetUser = userPrefix + str(self.targetUserID)
    self.sid = ""
    self.rid = Random().nextInt(1000000)
    self.inactivity = 0

  def initSession(self):
  
    result = request101.POST('',
      '<body xmlns=\"http://jabber.org/protocol/httpbind\" rid=\"' + str(self.rid) + '\" content=\"text/xml; charset=utf-8\" to=\"' + domain + '\" secure=\"true\" wait=\"' + str(boshWait) + '\" ack=\"1\" hold=\"1\" xml:lang=\"en\" xmpp:version=\"1.0\" xmlns:xmpp=\"urn:xmpp:xbosh\" />',
      ( NVPair('Content-Type', 'text/plain; charset=utf-8'), ))
    
    self.rid += 1
    
    body = getXMLcontent(result)
    self.sid = body.getAttribute('sid')
    self.inactivity = int(body.getAttribute('inactivity'))
    log("sid: %s, inactivity: %s" % (self.sid, self.inactivity))
    
    log("getSession response: %s" % result.getText())

    return result

  def auth(self):
    
    authtext = Codecs.base64Encode('%s\x00%s\x00%s' % (self.username + '@' + domain, self.username, self.password))
    log(authtext)
    if authtext[-1] == '\n':
	  authtext = authtext[:-1]
    
    result = request201.POST('',
      '<body xmlns=\"http://jabber.org/protocol/httpbind\" rid=\"' + str(self.rid) + '\" sid=\"' + self.sid + '\"><auth xmlns=\"urn:ietf:params:xml:ns:xmpp-sasl\" mechanism=\"PLAIN\">' + authtext + '</auth></body>',
      ( NVPair('Content-Type', 'text/plain; charset=utf-8'), ))
    
    self.rid += 1
    
    log("auth response: %s" % result.getText())

    return result

  def bind(self):
  
    result = request301.POST('',
      '<body xmlns=\"http://jabber.org/protocol/httpbind\" rid=\"' + str(self.rid) + '\" sid=\"' + self.sid + '\" xmpp:restart=\"true\" xmlns:xmpp=\"urn:xmpp:xbosh\" xml:lang=\"en\" to=\"' + domain + '\"><iq type=\"set\" id=\"bind_1\"><bind xmlns=\"urn:ietf:params:xml:ns:xmpp-bind\"><resource>Home</resource></bind></iq></body>',
      ( NVPair('Content-Type', 'text/plain; charset=utf-8'), ))
    
    self.rid += 1
    
    log("bind response: %s" % result.getText())

    return result

  def requestSession(self):
  
    log("rid = " + str(self.rid))
    result = request401.POST('',
      '<body xmlns=\"http://jabber.org/protocol/httpbind\" rid=\"' + str(self.rid) + '\" sid=\"' + self.sid + '\"><iq type=\"set\" from=\"' + self.username + '@' + domain + '/Home\" to=\"' + domain + '\" id=\"session_2\"><session xmlns=\"urn:ietf:params:xml:ns:xmpp-session\" /></iq></body>',
      ( NVPair('Content-Type', 'text/plain; charset=utf-8'), ))
    
    self.rid += 1
    
    log("requestSession response: %s" % result.getText())

    return result

  def getRoster(self):
  
    log("rid = " + str(self.rid))
    result = request501.POST('',
      '<body xmlns=\"http://jabber.org/protocol/httpbind\" rid=\"' + str(self.rid) + '\" sid=\"' + self.sid + '\"><iq type=\"get\" id=\"roster_3\"><query xmlns=\"jabber:iq:roster\" /></iq></body>',
      ( NVPair('Content-Type', 'text/plain; charset=utf-8'), ))
    
    self.rid += 1
    
    log("getRoster response: %s" % result.getText())

    return result

  def changePresence(self, show):
  
    result = request601.POST('',
      '<body xmlns=\"http://jabber.org/protocol/httpbind\" rid=\"' + str(self.rid) + '\" sid=\"' + self.sid + '\"><presence from=\"' + self.username + '@' + domain + '/Home\"><show>' + show + '</show></presence></body>',
      ( NVPair('Content-Type', 'text/plain; charset=utf-8'), ))
    
    self.rid += 1
    
    log("changePresence %s response: %s" % (show, result.getText()))

    return result

  def sendMessage(self, message, target):
  
    result = request701.POST('',
      '<body xmlns=\"http://jabber.org/protocol/httpbind\" rid=\"' + str(self.rid) + '\" sid=\"' + self.sid + '\"><message type=\"chat\" from=\"' + self.username + '@' + domain + '/Home\" to=\"' + target + '@' + domain + '\"><body>' + message + '</body></message></body>',
    ( NVPair('Content-Type', 'text/plain; charset=utf-8'), ))
    
    self.rid += 1
    
    log("sendMessage response: %s" % result.getText())

    return result

  def poll(self):
  
    result = request801.POST('',
      '<body xmlns=\"http://jabber.org/protocol/httpbind\" rid=\"' + str(self.rid) + '\" sid=\"' + self.sid + '\" />',
      ( NVPair('Content-Type', 'text/plain; charset=utf-8'), ))
    
    self.rid += 1
    
    log("poll response: %s" % result.getText())

    return result

  def terminate(self):
  
    result = request901.POST('',
      '<body xmlns=\"http://jabber.org/protocol/httpbind\" rid=\"' + str(self.rid) + '\" sid=\"' + self.sid + '\" type=\"terminate\"><presence type=\"unavailable\" from=\"' + self.username + '@' + domain + '/Home\" to=\"' + domain + '\" /></body>',
      ( NVPair('Content-Type', 'text/plain; charset=utf-8'), ))
    
    self.rid += 1
    
    log("terminate response: %s" % result.getText())

    return result

  def __call__(self):
    """This method is called for every run performed by the worker thread."""
    
    self.initSession()
    self.auth()
    self.bind()
    self.requestSession()
    self.getRoster()
    
    message = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Duis rutrum porttitor ante. Nunc arcu leo."
    show = "chat"
    
    #for i in range(2):
    while(True):
      if show == "dnd":
        show = "chat"
      else:
        show = "dnd"
      self.changePresence(show)
      if grinder.statistics.forLastTest.time < 5000:
        grinder.sleep(5000 - grinder.statistics.forLastTest.time)
      for j in range(5):
        self.sendMessage(message, self.targetUser)
        if grinder.statistics.forLastTest.time < 5000:
          grinder.sleep(5000 - grinder.statistics.forLastTest.time)
    
    self.terminate()
    
def getXMLcontent(result):
  parser = DOMParser()
  parser.reset()
  parser.parse(InputSource(result.inputStream))
  root = parser.getDocument().getDocumentElement()
    
  return root

def instrumentMethod(test, method_name, c=TestRunner):
  """Instrument a method with the given Test."""
  unadorned = getattr(c, method_name)
  import new
  method = new.instancemethod(test.wrap(unadorned), None, c)
  setattr(c, method_name, method)

# Replace each method with an instrumented version.
# You can call the unadorned method using self.getSession.__target__().
instrumentMethod(Test(100, 'Initiate a BOSH session'), 'initSession')
instrumentMethod(Test(200, 'Authenticate'), 'auth')
instrumentMethod(Test(300, 'Bind resource'), 'bind')
instrumentMethod(Test(400, 'Request a session from the server'), 'requestSession')
instrumentMethod(Test(500, 'Get roster'), 'getRoster')
instrumentMethod(Test(600, 'Change presence'), 'changePresence')
instrumentMethod(Test(700, 'Send one to one message'), 'sendMessage')
instrumentMethod(Test(800, 'Make an empty request to the server'), 'poll')
instrumentMethod(Test(900, 'Terminate the session'), 'terminate')
