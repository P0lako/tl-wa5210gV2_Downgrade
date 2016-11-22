# tl-wa5210gV2_Downgrade
This repository contains an exploit  useful for patching the checking mechanism present in TP-LINK WA5210g firmware version 2, disallowing the possibility of a downgrade. <br />
This is intended to install OpenWRT in this device. <br />

<b>step 1: </b><br />
&emsp;The device must be connected via cable to the terminal containins the exploit. <br />
<b>step 2: </b> <br />
&emsp;The device's IP must be 192.168.1.254. <br />
<b>step 3: </b>  <br />
&emsp;Run the following command: python exploit.py  <br />
<b>step 4: </b> <br />
&emsp;Install the firmware v1: http://www.tp-link.com/ar/download/TL-WA5210G_V1.html#Firmware <br />

Once installed the older version, airOS firmware must be installed. Steps for this can be found here: http://arg-wireless.com.ar/index.php?topic=1167.0 <br />
After installing airOS firmware, OpenWRT can be deployed <br />

Enjoy it :). <br />

Note: Use it at your own risk  <br />

