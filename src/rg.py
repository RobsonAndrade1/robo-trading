import ccxt
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import time
import os
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

# --- CONFIGURAÇÕES ---
exchange = ccxt.binance({'options': {'defaultType': 'future'}, 'enableRateLimit': True})
SYMBOL = 'BTC/USDT'
TF_GATILHO = '1m'
TF_ESTRUTURA = '5m'
PAREDE_INSTITUCIONAL = 100 

# Cores
VERDE, VERMELHO, AZUL = "\033[1;32m", "\033[1;31m", "\033[1;34m"
ROXO, AMARELO, LARANJA, RESET = "\033[1;35m", "\033[1;33m", "\033[38;5;208m", "\033[0m"

class SuperRoboRG:
    def __init__(self):
        self.historico_oi = []
        self.cvd_acumulado = 0
        self.tendencia_smc = "NEUTRA"
        self.last_dxy = self.last_spy = None
        self.ciclo_liq = 0 

    def buscar_dados(self, tf, limit=150):
        try:
            bars = exchange.fetch_ohlcv(SYMBOL, timeframe=tf, limit=limit)
            df = pd.DataFrame(bars, columns=['ts', 'open', 'high', 'low', 'close', 'vol'])
            df['ema9'] = ta.ema(df['close'], length=9)
            df['ema20'] = ta.ema(df['close'], length=20)
            df['ema200'] = ta.ema(df['close'], length=200)
            return df.ffill().infer_objects(copy=False)
        except: return None

    def calcular_cvd(self):
        try:
            trades = exchange.fetch_trades(SYMBOL, limit=1000)
            df_t = pd.DataFrame(trades)
            delta_atual = df_t[df_t['side'] == 'buy']['amount'].sum() - df_t[df_t['side'] == 'sell']['amount'].sum()
            self.cvd_acumulado += delta_atual
            return delta_atual, self.cvd_acumulado
        except: return 0, self.cvd_acumulado

    def obter_macro_aceleracao(self):
        try:
            data = yf.download("DX-Y.NYB SPY", period="1d", interval="1m", progress=False)
            curr_dxy, curr_spy = data['Close']['DX-Y.NYB'].iloc[-1], data['Close']['SPY'].iloc[-1]
            dxy_a = (curr_dxy / self.last_dxy) - 1 if self.last_dxy else 0
            spy_a = (curr_spy / self.last_spy) - 1 if self.last_spy else 0
            self.last_dxy, self.last_spy = curr_dxy, curr_spy
            d_st = f"{VERDE}QUEDA{RESET}" if dxy_a <= 0 else f"{VERMELHO}ALTA ↑{RESET}"
            s_st = f"{VERDE}ALTA{RESET}" if spy_a >= 0 else f"{VERMELHO}QUEDA ↓{RESET}"
            m_score = (2 if dxy_a < 0 else -2) + (1 if spy_a > 0 else -1)
            return d_st, s_st, m_score, dxy_a, spy_a
        except: return "---", "---", 0, 0, 0

    def monitorar(self):
        while True:
            res, detalhe, sl_val, msg_liq = f"{AZUL}PROCESSANDO...{RESET}", "COLETANDO DADOS", "N/A", "MAPEANDO..."
            try:
                df_1m, df_5m = self.buscar_dados(TF_GATILHO), self.buscar_dados(TF_ESTRUTURA)
                oi_data = exchange.fetch_open_interest(SYMBOL)
                book = exchange.fetch_order_book(SYMBOL, limit=50)
                delta_inst, cvd_total = self.calcular_cvd()
                
                if df_1m is not None and df_5m is not None:
                    preco = df_1m['close'].iloc[-1]
                    topo_5m, fundo_5m = df_5m['high'].iloc[-2], df_5m['low'].iloc[-2]
                    oi_atual = oi_data['openInterestAmount']
                    d_st, s_st, m_sc, d_a, s_a = self.obter_macro_aceleracao()

                    # --- CARROSSEL DE LIQUIDEZ ---
                    if self.ciclo_liq == 0:
                        msg_liq = f"{AZUL}VOLUME PROFILE (POC): {df_5m.sort_values(by='vol', ascending=False).iloc[0]['close']}{RESET}"
                    elif self.ciclo_liq == 1:
                        asks = pd.DataFrame(book['asks'], columns=['price', 'amount'])
                        b_v = asks[asks['amount'] > PAREDE_INSTITUCIONAL]
                        msg_liq = f"{AMARELO}ALERTA: PAREDE DE VENDA em {b_v.iloc[0]['price']}{RESET}" if not b_v.empty else f"{AZUL}BOOK: Sem Paredes{RESET}"
                    else:
                        msg_liq = f"{AZUL}ZONA DE LIQUIDAÇÃO: Equal Highs detectado acima de {df_5m['high'].iloc[-3]}{RESET}" if df_5m['high'].iloc[-3] == df_5m['high'].iloc[-4] else f"{AZUL}STOPS: Mapeando...{RESET}"
                    self.ciclo_liq = (self.ciclo_liq + 1) % 3

                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(f"============================================================")
                    print(f"      SISTEMA RG ULTRA 10.5 (CVD INTEGRADO) - {time.strftime('%H:%M:%S')}")
                    print(f"============================================================")
                    print(f"MACRO: DXY: {d_st} ({d_a*100:+.4f}%) | SPX: {s_st}")
                    print(f"FLUXO: Delta: {delta_inst:+.2f} | CVD: {cvd_total:+.2f}")
                    print(f"EMAs: 9: {df_1m['ema9'].iloc[-1]:.2f} | 20: {df_1m['ema20'].iloc[-1]:.2f}")
                    print(f"------------------------------------------------------------")
                    print(f"LIQUIDEZ ATUAL: {msg_liq}")
                    print(f"------------------------------------------------------------")

                    # Radar SMC
                    alertas = []
                    if preco > topo_5m: 
                        alertas.append(f"{VERDE}ESTRUTURA CONFIRMADA: BOS DE ALTA em {topo_5m}{RESET}")
                        self.tendencia_smc = "ALTA"
                    elif preco < fundo_5m: 
                        alertas.append(f"{VERMELHO}ALERTA DE REVERSÃO: CHoCH DETECTADO em {fundo_5m}{RESET}")
                        self.tendencia_smc = "BAIXA"

                    if len(self.historico_oi) > 1 and oi_atual < self.historico_oi[0] * 0.998:
                        alertas.append(f"{ROXO}ALERTA: EXAUSTÃO DETECTADA{RESET}")

                    if not alertas: print(f"{AZUL}RADAR: Mapeando...{RESET}")
                    else: 
                        for a in alertas: print(a)
                    print(f"------------------------------------------------------------")

                    # --- LÓGICA DE SCORE COM PESO DE CVD ---
                    ratio = sum([b[1] for b in book['bids'][:10]]) / sum([a[1] for a in book['asks'][:10]])
                    score = 5 + m_sc
                    score += 2 if preco > df_1m['ema20'].iloc[-1] else -1
                    score += 1 if delta_inst > 0 else -1 # Voto de Delta Instantâneo
                    score += 1 if ratio > 1.5 else 0

                    if score >= 6:
                        # TRAVA DE SEGURANÇA CVD: Impede compra se CVD estiver caindo (Absorção)
                        if ratio > 1 and delta_inst < 0:
                            res, sl_val, detalhe = f"{AZUL}NEUTRO (ABSORÇÃO VENDEDORA){RESET}", "N/A", "Delta negativo impede compra"
                        else:
                            res = f"{VERDE}COMPRA ({score}/10){RESET}" if ratio > 1 else f"{VERMELHO}VENDA ({score}/10){RESET}"
                            sl_val = fundo_5m if ratio > 1 else topo_5m
                            detalhe = f"{ratio:.1f}x PRESSÃO / Delta: {delta_inst:.1f}"
                    else:
                        res, sl_val, detalhe = f"{AZUL}NEUTRO (SCORE BAIXO){RESET}", "N/A", "Aguardando confluência"

                    print(f"VEREDICTO: {res}")
                    print(f"DETALHE: {detalhe}")
                    print(f"PREÇO: {preco:.2f} | STOP(5M): {sl_val}")
                    print(f"============================================================")

                    self.historico_oi.append(oi_atual)
                    if len(self.historico_oi) > 6: self.historico_oi.pop(0)

                time.sleep(10)
            except: time.sleep(5)

if __name__ == "__main__":
    SuperRoboRG().monitorar()