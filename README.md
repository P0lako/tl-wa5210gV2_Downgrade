# tl-wa5210gV2_Downgrade
This repository contains an exploit  useful for patching the checking mechanism present in TP-LINK WA5210g firmware version 2, disallowing the possibility of a downgrade.
This is intended to install OpenWRT in this device.

step 1:
    The device must be connected via cable to the terminal containins the exploit.
step 2:
    The device's IP must be 192.168.1.254.
step 3: 
    Run the following command: python exploit.py 
step 4:
    Install the firmware v1: http://www.tp-link.com/ar/download/TL-WA5210G_V1.html#Firmware

Once installed the older version, airOS firmware must be installed. Steps for this can be found here: http://arg-wireless.com.ar/index.php?topic=1167.0
After installing airOS firmware, OpenWRT can be deployed

Enjoy it :).

Note: Use it at your own risk 

