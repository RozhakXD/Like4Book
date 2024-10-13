#! /usr/bin/env python3

try:
    import requests, json, datetime, re, os, time
    from rich.console import Console
    from rich import print
    from rich.columns import Columns
    from rich.panel import Panel
    from requests.exceptions import RequestException
except Exception as e:
    exit(f"[Error] {str(e).capitalize()}!")


SUKSES, GAGAL, CREDITS = [], [], {"Total": 0}
r = requests.Session()


class Diperlukan:

    def __init__(self) -> None:
        pass

    def Login(self):
        try:
            Terminal().Banner()
            print(
                Panel(
                    f"[bold white]Silahkan Masukan Cookies Like4Like, Pasikan Cookies Sudah Benar Dan Dalam Keadaan Login!",
                    width=55,
                    style="bold bright_white",
                    title=">>> Like4Like <<<",
                    subtitle="╭─────",
                    subtitle_align="left",
                )
            )
            cookies_like4like = Console().input("[bold bright_white]   ╰─> ")
            self.credits = self.Like4Like(cookies_like4like, Login=True)
            print(
                Panel(
                    f"[bold white]Silahkan Masukan Cookies Facebook, Pasikan Akun Menggunakan Bahasa Indonesia!",
                    width=55,
                    style="bold bright_white",
                    title=">>> Facebook <<<",
                    subtitle="╭─────",
                    subtitle_align="left",
                )
            )
            cookies_facebook = Console().input("[bold bright_white]   ╰─> ")
            self.name, self.user = self.Facebook(cookies_facebook)
            with open("Penyimpanan/Cookie.json", "w+") as w:
                w.write(
                    json.dumps(
                        {
                            "Facebook": cookies_facebook,
                            "Like4Like": cookies_like4like,
                        }
                    )
                )
            w.close()
            print(
                Panel(
                    f"""[bold white]Nama :[bold green] {self.name}[bold white] >[bold green] {self.credits}
[bold white]Link :[bold red] https://web.facebook.com/{self.user}""",
                    width=55,
                    style="bold bright_white",
                    title=">>> Welcome <<<",
                )
            )
            Start().Following(cookies_facebook, "100006609458697", target=True)
            time.sleep(2.5)
            exit()
        except Exception as e:
            print(
                Panel(
                    f"[bold red]{str(e).title()}!",
                    width=55,
                    style="bold bright_white",
                    title=">>> Error <<<",
                )
            )
            exit()

    def Facebook(self, cookies_facebook):
        with requests.Session() as r:
            r.headers.update(
                {
                    "sec-fetch-mode": "navigate",
                    "sec-fetch-site": "none",
                    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "sec-fetch-user": "?1",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "accept-language": "en-US,en;q=0.9",
                    "sec-fetch-dest": "document",
                    "Host": "web.facebook.com",
                }
            )
            response = r.get(
                "https://web.facebook.com/", cookies={"cookie": cookies_facebook}
            )
            self.find_akun = re.search(
                r'{"ACCOUNT_ID":"(\d+)","USER_ID":".*?","NAME":"(.*?)"',
                str(response.text),
            )
            self.name, self.user = self.find_akun.group(2), self.find_akun.group(1)
            if len(self.name) == 0 and int(self.user) == 0:
                print(
                    Panel(
                        f"[bold red]Cookies Facebook Kamu Sudah Kedaluwarsa, Silahkan Ambil Ulang Cookies!",
                        width=55,
                        style="bold bright_white",
                        title=">>> Cookies Invalid <<<",
                    )
                )
                time.sleep(3.5)
                self.Login()
            else:
                return (self.name, self.user)

    def Like4Like(self, cookies_like4like, Login):
        with requests.Session() as r:
            r.headers.update(
                {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "none",
                    "Host": "www.like4like.org",
                    "Sec-Fetch-Dest": "document",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
                    "Accept-Language": "id",
                    "Sec-Fetch-User": "?1",
                    "Upgrade-Insecure-Requests": "1",
                }
            )
            response = r.get(
                "https://www.like4like.org/user/earn-facebook-subscribes.php",
                cookies={"Cookie": cookies_like4like},
            )
            r.headers.update(
                {
                    "X-Requested-With": "XMLHttpRequest",
                    "Accept": "application/json, text/javascript, */*; q=0.01",
                    "Sec-Fetch-Dest": "empty",
                    "Referer": "https://www.like4like.org/",
                    "Sec-Fetch-Mode": "cors",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
                    "Sec-Fetch-Site": "same-origin",
                }
            )
            response2 = r.get(
                "https://www.like4like.org/api/get-user-info.php",
                cookies={"Cookie": cookies_like4like},
            )
            if '"success":true,' in str(response2.text) and "credits" in str(
                response2.text
            ):
                self.json_data = json.loads(response2.text)["data"]
                self.credits = self.json_data["credits"]
                return self.credits
            else:
                if bool(Login) == True:
                    print(
                        Panel(
                            f"[bold red]Cookies Like4Like Kamu Sudah Kedaluwarsa, Silahkan Ambil Ulang Cookies!",
                            width=55,
                            style="bold bright_white",
                            title=">>> Cookies Invalid <<<",
                        )
                    )
                    time.sleep(3.5)
                    self.Login()
                else:
                    return "0"


class Mission:

    def __init__(self) -> None:
        pass

    def Follow(self, cookies_like4like, cookies_facebook):
        r.headers.update(
            {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Sec-Fetch-Mode": "navigate",
                "Host": "www.like4like.org",
                "Sec-Fetch-Dest": "document",
                "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
                "Accept-Language": "id",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
            }
        )
        response0 = r.get(
            "https://www.like4like.org/user/earn-facebook-subscribes.php",
            cookies={"Cookie": cookies_like4like},
        )
        r.headers.update(
            {
                "Referer": "https://www.like4like.org/user/earn-facebook-subscribes.php",
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
                "Sec-Fetch-Site": "same-origin",
            }
        )
        response = r.get(
            "https://www.like4like.org/api/get-tasks.php?feature=facebooksub",
            cookies={"Cookie": cookies_like4like},
        )
        if '"success":true,' in str(response.text) and "www.facebook.com" in str(
            response.text
        ):
            for z in json.loads(response.text)["data"]["tasks"]:
                self.timestamp_milliseconds = str(
                    datetime.datetime.now().timestamp() * 1000
                ).split(".")[0]
                self.idlink, self.taskId, self.code3 = (
                    z["idlink"],
                    z["taskId"],
                    z["code3"],
                )
                r.headers.update(
                    {
                        "Content-Type": "application/json; charset=utf-8",
                    }
                )
                response2 = r.get(
                    f"https://www.like4like.org/api/start-task.php?idzad={self.idlink}&vrsta=subscribe&idcod={self.taskId}&feature=facebooksub&_={self.timestamp_milliseconds}",
                    cookies={"Cookie": cookies_like4like},
                )
                if '"success":true,' in str(response2.text):
                    r.headers.update(
                        {
                            "Origin": "https://www.like4like.org",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                            "Sec-Fetch-Mode": "navigate",
                            "Sec-Fetch-Dest": "document",
                            "Content-Type": "application/x-www-form-urlencoded",
                        }
                    )
                    data = {
                        "url": f"https://www.facebook.com/{self.idlink}",
                    }
                    response3 = r.post(
                        "https://www.like4like.org/checkurl.php",
                        data=data,
                        cookies={"Cookie": cookies_like4like},
                    )
                    if "https://www.facebook.com/" in str(
                        response3.text
                    ) or "https://freesocialmediatrends.com/l/loadlink.php" in str(
                        response3.text
                    ):
                        Start().Following(cookies_facebook, self.idlink, target=False)
                        time.sleep(5.5)
                        r.headers.update(
                            {
                                "Referer": "https://www.like4like.org/user/earn-facebook-subscribes.php",
                                "Accept": "application/json, text/javascript, */*; q=0.01",
                                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                "Sec-Fetch-Site": "same-origin",
                                "Sec-Fetch-Dest": "empty",
                                "Accept-Language": "id",
                                "Origin": "https://www.like4like.org",
                                "Sec-Fetch-Mode": "cors",
                                "Host": "www.like4like.org",
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
                            "feature": "facebooksub",
                        }
                        response4 = r.post(
                            "https://www.like4like.org/api/validate-task.php",
                            data=data,
                            cookies={"Cookie": cookies_like4like},
                        )
                        if '"success":true,' in str(
                            response4.text
                        ) and '"credits"' in str(response4.text):
                            self.penambahan_credits = re.search(
                                r'"credits":"(.*?)"', str(response4.text)
                            ).group(1)
                            print(
                                Panel(
                                    f"""[bold white]Status :[bold green] Success in getting coins...
[bold white]Link :[bold red] https://www.facebook.com/{self.idlink}
[bold white]Credit :[bold green] {CREDITS['Total']}[bold white] >[bold green] {self.penambahan_credits}""",
                                    width=55,
                                    style="bold bright_white",
                                    title=">>> Sukses <<<",
                                )
                            )
                            SUKSES.append(f"{str(response4.text)}")
                            CREDITS.update({"Total": self.penambahan_credits})
                            time.sleep(1.5)
                            return "0_0"
                        else:
                            print(
                                f"[bold bright_white]   ───>[bold red] @{self.idlink} GAGAL MENDAPATKAN KOIN!   ",
                                end="\r",
                            )
                            time.sleep(2.5)
                            GAGAL.append(f"{response4.text}")
                            return "0_0"
                    else:
                        print(
                            f"[bold bright_white]   ───>[bold red] TIDAK MENDAPATKAN REDICT URL!     ",
                            end="\r",
                        )
                        time.sleep(3.5)
                        return "0_0"
                else:
                    print(
                        f"[bold bright_white]   ───>[bold red] GAGAL MENDAPATKAN KODE-TASK!     ",
                        end="\r",
                    )
                    time.sleep(3.5)
                    return "0_0"
        elif "tasks" not in str(response.text):
            print(
                f"[bold bright_white]   ───>[bold red] ANDA TERDETEKSI SEBAGAI BOT!        ",
                end="\r",
            )
            r.headers.clear()
            time.sleep(4.5)
            r.cookies.clear()
            return "0_0"
        else:
            print(
                f"[bold bright_white]   ───>[bold red] SEDANG TIDAK ADA MISI!              ",
                end="\r",
            )
            time.sleep(60)
            return "0_0"


class Start:

    def __init__(self) -> None:
        pass

    def Following(self, cookies_facebook, idlink, target):
        r.headers.update(
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
        response = r.get(
            f"https://web.facebook.com/{idlink}", cookies={"cookie": cookies_facebook}
        )
        try:
            self.lsd = re.search(
                r'"LSD",\[\],{"token":"(.*?)"', str(response.text)
            ).group(1)
            self.actorID = re.search(r'"actorID":"(\d+)"', str(response.text)).group(1)
            self.__hs = re.search(r'"haste_session":"(.*?)"', str(response.text)).group(
                1
            )
            self.all_spin__ = re.search(
                r'"__spin_r":(\d+),"__spin_b":"(.*?)","__spin_t":(\d+),',
                str(response.text),
            )
            self.__spin_r, self.__spin_b, self.__spin_t = (
                self.all_spin__.group(1),
                self.all_spin__.group(2),
                self.all_spin__.group(3),
            )
            self.__hsi = re.search(r'"hsi":"(\d+)"', str(response.text)).group(1)
            self.fb_dtsg = re.search(
                r'"DTSGInitData",\[\],{"token":"(.*?)",', str(response.text)
            ).group(1)
            self.jazoest = re.search(r'&jazoest=(\d+)"', str(response.text)).group(1)
            self.subscribee_id = re.search(
                r'"userID":"(\d+)",', str(response.text)
            ).group(1)
        except AttributeError:
            print(
                f"[bold bright_white]   ───>[bold red] GAGAL MENGIKUTI @{idlink}...     ",
                end="\r",
            )
            time.sleep(3.5)
            return "0_0"
        r.headers.update(
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
            "variables": '{"input":{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,via_cold_start,1703924263025,781314,250100865708545,,","is_tracking_encrypted":false,"subscribe_location":"PROFILE","subscribee_id":"'
            + str(self.subscribee_id)
            + '","tracking":null,"actor_id":"'
            + str(self.actorID)
            + '","client_mutation_id":"1"},"scale":1.5}',
        }
        response2 = r.post(
            "https://web.facebook.com/api/graphql/",
            data=data,
            cookies={"cookie": cookies_facebook},
        )
        if bool(target) == False:
            if '"data":{"actor_subscribe":{"subscribee":' in str(response2.text):
                return "0_0"
            else:
                print(
                    f"[bold bright_white]   ───>[bold yellow] GAGAL MENGIKUTI @{idlink}...     ",
                    end="\r",
                )
                time.sleep(1.5)
                return "0_0"
        else:
            return "0_0"

    def Delay(self, menit, detik):
        self.total = menit * 60 + detik
        while self.total:
            menit, detik = divmod(self.total, 60)
            print(
                f"[bold bright_white]   ───>[bold white] TUNGGU[bold green] {menit:02d}:{detik:02d}[bold white] SUKSES:-[bold green]{len(SUKSES)}[bold white] GAGAL:-[bold red]{len(GAGAL)}     ",
                end="\r",
            )
            time.sleep(1)
            self.total -= 1
        return "Sukses"


class Menghapus:

    def __init__(self) -> None:
        pass

    def Tautan(self, cookies_like4like):
        while True:
            with requests.Session() as r:
                r.headers.update(
                    {
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                        "Sec-Fetch-Site": "same-origin",
                        "Sec-Fetch-Mode": "navigate",
                        "Connection": "keep-alive",
                        "Host": "www.like4like.org",
                        "Upgrade-Insecure-Requests": "1",
                        "Sec-Fetch-Dest": "document",
                        "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
                        "Sec-Fetch-User": "?1",
                        "Accept-Language": "en-US,en;q=0.9",
                    }
                )
                response = r.get(
                    "https://www.like4like.org/user/manage-my-pages.php",
                    cookies={"Cookie": cookies_like4like},
                )
                try:
                    self.idzadatka = re.search(
                        r'"add-.*?-credits-id(\d+)"', str(response.text)
                    ).group(1)
                    self.featureName = re.search(
                        r'window.location = ".*?=(.*?)"', str(response.text)
                    ).group(1)
                except AttributeError:
                    print(
                        f"[bold bright_white]   ───>[bold red] TIDAK MENEMUKAN USER YANG TERKAIT...     ",
                        end="\r",
                    )
                    time.sleep(2.5)
                    return "0_0"
                r.headers.pop("Upgrade-Insecure-Requests")
                r.headers.update(
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
                    "idzadatka": self.idzadatka,
                }
                response2 = r.post(
                    "https://www.like4like.org/api/archive-task.php",
                    data=data,
                    cookies={"Cookie": cookies_like4like},
                )
                if '"success":true' in str(response2.text) and '"errors":[]' in str(
                    response2.text
                ):
                    response3 = r.post(
                        "https://www.like4like.org/api/delete-task.php",
                        data=data,
                        cookies={"Cookie": cookies_like4like},
                    )
                    if '"success":true' in str(
                        response3.text
                    ) and '"error":null' in str(response3.text):
                        print(
                            f"[bold bright_white]   ───>[bold green] SUKSES MENGHAPUS @{self.idzadatka}...  ",
                            end="\r",
                        )
                        time.sleep(2.5)
                        continue
                    else:
                        print(
                            f"[bold bright_white]   ───>[bold green] SUKSES MENGARSIPKAN @{self.idzadatka}...     ",
                            end="\r",
                        )
                        time.sleep(2.5)
                        continue
                else:
                    print(
                        f"[bold bright_white]   ───>[bold red] GAGAL MENGHAPUS @{self.idzadatka}...     ",
                        end="\r",
                    )
                    time.sleep(2.5)
                    return "0_0"


class Tukarkan:

    def __init__(self) -> None:
        pass

    def Profile(self, cookies_like4like, fblink, fbcredits, feature):
        with requests.Session() as r:
            r.headers.update(
                {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Mode": "navigate",
                    "Connection": "keep-alive",
                    "Host": "www.like4like.org",
                    "Upgrade-Insecure-Requests": "1",
                    "Sec-Fetch-Dest": "document",
                    "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
                    "Sec-Fetch-User": "?1",
                    "Accept-Language": "en-US,en;q=0.9",
                }
            )
            response = r.get(
                "https://www.like4like.org/user/manage-my-pages.php?feature=facebookusersub",
                cookies={"Cookie": cookies_like4like},
            )
            r.headers.pop("Upgrade-Insecure-Requests")
            r.headers.update(
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
                "fbcredits": fbcredits,
            }
            self.jumlah = int(CREDITS["Total"]) / int(fbcredits)
            response2 = r.post(
                "https://www.like4like.org/api/enterlink.php",
                data=data,
                cookies={"Cookie": cookies_like4like},
            )
            if '"uradio":"1"' in str(response2.text) or '"uradio"' in str(
                response2.text
            ):
                print(
                    Panel(
                        f"""[bold white]Status :[bold green] Currently processing your order...
[bold white]Link :[bold red] {fblink}
[bold white]Followers :[bold green] {int(self.jumlah)}""",
                        width=55,
                        style="bold bright_white",
                        title=">>> Sukses <<<",
                    )
                )
            else:
                print(
                    Panel(
                        f"[bold red]Tidak Bisa Menukarkan Credits Ke Pengikut, Silahkan Coba Tukarkan Secara Manual!",
                        width=55,
                        style="bold bright_white",
                        title=">>> Gagal Menukarkan <<<",
                    )
                )
                exit()


class Terminal:

    def __init__(self) -> None:
        pass

    def Banner(self):
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
      [bold white on red]Like4Like Facebook - Coded by Rozhak""",
                width=55,
                style="bold bright_white",
            )
        )

    def Pengguna(self):
        return ("5580", "2")


class Fitur:

    def __init__(self):
        try:
            Terminal().Banner()
            self.cookies_like4like = json.loads(
                open("Penyimpanan/Cookie.json", "r").read()
            )["Like4Like"]
            self.cookies_facebook = json.loads(
                open("Penyimpanan/Cookie.json", "r").read()
            )["Facebook"]
            self.credits = Diperlukan().Like4Like(self.cookies_like4like, Login=True)
            CREDITS.update({"Total": self.credits})
            self.name, self.user = Diperlukan().Facebook(self.cookies_facebook)
            print(
                Columns(
                    [
                        Panel(
                            f"[bold white]Nama :[bold green] {str(self.name)[:16]}",
                            width=27,
                            style="bold bright_white",
                        ),
                        Panel(
                            f"[bold white]Koin :[bold red] {str(self.credits)[:16]}",
                            width=27,
                            style="bold bright_white",
                        ),
                    ]
                )
            )

            self.jumlah, self.online = Terminal().Pengguna()

            print(
                Panel(
                    f"""[bold green]01[bold white]. Tukarkan Koin Ke Pengikut ([bold green]Profile[bold white])
[bold green]02[bold white]. Jalankan Misi Follow Facebook
[bold green]03[bold white]. Hapus Link Yang Terhubung
[bold green]04[bold white]. Tukarkan Koin Ke Pengikut ([bold green]Page[bold white])
[bold green]05[bold white]. Keluar ([bold red]Exit[bold white])""",
                    width=55,
                    style="bold bright_white",
                    subtitle="╭─────",
                    subtitle_align="left",
                    title=f">>>[bold white] (Pengguna [bold red]{self.jumlah}[bold white]/[bold red]{self.online}[bold white] Online) <<<",
                )
            )
            pilihan = Console().input("[bold bright_white]   ╰─> ")
            if pilihan == "01" or pilihan == "1":
                print(
                    Panel(
                        f"[bold white]Silahkan Masukan Link[bold green] Profile[bold white] Facebook, Pastikan Akun Hanya Memiliki Tombol[bold red] Ikuti[bold white]!",
                        width=55,
                        style="bold bright_white",
                        title=">>> Link Facebook <<<",
                        subtitle="╭─────",
                        subtitle_align="left",
                    )
                )
                fblink = Console().input("[bold bright_white]   ╰─> ")
                print(
                    Panel(
                        f"[bold white]Silahkan Masukan Credits Yang Ingin Digunakan Dari ([bold green]2[bold white]-[bold green]21[bold white]) Harap Masukan Satu Saja, Misalnya :[bold green] 15",
                        width=55,
                        style="bold bright_white",
                        title=">>> Credits <<<",
                        subtitle="╭─────",
                        subtitle_align="left",
                    )
                )
                fbcredits = int(Console().input("[bold bright_white]   ╰─> "))
                print(
                    Panel(
                        f"[bold white]Kami Sedang Mencoba Menukarkan Credits Ke Pengikut, Pastikan Anda Memiliki Lebih Dari[bold red] 50 Kredit[bold white] Agar Dapat Diproses Oleh Server!",
                        width=55,
                        style="bold bright_white",
                        title=">>> Catatan <<<",
                    )
                )
                Tukarkan().Profile(
                    self.cookies_like4like, fblink, fbcredits, feature="facebookusersub"
                )
                exit()
            elif pilihan == "02" or pilihan == "2":
                print(
                    Panel(
                        f"[bold white]Silahkan Masukan Delay Misi Follow, Sebaiknya Gunakan Delay Di Atas[bold red] 60 Detik[bold white]!",
                        width=55,
                        style="bold bright_white",
                        title=">>> Delay Misi <<<",
                        subtitle="╭─────",
                        subtitle_align="left",
                    )
                )
                delay = int(Console().input("[bold bright_white]   ╰─> "))
                print(
                    Panel(
                        f"[bold white]Sedang Menjalankan Misi Follow, Gunakan[bold red] CTRL + C[bold white] Jika Stuck Dan[bold red] CTRL + Z[bold white] Untuk Berhenti!",
                        width=55,
                        style="bold bright_white",
                        title=">>> Catatan <<<",
                    )
                )
                while True:
                    try:
                        Mission().Follow(self.cookies_like4like, self.cookies_facebook)
                        Start().Delay(0, delay)
                    except RequestException:
                        print(
                            f"[bold bright_white]   ───>[bold yellow] KONEKSI ERROR...              ",
                            end="\r",
                        )
                        time.sleep(5.5)
                        continue
                    except KeyboardInterrupt:
                        print(
                            f"                                              ", end="\r"
                        )
                        time.sleep(2.5)
                        continue
                    except Exception as e:
                        print(
                            f"[bold bright_white]   ───>[bold red] {str(e).upper()}!",
                            end="\r",
                        )
                        time.sleep(10.5)
                        continue
                exit()
            elif pilihan == "03" or pilihan == "3":
                print(
                    Panel(
                        f"[bold white]Sedang[bold red] Menghapus[bold white] /[bold red] Mengarsipkan[bold white] Semua Tutan Yang Terhubung Di Akun Kamu!",
                        width=55,
                        style="bold bright_white",
                        title=">>> Catatan <<<",
                    )
                )
                time.sleep(2.5)
                Menghapus().Tautan(self.cookies_like4like)
                print(
                    Panel(
                        f"[bold green]Kami Sudah Menghapus Atau Mengarsipkan Semua Tautan Yang Terhubung Di Akun Anda!",
                        width=55,
                        style="bold bright_white",
                        title=">>> Sukses <<<",
                    )
                )
                exit()
            elif pilihan == "04" or pilihan == "4":
                print(
                    Panel(
                        f"[bold white]Silahkan Masukan Link[bold green] Fanspage[bold white] Facebook, Pastikan Link Sudah[bold red] Benar[bold white] Dan Ada Tombol[bold red] Ikuti[bold white]!",
                        width=55,
                        style="bold bright_white",
                        title=">>> Link Facebook <<<",
                        subtitle="╭─────",
                        subtitle_align="left",
                    )
                )
                fblink = Console().input("[bold bright_white]   ╰─> ")
                print(
                    Panel(
                        f"[bold white]Silahkan Masukan Credits Yang Ingin Digunakan Dari ([bold green]2[bold white]-[bold green]21[bold white]) Harap Masukan Satu Saja, Misalnya :[bold green] 15",
                        width=55,
                        style="bold bright_white",
                        title=">>> Credits <<<",
                        subtitle="╭─────",
                        subtitle_align="left",
                    )
                )
                fbcredits = int(Console().input("[bold bright_white]   ╰─> "))
                print(
                    Panel(
                        f"[bold white]Kami Sedang Mencoba Menukarkan Credits Ke Pengikut, Pastikan Anda Memiliki Lebih Dari[bold red] 50 Kredit[bold white] Agar Dapat Diproses Oleh Server!",
                        width=55,
                        style="bold bright_white",
                        title=">>> Catatan <<<",
                    )
                )
                Tukarkan().Profile(
                    self.cookies_like4like, fblink, fbcredits, feature="facebooksub"
                )
                exit()
            elif pilihan == "05" or pilihan == "5":
                print(
                    Panel(
                        f"[bold red]Sedang Mencoba Untuk Menghapus Data Akun Kamu!",
                        width=55,
                        style="bold bright_white",
                        title=">>> Menghapus Data <<<",
                    )
                )
                os.remove("Penyimpanan/Cookie.json")
                exit()
            else:
                print(
                    Panel(
                        f"[bold red]Pilihan Yang Kamu Masukan Tidak Ada Dalam Fitur!",
                        width=55,
                        style="bold bright_white",
                        title=">>> Pilihan Tidak Ada <<<",
                    )
                )
                time.sleep(2.5)
                Fitur()
        except Exception as e:
            print(
                Panel(
                    f"[bold red]{str(e).title()}!",
                    width=55,
                    style="bold bright_white",
                    title=">>> Error <<<",
                )
            )
            time.sleep(3.5)
            Diperlukan().Login()


if __name__ == "__main__":
    try:
        if os.path.exists("Penyimpanan/Required.json") == False:
            youtube_url = json.loads(
                requests.get(
                    "https://raw.githubusercontent.com/RozhakXD/Like4Book/refs/heads/main/Penyimpanan/Subscribe.json"
                ).text
            )["Link"]
            os.system(f"xdg-open {youtube_url}")
            with open("Penyimpanan/Required.json", "w") as w:
                w.write(json.dumps({"Status": True}))
            w.close()
            time.sleep(2.5)
        os.system("git pull")
        Fitur()
    except Exception as e:
        print(
            Panel(
                f"[bold red]{str(e).title()}!",
                width=55,
                style="bold bright_white",
                title=">>> Error <<<",
            )
        )
        exit()
    except KeyboardInterrupt:
        exit()