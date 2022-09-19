#! /usr/bin/env python3
import requests, time, json, re, os
from rich import print
from rich.console import Console
from rich.panel import Panel

# Banner
banner = ("""[bold red]╦═╗┌─┐┌┐ ┌─┐  ╔═╗┬ ┬┬─┐┬ ┬
[bold red]╠╦╝│ │├┴┐│ │  ║ ╦│ │├┬┘│ │
[bold white]╩╚═└─┘└─┘└─┘  ╚═╝└─┘┴└─└─┘
[italic green4]Coded by Rozhak""")

# Pengguna
def Pengguna():
    try:
        response = requests.get('https://justpaste.it/4vj1t').text
        online = re.search('"onlineText":"(\d+)"', str(response)).group(1)
        jumlah = re.search('"viewsText":"(\d+)"', str(response)).group(1)
        return {
            "Jumlah": jumlah,
            "Online": online
        }
    except Exception as e:
        return {
            "Jumlah": 0,
            "Online": 0
        }
# Login
def Login():
    os.system('clear')
    Console().print(Panel(banner, style="bold plum4"), justify="left")
    try:
        Console(width=50).print(Panel("[italic white]Tools ini login menggunakan username dan password jika terjadi error silahkan melapor ke[italic green] admin", title="🙂", style="bold plum4"))
        email, password = json.loads(open('Data/Akun.json','r').read())["Email"], json.loads(open('Data/Akun.json','r').read())["Password"]
        x = ""
        for z in password:
            x = x + chr(ord(z)-2)
        password = x # Please don't change the password!
        with requests.Session() as r:
            url = ('https://account.ruangguru.com/api/login')
            r.headers.update({
                "Host": "account.ruangguru.com",
                "user-agent": "Mozilla/5.0 (Linux; Android 9; RMX1941 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.69 Mobile Safari/537.36",
                "content-type": "application/json",
                "accept": "application/json",
                "clientid": "WEB",
                "disable-node-proxy": "false",
                "country": "id",
                "platform": "Web",
                "with-auth": "false",
                "origin": "https://account.ruangguru.com",
                "sec-fetch-site": "same-origin",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://account.ruangguru.com/login?",
                "accept-encoding": "gzip, deflate",
                "accept-language":"id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
            })
            data = {
                "type": "default",
                "username": email,
                "password": password,
                "client_id": "roboguru",
                "remember_me": False
            }
            response = r.post(url, json = data).json()["data"][0]
            name = response["name"]
            cookie =  (";".join([str(x)+"="+str(y) for x,y in r.cookies.get_dict().items()]))
            with open('Data/Cookie.json','w') as simpan:
                simpan.write(json.dumps({"Cookie": cookie}))
            simpan.close()
        for x in ['.','..','...']:
            Console().print(f"[bold green][*][bold white] Login please wait{x}", end='\r')
            time.sleep(1)
        print("                                     ", end='\r')
        Console(width=50).print(Panel(f"[bold white]Welcome :[bold green] {name}", title="👋", style="bold plum4"));time.sleep(2.5);Menu(name)
    except Exception as e:
        Console(width=50).print(Panel(f"[italic red]{str(e).capitalize()}", title="😡", style="bold plum4"));exit()
# Sekolah
def Sekolah(cookie, x):
    with requests.Session() as r:
        url = ('https://roboguru.ruangguru.com/')
        r.headers.update({
            "Host": "roboguru.ruangguru.com",
            "cache-control": "max-age=0",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 9; RMX1941 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.69 Mobile Safari/537.36",
            "x-requested-with": "mark.via.gp",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "navigate",
            "sec-fetch-dest": "empty",
            "referer": "https://www.google.com/",
            "accept-encoding": "gzip, deflate",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "cookie": cookie
        })
        response = r.get(url).text
        cari = re.search('value="(.*?)">SD</option><option value="(.*?)">SMP</option><option selected="" value="(.*?)">SMA</option><option value="(.*?)">SBMPTN', str(response))
        if x == "SD":
            return cari.group(1)
        elif x == "SMP":
            return cari.group(2)
        elif x == "SMA":
            return cari.group(3)
        elif x == "UTBK":
            return cari.group(4)
        else:
            return 0
# Menu
def Menu(name):
    os.system('clear')
    Console().print(Panel(banner, style="bold plum4"), justify="left")
    try:
        cookie = json.loads(open('Data/Cookie.json','r').read())["Cookie"]
        jumlah, online = Pengguna()["Jumlah"], Pengguna()["Online"]
        Console(width=50).print(Panel(f"""[bold white]Welcome :[bold green] {name}
[bold white]Online  :[bold green] {online}[bold white]/[bold yellow]{jumlah}""", title="👋", style="bold plum4"))
    except Exception as e:
        Console(width=50).print(Panel(f"[italic red]{str(e).capitalize()}", title="😡", style="bold plum4"));time.sleep(3.5);Login()

    Console(width=50).print(Panel("""[bold white]1. Mencari Dari Sekolah Dasar
[bold white]2. Mencari Dari Sekolah Menengah Pertama
[bold white]3. Mencari Dari Sekolah Menengah Atas
[bold white]4. Mencari Dari Sbmptn Atau Utbk""", title="😎", style="bold plum4"))
    choose = Console().input("[bold green][?][bold white] Choose : ")
    if choose == "1" or choose == "01":
        try:
            x = Sekolah(cookie, "SD")
            Console(width=50).print(Panel("[bold white]Mata Pelajaran :[bold cyan] Matematika, Bahasa Indonesia, IPA Terpadu, Penjaskes, PPKN, IPS Terpadu, Seni, Agama, Bahasa Daerah", title="🤔", style="bold plum4"))
            mapel = Console().input("[bold green][?][bold white] Pelajaran : ")
            if mapel in ["Matematika", "Bahasa Indonesia", "IPA Terpadu", "Penjaskes", "PPKN", "IPS Terpadu", "Seni", "Agama", "Bahasa Daerah"]:
                Console(width=50).print(Panel("[italic white]Silahkan masukan kata pencarian. Misalnya :[italic green] Cacing Bernapas Melalui?", title="🙂", style="bold plum4"))
                query = Console().input("[bold green][?][bold white] Query : ")
                Jawaban(cookie, x, mapel, query)
            else:pass
        except Exception as e:
            Console(width=50).print(Panel(f"[italic red]{str(e).capitalize()}", title="😡", style="bold plum4"));exit()
    elif choose == "2" or choose == "02":
        try:
            x = Sekolah(cookie, "SMP")
            Console(width=50).print(Panel("[bold white]Mata Pelajaran :[bold cyan] Matematika, Fisika, Kimia, Biologi, Bahasa Indonesia, Bahasa Inggris, Sejarah, Ekonomi, Geografi, Sosiologi, Penjaskes, PPKN, Seni, Agama, Teknologi Informasi Dan Bahasa Daerah.", title="🤔", style="bold plum4"))
            mapel = Console().input("[bold green][?][bold white] Pelajaran : ")
            if mapel in ["Matematika", "Fisika", "Kimia", "Biologi", "Bahasa Indonesia", "Bahasa Inggris", "Sejarah", "Ekonomi", "Geografi", "Sosiologi", "Penjaskes", "PPKN", "Seni", "Agama", "Teknologi", "Informasi", "Bahasa Daerah"]:
                Console(width=50).print(Panel("[italic white]Silahkan masukan kata pencarian. Misalnya :[italic green] Contoh Organisme Prokariotik Ialah?", title="🙂", style="bold plum4"))
                query = Console().input("[bold green][?][bold white] Query : ")
                Jawaban(cookie, x, mapel, query)
            else:pass
        except Exception as e:
            Console(width=50).print(Panel(f"[italic red]{str(e).capitalize()}", title="😡", style="bold plum4"));exit()
    elif choose == "3" or choose == "03":
        try:
            x = Sekolah(cookie, "SMA")
            Console(width=50).print(Panel("[bold white]Mata Pelajaran :[bold cyan] Matematika, Fisika, Kimia, Biologi, Bahasa Indonesia, Bahasa Inggris, Sejarah, Ekonomi, Geografi, Sosiologi, Penjaskes, Ppkn, Seni, Agama, Kewirausahaan, Teknologi Informasi Dan Bahasa Daerah.", title="🤔", style="bold plum4"))
            mapel = Console().input("[bold green][?][bold white] Pelajaran : ")
            if mapel in ["Matematika", "Fisika", "Kimia", "Biologi", "Bahasa Indonesia", "Bahasa Inggris", "Sejarah", "Ekonomi", "Geografi", "Sosiologi", "Penjaskes", "Ppkn", "Seni", "Agama", "Kewirausahaan", "Teknologi", "Informasi", "Bahasa Daerah"]:
                Console(width=50).print(Panel("[italic white]Silahkan masukan kata pencarian. Misalnya :[italic green] Hubungan Sinartrosis Sifibrosis Terletak Pada Bagian?", title="🙂", style="bold plum4"))
                query = Console().input("[bold green][?][bold white] Query : ")
                Jawaban(cookie, x, mapel, query)
            else:pass
        except Exception as e:
            Console(width=50).print(Panel(f"[italic red]{str(e).capitalize()}", title="😡", style="bold plum4"));exit()
    elif choose == "4" or choose == "04":
        try:
            x = Sekolah(cookie, "UTBK")
            Console(width=50).print(Panel("[bold white]Mata Pelajaran :[bold cyan] Matematika, Ekonomi, Geografi, Sosiologi, Bahasa Indonesia, Bahasa Inggris, Sejarah, Fisika, Kimia Dan Biologi", title="🤔", style="bold plum4"))
            mapel = Console().input("[bold green][?][bold white] Pelajaran : ")
            if mapel in ["Matematika", "Ekonomi", "Geografi", "Sosiologi", "Bahasa Indonesia", "Bahasa Inggris", "Sejarah", "Fisika", "Kimia", "Biologi"]:
                Console(width=50).print(Panel("[italic white]Silahkan masukan kata pencarian. Misalnya :[italic green] Buku Harian Jurnal Penjualan Digunakan Untuk Mencatat Penjualan?", title="🙂", style="bold plum4"))
                query = Console().input("[bold green][?][bold white] Query : ")
                Jawaban(cookie, x, mapel, query)
            else:pass
        except Exception as e:
            Console(width=50).print(Panel(f"[italic red]{str(e).capitalize()}", title="😡", style="bold plum4"));exit()
    else:pass
# Jawaban
def Jawaban(cookie, x, y, query):
    with requests.Session() as r:
        url = ("https://roboguru.ruangguru.com/api/v3/roboguru-discovery/search/question?gradeSerial={}&subjectName={}&withVideo=true&text={}&imageURL=&singleQuestion=false".format(x, y, query.replace(' ','%20')))
        r.headers.update({
            "Host": "roboguru.ruangguru.com",
            "accept": "application/json",
            "disable-node-proxy": "false",
            "country": "id",
            "platform": "web",
            "user-agent": "Mozilla/5.0 (Linux; Android 9; RMX1941 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.69 Mobile Safari/537.36",
            "with-auth": "true",
            "content-type": "application/json",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://roboguru.ruangguru.com/search?",
            "accept-encoding": "gzip, deflate",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "cookie": cookie
        })
        response = r.get(url)
        if '"questions":[]' in str(response.text):
            Console(width=50).print(Panel("[italic red]Pertanyaan kamu tidak ada jawabannya!", title="😡", style="bold plum4"))
            Console().input("[bold white][[bold green]Kembali[bold white]]");Login()
        else:
            for x in json.loads(response.text)["data"]["questions"]:
                soal = x["contents"]
                jawaban = x["contentDefinition"]
                like = x["likeCount"]
                views = x["viewCount"]
                v = Convert(jawaban)
                Console(width=50).print(Panel(f"""[bold white]Soal    :[bold magenta] {soal.capitalize()}
[bold white]Jawaban :[bold green] {v}
[bold white]Likes   :[bold yellow] {like}
[bold white]Viewer  :[bold red] {views}""", title="😍", style="bold plum4"))
                Console().input("[bold white][[bold green]Kembali[bold white]]")
                name = Validate(cookie);Menu(name)
# Convert
def Convert(jawaban):
    x = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6})";')
    y = x.sub('', jawaban)
    return y
# Validate
def Validate(cookie):
    with requests.Session() as r:
        url = ('https://roboguru.ruangguru.com/api/v3/user')
        r.headers.update({
            "Host": "roboguru.ruangguru.com",
            "accept": "application/json",
            "disable-node-proxy": "false",
            "country": "id",
            "platform": "web",
            "user-agent": "Mozilla/5.0 (Linux; Android 9; RMX1941 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.69 Mobile Safari/537.36",
            "with-auth": "true",
            "content-type": "application/json",
            "sec-fetch-site":"same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": "https://roboguru.ruangguru.com/",
            "accept-encoding": "gzip, deflate",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cookie": cookie
        })
        response = r.get(url)
        return json.loads(response.text)["data"][0]["name"]

if __name__=='__main__':
    try:
        cookie = json.loads(open('Data/Cookie.json','r').read())["Cookie"]
        name = Validate(cookie)
        Menu(name)
    except Exception as e:
        Login()