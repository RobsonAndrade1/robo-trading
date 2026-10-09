import ccxt
import pandas as pd
import time
import os

# CONFIGURAÇÕES
exchange = ccxt.binance({'options': {'defaultType': 'future'}})
symbol = 'BTC/USDT'
TF_ESTRUTURA = '5m' # Tempo gráfico para SMC
PAREDE_INSTITUCIONAL = 100 

historico_oi = []

def buscar_dados_smc():
    # Busca candles de 5min para encontrar Topos e Fundos
    bars = exchange.fetch_ohlcv(symbol, timeframe=TF_ESTRUTURA, limit=50)
    df = pd.DataFrame(bars, columns=['ts', 'open', 'high', 'low', 'close', 'vol'])
    topo_anterior = df['high'].iloc[-2] # Último topo fixado
    fundo_anterior = df['low'].iloc[-2] # Último fundo fixado
    return topo_anterior, fundo_anterior, df['close'].iloc[-1]

def buscar_contexto():
    global historico_oi
    oi_data = exchange.fetch_open_interest(symbol)
    oi_atual = oi_data['openInterestAmount']
    
    historico_oi.append(oi_atual)
    if len(historico_oi) > 6:
        historico_oi.pop(0)
    
    book = exchange.fetch_order_book(symbol, limit=20)
    asks = pd.DataFrame(book['asks'], columns=['price', 'amount'])
    bids = pd.DataFrame(book['bids'], columns=['price', 'amount'])
    
    p_venda = asks[asks['amount'] > PAREDE_INSTITUCIONAL]
    p_compra = bids[bids['amount'] > PAREDE_INSTITUCIONAL]
    
    return oi_atual, p_venda, p_compra

def monitor_radar():
    print(f"Iniciando Robô Radar SMC (5M) para {symbol}...")
    tendencia_atual = "ALTA" # Estado inicial para rastrear CHoCH

    while True:
        try:
            oi, p_venda, p_compra = buscar_contexto()
            topo, fundo, preco_atual = buscar_dados_smc()
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # --- LÓGICA DE VEREDICTO SMC ---
            if preco_atual > topo:
                # BOS de Alta (Verde)
                print("\033[1;32mESTRUTURA CONFIRMADA: BOS DE ALTA\033[0m")
                print(f"Smart Money impulsionando acima de {topo}")
                tendencia_atual = "ALTA"
            
            elif preco_atual < fundo:
                # CHoCH de Baixa (Vermelho)
                print("\033[1;31mALERTA DE REVERSÃO: CHoCH DETECTADO\033[0m")
                print(f"Preço quebrou fundo de 5M em {fundo}!")
                tendencia_atual = "BAIXA"

            # --- LÓGICA DE EXAUSTÃO E PAREDES ---
            elif len(historico_oi) > 1 and oi < historico_oi[0] * 0.998:
                print("\033[1;35mEXAUSTÃO DETECTADA\033[0m")
                print("OI caindo: Smart Money realizando lucros.")
            
            elif not p_venda.empty:
                print("\033[1;33mALERTA: PAREDE DE VENDA\033[0m")
                print(f"Resistência institucional em: {p_venda.iloc[0]['price']}")
                
            elif not p_compra.empty:
                print("\033[38;5;208mALERTA: PAREDE DE COMPRA\033[0m")
                print(f"Suporte institucional em: {p_compra.iloc[0]['price']}")

            else:
                print("\033[1;32mFAVORÁVEL\033[0m")
                print(f"Tendência Macro (5M): {tendencia_atual}")

            print("-" * 40)
            print(f"Preço: {preco_atual:.2f} | OI: {oi:.2f}")
            print(f"Topo 5M: {topo} | Fundo 5M: {fundo}")
            print(f"Horário: {time.strftime('%H:%M:%S')}")
            print("-" * 40)
            
            time.sleep(10)
            
        except Exception as e:
            print(f"Erro no Radar: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor_radar()