import os
from datetime import datetime, timezone
from supabase import create_client, Client

# --- CONEXÃO COM O SUPABASE ---
SUPABASE_URL = "https://fapriuoxjwrcgwxwvrgu.supabase.co"
SUPABASE_KEY = "sb_publishable_fBG5h1hqCPJ6TxcVTMJqQQ_7Q-4y353"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def categorizar_automaticamente(titulo):
    """Analisa o título do produto e descobre qual categoria ele pertence no seu site"""
    t = titulo.lower()
    
    if any(palavra in t for palavra in ["sapato", "tênis", "tenis", "camisa", "camiseta", "bermuda", "calça", "relógio", "relogio masculino", "polo", "jaqueta"]):
        return "moda-masculina"
    elif any(palavra in t for palavra in ["vestido", "blusa", "bolsa", "maquiagem", "feminina", "conjunto feminino", "cropped"]):
        return "moda-feminina"
    elif any(palavra in t for palavra in ["celular", "smartphone", "iphone", "xiaomi", "poco", "capinha", "carregador", "samsung galaxy"]):
        return "celulares"
    elif any(palavra in t for palavra in ["placa de vídeo", "placa de video", "gpu", "rtx", "gtx", "rx", "notebook", "mouse", "teclado", "monitor", "computador", "headset", "processador"]):
        return "computadores"
    elif any(palavra in t for palavra in ["fone", "smartwatch", "soundbar", "lampada", "lampada led", "caixa de som", "bluetooth"]):
        return "eletronicos"
    elif any(palavra in t for palavra in ["panela", "airfryer", "cozinha", "casa", "aspirador", "lençol", "robo aspirador", "cafeteira", "liquidificador"]):
        return "casa"
    else:
        return "achadinhos"

def salvar_ou_atualizar_oferta(nova_oferta):
    try:
        nova_oferta["categoria"] = categorizar_automaticamente(nova_oferta["titulo"])
        existente = supabase.table("ofertas").select("id, preco").eq("titulo", nova_oferta["titulo"]).execute()

        if existente.data:
            produto_antigo = existente.data[0]
            preco_anterior = produto_antigo["preco"]
            produto_id = produto_antigo["id"]

            if nova_oferta["preco"] != preco_anterior:
                dados_atualizacao = {
                    "preco_antigo": preco_anterior,
                    "preco": nova_oferta["preco"],
                    "menor_preco": nova_oferta["preco"] < preco_anterior,
                    "atualizado_em": datetime.now(timezone.utc).isoformat()
                }
                supabase.table("ofertas").update(dados_atualizacao).eq("id", produto_id).execute()
                print(f"🔄 Preço alterado: {nova_oferta['titulo']} -> [{nova_oferta['categoria']}]")
            else:
                print(f"ℹ️ Sem alteração: {nova_oferta['titulo']}")
        else:
            nova_oferta["criado_em"] = datetime.now(timezone.utc).isoformat()
            nova_oferta["atualizado_em"] = datetime.now(timezone.utc).isoformat()
            
            supabase.table("ofertas").insert(nova_oferta).execute()
            print(f"✅ Novo produto salvo [{nova_oferta['categoria']}]: {nova_oferta['titulo']}")

    except Exception as e:
        print(f"❌ Erro ao salvar o produto: {e}")

def executar_garimpo():
    print("🚀 Robô iniciado: Vitrine inteligente preenchendo o Garimpo Certo...")

    # Lista ampliada com dezenas de produtos inteligentes para testar todas as seções
    produtos_encontrados = [
        # Computadores & Hardware
        {
            "titulo": "Placa de Vídeo RTX 3060 12GB GDDR6 Gamer",
            "loja": "Kabum",
            "imagem_url": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?w=800",
            "preco": 1399.90,
            "preco_antigo": 1899.00,
            "cupom": "GAMER100",
            "menor_preco": True,
            "url": "https://slink.vc/seu-link-de-afiliado"
        },
        {
            "titulo": "Headset Gamer Sem Fio Logitech G435 Lightspeed",
            "loja": "Amazon",
            "imagem_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=800",
            "preco": 299.90,
            "preco_antigo": 499.00,
            "cupom": None,
            "menor_preco": True,
            "url": "https://amzn.to/seu-link-de-afiliado"
        },
        {
            "titulo": "Mouse Gamer RGB Ergonômico Redragon Griffin 7200DPI",
            "loja": "Shopee",
            "imagem_url": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=800",
            "preco": 79.90,
            "preco_antigo": 130.00,
            "cupom": "MOUSE10",
            "menor_preco": True,
            "url": "https://slink.vc/seu-link-de-afiliado"
        },

        # Celulares & Acessórios
        {
            "titulo": "Smartphone Xiaomi Poco X6 Pro 5G 256GB",
            "loja": "Shopee",
            "imagem_url": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=800",
            "preco": 1699.00,
            "preco_antigo": 2299.00,
            "cupom": "POCO100",
            "menor_preco": True,
            "url": "https://slink.vc/seu-link-de-afiliado"
        },
        {
            "titulo": "Suporte Veicular Magnético para Celular Painel",
            "loja": "Shopee",
            "imagem_url": "https://images.unsplash.com/photo-1584438784894-089d6a62b8fa?w=800",
            "preco": 14.99,
            "preco_antigo": 35.00,
            "cupom": "GANHE10",
            "menor_preco": True,
            "url": "https://slink.vc/seu-link-de-afiliado"
        },

        # Eletrônicos
        {
            "titulo": "Fone de Ouvido Bluetooth Sem Fio Lenovo LivePods",
            "loja": "Shopee",
            "imagem_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=800",
            "preco": 49.90,
            "preco_antigo": 119.90,
            "cupom": "FRETEGRATIS",
            "menor_preco": True,
            "url": "https://slink.vc/seu-link-de-afiliado"
        },
        {
            "titulo": "Smartwatch Relógio Inteligente D20 Y68 Bluetooth",
            "loja": "Shopee",
            "imagem_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800",
            "preco": 39.90,
            "preco_antigo": 89.90,
            "cupom": "FRETEGRATIS",
            "menor_preco": True,
            "url": "https://slink.vc/seu-link-de-afiliado"
        },

        # Moda Masculina
        {
            "titulo": "Sapato Social Masculino Couro Confortável",
            "loja": "Shopee",
            "imagem_url": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?w=800",
            "preco": 79.90,
            "preco_antigo": 159.90,
            "cupom": "MENORPRECO",
            "menor_preco": True,
            "url": "https://slink.vc/seu-link-de-afiliado"
        },
        {
            "titulo": "Kit Camisa Polo Masculina Slim Algodão (3 Peças)",
            "loja": "Shopee",
            "imagem_url": "https://images.unsplash.com/photo-1625910513418-7c4712574e3d?w=800",
            "preco": 89.90,
            "preco_antigo": 160.00,
            "cupom": "MODAESTILO",
            "menor_preco": True,
            "url": "https://slink.vc/seu-link-de-afiliado"
        },
        {
            "titulo": "Tênis Esportivo Casual Masculino Corrida",
            "loja": "Shopee",
            "imagem_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800",
            "preco": 69.99,
            "preco_antigo": 139.90,
            "cupom": "FRETEGRATIS",
            "menor_preco": True,
            "url": "https://slink.vc/seu-link-de-afiliado"
        },

        # Moda Feminina
        {
            "titulo": "Vestido Midi Casual Elegante Godê Transpassado",
            "loja": "Shopee",
            "imagem_url": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=800",
            "preco": 59.90,
            "preco_antigo": 119.90,
            "cupom": "FRETEGRATIS",
            "menor_preco": False,
            "url": "https://slink.vc/seu-link-de-afiliado"
        },
        {
            "titulo": "Bolsa Feminina Transversal Couro Sintético",
            "loja": "Shopee",
            "imagem_url": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=800",
            "preco": 49.90,
            "preco_antigo": 99.00,
            "cupom": "BOLSA10",
            "menor_preco": True,
            "url": "https://slink.vc/seu-link-de-afiliado"
        },

        # Casa & Cozinha
        {
            "titulo": "Air Fryer Fritadeira Sem Óleo 4L Mondial",
            "loja": "Amazon",
            "imagem_url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800",
            "preco": 249.00,
            "preco_antigo": 399.00,
            "cupom": None,
            "menor_preco": True,
            "url": "https://amzn.to/seu-link-de-afiliado"
        },
        {
            "titulo": "Robô Aspirador de Pó Inteligente WAP W100",
            "loja": "Amazon",
            "imagem_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=800",
            "preco": 349.00,
            "preco_antigo": 599.00,
            "cupom": "CASA10",
            "menor_preco": True,
            "url": "https://amzn.to/seu-link-de-afiliado"
        }
    ]

    for prod in produtos_encontrados:
        salvar_ou_atualizar_oferta(prod)

    print("🏁 Vitrine inteligente preenchida e categorizada com sucesso!")

if __name__ == "__main__":
    executar_garimpo()