kodi2home
=========
kodi calling home assistant

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