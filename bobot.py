import os
import telebot
from telebot import types
import phonenumbers
from phonenumbers import geocoder, carrier
import requests
import re
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

def menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("Phone Lookup", callback_data="phone"),
        types.InlineKeyboardButton("Email Check", callback_data="email"),
        types.InlineKeyboardButton("Username Search", callback_data="username"),
        types.InlineKeyboardButton("Subdomain Finder", callback_data="subdomain"),
        types.InlineKeyboardButton("Check Nopol", callback_data="nopol"),
        types.InlineKeyboardButton("IP Lookup", callback_data="ip"),
        types.InlineKeyboardButton("Domain Check", callback_data="domain"),
        types.InlineKeyboardButton("Info Bot", callback_data="info"),
    )
    return markup

@bot.message_handler(commands=['start', 'menu'])
def start(m):
    teks = "OSINT BOT\nLegal & Aman 100%\n\nHalo, " + m.from_user.first_name + "!\nSelamat datang di OSINT Bot.\n\nSilahkan pilih menu di bawah:"
    bot.send_message(m.chat.id, teks, reply_markup=menu())

@bot.callback_query_handler(func=lambda c: True)
def tombol(c):
    if c.data == "info":
        bot.send_message(c.message.chat.id, "INFO BOT\n\nBot ini hanya memakai data PUBLIK.\nTidak bisa cek NIK, nama pemilik, alamat, dll.")
    elif c.data == "phone":
        bot.send_message(c.message.chat.id, "PHONE LOOKUP\n\nKirim:\n/hp 08123456789")
    elif c.data == "email":
        bot.send_message(c.message.chat.id, "EMAIL CHECK\n\nKirim:\n/email contoh@gmail.com")
    elif c.data == "username":
        bot.send_message(c.message.chat.id, "USERNAME SEARCH\n\nKirim:\n/user alif123")
    elif c.data == "subdomain":
        bot.send_message(c.message.chat.id, "SUBDOMAIN FINDER\n\nKirim:\n/sub google.com")
    elif c.data == "nopol":
        bot.send_message(c.message.chat.id, "CHECK NOPOL\n\nKirim:\n/nopol D1234ABC")
    elif c.data == "ip":
        bot.send_message(c.message.chat.id, "IP LOOKUP\n\nKirim:\n/ip 8.8.8.8")
    elif c.data == "domain":
        bot.send_message(c.message.chat.id, "DOMAIN CHECK\n\nKirim:\n/domain google.com")

@bot.message_handler(commands=['hp'])
def hp(m):
    try:
        nomor = m.text.split()[1]
        if nomor.startswith("0"):
            nomor = "+62" + nomor[1:]
        elif nomor.startswith("62"):
            nomor = "+" + nomor
        parsed = phonenumbers.parse(nomor, "ID")
        valid = phonenumbers.is_valid_number(parsed)
        bot.reply_to(m, "PHONE LOOKUP\n\nNomor: " + nomor + "\nValid: " + str(valid) + "\nNegara: " + str(geocoder.description_for_number(parsed, 'id')) + "\nOperator: " + str(carrier.name_for_number(parsed, 'id')))
    except:
        bot.reply_to(m, "Format salah. Contoh: /hp 08123456789")

@bot.message_handler(commands=['email'])
def email(m):
    try:
        e = m.text.split()[1]
        if re.match(r"[^@]+@[^@]+\.[^@]+", e):
            bot.reply_to(m, "EMAIL CHECK\n\nEmail: " + e + "\nFormat: Valid")
        else:
            bot.reply_to(m, "Format email salah.")
    except:
        bot.reply_to(m, "Contoh: /email contoh@gmail.com")

@bot.message_handler(commands=['user'])
def user(m):
    try:
        u = m.text.split()[1].strip()
        bot.reply_to(m, "Cek username " + u + "...")
        situs = {
            "Instagram": "https://instagram.com/" + u,
            "TikTok": "https://tiktok.com/@" + u,
            "GitHub": "https://github.com/" + u,
            "Twitter/X": "https://x.com/" + u,
            "YouTube": "https://youtube.com/@" + u,
        }
        hasil = "USERNAME SEARCH: " + u + "\n\n"
        for nama, url in situs.items():
            try:
                r = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
                status = "Ditemukan" if r.status_code == 200 else "Tidak ada"
            except:
                status = "Gagal cek"
            hasil += nama + ": " + status + "\n" + url + "\n\n"
        bot.send_message(m.chat.id, hasil)
    except:
        bot.reply_to(m, "Contoh: /user alif123")

@bot.message_handler(commands=['sub'])
def sub(m):
    try:
        d = m.text.split()[1].strip().replace("https://","").replace("http://","").split("/")[0]
        bot.reply_to(m, "Cari subdomain " + d + "...")
        r = requests.get("https://crt.sh/?q=%." + d + "&output=json", timeout=15)
        data = r.json()
        subs = sorted(set([x['name_value'] for x in data]))[:20]
        hasil = "SUBDOMAIN FINDER: " + d + "\n\nDitemukan " + str(len(data)) + " (ditampilkan 20):\n\n" + "\n".join(subs)
        bot.send_message(m.chat.id, hasil)
    except:
        bot.reply_to(m, "Gagal. Contoh: /sub google.com")

@bot.message_handler(commands=['nopol'])
def nopol(m):
    kode_wilayah = {"D": "Bandung / Jawa Barat", "B": "Jakarta", "L": "Surabaya", "AB": "Yogyakarta", "H": "Semarang", "N": "Malang", "F": "Bogor", "T": "Karawang", "E": "Cirebon", "A": "Banten", "Z": "Tasikmalaya", "G": "Pekalongan", "K": "Pati", "R": "Banyumas", "S": "Bojonegoro", "W": "Sidoarjo", "AG": "Kediri", "AE": "Madiun", "AD": "Solo", "AA": "Magelang", "DK": "Bali", "DR": "Lombok", "BM": "Riau", "BA": "Sumbar", "BB": "Sumut", "BL": "Aceh", "BG": "Palembang", "BH": "Jambi", "BE": "Lampung", "KT": "Kaltim", "KB": "Kalbar", "DA": "Kalsel", "KH": "Kalteng", "DN": "Sulteng", "DD": "Makassar", "DB": "Manado", "DE": "Maluku", "DS": "Papua"}
    try:
        plat = m.text.split()[1].upper()
        kode = ""
        for huruf in plat:
            if huruf.isalpha():
                kode += huruf
            else:
                break
        wilayah = kode_wilayah.get(kode, "Tidak diketahui")
        bot.reply_to(m, "CHECK NOPOL\n\nPlat: " + plat + "\nKode Wilayah: " + kode + "\nWilayah Samsat: " + wilayah + "\n\nIni hanya cek wilayah, BUKAN data pemilik.")
    except:
        bot.reply_to(m, "Contoh: /nopol D1234ABC")

@bot.message_handler(commands=['ip'])
def ip(m):
    try:
        ip_addr = m.text.split()[1]
        r = requests.get("http://ip-api.com/json/" + ip_addr).json()
        if r['status'] == 'success':
            bot.reply_to(m, "IP LOOKUP\n\nIP: " + ip_addr + "\nNegara: " + str(r.get('country')) + "\nKota: " + str(r.get('city')) + "\nISP: " + str(r.get('isp')))
        else:
            bot.reply_to(m, "IP tidak ditemukan.")
    except:
        bot.reply_to(m, "Contoh: /ip 8.8.8.8")

@bot.message_handler(commands=['domain'])
def domain(m):
    try:
        d = m.text.split()[1].strip().replace("https://","").replace("http://","").split("/")[0]
        bot.reply_to(m, "Cek domain " + d + "...")
        r = requests.get("https://who-dat.net/api/v1/domain/" + d, timeout=10).json()
        hasil = "DOMAIN CHECK: " + d + "\n\nRegistrar: " + str(r.get('registrar', 'Tidak diketahui')) + "\nDibuat: " + str(r.get('created', 'Tidak diketahui')) + "\nExpired: " + str(r.get('expires', 'Tidak diketahui'))
        bot.send_message(m.chat.id, hasil)
    except:
        bot.reply_to(m, "Contoh: /domain google.com")
@bot.message_handler(commands=['web'])
def web(m):
    try:
        d = m.text.split()[1].strip().replace("https://","").replace("http://","").split("/")[0]
        url = "https://" + d
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        bot.reply_to(m, "WEB CHECK\n\nWebsite: " + url + "\nStatus: " + str(r.status_code) + " (Online)" + "\nWaktu respon: " + str(round(r.elapsed.total_seconds(), 2)) + " detik")
    except:
        bot.reply_to(m, "Website offline. Contoh: /web google.com")

@bot.message_handler(commands=['cuaca'])
def cuaca(m):
    try:
        kota = m.text.split()[1].lower()
        coords = {"jakarta": "-6.2088,106.8456", "semarang": "-6.9667,110.4167", "surabaya": "-7.2575,112.7521", "bandung": "-6.9175,107.6191", "medan": "3.5952,98.6722", "yogyakarta": "-7.7956,110.3695"}
        latlon = coords.get(kota, "-6.2088,106.8456")
        lat, lon = latlon.split(",")
        r = requests.get("https://api.open-meteo.com/v1/forecast?latitude=" + lat + "&longitude=" + lon + "&current=temperature_2m,relative_humidity_2m,wind_speed_10m").json()
        cur = r['current']
        bot.reply_to(m, "CUACA " + kota.upper() + "\n\nSuhu: " + str(cur['temperature_2m']) + " C\nKelembaban: " + str(cur['relative_humidity_2m']) + "%\nAngin: " + str(cur['wind_speed_10m']) + " km/jam")
    except:
        bot.reply_to(m, "Contoh: /cuaca semarang")

@bot.message_handler(commands=['short'])
def short(m):
    try:
        link = m.text.split()[1]
        r = requests.get("https://tinyurl.com/api-create.php?url=" + link, timeout=10).text
        bot.reply_to(m, "SHORTLINK\n\nAsli: " + link + "\nPendek: " + r)
    except:
        bot.reply_to(m, "Contoh: /short https://google.com")
print("Bot jalan...")
bot.infinity_polling()
