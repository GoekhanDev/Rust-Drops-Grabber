import requests, os, time, json, datetime, sys, platform, psutil
from colorama import Back, Fore, Style, init
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

init(convert=True)

class Twitch(): 

    def __init__(self):

        if platform.system() == "Linux": 
            self.clean = "clear"
            self.FDriverPath = "./geckodriver"
            self.CDriverPath = "./chromedriver"
        elif platform.system() == "Windows":
            sys.stdout.write('\33]0;Rust Drop Grabber | gökhan.dev\a')
            self.clean = "cls"
            self.FDriverPath = "./geckodriver.exe"
            self.CDriverPath = "./chromedriver.exe"

        os.system(self.clean)
        confingjson = json.dumps({"Config":{"OAuth":"","Browser":"Firefox","Headless":True,"ChromePath":"","FirefoxPath":""}}, indent=4)

        while True:
            if not os.path.exists("config.json"): 
                open("config.json", "w+").write(confingjson)
                print("Please Configure config.json, Closing in 3 seconds...")
                time.sleep(3), sys.exit(0)
            else:
                self.Config = json.loads(open("config.json", "r+").read())
                break
        
        for key in self.Config["Config"]: 
            if key != "ChromePath" and key != "FireFoxPath":
                if self.Config["Config"][key] == "":
                    print(f"{key} value is empty in config.json! Closing in 3 seconds...")
                    time.sleep(3), sys.exit(0)

        if self.Config["Config"]["Browser"] == "Chrome": self.Browser = True
        elif self.Config["Config"]["Browser"] == "Firefox": self.Browser = False

        self.Auth = self.Config["Config"]["OAuth"]
        self.ChromeProfile = self.Config["Config"]["ChromePath"].replace("\\", "\\\\")
        self.FirefoxProfile = self.Config["Config"]["FirefoxPath"].replace("\\", "\\\\")
        
        self.Watching = f"{Fore.MAGENTA} Getting ready... {Style.RESET_ALL}"
        self.Watch()

    def Firefox(self):

        for proc in psutil.process_iter():
            if proc.name() == "firefox.exe": proc.kill()

        options = Options()
        if self.Config["Config"]["Headless"] == True: options.headless = True

        profile = webdriver.FirefoxProfile(self.FirefoxProfile)
        profile.set_preference("media.volume_scale", "0.0")
        profile.update_preferences()

        self.driver = webdriver.Firefox(executable_path=self.FDriverPath, firefox_profile=profile, options=options)

    def Chrome(self):

        for proc in psutil.process_iter():
            if proc.name() == "chrome.exe": proc.kill()
        
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_argument('lang=en')
        options.add_argument("--mute-audio")
        options.add_argument(f"user-data-dir={self.ChromeProfile}")

        if self.Config["Config"]["Headless"] == True: options.add_argument('headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(executable_path=self.CDriverPath, options=options)

    def Resources(self):

        self.Drops = []

        response = requests.get("https://twitch.facepunch.com/")
        soup = BeautifulSoup(response.text, "lxml")

        Streamer = [Link["href"] for Link in soup.find_all("a", class_="drop", href=True)]
        Items = [Drop.text for Drop in soup.find_all('h3', class_="title")]
        Status = [''.join(i for i in Stats.text if i not in [" ", "\n", "\r"]) for Stats in soup.find_all('div', class_="status")]

        for x, item in enumerate(Streamer):
            try: self.Drops.append([Items[x], Streamer[x], Status[x]])
            except: pass

        response = requests.post('https://gql.twitch.tv/gql', headers={'Authorization': f'OAuth {self.Auth}'}, 
            data='[{"operationName":"Inventory","variables":{},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"e0765ebaa8e8eeb4043cc6dfeab3eac7f682ef5f724b81367e6e55c7aef2be4c"}}}]').json()

        for JSON in response:
            for JSON in JSON["data"]["currentUser"]["inventory"]["gameEventDrops"]:
                for Item in self.Drops:
                    if Item[0] == JSON["name"]: self.Drops.remove(Item)

    def Status(self):

        self.Stats = []

        response = requests.post('https://gql.twitch.tv/gql', headers={'Authorization': f'OAuth {self.Auth}'}, 
            data='[{"operationName":"Inventory","variables":{},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"e0765ebaa8e8eeb4043cc6dfeab3eac7f682ef5f724b81367e6e55c7aef2be4c"}}}]').json()

        for JSON in response:
            for JSON in JSON["data"]["currentUser"]["inventory"]["dropCampaignsInProgress"]:
                for JSON in JSON["timeBasedDrops"]:
                    if JSON["campaign"]["accountLinkURL"] == "https://twitch.facepunch.com/":
                        if JSON['self']['isClaimed'] != True:
                            if JSON['requiredMinutesWatched'] != JSON['self']['currentMinutesWatched']: self.Stats.append([JSON['name'], JSON['requiredMinutesWatched'], JSON['self']['currentMinutesWatched']])
                            else: 
                                self.Stats.append([JSON['name'], "CLAIMABLE", JSON["self"]['dropInstanceID']])
                                for Item in self.Drops:       
                                    if Item[0] == JSON['name']: self.Drops.remove(Item)
                        else: pass

        os.system(self.clean)

        print(f"Drop Status - Last Checked: {Fore.CYAN + str(datetime.datetime.now())[:-7]} \n")

        if len(self.Stats) != 0: 
            for Info in self.Stats:
                if Info[1] != "CLAIMABLE": print(f"{Fore.RED + Info[0]} {Fore.WHITE}| Required: {Fore.YELLOW + str(Info[1])} Minutes {Fore.WHITE}| Watched: {Fore.GREEN + str(Info[2]) + Style.RESET_ALL} Minutes")
                else: print(f"{Fore.GREEN + Info[0]} | CLAIMABLE!{Style.RESET_ALL}")
        elif len(self.Stats) == 0: print("No Active Drops.")
        
        print(f"\nBot Status: {self.Watching}")

        

    def Watch(self):

        if self.Browser == True: self.Chrome()
        elif self.Browser == False: self.Firefox()

        Link = ""

        while True:
            self.Resources()
            if len(self.Drops) == 0: 
                os.system(self.clean)
                print("You already have all drops, closing in 3 seconds...")
                time.sleep(3), sys.exit(0)
            for Item in self.Drops:
                if "Live" in Item: 
                    Link = Item[1]
                    self.Drop = Item[0]
            if Link == "": 
                os.system(self.clean)
                print("\rWaiting for Streamers to go Live...")
                time.sleep(5)
                continue
            break

        self.Status()

        while True: 
            self.driver.get(Link)

            time.sleep(5)

            soup = BeautifulSoup(self.driver.page_source, "lxml")
            Restricted = soup.find("p", class_="content-overlay-gate__allow-pointers tw-c-text-overlay tw-font-size-4 tw-line-height-heading tw-strong")
            
            if Restricted != None:
                if Restricted.text == "The broadcaster has indicated that this channel is intended for mature audiences.":
                    self.driver.find_element_by_xpath("//body[1]/div[1]/div[1]/div[2]/div[1]/main[1]/div[2]/div[3]/div[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[5]/div[1]/div[3]/button[1]/div[1]/div[1]").click()

            while True:
                os.system(self.clean)

                self.Watching = f"Currently Watching {Fore.GREEN + Link + Style.RESET_ALL}"
                self.Resources()
                self.Status()

                for Item in self.Drops:
                    if Item[1] == Link:
                        if Item[2] == "Live": pass
                        elif Item[2] == "Offline":
                            os.system(self.clean)
                            print(f"Streamer {Link.split('/')[-1]} went Offline. Moving on to the next Drop...")
                            time.sleep(2)
                            self.driver.quit()
                            Twitch()

                for Item in self.Stats: 
                    if Item[0] == self.Drop:
                        if Item[1] != "CLAIMABLE": pass
                        elif Item[1] == "CLAIMABLE":
                            os.system(self.clean)
                            
                            response = requests.post('https://gql.twitch.tv/gql', headers={'Authorization': f'OAuth {self.Auth}'}, 
                                data='[{"operationName":"DropsPage_ClaimDropRewards","variables":{"input":{"dropInstanceID":"' + str(Item[2]) +'"}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"2f884fa187b8fadb2a49db0adc033e636f7b6aaee6e76de1e2bba9a7baf0daf6"}}}]')
                            
                            print(f"{self.Drop} Claimed! Moving on to the next Drop...")
                            self.driver.quit()
                            time.sleep(2)

                            Twitch()

                time.sleep(60)
        
        Twitch()


if __name__ == "__main__":
    Twitch()
