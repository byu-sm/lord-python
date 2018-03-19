
#COM_PORT = "COM3"
#BS_BAUD = 921600
#NODE_ADD = 56609
#THINGWORX_HOST = "localhost"
#APP_KEY = "513a4151-3702-4998-9676-e4416d1fe3fe"
#HTTP_BASIC_AUTH = "Basic QWRtaW5pc3RyYXRvcjpQZXRlck9zb1NvbmdUMW0z"

import testing

COM_PORT = input("Comport:")
print (COM_PORT)
BS_BAUD = input("BS_BAUD Number:")
NODE_ADD = input("NODE_ADD Number:")
THINGWORX_HOST = input("Thingworx host:")
APP_KEY = input("Api Key")

testing.test()
HTTP_BASIC_AUTH = input("http Basic Auth:")
