"""
Buscador de Vagas — David Cavalcante
======================================
Usa o feed RSS do Indeed Brasil (funciona sem API e sem bloqueio).
Rode: python buscar_vagas.py
Dependência: pip install pandas requests
"""

import requests
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
import time

# ============================================================
# CONFIGURE AQUI
# ============================================================

TERMOS = [
    "web designer",
    "designer grafico",
    "ui designer",
    "branding designer",
    "assistente de marketing",
    "social media",
    "estagio front end",
    "junior front end",
]

LOCAIS = [
    "Vitoria,+ES",
    "Vila+Velha,+ES",
    "Serra,+ES",
    "",           # vazio = todo Brasil (pega remotas)
]

SALVAR_EM = "vagas.csv"

# ============================================================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def buscar_indeed_rss(termo, local):
    vagas = []
    try:
        q = termo.replace(" ", "+")
        url = f"https://br.indeed.com/rss?q={q}&l={local}&sort=date"
        resp = requests.get(url, headers=HEADERS, timeout=12)
        resp.encoding = "utf-8"
        root = ET.fromstring(resp.content)

        for item in root.findall(".//item"):
            titulo  = item.findtext("title", "N/A")
            empresa = item.findtext("source", "N/A")
            local_v = item.findtext("{http://www.indeed.com/about/jobs}city", "") or local.replace("+", " ")
            link    = item.findtext("link", "")
            data    = item.findtext("pubDate", "")

            if titulo != "N/A":
                vagas.append({
                    "Cargo":   titulo,
                    "Empresa": empresa,
                    "Local":   local_v or "Brasil",
                    "Link":    link,
                    "Busca":   termo,
                    "Data":    datetime.now().strftime("%d/%m/%Y"),
                })
    except Exception as e:
        print(f"  [!] Erro em '{termo}' / '{local}': {e}")
    return vagas


def main():
    print("=" * 50)
    print("  Buscando vagas — Indeed Brasil")
    print("=" * 50)

    todas = []

    for termo in TERMOS:
        for local in LOCAIS:
            label = local.replace("+", " ") or "Brasil/Remoto"
            print(f"  '{termo}' em '{label}'...")
            vagas = buscar_indeed_rss(termo, local)
            print(f"  → {len(vagas)} vagas")
            todas.extend(vagas)
            time.sleep(1)

    # remove duplicatas pelo link
    vistos = set()
    unicas = []
    for v in todas:
        if v["Link"] and v["Link"] not in vistos:
            vistos.add(v["Link"])
            unicas.append(v)

    if not unicas:
        print("\n  Nenhuma vaga encontrada.")
        return

    df = pd.DataFrame(unicas)
    df.to_csv(SALVAR_EM, index=False, encoding="utf-8-sig")

    print("\n" + "=" * 50)
    print(f"  {len(unicas)} vagas salvas em '{SALVAR_EM}'")
    print("  Abra no Excel ou Google Sheets!")
    print("=" * 50)


if __name__ == "__main__":
    main()