import ccxt
import pandas as pd
import time
import os

# CONFIGURAÇÕES
exchange = ccxt.binance({'options': {'defaultType': 'future'}})
symbol = 'BTC/USDT'
TEMPOS_GRAFICOS = ['15m', '1h', '4h']

def identificar_sinais_nativos(tf):
    try:
        bars = exchange.fetch_ohlcv(symbol, timeframe=tf, limit=100)
        df = pd.DataFrame(bars, columns=['ts', 'open', 'high', 'low', 'close', 'vol'])
        
        c1 = df.iloc[-1] # Candle atual
        c2 = df.iloc[-2] # Candle anterior
        
        # Variáveis de cálculo de preço
        corpo_c1 = abs(c1['close'] - c1['open'])
        pavio_inf_c1 = min(c1['open'], c1['close']) - c1['low']
        pavio_sup_c1 = c1['high'] - max(c1['open'], c1['close'])
        
        # Variáveis de volume
        volume_atual = c1['vol']
        volume_medio = df['vol'].tail(20).mean()
        
        veredicto = "NEUTRO"
        cor = "\033[1;34m" # Azul
        mensagem = "Monitorando estrutura..."

        # --- LÓGICA DE PADRÕES DE CANDLE (VERDE/VERMELHO) ---
        
        # 1. ENGOLFO DE ALTA (Com Volume de Confirmação)
        if c1['close'] > c2['open'] and c1['open'] < c2['close'] and c1['close'] > c1['open'] and volume_atual > volume_medio:
            return "COMPRA", "ENGOLFO DE ALTA (Força + Volume)", "\033[1;32m"
        
        # 2. ENGOLFO DE BAIXA (Com Volume de Confirmação)
        if c1['close'] < c2['open'] and c1['open'] > c2['close'] and c1['close'] < c1['open'] and volume_atual > volume_medio:
            return "VENDA", "ENGOLFO DE BAIXA (Pressão + Volume)", "\033[1;31m"

        # 3. MARTELO (Rejeição de Fundo)
        if pavio_inf_c1 > (2 * corpo_c1) and pavio_sup_c1 < corpo_c1 and corpo_c1 > 0:
            return "COMPRA", "MARTELO (Captação de Liquidez)", "\033[1;32m"

        # 4. ESTRELA CADENTE (Rejeição de Topo)
        if pavio_sup_c1 > (2 * corpo_c1) and pavio_inf_c1 < corpo_c1 and corpo_c1 > 0:
            return "VENDA", "ESTRELA CADENTE (Rejeição de Oferta)", "\033[1;31m"

        # --- LÓGICA DE FIGURAS COM FILTRO DE VOLUME (AZUL) ---
        corpo_medio = abs(df['close'] - df['open']).tail(20).mean()
        
        # Critério: Preço parado (corpo pequeno) E Volume caindo (abaixo da média)
        if corpo_c1 < (corpo_medio * 0.6) and volume_atual < (volume_medio * 0.8):
            veredicto = "NEUTRO"
            cor = "\033[1;34m"
            mensagem = "POSSÍVEL BANDEIRA/CUNHA (Baixo Volume/Acumulação)"

        return veredicto, mensagem, cor

    except Exception as e:
        return "ERRO", str(e), "\033[1;31m"

def monitor_sinais():
    while True:
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"=== ANALISTA DE SINAIS MTF PRO - {time.strftime('%H:%M:%S')} ===")
            print(f"Símbolo: {symbol} | Filtro: Volume + Geometria")
            print("-" * 50)
            for tf in TEMPOS_GRAFICOS:
                verd, msg, cor = identificar_sinais_nativos(tf)
                print(f"{cor}[{tf.upper()}] VEREDICTO: {verd}\033[0m")
                print(f" -> {msg}\n")
            print("-" * 50)
            time.sleep(60)
        except Exception as e:
            print(f"Erro no ciclo: {e}")
            time.sleep(10)

if __name__ == "__main__":
    monitor_sinais()