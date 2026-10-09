import subprocess
import time
import sys
import os

def iniciar_ecossistema():
    # Detecta automaticamente o caminho do Python que você está usando agora no VS Code
    python_exe = sys.executable

    scripts = [
        {"arquivo": "robo.py", "nome": "GATILHO (1M) - Fluxo e Médias"},
        {"arquivo": "radar.py", "nome": "RADAR (5M) - Liquidez e SMC"},
        {"arquivo": "sinais.py", "nome": "SINAIS (MTF) - Padrões e Estrutura"}
    ]

    print("="*50)
    print("INICIALIZANDO ECOSSISTEMA COM CAMINHO ABSOLUTO")
    print(f"Usando Python: {python_exe}")
    print("="*50)

    for script in scripts:
        arquivo = script["arquivo"]
        titulo = script["nome"]
        
        print(f"[*] Abrindo {titulo}...")
        
        # Comando forçando o uso do executável do Python correto
        comando = f'start "{titulo}" "{python_exe}" {arquivo}'
        
        try:
            subprocess.Popen(comando, shell=True)
            time.sleep(2)
        except Exception as e:
            print(f"[ERRO] Falha ao abrir {arquivo}: {e}")

if __name__ == "__main__":
    iniciar_ecossistema()