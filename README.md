# iPhone-Manager
---
A Python Discord bot to monitor and have some control over iPhone's connected to a Mac by USB.
To be used along side RDM. 

## Features
---
iPhone-Manage will generate a list of iPhones from your RDM manager SQLite database(s).
The list will contain the iPhone name, UUID and a generated ID for each iPhone.
iPhone-Manage will only accept commands from the Discord role you set and only post in a channel you set.
All config settings are in a YAML file.

+ Manage your iphone's by taking screenshot's and have them upload to Discord.
+ Have RDM rebuild and restart Pogo on an iPhone
+ Kill usbmuxd on the Mac (it will auto restart), which should have all iPhone's rebuild.
+ Reboot your iPhone
+ Take a screenshot of your Mac and upload to Discord


### Prerequisites
---
iPhone Manager is made using Python3 and will require :

pyyaml

discord

psutil

Xcode 10.2.1>


You will also need libimobiledevice installed on the Mac.

### Troubleshooting libimobiledevice
---
After install of libimobiledevice, check it's working. You can test by taking a screenshot on an iPhone. Connect the iPhone to your Mac and get it's UUID from Xcode, in terminal type:
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
Install the Python3 requirements using pip3 install -r requirements.txt 

In config.yaml you will need to edit :

* **Path to the database :** 
*A Python list, use full path including filename and extension*

* **Channel name :**
*The channel you want the bot to post to*

* **Discord Role :**
*The role required by the user to control the bot*

* **Discord Token :**
*Enter your bot token*


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

**Display the help**

`!help`








