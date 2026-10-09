import ccxt
import pandas as pd
import pandas_ta as ta
import time
import os

# --- CONFIGURAÇÕES DE API (Opcional para leitura pública) ---
exchange = ccxt.binance({
    'enableRateLimit': True,
})

SYMBOL = 'BTC/USDT'
TIMEFRAME_GAILHO = '1m'
TIMEFRAME_TENDENCIA = '15m'

def buscar_dados(symbol, timeframe, limit=200):
    bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    return df

def calcular_indicadores(df):
    # EMAs do seu Setup
    df['ema9'] = ta.ema(df['close'], length=9)
    df['ema20'] = ta.ema(df['close'], length=20)
    df['ema200'] = ta.ema(df['close'], length=200)
    
    # MACD
    macd = ta.macd(df['close'])
    df = pd.concat([df, macd], axis=1)
    
    # Volume Médio
    df['vol_avg'] = ta.sma(df['volume'], length=20)
    return df

def calcular_delta(symbol):
    # Simulação de leitura de fluxo (Trades recentes)
    trades = exchange.fetch_trades(symbol, limit=1000)
    df_t = pd.DataFrame(trades)
    buys = df_t[df_t['side'] == 'buy']['amount'].sum()
    sells = df_t[df_t['side'] == 'sell']['amount'].sum()
    delta = buys - sells
    return delta

def monitor_de_sinal():
    print(f"Iniciando Monitoramento de {SYMBOL}...")
    
    while True:
        try:
            # 1. Obter Dados
            df_1m = buscar_dados(SYMBOL, '1m')
            df_15m = buscar_dados(SYMBOL, '15m')
            
            # 2. Calcular Indicadores
            df_1m = calcular_indicadores(df_1m)
            df_15m = calcular_indicadores(df_15m)
            
            # 3. Obter Delta e Preço Atual
            delta = calcular_delta(SYMBOL)
            preco = df_1m['close'].iloc[-1]
            
            # --- LÓGICA DO CÉREBRO (CONFLUÊNCIA) ---
            # Tendência Principal
            tendencia_alta = preco > df_15m['ema200'].iloc[-1]
            
            # Gatilho de Delta vs Preço (Divergência)
            # Se delta é muito positivo mas o candle de 1m é neutro/queda = ABSORÇÃO
            absorcao_venda = (delta > 0) and (df_1m['close'].iloc[-1] <= df_1m['open'].iloc[-1])
            absorcao_compra = (delta < 0) and (df_1m['close'].iloc[-1] >= df_1m['open'].iloc[-1])

            # --- EMISSÃO DO VEREDICTO ---
            os.system('cls' if os.name == 'nt' else 'clear')
            
            if tendencia_alta and not absorcao_venda and delta > 0:
                print("\033[1;32mCOMPRA\033[0m") # Verde em negrito
            elif not tendencia_alta and not absorcao_compra and delta < 0:
                print("\033[1;31mVENDA\033[0m")  # Vermelho em negrito
            else:
                print("\033[1;34mNEUTRO\033[0m") # Azul em negrito

            print("-" * 30)
            print(f"Preço: {preco} | Delta: {delta:.4f}")
            print(f"EMAs: 9({df_1m['ema9'].iloc[-1]:.2f}) | 20({df_1m['ema20'].iloc[-1]:.2f})")
            print(f"MACD Hist: {df_1m.iloc[-1, -1]:.4f}")
            print(f"Volume vs Média: {df_1m['volume'].iloc[-1]:.2f} / {df_1m['vol_avg'].iloc[-1]:.2f}")
            print("-" * 30)
            print("Aguardando próxima leitura de fluxo...")
            
            time.sleep(10) # Atualiza a cada 10 segundos para evitar ban de IP

        except Exception as e:
            print(f"Erro na conexão: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor_de_sinal()