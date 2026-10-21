"""Gera cenário normal ou incidente observável, sem Bash/curl."""
import argparse,random,time
import httpx
p=argparse.ArgumentParser();p.add_argument('--total',type=int,default=80);p.add_argument('--cenario',choices=['normal','incidente'],default='normal');p.add_argument('--pausa',type=float,default=.02)
a=p.parse_args(); rng=random.Random(12)
counts={200:0,503:0,'outro':0}
with httpx.Client(timeout=8) as c:
 for i in range(a.total):
    pld={'idade':rng.randrange(19,75),'meses_cliente':rng.randrange(1,96),'chamados_suporte':rng.randrange(0,8), 'dias_sem_login':rng.randrange(0,65),'valor_mensal':round(rng.uniform(40,400),2)}
    if a.cenario=='incidente':
        pld['simular_lentidao']=(i%3)!=0
        pld['simular_erro']=(i%10)==0
    try: status=c.post('http://127.0.0.1:8000/predict',json=pld).status_code
    except Exception as exc:
        print('Falha de conexão:',exc,'\nInicie o servidor no Terminal 1 com: python -m uvicorn api:app --reload');raise SystemExit(2)
    key=status if status in (200,503) else 'outro';counts[key]+=1
    if (i+1)%20==0:print(f'{i+1}/{a.total} requisições realizadas; HTTP 200={counts[200]}; HTTP 503={counts[503]}')
    time.sleep(max(0,a.pausa))
print('CENARIO',a.cenario,'RESULTADO',counts)
