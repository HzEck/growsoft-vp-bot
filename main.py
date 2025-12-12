# main.py (YENİ VE GÜNCELLENMİŞ VERSİYON)
import discord
from discord.ext import tasks
import asyncio
import os 
from flask import Flask
import threading # Yeni bir süreci başlatmak için

# ================= FLASK WEB SUNUCUSU (RENDER İÇİN ZORUNLU) =================
app = Flask(__name__)

# Render bu adrese bağlandığında "Bot çalışıyor" mesajı görecek.
@app.route('/')
def home():
    return "GrowSoft VP Bot is running!"

# Flask sunucusunu ayrı bir süreçte başlatacak fonksiyon
def run_flask():
    # Render, PORT adında bir Ortam Değişkeni verir, onu kullanıyoruz.
    port = int(os.environ.get('PORT', 5000)) 
    app.run(host='0.0.0.0', port=port)

# =============================================================================


# ================= BOT AYARLARI =================
TOKEN = os.environ.get("DISCORD_TOKEN") 

VOICE_CHANNEL_ID = 1448444047730671798 
ALLOWED_CHANNEL_ID = 1449082803739164734 # << BURAYA KOMUT KANALI ID'SİNİ YAZIN!

VP_AMOUNT = 1 
INTERVAL_MINUTES = 1
# ========================================================

class VPCommander(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'{self.user} olarak giriş yapıldı. Otomatik döngü başlatılıyor...')
        self.check_voice_channel.start()

    @tasks.loop(minutes=INTERVAL_MINUTES)
    async def check_voice_channel(self):
        voice_channel = self.get_channel(VOICE_CHANNEL_ID)
        target_channel = self.get_channel(ALLOWED_CHANNEL_ID)
        
        if not voice_channel or not target_channel:
            print("Hata: Kanal ID'leri bulunamadı. Kontrol edin.")
            return

        members = voice_channel.members
        
        if len(members) == 0:
            return

        print(f"[{INTERVAL_MINUTES} dk] Ses kanalında {len(members)} kişi bulundu. Komutlar gönderiliyor...")

        for member in members:
            command = f"-givevp {member.id} {VP_AMOUNT}"
            
            try:
                await target_channel.send(command)
                await asyncio.sleep(0.5) 
            except Exception as e:
                print(f"Mesaj gönderme hatası: {e}")
        
        print("Komut döngüsü tamamlandı.")


    @check_voice_channel.before_loop
    async def before_check(self):
        await self.wait_until_ready()

intents = discord.Intents.default()
intents.members = True 
intents.voice_states = True 

client = VPCommander(intents=intents)

if __name__ == "__main__":
    # Flask sunucusunu ayrı bir thread'de (süreçte) başlat
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    
    # Discord Botunu ana süreçte başlat
    if not TOKEN:
        print("HATA: DISCORD_TOKEN ortam değişkeni ayarlanmamış!")
    else:
        try:
            client.run(TOKEN)
        except discord.HTTPException as e:
            print(f"HATA: Discord API Hatası. Token yanlış veya Intent'ler eksik. Hata kodu: {e.status}")


