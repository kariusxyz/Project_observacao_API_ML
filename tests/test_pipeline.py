from pathlib import Path
import importlib.util,json,subprocess,sys
from fastapi.testclient import TestClient

BASE = Path(__file__).resolve().parents[1]

def ensure_model():
    subprocess.run([sys.executable,'01_treinar_modelo.py'],cwd=BASE,check=True,capture_output=True)

def test_train_produces_model_and_metadata():
    ensure_model()
    assert (BASE/'modelos/churn.joblib').exists()
    assert json.loads((BASE/'modelos/metricas.json').read_text())['accuracy']>.5

def test_api_predict_metrics_error_and_panel():
    ensure_model()
    from api import app
    with TestClient(app) as c:
        assert c.get('/health').status_code==200
        body={'idade':34,'meses_cliente':18,'chamados_suporte':3,'dias_sem_login':25,'valor_mensal':119.0}
        ok=c.post('/predict',json=body)
        assert ok.status_code==200 and 0 <=ok.json()['probabilidade_churn']<=1
        assert c.post('/predict',json={'idade':12}).status_code==422
        assert c.post('/predict',json={**body,'simular_erro':True}).status_code==503
        metrics=c.get('/metrics').text
        for name in ('predicoes_total','latencia_inferencia_segundos_bucket','modelo_carregado','predicoes_em_andamento'):assert name in metrics
        assert 'painel' in c.get('/painel').text.lower()
        snap=c.get('/api/snapshot').json()
        assert snap['total_processado']>=2
        assert snap['erros_60s'] if 'erros_60s' in snap else snap['taxa_erro_pct']>0

def test_config_files():
    import yaml
    conf=yaml.safe_load((BASE/'docker-compose.yml').read_text())
    assert all(name in conf['services'] for name in ['modelo','grafana','prometheus'])
    prom=yaml.safe_load((BASE/'prometheus/prometheus.yml').read_text())
    assert prom['scrape_configs'][0]['static_configs'][0]['targets']==['modelo:8000']
    alerts=yaml.safe_load((BASE/'prometheus/alerts.yml').read_text())
    assert 'sum by (le)' in alerts['groups'][0]['rules'][0]['expr']
    graf=json.loads((BASE/'grafana/dashboards/mlops_semana12.json').read_text())
    assert len(graf['panels'])==4
