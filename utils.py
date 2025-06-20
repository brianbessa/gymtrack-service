import qrcode
from io import BytesIO
import base64
import difflib
import re
from datetime import time
import difflib
from collections import defaultdict


def gerar_qr_pix(chave_pix, nome, cidade, valor, txid="GTX001"):
    payload = f"""
    000201
    26360014BR.GOV.BCB.PIX0114{chave_pix}
    52040000
    5303986
    5405{valor:0>5}
    5802BR
    5913{nome[:13].upper()}
    6011{cidade[:11].upper()}
    62070503{txid}
    6304"""
    payload = ''.join(payload.split())

    qr = qrcode.make(payload)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_str

refeicoes_padrao = [
    "café da manhã",
    "lanche da manhã",
    "almoço",
    "lanche da tarde",
    "jantar",
    "ceia"
]

def identificar_refeicao(texto):
    texto = texto.lower()
    texto = re.sub(r"refei[cç][aã]o\s*\d+\s*[–-]?", "", texto)
    texto = re.sub(r"\(.*?\)", "", texto).strip()
    match = difflib.get_close_matches(texto, refeicoes_padrao, n=1, cutoff=0.6)
    return match[0] if match else None

def extrair_horario(texto):
    match = re.search(r'\((\d{2}:\d{2})\)', texto)
    if match:
        h, m = map(int, match.group(1).split(":"))
        return time(h, m)
    return None

def processar_txt_inteligente(conteudo):
    linhas = conteudo.strip().split('\n')
    plano = {}
    refeicao_atual = None

    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue

        horario_extraido = extrair_horario(linha)
        tentativa_refeicao = identificar_refeicao(linha)

        if tentativa_refeicao:
            refeicao_atual = tentativa_refeicao
            plano[refeicao_atual] = {
                "horario": horario_extraido,
                "alimentos": []
            }
            continue

        if refeicao_atual:
            plano[refeicao_atual]["alimentos"].append(linha)

    return plano