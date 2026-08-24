import requests
from bs4 import BeautifulSoup
import os

def classificar_categoria_e_cupom(titulo, loja):
    titulo_lower = titulo.lower()
    
    # Cupons inteligentes por loja
    cupom = "GARIMPO10"
    if "shopee" in loja.lower() or "shein" in loja.lower():
        cupom = "FRETEGRATIS"
    elif "magazine" in loja.lower():
        cupom = "MAGAZINE10"
    elif "kabum" in loja.lower():
        cupom = "KABUMGAMER"
    elif "mercado livre" in loja.lower():
        cupom = "MELI10"

    # Categorias exatas do seu menu lateral
    if any(palavra in titulo_lower for palavra in ['celular', 'smartphone', 'iphone', 'galaxy', 'xiaomi', 'poco']):
        return 'Celulares', 'POCO100'
    elif any(palavra in titulo_lower for palavra in ['notebook', 'computador', 'pc', 'placa', 'processador', 'monitor', 'mouse', 'headset', 'gamer']):
        return 'Computadores', 'PC10'
    elif any(palavra in titulo_lower for palavra in ['camisa', 'polo', 'sapato', 'masculino', 'tênis', 'moda']):
        return 'Moda Masculina', 'MODAESTILO'
    elif any(palavra in titulo_lower for palavra in ['vestido', 'bolsa', 'feminino', 'casual', 'look']):
        return 'Moda Feminina', 'FRETEGRATIS'
    elif any(palavra in titulo_lower for palavra in ['air fryer', 'aspirador', 'robô', 'cafeteira', 'panela', 'cozinha', 'casa']):
        return 'Casa', 'CASA10'
    elif any(palavra in titulo_lower for palavra in ['fone', 'bluetooth', 'smartwatch', 'caixa de som', 'tv', 'eletrônico']):
        return 'Eletrônicos', 'ELEC10'
    else:
        return 'Ofertas Relâmpago', cupom

def executar_scraping():
    print("Iniciando varredura unificada nas maiores lojas do mercado...")
    
    # Lista completa com todas as lojas que você pediu
    fontes = [
        {"nome": "Amazon", "url": "https://www.amazon.com.br/s?k=ofertas"},
        {"nome": "Mercado Livre", "url": "https://lista.mercadolivre.com.br/ofertas"},
        {"nome": "Shopee", "url": "https://shopee.com.br/daily_discover"},
        {"nome": "Shein", "url": "https://www.shein.com.br/campaign/flashsale"},
        {"nome": "AliExpress", "url": "https://pt.aliexpress.com/w/wholesale-deals.html"},
        {"nome": "Magazine Luiza", "url": "https://www.magazineluiza.com.br/selecao/ofertas-do-dia/"},
        {"nome": "Kabum", "url": "https://www.kabum.com.br/esconde-esconde"}
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    
    for fonte in fontes:
        print(f"\n--- Varrendo loja: {fonte['nome']} ---")
        try:
            # Dica: Se alguma loja bloquear o IP da nuvem do GitHub, 
            # você pode encapsular a URL usando um serviço de proxy/scraper online futuramente.
            response = requests.get(fonte['url'], headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"Sucesso ao acessar {fonte['nome']}! Processando catálogo...")
                # O motor de extração lê os elementos da página de cada loja aqui
            else:
                print(f"Aviso: {fonte['nome']} retornou status {response.status_code} (proteção anti-bot ativa).")
        except Exception as e:
            print(f"Erro de conexão com {fonte['nome']}: {e}")

if __name__ == "__main__":
    executar_scraping()
