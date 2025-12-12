# main.py
import discord
from discord.ext import tasks
import asyncio
import os 

TOKEN = os.environ.get("DISCORD_TOKEN")

VOICE_CHANNEL_ID = 1448444047730671798 
ALLOWED_CHANNEL_ID = 1418862486974763071 # << BURAYA KOMUT KANALI ID'SİNİ YAZIN!

VP_AMOUNT = 1 
INTERVAL_MINUTES = 3

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
    if not TOKEN:
        print("HATA: DISCORD_TOKEN ortam değişkeni ayarlanmamış!")
    else:
        try:
            client.run(TOKEN)
        except discord.HTTPException as e:

            print(f"HATA: Discord API Hatası. Token yanlış veya Intent'ler eksik. Hata kodu: {e.status}")


