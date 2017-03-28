import asyncio
import time
import os

#os.chdir("/var/www/html")
OUTPUT_PAGE = os.getcwd()+"/orb.html"
GAMES = ["/arcanistsmulti/serverlist.ws",
         "/armiesofgielinor/serverlist.ws",
         "/bachelorfridge/serverlist.ws",
         "/brickabrac/serverlist.ws",
         "/chess/serverlist.ws",
         "/dekobloko/serverlist.ws",
         "/kickabout/serverlist.ws",
         "/pixelate/serverlist.ws",
         "/pool/serverlist.ws",
         "/shatteredplans/serverlist.ws",
         "/steelsentinels/serverlist.ws",
         "/tetralink/serverlist.ws",
         "/tombracer/serverlist.ws",
         "/vertigo2/serverlist.ws",
         "/virogrid/serverlist.ws",
         "/voidhunters/serverlist.ws",
         "/zombiedawnmulti/serverlist.ws"]

def retrieveHTML(url):
    response = urllib.request.urlopen(url)
    html = str(response.read(),"ISO-8859-1")
    html = html[html.rfind("<tbody>"):html.find("</tbody>")]
    return html

@asyncio.coroutine
def async_retrieveHTML(url):
    connect = asyncio.open_connection("funorb.com",80)
    reader,writer = yield from connect
    writer.write("GET {} HTTP/1.0\r\nHost: funorb.com\r\n\r\n".format(url).encode("UTF-8"))
    html = yield from reader.read()
    html = str(html, "ISO-8859-1")
    return html[html.rfind("<tbody>")+len("<tbody>"):html.find("</tbody>")]

def cleanEntry(html):
    html = html.strip()
    html = html.replace('a onclick="suffixize(this)"', "a")
    html = html.replace(' class="row_b"', "")
    html = html.replace(' class="row_c"', "")
    return html

#MAIN:
start = time.time()

eventLoop = asyncio.get_event_loop()
bodyHTML = eventLoop.run_until_complete(asyncio.gather(*[async_retrieveHTML(url) for url in GAMES]))
eventLoop.close()

bodyHTML = [cleanEntry(x) for x in bodyHTML]

runtime = time.time() - start
tableBody = "".join(bodyHTML)
with open(OUTPUT_PAGE,mode="w") as file:
    file.write("""<html><head><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"><link rel="icon" type="image/png" href="/favicon-32x32.png" sizes="32x32"><link rel="icon" type="image/png" href="/favicon-16x16.png" sizes="16x16"><link rel="manifest" href="/manifest.json"><link rel="mask-icon" href="/safari-pinned-tab.svg" color="#5bbad5"><meta name="theme-color" content="#ffffff"><meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate, max-age=0"><meta http-equiv="Pragma" content="no-cache, no-store"><meta http-equiv="Expires" content="0"><title>FanOrb Central</title></head><body><table><thead><tr><th>Server</th><th>Location</th><th>Capacity</th><th>Players</th><th>Type</th></tr></thead><tbody>"""+tableBody+"""</tbody></table><p>This table was generated at """+time.asctime(time.gmtime(time.time()))+""" (GMT).<br>Script checks FunOrb servers approximately once per minute. <a href="http://binarydigit.io/orb">Refresh</a> to update.</p><p style="color:white;">"""+str(runtime)+"""</p></body></html>""")
