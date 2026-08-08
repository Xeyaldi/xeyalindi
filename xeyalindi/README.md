<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:26A5E4,100:6C63FF&height=200&section=header&text=Xeyal%20Music&fontSize=60&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Telegram%20Qrup%20Zəngi%20Musiqi%20Botu&descAlignY=55&descSize=18" width="100%"/>

<a href="https://github.com/Xeyaldi/ariabotum_fixed">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&duration=3000&pause=1000&color=26A5E4&center=true&vCenter=true&width=560&lines=Y%C3%BCksək+keyfiyyətli+musiqi+%2B+əylə%C5%9F;13+dildə+tam+t%C9%99rc%C3%BCm%C9%99+d%C9%99st%C9%99yi;Groq+AI+%2B+Pexels+inteqrasiyası;Pyrogram+(Kurigram)+%2B+PyTgCalls" alt="Typing SVG" />
</a>

<br><br>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-Kurigram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://github.com/KurimuzonAkuma/pyrogram)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](./LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](./Dockerfile)

[![Telegram](https://img.shields.io/badge/Telegram-Open_Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/kullaniciadidi)
[![Dəstək](https://img.shields.io/badge/Dəstək-Kanal-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Ekoodu)

![Stars](https://img.shields.io/github/stars/Xeyaldi/ariabotum_fixed?style=social)
![Forks](https://img.shields.io/github/forks/Xeyaldi/ariabotum_fixed?style=social)
![Last Commit](https://img.shields.io/github/last-commit/Xeyaldi/ariabotum_fixed?color=6C63FF)
![Repo Size](https://img.shields.io/github/repo-size/Xeyaldi/ariabotum_fixed?color=26A5E4)

</div>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.gif" width="100%">

## 📖 Haqqında

**Xeyal Music**, Telegram qrup zənglərinə qoşulub yüksək keyfiyyətli musiqi çalan, eyni zamanda əyləncə, süni intellekt və media endirmə funksiyalarını özündə birləşdirən açıq mənbəli bir botdur. Pyrogram (Kurigram) və PyTgCalls üzərində qurulub, 13 dildə tam tərcümə dəstəyi var.

<div align="center">

| 🎧 Musiqi | ⬇️ Endirmə | 🤖 Süni İntellekt | 🌍 13 Dil |
|:---:|:---:|:---:|:---:|
| Qrup zəngində canlı çalma | MP3 (ID3 + cover) | Groq AI + Pexels | Tam tərcümə |

</div>

---

## ✨ Xüsusiyyətlər

<details open>
<summary><b>🎧 Musiqi</b></summary>
<br>

- YouTube, Spotify və digər mənbələrdən qrup zəngində birbaşa musiqi/video çalma
- `/play`, `/pause`, `/resume`, `/skip`, `/stop`, `/seek`, `/loop` və növbə (`/queue`) idarəetməsi
- Playlist dəstəyi və avtomatik keyfiyyət seçimi

</details>

<details>
<summary><b>⬇️ Media endirmə</b></summary>
<br>

- YouTube, TikTok, Instagram və `yt-dlp`-nin dəstəklədiyi digər saytlardan birbaşa MP3 endirmə
- ID3 tag və üz qabığı şəkli embed olunmuş həqiqi audio fayl (Telegram-da player kimi açılır)

</details>

<details>
<summary><b>🔍 Inline rejim</b></summary>
<br>

- `@botadi mahnı adı` yazaraq bot söhbətdən kənarda birbaşa musiqi axtarışı

</details>

<details>
<summary><b>🎭 Əyləncə</b></summary>
<br>

- `/slap`, `/hug`, `/kiss`, `/bite`, `/8ball`, `/rate`, `/couple`, `/marry`, `/love` və digər əyləncə əmrləri
- Zər-əsaslı mini-oyunlar (`/games`)

</details>

<details>
<summary><b>🤖 Süni intellekt</b></summary>
<br>

- Groq AI ilə sual-cavab (`/ask`)
- Pexels üzərindən şəkil/video axtarışı (`/img`, `/vid`)
- Fayl kataloqu idarəetməsi (`/catalog`, `/addfile`)

</details>

<details>
<summary><b>🛠️ Admin alətləri</b></summary>
<br>

- Sudo istifadəçi idarəetməsi, qara siyahı, broadcast, statistika
- Aktivlik izləmə və qrup autentifikasiyası

</details>

<details>
<summary><b>🌍 Çoxdillilik</b></summary>
<br>

13 dildə tam tərcümə dəstəyi:

`az` `en` `ru` `tr` `ar` `de` `es` `fr` `hi` `ja` `pa` `pt` `zh`

</details>

---

## 🚀 Qurulum

### 1️⃣ Repozitoriyanı klonla

```bash
git clone https://github.com/Xeyaldi/ariabotum_fixed.git
cd ariabotum_fixed
```

### 2️⃣ Mühit dəyişənlərini təyin et

`sample.env` faylını `.env` adı ilə kopyala və özünə uyğun dəyərlərlə doldur:

```bash
cp sample.env .env
```

<div align="center">

| Dəyişən | Açıqlama |
|:---|:---|
| `API_ID` / `API_HASH` | [my.telegram.org](https://my.telegram.org/apps) ünvanından alınır |
| `BOT_TOKEN` | [@BotFather](https://t.me/BotFather)-dan alınan bot tokeni |
| `MONGO_URL` | [cloud.mongodb.com](https://cloud.mongodb.com) verilənlər bazası ünvanı |
| `LOGGER_ID` | Botun loq atacağı qrupun ID-si |
| `OWNER_ID` | Bot sahibinin Telegram istifadəçi ID-si |
| `SESSION` | [@StringFatherBot](https://t.me/StringFatherBot) vasitəsilə alınan Pyrogram sessiya sətri |

</div>

### 3️⃣ İşə sal

**uv ilə (tövsiyə olunur):**

```bash
uv sync
bash start
```

**Docker ilə:**

```bash
docker build -t xeyal-music .
docker run --env-file .env xeyal-music
```

---

## 📂 Layihə strukturu

```
xeyal/
├── core/         → Bot, userbot, mongo, telegram və youtube əsas modulları
├── helpers/      → Kömekçi funksiyalar (növbə, thumbnail, admin yoxlamaları və s.)
├── plugins/      → Bütün əmrlərin (play, queue, fun, edu, admin...) plugin faylları
├── locales/      → 13 dildə tərcümə faylları (JSON)
└── cookies/      → yt-dlp üçün istifadə olunan cookie şablonları
```

---

## 🤝 Töhfə vermək

Pull request-lər açıqdır! Yeni dil tərcüməsi əlavə etmək üçün `xeyal/locales/en.json` faylını nümunə götürüb öz dilinizə çevirin və PR açın.

## 📜 Lisenziya

Bu layihə [MIT lisenziyası](./LICENSE) altında yayımlanır.

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:6C63FF,100:26A5E4&height=120&section=footer" width="100%"/>

Made with ❤️ by **Xeyal**

</div>
