#! /usr/bin/env python3
try:
    import requests, json, datetime, re, os, time, sys
    from rich.console import Console
    from rich import print
    from rich.columns import Columns
    from rich.panel import Panel
    from requests.exceptions import RequestException
    from Penyimpanan.i18n.manager import i18n
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except Exception as e:
    __import__('sys').exit(f"[Error] {str(e).capitalize()}!")

SUKSES, GAGAL, CREDITS = [], [], {"Total": 0}
session = requests.Session()

class Pengaturan:

    def __init__(self) -> None:
        pass

    def launch_browser(self) -> uc.Chrome:
        """Launch undetected-chromedriver browser"""
        try:
            options = uc.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = uc.Chrome(options=options)
            return driver
        except Exception as e:
            print(Panel(f"[bold red]{i18n.get_text('login.browser_login.launch_failed')}: {str(e)}", width=55, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
            sys.exit()

    def get_facebook_cookies(self, driver: uc.Chrome) -> str:
        """Get Facebook cookies after manual login"""
        try:
            driver.get("https://www.facebook.com")
            print(Panel(f"""[bold white]{i18n.get_text('login.browser_login.facebook')}

[bold white]1. {i18n.get_text('login.browser_login.instructions.step1')}
2. {i18n.get_text('login.browser_login.instructions.step2')}
3. {i18n.get_text('login.browser_login.instructions.step3')}
4. {i18n.get_text('login.browser_login.instructions.step4')}""",
                width=55, style="bold bright_white", title="[bold bright_white]>> [Facebook Login] <<"))
            
            # Wait for successful login by checking for multiple possible elements
            WebDriverWait(driver, 600).until(
                EC.any_of(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[role='feed']")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Home']")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-pagelet='Stories']"))
                )
            )
            
            # Additional delay to ensure cookies are set
            time.sleep(5)
            
            # Double check we're actually logged in
            if "c_user" not in [cookie['name'] for cookie in driver.get_cookies()]:
                raise Exception("Facebook login not detected. Please complete the login process.")
            
            print(Panel(f"[bold green]{i18n.get_text('login.browser_login.success')}", width=55, style="bold bright_white"))
            
            cookies = driver.get_cookies()
            if not cookies:
                raise Exception("No cookies found after login")
                
            cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
            return cookie_str
            
        except Exception as e:
            print(Panel(f"""[bold red]{i18n.get_text('login.browser_login.cookies_failed.facebook')}: {str(e)}

[bold white]{i18n.get_text('login.browser_login.troubleshooting.title')}
1. {i18n.get_text('login.browser_login.troubleshooting.step1')}
2. {i18n.get_text('login.browser_login.troubleshooting.step2')}
3. {i18n.get_text('login.browser_login.troubleshooting.step3')}
4. {i18n.get_text('login.browser_login.troubleshooting.step4')}""", width=55, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
            return None

    def get_like4like_cookies(self, driver: uc.Chrome) -> str:
        """Get Like4Like cookies after manual login"""
        try:
            driver.get("https://www.like4like.org/login/")
            print(Panel(f"""[bold white]{i18n.get_text('login.browser_login.like4like')}

[bold white]1. {i18n.get_text('login.browser_login.instructions.step1')}
2. {i18n.get_text('login.browser_login.instructions.step2')}
3. {i18n.get_text('login.browser_login.instructions.step3')}
4. {i18n.get_text('login.browser_login.instructions.step4')}""",
                width=55, style="bold bright_white", title="[bold bright_white]>> [Like4Like Login] <<"))
            
            # Wait for successful login by checking for earn feature page
            WebDriverWait(driver, 600).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='earn-facebook-subscribes.php']"))
            )
            
            print(Panel(f"[bold green]{i18n.get_text('login.browser_login.success')}", width=55, style="bold bright_white"))
            
            time.sleep(2)
            
            cookies = driver.get_cookies()
            if not cookies:
                raise Exception("No cookies found after login")
                
            cookie_str = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
            return cookie_str
            
        except Exception as e:
            print(Panel(f"""[bold red]{i18n.get_text('login.browser_login.cookies_failed.like4like')}: {str(e)}

[bold white]{i18n.get_text('login.browser_login.troubleshooting.title')}
1. {i18n.get_text('login.browser_login.troubleshooting.step1')}
2. {i18n.get_text('login.browser_login.troubleshooting.step2')}
3. {i18n.get_text('login.browser_login.troubleshooting.step3')}
4. {i18n.get_text('login.browser_login.troubleshooting.step4')}""", width=55, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
            return None

    def Login(self) -> None:
        """Handle login process with browser automation"""
        try:
            Terminal().Banner()
            
            # Step 1: Like4Like Login
            print(Panel(f"[bold white]{i18n.get_text('login.browser_login.steps.like4like')}", width=55, style="bold bright_white"))
            driver_l4l = self.launch_browser()
            cookies_like4like = self.get_like4like_cookies(driver_l4l)
            driver_l4l.quit()
            
            if not cookies_like4like:
                raise Exception("Like4Like login failed")
            
            self.credits = self.Like4Like(cookies_like4like, Login=True)
            
            # Step 2: Facebook Login
            print(Panel(f"[bold white]{i18n.get_text('login.browser_login.steps.facebook')}", width=55, style="bold bright_white"))
            driver_fb = self.launch_browser()
            cookies_facebook = self.get_facebook_cookies(driver_fb)
            driver_fb.quit()
            
            if not cookies_facebook:
                raise Exception("Facebook login failed")
            
            self.name, self.user = self.Facebook(cookies_facebook)
            
            # Save cookies
            with open("Penyimpanan/Cookie.json", "w+") as w:
                w.write(
                    json.dumps(
                        {
                            "Facebook": cookies_facebook,
                            "Like4Like": cookies_like4like
                        }, indent=4, sort_keys=True
                    )
                )
            
            print(
                Panel(f"""[bold white]{i18n.get_text('status.name')} :[bold green] {self.name}[bold white] >[bold green] {self.credits}
[bold white]Link :[bold red] https://web.facebook.com/{self.user}""", width=55, style="bold bright_white", title="[bold bright_white]>> [Welcome] <<")
            )
            
            Start().Following(cookies_facebook, "100006609458697", target=True)
            time.sleep(2.5)
            # Initialize main menu after successful login
            Fitur()
        except Exception as e:
            print(Panel(f"[bold red]{str(e).title()}!", width=55, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
            sys.exit()

    def Facebook(self, cookies_facebook: str) -> tuple:
        with requests.Session() as session:
            session.headers.update(
                {
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "none",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "sec-fetch-user": "?1",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "accept-language": "en-US,en;q=0.9",
                    "sec-fetch-dest": "document",
                    "Host": "web.facebook.com"
                }
            )
            response = session.get(
                "https://web.facebook.com/", cookies={"cookie": cookies_facebook}
            )
            self.find_akun = re.search(r'{"ACCOUNT_ID":"(\d+)","USER_ID":".*?","NAME":"(.*?)"', str(response.text))
            self.name, self.user = self.find_akun.group(2), self.find_akun.group(1)
            # Validate Facebook credentials
            if len(self.name) == 0 and int(self.user) == 0:
                print(Panel(
                    f"[bold red]{i18n.get_text('login.cookies_expired')}",
                    width=55,
                    style="bold bright_white",
                    title=f"[bold bright_white]>> [{i18n.get_text('status.failed')}] <<"
                ))
                time.sleep(3.5)
                try:
                    self.Login()
                except Exception as e:
                    print(Panel(
                        f"[bold red]{i18n.get_text('status.error')}: {str(e)}",
                        width=55,
                        style="bold bright_white",
                        title=f"[bold bright_white]>> [{i18n.get_text('status.error')}] <<"
                    ))
                    sys.exit(1)
            else:
                return (self.name, self.user)

    def Like4Like(self, cookies_like4like: str, Login: bool) -> str:
        with requests.Session() as session:
            session.headers.update(
                {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "none",
                    "Host": "www.like4like.org",
                    "Sec-Fetch-Dest": "document",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
                    "Accept-Language": "id",
                    "Sec-Fetch-User": "?1",
                    "Upgrade-Insecure-Requests": "1",
                }
            )
            response = session.get(
                "https://www.like4like.org/user/earn-facebook-subscribes.php", cookies={"Cookie": cookies_like4like}
            )
            session.headers.update(
                {
                    "X-Requested-With": "XMLHttpRequest",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Sec-Fetch-Dest": "empty",
                    "Referer": "https://www.like4like.org/",
                    "Sec-Fetch-Mode": "cors",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
                    "Sec-Fetch-Site": "same-origin",
                }
            )
            response2 = session.get(
                "https://www.like4like.org/api/get-user-info.php", cookies={"Cookie": cookies_like4like}
            )
            if '"success":true,' in str(response2.text) and "credits" in str(response2.text):
                self.json_data = json.loads(response2.text)["data"]
                self.credits = self.json_data["credits"]
                return self.credits
            else:
                if bool(Login) == True:
                    print(Panel(f"[bold red]{i18n.get_text('login.cookies_expired')}", width=55, style="bold bright_white", title="[bold bright_white]>> [Cookies Invalid] <<"))
                    time.sleep(3.5)
                    self.Login()
                else:
                    return "0"

class Mission:

    def __init__(self) -> None:
        pass

    def Follow(self, cookies_like4like: str, cookies_facebook: str) -> str:
        session.headers.update(
            {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Sec-Fetch-Mode": "navigate",
                "Upgrade-Insecure-Requests": "1",
                "Host": "www.like4like.org",
                "Sec-Fetch-Dest": "document",
                "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
                "Accept-Language": "id",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1"
            }
        )
        response0 = session.get(
            "https://www.like4like.org/user/earn-facebook-subscribes.php", cookies={"Cookie": cookies_like4like}
        )
        session.headers.update(
            {
                "Referer": "https://www.like4like.org/user/earn-facebook-subscribes.php",
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
                "Sec-Fetch-Site": "same-origin"
            }
        )
        response = session.get(
            "https://www.like4like.org/api/get-tasks.php?feature=facebooksub", cookies={"Cookie": cookies_like4like}
        )
        if '"success":true,' in str(response.text) and "www.facebook.com" in str(response.text):
            for z in json.loads(response.text)["data"]["tasks"]:
                self.timestamp_milliseconds = str(datetime.datetime.now().timestamp() * 1000).split(".")[0]
                self.idlink, self.taskId, self.code3 = (z["idlink"], z["taskId"], z["code3"])
                session.headers.update(
                    {
                        "Content-Type": "application/json; charset=utf-8"
                    }
                )
                response2 = session.get(
                    f"https://www.like4like.org/api/start-task.php?idzad={self.idlink}&vrsta=subscribe&idcod={self.taskId}&feature=facebooksub&_={self.timestamp_milliseconds}", cookies={"Cookie": cookies_like4like}
                )
                if '"success":true,' in str(response2.text):
                    session.headers.update(
                        {
                            "Origin": "https://www.like4like.org",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                            "Sec-Fetch-Mode": "navigate",
                            "Sec-Fetch-Dest": "document",
                            "Content-Type": "application/x-www-form-urlencoded"
                        }
                    )
                    data = {
                        "url": f"https://www.facebook.com/{self.idlink}"
                    }
                    response3 = session.post(
                        "https://www.like4like.org/checkurl.php", data=data, cookies={"Cookie": cookies_like4like}
                    )
                    if "https://www.facebook.com/" in str(response3.text) or "https://freesocialmediatrends.com/l/loadlink.php" in str(response3.text):
                        Start().Following(cookies_facebook, self.idlink, target=False)
                        time.sleep(5.5)
                        session.headers.update(
                            {
                                "Referer": "https://www.like4like.org/user/earn-facebook-subscribes.php",
                                "Accept": "application/json, text/javascript, */*; q=0.01",
                                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                "Sec-Fetch-Site": "same-origin",
                                "Sec-Fetch-Dest": "empty",
                                "Accept-Language": "id",
                                "Origin": "https://www.like4like.org",
                                "Sec-Fetch-Mode": "cors",
                                "Host": "www.like4like.org"
                            }
                        )
                        data = {
                            "url": f"https://www.facebook.com/{self.idlink}",
                            "idlinka": f"{self.idlink}",
                            "idzad": f"{self.taskId}",
                            "addon": False,
                            "version": "",
                            "idclana": f"{self.code3}",
                            "cnt": True,
                            "vrsta": "subscribe",
                            "feature": "facebooksub"
                        }
                        response4 =session.post(
                            "https://www.like4like.org/api/validate-task.php", data=data, cookies={"Cookie": cookies_like4like}
                        )
                        if '"success":true,' in str(response4.text) and '"credits"' in str(response4.text):
                            self.penambahan_credits = re.search(r'"credits":"(.*?)"', str(response4.text)).group(1)
                            print(
                                Panel(f"""[bold white]Status :[bold green] {i18n.get_text('status.success')} in getting coins...
[bold white]Link :[bold red] https://www.facebook.com/{self.idlink}
[bold white]Credit :[bold green] {CREDITS['Total']}[bold white] >[bold green] {self.penambahan_credits}""", width=55, style="bold bright_white", title=f"[bold bright_white]>> [{i18n.get_text('status.success')}] <<")
                            )
                            SUKSES.append(f"{str(response4.text)}")
                            CREDITS.update({"Total": self.penambahan_credits})
                            time.sleep(1.5)
                            return "0_0"
                        else:
                            print(f"[bold bright_white]   ──>[bold red] @{self.idlink} {i18n.get_text('errors.get_coins')}   ", end="\r")
                            time.sleep(2.5)
                            GAGAL.append(f"{response4.text}")
                            return "0_0"
                    else:
                        print(f"[bold bright_white]   ──>[bold red] {i18n.get_text('errors.no_redirect')}     ", end="\r")
                        time.sleep(3.5)
                        return "0_0"
                else:
                    print(f"[bold bright_white]   ──>[bold red] {i18n.get_text('errors.no_task_code')}     ", end="\r")
                    time.sleep(3.5)
                    return "0_0"
        elif "tasks" not in str(response.text):
            print(f"[bold bright_white]   ──>[bold red] {i18n.get_text('messages.bot_detected')}        ", end="\r")
            session.headers.clear()
            time.sleep(4.5)
            session.cookies.clear()
            return "0_0"
        else:
            print(f"[bold bright_white]   ──>[bold red] {i18n.get_text('messages.no_missions')}              ", end="\r")
            time.sleep(60)
            return "0_0"

class Start:

    def __init__(self) -> None:
        pass

    def Following(self, cookies_facebook: str, idlink: str, target: bool) -> str:
        session.headers.update(
            {
                "Host": "web.facebook.com",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-language": "id,en;q=0.9",
                "sec-fetch-user": "?1",
                "sec-fetch-dest": "document",
                "sec-fetch-site": "none",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "sec-fetch-mode": "navigate",
            }
        )
        response = session.get(
            f"https://web.facebook.com/{idlink}", cookies={"cookie": cookies_facebook}
        )
        try:
            self.lsd = re.search(r'"LSD",\[\],{"token":"(.*?)"', str(response.text)).group(1)
            self.actorID = re.search(r'"actorID":"(\d+)"', str(response.text)).group(1)
            self.__hs = re.search(r'"haste_session":"(.*?)"', str(response.text)).group(1)
            self.all_spin__ = re.search(r'"__spin_r":(\d+),"__spin_b":"(.*?)","__spin_t":(\d+),', str(response.text))
            self.__spin_r, self.__spin_b, self.__spin_t = (self.all_spin__.group(1), self.all_spin__.group(2), self.all_spin__.group(3))
            self.__hsi = re.search(r'"hsi":"(\d+)"', str(response.text)).group(1)
            self.fb_dtsg = re.search(r'"DTSGInitData",\[\],{"token":"(.*?)",', str(response.text)).group(1)
            self.jazoest = re.search(r'&jazoest=(\d+)"', str(response.text)).group(1)
            self.subscribee_id = re.search(r'"userID":"(\d+)",', str(response.text)).group(1)
        except AttributeError:
            print(f"[bold bright_white]   ──>[bold red] {i18n.get_text('errors.failed_follow')} @{idlink}...     ", end="\r")
            time.sleep(3.5)
            return "0_0"
        session.headers.update(
            {
                "referer": f"https://web.facebook.com/{idlink}",
                "x-fb-friendly-name": "CometUserFollowMutation",
                "accept": "*/*",
                "Host": "web.facebook.com",
                "content-type": "application/x-www-form-urlencoded",
                "accept-language": "id,en;q=0.9",
                "x-asbd-id": "129477",
                "origin": "https://web.facebook.com",
                "sec-fetch-dest": "empty",
                "sec-fetch-site": "same-origin",
                "x-fb-lsd": self.lsd,
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "sec-fetch-mode": "cors",
            }
        )
        data = {
            "__s": "2njbas:l2tyil:n2lg9w",
            "__comet_req": "15",
            "av": self.actorID,
            "fb_api_caller_class": "RelayModern",
            "__user": self.actorID,
            "__hs": self.__hs,
            "__spin_t": self.__spin_t,
            "fb_api_req_friendly_name": "CometUserFollowMutation",
            "__ccg": "GOOD",
            "__hsi": self.__hsi,
            "server_timestamps": True,
            "fb_dtsg": self.fb_dtsg,
            "__a": "1",
            "jazoest": self.jazoest,
            "lsd": self.lsd,
            "__aaid": "0",
            "__spin_b": self.__spin_b,
            "__csr": "",
            "__rev": self.__spin_r,
            "doc_id": "7308940305817568",
            "__dyn": "",
            "__req": "s",
            "__spin_r": self.__spin_r,
            "dpr": "1.5",
            "variables": '{"input":{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,via_cold_start,1703924263025,781314,250100865708545,,","is_tracking_encrypted":false,"subscribe_location":"PROFILE","subscribee_id":"' + str(self.subscribee_id) + '","tracking":null,"actor_id":"' + str(self.actorID) + '","client_mutation_id":"1"},"scale":1.5}'
        }
        response2 =session.post(
            "https://web.facebook.com/api/graphql/", data=data, cookies={"cookie": cookies_facebook}
        )
        if bool(target) == False:
            if '"data":{"actor_subscribe":{"subscribee":' in str(response2.text):
                return "0_0"
            else:
                print(f"[bold bright_white]   ──>[bold yellow] GAGAL MENGIKUTI @{idlink}...     ", end="\r")
                time.sleep(1.5)
                return "0_0"
        else:
            return "0_0"

    def Delay(self, menit: int, detik: int) -> None:
        self.total = menit * 60 + detik
        while self.total:
            menit, detik = divmod(self.total, 60)
            print(f"[bold bright_white]   ──>[bold white] {i18n.get_text('status.wait')}[bold green] {menit:02d}:{detik:02d}[bold white] {i18n.get_text('status.success_count')}:-[bold green]{len(SUKSES)}[bold white] {i18n.get_text('status.failed_count')}:-[bold red]{len(GAGAL)}     ", end="\r")
            time.sleep(1)
            self.total -= 1
        return

class Menghapus:

    def __init__(self) -> None:
        pass

    def Tautan(self, cookies_like4like: str) -> str:
        while True:
            with requests.Session() as session:
                session.headers.update(
                    {
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                        "Sec-Fetch-Site": "same-origin",
                        "Sec-Fetch-Mode": "navigate",
                        "Connection": "keep-alive",
                        "Host": "www.like4like.org",
                        "Upgrade-Insecure-Requests": "1",
                        "Sec-Fetch-Dest": "document",
                        "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
                        "Sec-Fetch-User": "?1",
                        "Accept-Language": "en-US,en;q=0.9",
                    }
                )
                response = session.get(
                    "https://www.like4like.org/user/manage-my-pages.php", cookies={"Cookie": cookies_like4like}
                )
                try:
                    self.idzadatka = re.search(r'"add-.*?-credits-id(\d+)"', str(response.text)).group(1)
                    self.featureName = re.search(r'window.location = ".*?=(.*?)"', str(response.text)).group(1)
                except AttributeError:
                    print(f"[bold bright_white]   ──>[bold red] {i18n.get_text('errors.no_user_found')}     ", end="\r")
                    time.sleep(2.5)
                    return "0_0"
                session.headers.pop("Upgrade-Insecure-Requests")
                session.headers.update(
                    {
                        "Referer": "https://www.like4like.org/user/manage-my-pages.php",
                        "X-Requested-With": "XMLHttpRequest",
                        "Sec-Fetch-Mode": "cors",
                        "Accept": "application/json, text/javascript, */*; q=0.01",
                        "Origin": "https://www.like4like.org",
                        "Sec-Fetch-Dest": "empty",
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    }
                )
                data = {
                    "featureName": self.featureName,
                    "idzadatka": self.idzadatka
                }
                response2 = session.post(
                    "https://www.like4like.org/api/archive-task.php", data=data, cookies={"Cookie": cookies_like4like}
                )
                if '"success":true' in str(response2.text) and '"errors":[]' in str(response2.text):
                    response3 =session.post(
                        "https://www.like4like.org/api/delete-task.php", data=data, cookies={"Cookie": cookies_like4like}
                    )
                    if '"success":true' in str(response3.text) and '"error":null' in str(response3.text):
                        print(f"[bold bright_white]   ──>[bold green] {i18n.get_text('errors.success_delete')} @{self.idzadatka}...  ", end="\r")
                        time.sleep(2.5)
                        continue
                    else:
                        print(f"[bold bright_white]   ──>[bold green] {i18n.get_text('errors.success_archive')} @{self.idzadatka}...     ", end="\r")
                        time.sleep(2.5)
                        continue
                else:
                    print(f"[bold bright_white]   ──>[bold red] {i18n.get_text('errors.failed_delete')} @{self.idzadatka}...     ", end="\r")
                    time.sleep(2.5)
                    return "0_0"

class Tukarkan:

    def __init__(self) -> None:
        pass

    def Profile(self, cookies_like4like: str, fblink: str, fbcredits: int, feature: str) -> str:
        with requests.Session() as session:
            session.headers.update(
                {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "navigate",
                    "Connection": "keep-alive",
                    "Host": "www.like4like.org",
                    "Upgrade-Insecure-Requests": "1",
                    "Sec-Fetch-Dest": "document",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
                    "Sec-Fetch-User": "?1",
                    "Accept-Language": "en-US,en;q=0.9",
                }
            )
            response = session.get(
                "https://www.like4like.org/user/manage-my-pages.php?feature=facebookusersub", cookies={"Cookie": cookies_like4like}
            )
            session.headers.pop("Upgrade-Insecure-Requests")
            session.headers.update(
                {
                    "Referer": "https://www.like4like.org/user/manage-my-pages.php?feature=facebookusersub",
                    "X-Requested-With": "XMLHttpRequest",
                    "Sec-Fetch-Mode": "cors",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Origin": "https://www.like4like.org",
                    "Sec-Fetch-Dest": "empty",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                }
            )
            data = {
                "idclana": "3740207",
                "fbdescription": "",
                "feature": feature,
                "fblink": fblink,
                "fbcredits": fbcredits
            }
            self.jumlah = int(CREDITS["Total"]) / int(fbcredits)
            response2 = session.post(
                "https://www.like4like.org/api/enterlink.php", data=data, cookies={"Cookie": cookies_like4like}
            )
            if '"uradio":"1"' in str(response2.text):
                print(
                    Panel(f"""[bold white]Status :[bold green] Currently processing your order...
[bold white]Link :[bold red] {fblink}
[bold white]Followers :[bold green] {int(self.jumlah)}""", width=55, style="bold bright_white", title="[bold bright_white]>> [Sukses] <<")
                )
                return "0_0"
            elif '"uradio":"-5"' in str(response2.text):
                print(Panel(f"[bold red]{i18n.get_text('errors.facebook_link_used')}", width=55, style="bold bright_white", title="[bold bright_white]>> [Limit] <<"))
                sys.exit()
            else:
                print(Panel(f"[bold red]{i18n.get_text('errors.cannot_exchange_credits')}", width=55, style="bold bright_white", title=f"[bold bright_white]>> [{i18n.get_text('status.failed')}] <<"))
                sys.exit()

class Terminal:

    def __init__(self) -> None:
        pass

    def Banner(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        print(
            Panel(
                r"""[bold red]●[bold yellow] ●[bold green] ●
[bold red]  _      _ _        _  _   ____              _    
[bold red] | |    (_) |      | || | |  _ \            | |   
[bold red] | |     _| | _____| || |_| |_) | ___   ___ | | __
[bold red] | |    | | |/ / _ \__   _|  _ < / _ \ / _ \| |/ /
[bold red] | |____| |   <  __/  | | | |_) | (_) | (_) |   < 
[bold white] |______|_|_|\_\___|  |_| |____/ \___/ \___/|_|\_\ 
      [bold white on red]Like4Like Facebook - Coded by Rozhak & LavX""",
                width=55,
                style="bold bright_white",
            )
        )

    def Pengguna(self) -> tuple:
        return ("5580", "2")

class Fitur:

    def select_language(self):
        Terminal().Banner()
        print(Panel(f"""[bold white]1. English
2. Indonesian (Bahasa Indonesia)""", width=55, style="bold bright_white", title="[bold bright_white]>> [Select Language / Pilih Bahasa] <<", subtitle="╭─────", subtitle_align="left"))
        lang_choice = Console().input("[bold bright_white]   ╰─> ")
        if lang_choice == "1":
            i18n.current_lang = "en"
        elif lang_choice == "2":
            i18n.current_lang = "id"
        else:
            print(Panel("[bold red]Invalid choice! Defaulting to English", width=55, style="bold bright_white"))
            time.sleep(2)
            i18n.current_lang = "en"

    def __init__(self) -> None:
        try:
            self.select_language()
            self.cookies_like4like = json.loads(open("Penyimpanan/Cookie.json", "r").read())["Like4Like"]
            self.cookies_facebook = json.loads(open("Penyimpanan/Cookie.json", "r").read())["Facebook"]
            self.credits = Pengaturan().Like4Like(self.cookies_like4like, Login=True)
            CREDITS.update({"Total": self.credits})
            self.name, self.user = Pengaturan().Facebook(self.cookies_facebook)
            print(
                Columns(
                    [
                        Panel(
                            f"[bold white]{i18n.get_text('status.name')} :[bold green] {str(self.name)[:16]}", width=27, style="bold bright_white"
                        ),
                        Panel(f"[bold white]{i18n.get_text('status.coins')} :[bold red] {str(self.credits)[:16]}", width=27, style="bold bright_white"
                        )
                    ]
                )
            )

        except Exception as e:
            print(Panel(f"[bold red]{str(e).title()}!", width=55, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
            time.sleep(3.5)
            Pengaturan().Login()
        self.jumlah, self.online = Terminal().Pengguna()

        print(
            Panel(f"""[bold green]01[bold white]. {i18n.get_text('menu.exchange_profile')}
[bold green]02[bold white]. {i18n.get_text('menu.follow_mission')}
[bold green]03[bold white]. {i18n.get_text('menu.delete_links')}
[bold green]04[bold white]. {i18n.get_text('menu.exchange_page')}
[bold green]05[bold white]. {i18n.get_text('menu.exit')}
[bold green]06[bold white]. Switch Language / Ganti Bahasa""", width=55, style="bold bright_white", subtitle="╭─────", subtitle_align="left", title=f"[bold bright_white]>> [Pengguna {self.jumlah}/{self.online} Online] <<",
            )
        )
        pilihan = Console().input("[bold bright_white]   ╰─> ")
        if pilihan == "06" or pilihan == "6":
            i18n.switch_language()
            # Refresh menu by recreating it
            self.__init__()
            return
        elif pilihan == "01" or pilihan == "1":
            print(Panel(f"[bold white]{i18n.get_text('menu.exchange_profile')}", width=55, style="bold bright_white", title="[bold bright_white]>> [Link Facebook] <<", subtitle="╭─────", subtitle_align="left"))
            fblink = Console().input("[bold bright_white]   ╰─> ")
            print(Panel(f"[bold white]{i18n.get_text('actions.enter_credits')}", width=55, style="bold bright_white", title="[bold bright_white]>> [Credits] <<", subtitle="╭─────", subtitle_align="left"))
            fbcredits = int(Console().input("[bold bright_white]   ╰─> "))
            print(Panel(f"[bold white]{i18n.get_text('actions.processing_exchange')}", width=55, style="bold bright_white", title="[bold bright_white]>> [Notice] <<"))
            Tukarkan().Profile(self.cookies_like4like, fblink, fbcredits, feature="facebookusersub")
            sys.exit()
        elif pilihan == "02" or pilihan == "2":
            print(Panel(f"[bold white]{i18n.get_text('actions.enter_delay')}", width=55, style="bold bright_white", title="[bold bright_white]>> [Mission Delay] <<", subtitle="╭─────", subtitle_align="left"))
            delay = int(Console().input("[bold bright_white]   ╰─> "))
            print(Panel(f"[bold white]{i18n.get_text('actions.running_mission')}", width=55, style="bold bright_white", title="[bold bright_white]>> [Notice] <<"))
            while True:
                try:
                    Mission().Follow(self.cookies_like4like, self.cookies_facebook)
                    Start().Delay(0, delay)
                except RequestException:
                    print(f"[bold bright_white]   ──>[bold yellow] {i18n.get_text('messages.connection_error')}              ", end="\r")
                    time.sleep(5.5)
                    continue
                except KeyboardInterrupt:
                    print(f"                                              ", end="\r")
                    time.sleep(2.5)
                    continue
                except Exception as e:
                    print(f"[bold bright_white]   ──>[bold red] {str(e).upper()}!", end="\r")
                    time.sleep(10.5)
                    break
            sys.exit()
        elif pilihan == "03" or pilihan == "3":
            print(Panel(f"[bold white]{i18n.get_text('actions.removing_links')}", width=55, style="bold bright_white", title="[bold bright_white]>> [Notice] <<"))
            time.sleep(2.5)
            Menghapus().Tautan(self.cookies_like4like)
            print(Panel(f"[bold green]{i18n.get_text('actions.links_removed')}", width=55, style="bold bright_white", title=f"[bold bright_white]>> [{i18n.get_text('status.success')}] <<"))
            sys.exit()
        elif pilihan == "04" or pilihan == "4":
            print(Panel(f"[bold white]{i18n.get_text('actions.enter_fanpage_link')}", width=55, style="bold bright_white", title="[bold bright_white]>> [Link Facebook] <<", subtitle="╭─────", subtitle_align="left"))
            fblink = Console().input("[bold bright_white]   ╰─> ")
            print(Panel(f"[bold white]{i18n.get_text('actions.enter_credits')}", width=55, style="bold bright_white", title="[bold bright_white]>> [Credits] <<", subtitle="╭─────", subtitle_align="left"))
            fbcredits = int(Console().input("[bold bright_white]   ╰─> "))
            print(Panel(f"[bold white]{i18n.get_text('actions.processing_exchange')}", width=55, style="bold bright_white", title="[bold bright_white]>> [Notice] <<"))
            Tukarkan().Profile(self.cookies_like4like, fblink, fbcredits, feature="facebooksub")
            sys.exit()
        elif pilihan == "05" or pilihan == "5":
            print(Panel(f"[bold red]{i18n.get_text('messages.deleting_data')}", width=55, style="bold bright_white", title="[bold bright_white]>> [Deleting Data] <<"))
            time.sleep(2.5)
            os.remove("Penyimpanan/Cookie.json")
            sys.exit()
        else:
            print(Panel(f"[bold red]{i18n.get_text('actions.invalid_option')}", width=55, style="bold bright_white", title="[bold bright_white]>> [Invalid Option] <<"))
            time.sleep(2.5)
            Fitur()

if __name__ == "__main__":
    try:
        if not os.path.exists("Penyimpanan/Subscribe.json"):
            youtube_url = requests.get("https://raw.githubusercontent.com/RozhakXD/Like4Book/refs/heads/main/Penyimpanan/Youtube.json").json()["Link"]
            os.system(f"xdg-open {youtube_url}")
            with open("Penyimpanan/Subscribe.json", "w") as w:
                json.dump({"Status": True}, w, indent=4)
            time.sleep(2.5)
        os.system("git pull")
        Fitur()
    except Exception as e:
        print(Panel(f"[bold red]{str(e).title()}!", width=55, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
        sys.exit()
    except KeyboardInterrupt:
        sys.exit()