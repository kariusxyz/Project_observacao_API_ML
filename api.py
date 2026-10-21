"""FastAPI + instrumentação real prometheus_client; dashboard local didático."""
from __future__ import annotations
from contextlib import asynccontextmanager
from collections import deque
from pathlib import Path
from threading import Lock
from time import perf_counter, time, sleep
import math
import joblib
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST

HERE = Path(__file__).resolve().parent
PREDICOES = Counter('predicoes_total', 'Total de tentativas de inferencia', ['resultado'])
LATENCIA = Histogram('latencia_inferencia_segundos', 'Duracao das tentativas de inferencia', buckets=(.005,.01,.025,.05,.1,.2,.3,.5,1,2))
EM_ANDAMENTO = Gauge('predicoes_em_andamento', 'Inferencias em andamento')
MODELO_CARREGADO = Gauge('modelo_carregado', '1 se modelo carregado, 0 caso contrario')
HIST = deque(maxlen=4000)
LOCK = Lock()

@asynccontextmanager
async def lifespan(app: FastAPI):
    caminho = HERE/'modelos'/'churn.joblib'
    if not caminho.exists():
        MODELO_CARREGADO.set(0)
        raise RuntimeError('Modelo ausente. Execute: python 01_treinar_modelo.py')
    pacote = joblib.load(caminho)
    app.state.modelo = pacote['model']
    app.state.features = pacote['features']
    MODELO_CARREGADO.set(1)
    try:
        yield
    finally:
        MODELO_CARREGADO.set(0)

app = FastAPI(title='MLOps Semana 12 · API Observável', version='1.0.0', lifespan=lifespan)

class Entrada(BaseModel):
    idade: int = Field(ge=18, le=110)
    meses_cliente: int = Field(ge=0, le=500)
    chamados_suporte: int = Field(ge=0, le=100)
    dias_sem_login: int = Field(ge=0, le=365)
    valor_mensal: float = Field(ge=0, le=10000)
    simular_lentidao: bool = False
    simular_erro: bool = False

@app.get('/health')
def health():
    return {'status':'ok','modelo_carregado':True, 'observacao':'health verifica disponibilidade, nao qualidade estatistica'}

@app.post('/predict')
def predict(dados: Entrada):
    inicio = perf_counter()
    EM_ANDAMENTO.inc()
    status = 'erro'
    try:
        if dados.simular_lentidao:
            sleep(.28)
        if dados.simular_erro:
            raise HTTPException(status_code=503, detail='Erro didatico simulado para visualizar o Counter')
        valores = [[float(getattr(dados,col)) for col in app.state.features]]
        pred = int(app.state.modelo.predict(valores)[0])
        proba = float(app.state.modelo.predict_proba(valores)[0][1])
        status = 'sucesso'
        return {'prediction':pred,'probabilidade_churn':round(proba,4),'risco':('alto' if proba>=.5 else 'baixo')}
    finally:
        duracao = perf_counter()-inicio
        LATENCIA.observe(duracao)
        PREDICOES.labels(resultado=status).inc()
        EM_ANDAMENTO.dec()
        with LOCK:
            HIST.append((time(),duracao,status))

@app.get('/metrics')
def metrics():
    return Response(content=generate_latest(),media_type=CONTENT_TYPE_LATEST)

def snapshot():
    agora=time()
    with LOCK:
        total=len(HIST)
        janela=[(t,d,s) for t,d,s in HIST if t>=agora-60]
    erros=sum(s=='erro' for _,_,s in janela)
    durs=sorted(d*1000 for _,d,_ in janela)
    p95=durs[max(0,math.ceil(.95*len(durs))-1)] if durs else 0
    p50=durs[max(0,math.ceil(.5*len(durs))-1)] if durs else 0
    ultimas=[round(x,1) for x in durs[-40:]]
    return {'total_processado':total,'total_ultimos_60s':len(janela),'rps':round(len(janela)/60,3),
            'erros_60s':erros,'taxa_erro_pct':round(100*erros/len(janela),1) if janela else 0,
            'p50_ms':round(p50,1),'p95_ms':round(p95,1),'alerta_p95':len(janela)>=10 and p95>200,
            'amostras_ms':ultimas,'modelo_carregado':1}

@app.get('/api/snapshot')
def api_snapshot(): return snapshot()

@app.get('/painel', response_class=HTMLResponse)
def painel():
    """Dashboard local de aprendizado. Não substitui Prometheus/Grafana."""
    return (HERE/'painel_local.html').read_text(encoding='utf-8')
