kodi2home
=========
kodi calling Home Assistant

Install by going to Supervisor -> Add-on store -> Add new repository by url and fill in `https://github.com/DJJo14/kodi2home`.

Example config for the add-on:
```yaml
kodi_adress: youre kodi ip adress
kodi_http_port: 8080
kodi_ws_port: 9090
kodi_username: Youre username
kodi_password: Youre password
home_adress: 'ws://supervisor/core/api/websocket'
home_ssl: false
```

if you are using hassio you do not need to change the home_adress and home_ssl. the values are already set to the add-on values.

put somting like this in your keymap of kodi:
```xml
<volume_up>NotifyAll("kodi2home", "kodi_call_home", {"trigger":"automation.volume_up"})</volume_up>
```
add "automation.volume_up" will be triggert, when pressing volume_up.


## Why
This is done so you can easy call services at home assistant, the other way around was already possible but, this is still a missing feature of Home Assistant.

## Why this way
With Kodi you can call scripts and with that do the same, because it has to start the script and then connect, it can be a sec later before the action is done.

## How is it done
Kodi2home is not more than two websocket's connected to etch other. One to code lisening to the "NotifyAll" and the other one sending it to Home Assistant. Both of the websockets are already connected.
It is done in a way Home Assistant uses kodi, so if it is liked, it can be intergated in to Home Assistant kodi intergration.

### Reload keymap
When you start the addon the keymap of kodi gets reloaded. So no need to restart all of kodi when changing the keymap(.xml), just restart the addon

## Known issue
For some reason Home Assistant disconnects when you fire to may, automations at ones. and it response to that with a disconnect, i do not know a better way to then to just reconnect. 

# example
In webos_example_automation.yaml there is a example of the automations that switches the remote between kodi(at the HDMI) and the webos apps. This way you can control the tv with one remote. For example a Measy GP811 or a RII usb wireless keyboard. In webos_example_keymap.xml is the kodi keymap to use with that.

Tip's, commands or spelling error's, just submit an issue
