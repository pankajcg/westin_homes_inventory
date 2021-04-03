import sys, urllib.request
import time, logging, os, threading
from twilio.rest import Client
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger('main')
logger.setLevel(logging.INFO)

twilio_account_sid = os.environ['TWILIO_ACCOUNT_SID']
twilio_auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_from_num = os.environ['TWILIO_FROM_NUM']
twilio_to_num_1 = os.environ['TWILIO_TO_NUM_1']
twilio_to_num_2 = os.environ['TWILIO_TO_NUM_2']
westinURL = "https://westin-homes.com/subdivision/santa-rita-ranch-south/"
westinNoInventory = "No Inventory Available"
serverHostName = "localhost"
serverPort = 8080

def check_inventory():
    try:
        logger.info("Checking Inventory...")
        res = urllib.request.urlopen(westinURL)
        resStr = res.read()
        resStr = resStr.decode('utf-8')
        if westinNoInventory in resStr:
            logger.info("Inventory not found... :(")
            return 0
        else:
            logger.info("Found Inventory!!!")
            return 1
    except:
        logger.warning(res)
        return -1

def send_msg():
    logger.info("Build and send msg!")
    client = Client(twilio_account_sid, twilio_auth_token)
    message = client.messages.create(body="Westin Homes Inventory Is Open!!",
                                     from_ =twilio_from_num, to=twilio_to_num_1)
    logger.info(message.sid)

    message = client.messages.create(body="Westin Homes Inventory Is Open!!",
                                     from_=twilio_from_num, to=twilio_to_num_2)
    logger.info(message.sid)

def inventory_checker(sTimeSecs):
    exceptionCount = 0
    sendMsgCount = 0
    logger.info('Starting inventory check...')
    while True:
        result = check_inventory()
        if result == 1:
            send_msg()
            logger.info("Msg sent, finger's crossed!!")
            sendMsgCount += 1
            if sendMsgCount == 5:
                logger.info("All msgs have been sent, exiting!!")
                return
        elif result == -1:
            exceptionCount += 1
            if exceptionCount == 5:
                logger.info("Too many exceptions!!")
                return
        time.sleep(sTimeSecs)

class HttpServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>Web Server</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>Sorry, nothing here!! :( </p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

def start_server():
    webServer = HTTPServer((serverHostName, serverPort), HttpServer)
    logger.info('Starting server (http://%s:%s)...', serverHostName, serverPort)

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    logger.info('Stopping server thread...')


if __name__ == '__main__':
    sTimeSecs = int(sys.argv[1])
    inv_chk_thr = threading.Thread(target=inventory_checker, args=(sTimeSecs,))
    dummy_server = threading.Thread(target=start_server(), args=())
    inv_chk_thr.start()
    dummy_server.start()
    inv_chk_thr.join()
    dummy_server.join()
