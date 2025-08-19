  GNU nano 8.5          fxbot.py
import telebot
import yt_dlp
import os

# 🔑 Tokeningizni shu yerga yozing
BOT_TOKEN = "7391287511:AAFlhG31hoxEAglcuWSFHLl9lM48>

bot = telebot.TeleBot(BOT_TOKEN)

# 📂 Fayl qidirish yordamchi funksiyasi
def find_file_by_prefix(prefix, exts):
    for ext in exts:
        fname = f"{prefix}.{ext}"
        if os.path.exists(fname):
            return fname
    return None

# 📥 Video yuklab olish
def download_video(url, prefix="video"):
    ydl_opts = {
        "outtmpl": f"{prefix}.%(ext)s",
        "format": "best[height<=480][ext=mp4]/best[h>
        "merge_output_format": "mp4",
        "noplaylist": True,
        "max_filesize": 50*1024*1024 # 50 MB dan ka>
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    path = find_file_by_prefix(prefix, ["mp4", "mkv">
    if not path:
        raise FileNotFoundError("Video fayli topilma>
    return path

# 🎵 MP3 yuklab olish
def download_audio(url, prefix="audio"):
    ydl_opts = {
        "outtmpl": f"{prefix}.%(ext)s",
        "format": "bestaudio/best",
        "noplaylist": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "max_filesize": 50*1024*1024 }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    path = find_file_by_prefix(prefix, ["mp3"])
    if not path:
        raise FileNotFoundError("Audio fayli topilma>
    return path

# 🚀 /start komandasi
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom 👋\nMenga YouTube, >
                          "🎬 Video olish uchun: lin>
                          "🎵 MP3 olish uchun: link >

# 🔗 Linkni qabul qilish
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()

    try:
        if "mp3" in url:  # MP3 so‘zi bor bo‘lsa
            url = url.replace("mp3", "").strip()
            bot.reply_to(message, "⏳ Audio yuklanmo>
            audio_path = download_audio(url)
  with open(audio_path, "rb") as f:
                bot.send_audio(message.chat.id, f)
            os.remove(audio_path)

        else:  # Oddiy video
            bot.reply_to(message, "⏳ Video yuklanmo>
            video_path = download_video(url)
            with open(video_path, "rb") as f:
                bot.send_video(message.chat.id, f)
            os.remove(video_path)

    except Exception as e:
        bot.reply_to(message, f"❌ Xato: {e}")

# ♾ Botni ishga tushirish
print("🤖 Bot ishlayapti...")
bot.infinity_polling()
