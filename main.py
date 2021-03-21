import sys, urllib.request
import time, logging, os
from twilio.rest import Client

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger('main')
logger.setLevel(logging.INFO)

twilio_account_sid = os.environ['TWILIO_ACCOUNT_SID']
twilio_auth_token = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_FROM_NUM = "+16692382013"
TO_NUM_1 = "+19782210132"
TO_NUM_2 = "+18123915218"
westinURL = "https://westin-homes.com/subdivision/santa-rita-ranch-south/"
westinNoInventory = "No Inventory Available"

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
                                     from_ =TWILIO_FROM_NUM, to=TO_NUM_1)
    logger.info(message.sid)

    message = client.messages.create(body="Westin Homes Inventory Is Open!!",
                                     from_=TWILIO_FROM_NUM, to=TO_NUM_2)
    logger.info(message.sid)


if __name__ == '__main__':
    sTimeSecs = int(sys.argv[1])
    exceptionCount = 0
    sendMsgCount = 0
    logger.info('Starting inventory check...')
    while True:
        result = check_inventory()
        if result == 1:
            result = send_msg()
            logger.info("Msg sent, finger's crossed!!")
            sendMsgCount += 1
            if sendMsgCount == 5:
                sys.exit("All msgs have been sent, exiting!!")
        elif result == -1:
            exceptionCount += 1
            if exceptionCount == 5:
                sys.exit("Too many exceptions!!")
        time.sleep(sTimeSecs)
