## Rust Drop Grabber
A Bot Which Watches & Claims Rust Drops For You.

- Linux optimization.
- Firefox & Chrome support.

### ● How it works

The Bot makes a request to https://twitch.facepunch.com/ and Scrapes Streamer, Drop Name & Live Status.<br/>
Then it will check your drop status making a request to the GQL API from Twitch.<br/>
After that it will watch & claim the drop.

<br/>

### ● Preview

![](https://i.gyazo.com/8e5cf453599d15a4d731672228f15822.png)<br/><br/>


### ● Requirements
 ```bash 
 pip install -r requirements.txt
```
> Twitch OAuth Key, https://www.twitch.tv/ > Inspect Element > Network > Click one of the GQL requests https://ibb.co/gR1vYvh<br/>
> Geckodriver (Firefox): https://github.com/mozilla/geckodriver/releases<br/>
> Chromedriver (Chrome): https://sites.google.com/a/chromium.org/chromedriver/downloads/<br/>

<br/>

### ● Config File

| Key           | Description                          |
| ------------- |:------------------------------------:|
| OAuth         | Twitch OAuth Key (Not Twitch API v5) |
| Browser       | Firefox or Chrome.                   |
| Headless      | Headless Mode [true/false]           |
| ChromePath    | Chrome Profile: URL chrome://version     |
| FirefoxPath   | Firefox Profile: URL about:support       |


<br/>
<br/>
<a href="https://www.buymeacoffee.com/GoekhanA" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-blue.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 100px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>



