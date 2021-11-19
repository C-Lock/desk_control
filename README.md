# desk_control

## Purpose
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Work provided me a desk. Fancy. Sit to stand. It was crap.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Well, it looked like crap, because the desk-top was cheap, small, and ugly.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;When I began to disassemble it, though, I noticed that the mechanics beneath it's surface were of very high quality.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This is the UPLIFT sit-to-stand desk from a major paper-supply company named after the tiny bits of metal used to bind their paper-products together.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;I decided that the desk-top was the only low quality bit involved, so I kept the desk and purchased a new  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;countertop from a Swedish Furniture store popular in my area. The new countertop is HEAVY (65lbs), but the dual 200N motors on this baby can support that just fine!

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;So, as I'm re-assembling the  desk, I notice an odd rj11 device. It's...bluetooth?!  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;That's right. a bluetooth device set up on an rj-11 port. Why not like, integrate or go USB?  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Anyway, to operate this Bluetooth dongle, and therefore my desk, you've got to DOWNLOAD THE APP.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Yep. Another. Stinking. App.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;As you'd expect, it's a cheap product with Chinese Developer making the app.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;I don't need another app on my phone, especially not a low-budget app which requires camera access to operate.  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Well, it's just a device. At the basic level, it's just sending some data to the desk. If I can identify that data, then I can send that data to the desk myself. Idk, with a pi or something?  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;My first thought was to patch together an rj-11 listening device, path the split to rpi GPIO and just listen in on the physical data transmissions,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;replace the bluetooth all-together with an ethernet cable from the rpi-GPIO to the rj11.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;A Buddy, however, suggested I learn me a bluetooth hack. Turns out it didn't require much hacking. Security was very low.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This repo holds the code used now to control my desk, as well as some auxiliary info obtained during the reverse engineering process.  

---
## Contents
* desk_control.sh : The core of the desk-control ecosystem. Baisc. Get's the Job done. Great for impressing the ladies with Command Line superpowers.
* desk_control.py : A Python3 implementation of the same code. Slightly more refined, designed to allow for easy importing (to an api, maybe write your own app?)
* desk_characteristics.txt : Data from the bluetooth reconnaisance
* bluetooth_ctl_properties.txt : Some attempted reconnaisance using bluetoothctl. MUCH Less useful than gatttool.
* README.MD : A useless file full of sentimental reminiscing
* delta.txt : A saved version of advertised BT data after making a change to height. There's no discernable declaration of the desk height, though. So it's a useless file. (I'm gonna go back to this and learn more, it's simply ***GOT*** to have the data.)

---
## Requirements
### Basic Functionality:
  - Uplift Sit-to-Stand Desk from Staples with the jcp35n-blt bluetooth adapter
  - Linux
  - gatttol installed
  - compatible bluetooth chip/dongle
  
### Advanced Functionality:
  - Basic Requirements+
  - Python3
  - [pygatt](https://github.com/peplin/pygatt) (a Front End for gatttool) (also in the requirements.txt, can be installed via pip.)
  - non-root user with sudo (python can't access the bluetooth without sudo)

---
## Usage

- ***Note***: the 'sit' and 'stand' features presume that you've already saved these values into the desk memory.
   - You can do this with the crappy app, or you can do so with the physical controller.
   - Once you have this script working, you can *unplug the physical controller*.
      - I've tested this, as my toddler recently learned how to push the buttons while I'm working. 
         - That maybe one of the biggest motivations for this codebase.
- ***Note***: Edge Cases. They're a thing. I have not yet identified how to discern the current extension length of the desk. 
   - If you bottom out, it doesn't do anything, but I'm not sure about maxing out. Excersie caution at great heights.

### Bash
1) Once all requirements are met, put the desk_control.sh file wherever you like to put scripts, and make it executable.
2) Edit the desk_control.sh file to replace my bt_addr with your bt_addr.
3) Make your desk bounce like a hydrolic lowrider with `bash desk_control.sh -s stand` or `bash desk_control.sh -s sit`
   

### Python3
1) Once all requirements are met, put the desk_control.py file wherever you like to put scripts, and make it executable.
2) Edit the desk_control.py file to replace my bt_addr with your bt_addr in the `__main__` section.
3) Make your desk bounce like a hydrolic lowrider with `sudo python3 desk_control.py sit` or `sudo python3 desk_control.py raise 10`
   - On my desk, each iteration of `raise` or `lower` is approximately `.3 inches` as measured by my LASER MEASURING TAPE.
---
## Future Features
1) Read the current height from the bluetooth. This will allow setting specific heights in the code.
2) Program my own presets (eliminate physical controls completely!)
3) API Wrapper. That way I can control it from my phone. So cool and innovative!