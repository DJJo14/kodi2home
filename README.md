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

home_adress and home_ssl you not need to change when your are using it in hassio

put somting like this in your keymap of kodi:
```xml
<volume_up>NotifyAll("kodi2home", "kodi_call_home", {"trigger":"automation.volume_up"})</volume_up>
```
add "automation.volume_up" will be triggert, when pressing volume_up

#Why
This is done so you can easy call services at home assistant, the other way around was already possible but, this is still a missing feature of Home Assistant.

#Why this way
With Kodi you can call scripts and with that do the same, because it has to start the script and then connect, it can be a sec later before the action is done.

#How is it done
Kodi2home is not more than two websocket's connected to etch other. One to code lisening to the "NotifyAll" and the other one sending it to Home Assistant.
It is done in a way Home Assistant uses kodi, so if it is liked, it can be intergated in to Home Assistant kodi intergration.

Tip's, commands or spelling error's, just supmit a isue
