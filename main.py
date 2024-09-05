import yfinance as yf
import talib as ta
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots


'''
ATTENZIONE! SE DOVESSI AVERE UN ERRORE DEL TIPO 'numpy.dtype size changed, may indicate binary incompatibility. Expected 96 from C header, got 88 from PyObject'

ALLORA ESEGUI: pip3 install "numpy<2.0.0" --force-reinstall
'''

# Mettilo sul browser
pio.renderers.default = 'browser'

# Provo con AAPL, Apple

ticker = 'AAPL'
start_date = '2015-01-01'
end_date = '2024-09-06'


# Scarico i dati

df = yf.download(ticker, start_date)

# Indicatore SMA (simple moving average) degli ultimi 20 giorni.
# Ovviamente i primi 20 giorni avranno SMA come Not a Number (NaN)

df['SMA'] = ta.SMA(df['Close'], timeperiod=20) # Prendo il prezzo di chiusura.

df['EMA15'] = ta.EMA(df['Close'],timeperiod=15)
# Indicatore RSI (relative strength index), indicatore di momentum: una soglia al 70esimo o 30esimo percentile: in teoria sopra il 70 vendi e sotto il 30 compra

df['RSI'] = ta.RSI(df['Close'], timeperiod=14) # 14 giorni

# Indicatore Ballinger B (VOLATILITÀ): 3 valori (upper lower e middle, il middle sarà la SMA di 20 giorni, upper e lower sono delle deviazioni standard)

df['Upper_BB'], df['Middle_BB'], df['Lower_BB'] = ta.BBANDS(df['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
# matype=0 significa simple moving average, 1 sarebbe la exponential
# nbdevup e nbdevdn sono le deviazioni standard sopra e sotto

# Abbiamo i dati, ora dobbiamo fare la *VISUALIZZAZIONE*, servono dei PLOT

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, # Condividiamo gli assi delle x, il tempo tra candele e RSI
                    vertical_spacing=0.2,
                    row_heights=[0.7,0.3],
                    subplot_titles=[f'Prezzo e Indicatori di {ticker}', 'Indicatore RSI'])

# Ora facciamo le candele

candlestick = go.Candlestick(
    x=df.index,
    open=df.Open,
    high=df.High,
    low=df.Low,
    close=df.Close,
    name='Prezzo'
)

sma_line = go.Scatter(
    x=df.index,
    y=df.SMA,
    line={'color': 'blue', 'width':2},
    name='SMA'
)

ema_line = go.Scatter(
    x=df.index,
    y=df.EMA15,
    line={'color': 'cyan', 'width':2},
    name='EMA'
)

upper_bb=go.Scatter(
    x=df.index,
    y=df['Upper_BB'],
    line={'color':'red','width':1},
    name='Upper BB'
)

lower_bb=go.Scatter(
    x=df.index,
    y=df['Lower_BB'],
    line={'color':'red','width':1},
    name='Lower BB'
)

middle_bb=go.Scatter(
    x=df.index,
    y=df['Middle_BB'],
    line={'color':'green','width':1},
    name='Middle BB'
)

fig.add_trace(candlestick,row=1, col=1)
fig.add_trace(sma_line,row=1, col=1)
fig.add_trace(ema_line,row=1, col=1)
fig.add_trace(upper_bb,row=1, col=1)
fig.add_trace(lower_bb,row=1, col=1)
fig.add_trace(middle_bb,row=1, col=1)



rsi = go.Scatter(
    x=df.index,
    y=df.RSI,
    line={'color':'purple','width':2},
    name='RSI'
)

fig.add_trace(rsi,row=2,col=1)

mark30 = go.layout.Shape(
    type='line',
    x0=df.index[0],
    y0=30,
    x1=df.index[-1],
    y1=30,
    line={'color': 'gray', 'width':1,'dash':'dash'}
)

mark70 = go.layout.Shape(
    type='line',
    x0=df.index[0],
    y0=70,
    x1=df.index[-1],
    y1=70,
    line={'color': 'gray', 'width':1,'dash':'dash'}
)

fig.add_shape(mark30,row=2,col=1)
fig.add_shape(mark70,row=2,col=1)

fig.update_layout(
    title=f'Analisi Tecnica {ticker} - fatto da Balass1',
    yaxis_title='Prezzo',
    xaxis_title='Data',
    xaxis_rangeslider_visible=False,
    height=800,
    template='plotly_dark'
)

fig.update_yaxes(range=[0,100],row=2,col=1) # Per far sì che RSI vada da 0 a 100

fig.show()


print(df)
