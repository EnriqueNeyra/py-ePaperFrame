# pyePaper - A Dynamic ePaper Picture Frame Powered by Raspberry Pi

![IMG_1018](https://github.com/user-attachments/assets/1bd1e7ef-88f7-4934-b615-8c36d0d4ea9e)

### The pyePaper is a digital picture frame that utilizes the **[Waveshare 5.65 7-Color ePaper Display](https://www.waveshare.com/5.65inch-e-paper-module-f.htm)** for a natural look. Use the integrated WebUI to upload images that the display will automatically cycle through at a set time interval.

## Contents:
[Required Hardware](#required-hardware-and-assembly)  
[Setup](#setup)  
[WebUI Usage](#using-the-web-ui)
[Video Demo](#video-demo)

## Required Hardware

- **Raspberry Pi Zero 2 W**
- **ePaper Display:** The current version of this application only supports the [Waveshare 5.65 7-Color ePaper Display](https://www.waveshare.com/5.65inch-e-paper-module-f.htm)
- **Picture Frame**: Any frame or stand of your choice. A 6x8 frame like [this](https://www.amazon.com/dp/B0D24P42SM?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1) goes well with the 5.65 inch display

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
After completing the setup and rebooting your Pi, a QR code will be displayed. Scan this QR code to access the Web UI. Alternatively, you can open any browser and go to **<Pi_IP_Address>.local:5000** to access the Web UI.

<p align="center">
<img src="https://github.com/user-attachments/assets/539b5ac4-83e3-44b7-b96b-35676409df7b" alt="Alt Text" width="300" >
</p>

### Summary of Controls
**Start Button**: This button starts the display, making it cycle through images you have uploaded in random order  
**Reset Button**: Use this to clear the display in the case of any image artifacts  
**Image Upload**: Supported formats include JPG, JPEG, and PNG  
**Removing Images**: Use the red 'X' in the upper left of an image thumbnail to permanently remove it

## Video Demo
Note: The video was shortened due to upload size constraints. Actual screen refresh time is ~30 seconds
<video src="https://github.com/user-attachments/assets/684ee0bd-c2ec-477d-89fd-c4c316bff03f" />



