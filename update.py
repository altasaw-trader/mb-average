import json, time, datetime as dt
from pathlib import Path
import yfinance as yf

PAIRS = ['AUDCAD','AUDCHF','AUDJPY','AUDNZD','AUDUSD','CADCHF','CADJPY','CHFJPY','EURAUD','EURCAD','EURCHF','EURGBP','EURJPY','EURNZD','EURUSD','GBPAUD','GBPCAD','GBPCHF','GBPJPY','GBPNZD','GBPUSD','NZDCAD','NZDCHF','NZDJPY','NZDUSD','USDCAD','USDCHF','USDJPY']
OUT = Path(__file__).resolve().parent / 'data.json'
previous = {}
if OUT.exists():
    try: previous = json.loads(OUT.read_text(encoding='utf8')).get('pairs', {})
    except Exception: pass

results = {}
for pair in PAIRS:
    try:
        ticker = yf.Ticker(pair+'=X')
        df = ticker.history(period='3y', interval='1d', auto_adjust=False)
        if df.empty: raise ValueError('No daily prices')
        today = dt.datetime.now(dt.timezone.utc).date()
        entries=[]
        for date,row in df.iterrows():
            day = date.date()
            # Exclude today's possibly unfinished daily candle (UTC conservative).
            if day >= today: continue
            hi,lo=float(row['High']),float(row['Low'])
            if hi<=0 or lo<=0 or hi<lo: continue
            point = 0.001 if pair.endswith('JPY') else 0.00001
            entries.append({'date':day.isoformat(),'high':round(hi,5),'low':round(lo,5),'points':round((hi-lo)/point)})
        top=sorted(entries,key=lambda x:x['points'],reverse=True)[:5]
        if len(top)<5: raise ValueError('Fewer than 5 closed D1 candles')
        avg=sum(x['points'] for x in top)/5
        results[pair]={'average':round(avg,1),'suggested':round(avg/2,1),'top5':top,'count':len(entries),'status':'ok'}
        print(pair, round(avg,1))
    except Exception as e:
        print(pair, 'ERROR',str(e))
        if pair in previous:
            results[pair]={**previous[pair],'status':'stale'}
        else:
            results[pair]={'status':'unavailable','error':'Market data unavailable'}
    time.sleep(0.5)

payload={'updated_utc':dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),'source':'Yahoo Finance via yfinance (unofficial)','basis':'3y rolling daily, completed candles, 0.00001 non-JPY / 0.001 JPY point','pairs':results}
OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf8')
