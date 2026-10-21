"""Gera modelo real, de forma determinística, sem depender de arquivos externos."""
from pathlib import Path
import json
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split

BASE = Path(__file__).resolve().parent
FEATURES = ['idade', 'meses_cliente', 'chamados_suporte', 'dias_sem_login', 'valor_mensal']

def treinar():
    rng = np.random.default_rng(2026)
    n = 900
    X = np.column_stack([
        rng.integers(18, 80, n),
        rng.integers(1, 100, n),
        rng.poisson(2.0, n),
        rng.integers(0, 70, n),
        rng.uniform(25, 450, n),
    ]).astype(float)
    logit = -3.0 + .07*X[:, 3] + .32*X[:, 2] - .019*X[:, 1] + .0015*X[:, 4]
    prob = 1/(1+np.exp(-logit))
    y = (rng.random(n) < prob).astype(int)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.25, random_state=2026, stratify=y)
    modelo = RandomForestClassifier(n_estimators=70, max_depth=8, min_samples_leaf=3, random_state=2026, n_jobs=1)
    modelo.fit(Xtr, ytr)
    out = BASE/'modelos'; out.mkdir(exist_ok=True)
    joblib.dump({'model': modelo, 'features': FEATURES}, out/'churn.joblib')
    metricas = {'accuracy':round(float(accuracy_score(yte,modelo.predict(Xte))),4),'f1':round(float(f1_score(yte,modelo.predict(Xte))),4),'samples':n,'features':FEATURES}
    (out/'metricas.json').write_text(json.dumps(metricas,indent=2,ensure_ascii=False),encoding='utf-8')
    print('Modelo salvo em modelos/churn.joblib')
    print('Accuracy:',metricas['accuracy'],'| F1:',metricas['f1'])
    print('Próxima etapa: python -m uvicorn api:app --reload')
    return metricas

if __name__=='__main__': treinar()
