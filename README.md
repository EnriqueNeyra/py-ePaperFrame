# py-ePaperFrame - Dynamic ePaper Picture Frame Powered by Raspberry pi

IMAGE HERE

### The py-ePaperFrame is a digital picture frame that utilizes the **[Waveshare 5.65 7-Color ePaper Display](https://www.waveshare.com/5.65inch-e-paper-module-f.htm)** for a natural look. Use the integrated WebUI to easily upload 

## Contents:
[Required Hardware](#required-hardware-and-assembly)  
[Setup](#setup)  
[WebUI Usage](#using-the-web-ui)

## Required Hardware and Assembly

### Hardware
- **Raspberry Pi Zero 2 W**
- **ePaper Display:** The current version of this application only supports the [Waveshare 5.65 7-Color ePaper Display](https://www.waveshare.com/5.65inch-e-paper-module-f.htm)
- **Picture Frame**: Any frame or stand of your choice. A 6x8 frame like [this](https://www.amazon.com/dp/B0D24P42SM?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1) goes well with the 5.65 inch display

### Assembly


## Setup

**Before starting**, ensure that your Pi is running Pi OS or OS Lite, and is connected to your home network

Run the following commands to complete the setup:
```
git clone https://github.com/EnriqueNeyra/py-ePaperFrame.git 
cd py-ePaperFrame
sudo bash setup.sh
```

Be sure to reboot the Pi after the setup completes!

## Web UI Usage
After completing the setup and rebooting your Pi, a QR code should display. Scan the QR code to access the Web UI. Alternatively, you can open any browser and go to **<Pi_IP_Address>.local:5000** to access the Web UI.

IMAGE HERE

### Summary of Controls
**Start Button**: This button starts the display, making it cycle through images you have uploaded in random order  
**Reset Button**: Use this to clear the display in the case of any image artifacts  
**Image Upload**: Supported formats include JPG, JPEG, and PNG  
**Removing Images**: Use the red 'X' in the upper left of an image thumbnail to permanently remove it



