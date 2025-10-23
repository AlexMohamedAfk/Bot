import telebot
import yt_dlp
import os
import nest_asyncio
import asyncio

nest_asyncio.apply()

TOKEN = "8318747741:AAGwIa_6OuLUoaJKBW2XNfSCMap1v1kHxXk"
bot = telebot.TeleBot(TOKEN, parse_mode=None)

# تحميل الأغنية
async def download_song(query):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloaded_song.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)
            filename = ydl.prepare_filename(info['entries'][0])
            mp3_file = 'downloaded_song.mp3'
            return mp3_file

    except Exception as e:
        return str(e)

# استقبال الرسائل
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    query = message.text.strip()
    if not query:
        bot.reply_to(message, "🎵 اكتب اسم الأغنية اللي عايزها:")
        return

    bot.reply_to(message, f"⏳ جاري تحميل الأغنية: {query}")
    try:
        loop = asyncio.get_event_loop()
        mp3_file = loop.run_until_complete(download_song(query))

        if os.path.exists(mp3_file):
            with open(mp3_file, 'rb') as audio:
                bot.send_audio(message.chat.id, audio)
            os.remove(mp3_file)
        else:
            bot.reply_to(message, f"❌ حصل خطأ أثناء التحميل:\n{mp3_file}")

    except Exception as e:
        bot.reply_to(message, f"❌ حصل خطأ أثناء التحميل:\n{e}")

print("🤖 البوت شغال... ابعت أي اسم أغنية بالعربي أو الإنجليزي 🎶")
bot.infinity_polling()
