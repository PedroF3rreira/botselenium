import re
from bot import Wppbot

bot = Wppbot('robot')

bot.treinar('treino')
bot.iniciar('Testando bot')
bot.saudacoe(['Bot: oi tudo bem', 'Bot: Como vc esta'])
ultimo_texto = ''

while True:
    texto = bot.escuta()
    if texto != ultimo_texto and re.match(r'^::', texto):
        texto = texto.replace('::', '')
        texto = texto.lower()
        bot.responde(texto)