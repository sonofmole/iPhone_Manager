# iPhone-Manager
---
A python Discord bot to monitor and have some control over iPhone's connected to a Mac by USB.
To be used along side RDM and RDMMonitor.

## Features
---
The bot will generate a list of iPhones from your RDM build database.
The list will contain the iPhone name, UUID and a generated ID for each iPhone.
The bot will only accept commands from the Discord role you set and post in a channel you set.

+ Manage your iphone's by taking screenshot's and have the bot upload them.
+ Have RDM rebuild and restart Pogo on a iPhone
+ Kill usbmuxd on the Mac, which should have all iPhone's rebuild.
+ Reboot your iPhone
+ Take a screenshot of your Mac and upload to Discord


### Prerequisites
---
iPhone Manager is made using Python3 and will require :

sqlite3

hashlib

discord

psutil

subprocess

asyncio

You will also need libimobiledevice installed on the Mac.

### Troubleshooting libimobiledevice
---
After install of libimobiledevice, check it's working. You can test by taking a screenshot on a iPhone. Connect the iPhone to your Mac and get it's UUID from Xcode, in terminal type:
idevicescreenshot -u your-uuid-of-iphone  This will save a screenshot of the connected iPhone. If you get the error "Could not connect to lockdownd, error code -21" 
please see https://github.com/google/ios-webkit-debug-proxy/issues/290

Info from page
    
    brew update
    brew uninstall --ignore-dependencies libimobiledevice
    brew uninstall --ignore-dependencies usbmuxd
    brew install --HEAD usbmuxd
    brew unlink usbmuxd & brew link usbmuxd
    brew install --HEAD libimobiledevice
    brew link --overwrite libimobiledevice
    brew install ideviceinstaller
    brew link --overwrite ideviceinstaller

### Getting started
---
In iphone_manager.py you will need to edit :

* **Path to the database** 
*Use the full path*

* **Channel name**
*The channel you want the bot to post to*

* **Discord Role**
*The role requied by the user to control the bot*


### Starting the bot
---

    sudo python3 iphone_manager.py


### Usages 
---
**Screenshot device & upload image to discord**

`!sc {device_id} or {device_name}`

*Example : !sc iphone-se1*  &nbsp; **or** &nbsp; *!sc 7ab3*

**Make RDM rebuild & reload pogo**

`!reload {device_id} or {device_name}`

*Example : !reload iphone-se1* &nbsp;  **or**  &nbsp; *!reload 7ab3*

**Reboot iPhone**

`!reboot {device_id} or {device_name}`

*Example : !reboot iphone-se1* &nbsp;  **or** &nbsp;  *!reboot 7ab3*

**Screenshot the Mac**

`!mac grab`


**Kill the usbmuxd process ID**

`!kill usb`









