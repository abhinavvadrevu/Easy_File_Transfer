import tornado.ioloop
from tornado.web import *
import glob
import socket
import urllib

import tornado.httpserver, os.path, random, string


#########################
# Configuration options #
#########################
port = 8002
tornado_options = {
  "port": port
}

#########################
# maketinyurl link      #
#########################

print("initializing... please wait")
IP = socket.gethostbyname(socket.gethostname())

#192.168.0.1068001%2F
#http://tinyurl.com/create.php?source=indexpage&url=http%3A%2F%2F192.168.0.106%3A8001%2F&submit=Make+TinyURL%21&alias=abhinavstest11

myUrl = "http%3A%2F%2F" + str(IP) + '%3A' + str(port) + "%2F"
directfrom = "abhinavsfiles"
"""
reqadd = "http://tinyurl.com/create.php?source=indexpage&url=" + myUrl + "&submit=Make+TinyURL%21&alias=" + directfrom
response = urllib.urlopen(reqadd)
mypage = response.read()
worked = True
if not("not available" in mypage):
    worked = False
"""
index = ''
worked = False
newdirectfrom = ''
while not worked:
    newdirectfrom = directfrom + str(index)
    reqadd = "http://tinyurl.com/create.php?source=indexpage&url=" + myUrl + "&submit=Make+TinyURL%21&alias=" + newdirectfrom
    response = urllib.urlopen(reqadd)
    mypage = response.read()
    if not("not available" in mypage):
        worked = True
    if index == '':
        index = 0
    index += 1
    print("url shortening attempted " + str(index) + " time(s)")
    
    
print("You should open www.tinyurl.com/" + newdirectfrom)
print("This has been directed to reach "+myUrl)

#########################
# Handlers go here      #
#########################

class MainHandler(RequestHandler):
  def get(self):
    toSend1 = glob.glob('My_Docs/*.*')
    toSend2 = []
    for x in toSend1:
        newfile = x[8:]
        toSend2.append(newfile)
    print toSend2
    self.render("index.html",filelist=toSend2)

class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        file1 = self.request.files['file1'][0]
        fname = file1['filename']
        output_file = open("My_Docs/" + fname, 'w')
        output_file.write(file1['body'])
        self.finish("file " + fname + " is uploaded")

############################
# Routes go here           #
############################
application = tornado.web.Application([

  # Add more routes to handle the requests

  (r"/",                 MainHandler),
  (r"/upload",        UploadHandler),
  (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "/var/www"})

  ###### routes end here ######
  
  
#########################
# Don't change this     #
#########################
], debug=True,
   template_path=os.path.join(os.path.dirname(__file__), ""),
   static_path=os.path.join(os.path.dirname(__file__), "My_Docs"),
)




if __name__ == "__main__":
  application.listen(tornado_options["port"])
  tornado.ioloop.IOLoop.instance().start()
