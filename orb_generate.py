import urllib.request
import time
import os

#os.chdir("/var/www/html")
OUTPUT_PAGE = os.getcwd()+"/orb.html"
GAMES = ["http://www.funorb.com/arcanistsmulti/serverlist.ws",
         "http://www.funorb.com/armiesofgielinor/serverlist.ws",
         "http://www.funorb.com/bachelorfridge/serverlist.ws",
         "http://www.funorb.com/brickabrac/serverlist.ws",
         "http://www.funorb.com/chess/serverlist.ws",
         "http://www.funorb.com/dekobloko/serverlist.ws",
         "http://www.funorb.com/kickabout/serverlist.ws",
         "http://www.funorb.com/pixelate/serverlist.ws",
         "http://www.funorb.com/pool/serverlist.ws",
         "http://www.funorb.com/shatteredplans/serverlist.ws",
         "http://www.funorb.com/steelsentinels/serverlist.ws",
         "http://www.funorb.com/tetralink/serverlist.ws",
         "http://www.funorb.com/tombracer/serverlist.ws",
         "http://www.funorb.com/vertigo2/serverlist.ws",
         "http://www.funorb.com/virogrid/serverlist.ws",
         "http://www.funorb.com/voidhunters/serverlist.ws",
         "http://www.funorb.com/zombiedawnmulti/serverlist.ws"]

def retrieveHTML(url):
    response = urllib.request.urlopen(url)
    html = str(response.read(),"ISO-8859-1")
    html = html[html.rfind("<tbody>"):html.find("</tbody>")]
    return html

async def gen_retrieveHTML(urls):
    for url in urls:
        yield retrieveHTML(url)

start = time.time()
bodyHTML = [retrieveHTML(url) for url in GAMES]
runtime = time.time() - start
tableBody = "".join(bodyHTML)
with open(OUTPUT_PAGE,mode="w") as file:
    file.write("""<html><head><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"><link rel="icon" type="image/png" href="/favicon-32x32.png" sizes="32x32"><link rel="icon" type="image/png" href="/favicon-16x16.png" sizes="16x16"><link rel="manifest" href="/manifest.json"><link rel="mask-icon" href="/safari-pinned-tab.svg" color="#5bbad5"><meta name="theme-color" content="#ffffff"><meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate, max-age=0"><meta http-equiv="Pragma" content="no-cache, no-store"><meta http-equiv="Expires" content="0"><title>FanOrb Central</title></head><body><table><thead><tr><th>Server</th><th>Location</th><th>Capacity</th><th>Players</th><th>Type</th></tr></thead>"""+tableBody+"""</tbody></table><p>This table was generated at """+time.asctime(time.gmtime(time.time()))+""" (GMT).<br>Script checks FunOrb servers approximately once per minute. <a href="http://binarydigit.io/orb">Refresh</a> to update.</p><p style="color:white;">"""+str(runtime)+"""</p></body></html>""")
