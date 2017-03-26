from tornado import ioloop, httpclient
import time
import os

#os.chdir("/var/www/html")
OUTPUT_PAGE = os.getcwd()+"/orb.html"
GAMES = {"http://www.funorb.com/arcanistsmulti/serverlist.ws":0,
         "http://www.funorb.com/armiesofgielinor/serverlist.ws":1,
         "http://www.funorb.com/bachelorfridge/serverlist.ws":2,
         "http://www.funorb.com/brickabrac/serverlist.ws":3,
         "http://www.funorb.com/chess/serverlist.ws":4,
         "http://www.funorb.com/dekobloko/serverlist.ws":5,
         "http://www.funorb.com/kickabout/serverlist.ws":6,
         "http://www.funorb.com/pixelate/serverlist.ws":7,
         "http://www.funorb.com/pool/serverlist.ws":8,
         "http://www.funorb.com/shatteredplans/serverlist.ws":9,
         "http://www.funorb.com/steelsentinels/serverlist.ws":10,
         "http://www.funorb.com/tetralink/serverlist.ws":11,
         "http://www.funorb.com/tombracer/serverlist.ws":12,
         "http://www.funorb.com/vertigo2/serverlist.ws":13,
         "http://www.funorb.com/virogrid/serverlist.ws":14,
         "http://www.funorb.com/voidhunters/serverlist.ws":15,
         "http://www.funorb.com/zombiedawnmulti/serverlist.ws":16}
bodyHTML = [None]*len(GAMES)

_i = 0
http_client = httpclient.AsyncHTTPClient()

def voodoo(response):
    html = str(response.body,"ISO-8859-1")
    html = html[html.rfind("<tbody>"):html.find("</tbody>")]
    bodyHTML[GAMES[response.effective_url]] = html
    global _i
    _i -= 1
    if _i == 0:
        ioloop.IOLoop.instance().stop()
        tableBody = ""
        for content in bodyHTML:
            tableBody += content
        runtime = time.time() - start
        with open(OUTPUT_PAGE,mode="w") as file:
            file.write("""<html><head><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"><link rel="icon" type="image/png" href="/favicon-32x32.png" sizes="32x32"><link rel="icon" type="image/png" href="/favicon-16x16.png" sizes="16x16"><link rel="manifest" href="/manifest.json"><link rel="mask-icon" href="/safari-pinned-tab.svg" color="#5bbad5"><meta name="theme-color" content="#ffffff"><meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate, max-age=0"><meta http-equiv="Pragma" content="no-cache, no-store"><meta http-equiv="Expires" content="0"><title>FanOrb Central</title></head><body><table><thead><tr><th>Server</th><th>Location</th><th>Capacity</th><th>Players</th><th>Type</th></tr></thead>"""+tableBody+"""</tbody></table><p>This table was generated at """+time.asctime(time.gmtime(time.time()))+""" (GMT).<br>Script checks FunOrb servers approximately once per minute. <a href="http://binarydigit.io/orblist">Refresh</a> to update.</p><p style="color:white;">"""+str(runtime)+"""</p></body></html>""")

for url in GAMES.keys():
    _i += 1
    http_client.fetch(url, voodoo)

start = time.time()
ioloop.IOLoop.instance().start()
