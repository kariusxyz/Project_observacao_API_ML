# Semana 12 — MLOps | Observabilidade de uma API de inferência

O kit inclui uma API FastAPI com modelo de ML REAL treinado localmente, métricas Prometheus, tráfego normal/incidente e um painel didático local. **Docker NÃO é obrigatório**. Se estiver disponível, há uma extensão com Prometheus e Grafana reais, dashboard provisionado e regras de alerta.

## Caminho principal — VS Code + PowerShell (sem Docker)

1. Extraia o ZIP, abra a pasta `mlops_semana12_kit` no VS Code e abra `Terminal > Novo Terminal`.
2. Terminal 1, um comando por linha:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python 00_preflight.py
python 01_treinar_modelo.py
python -m uvicorn api:app --reload
```

3. Deixe Terminal 1 aberto. Abra **Terminal 2**, ative a mesma venv: ` .\.venv\Scripts\Activate.ps1 `.
4. Abra `http://127.0.0.1:8000/docs`. Execute `POST /predict` com o exemplo no caderno.
5. Terminal 2:

```powershell
python 02_testar_api.py
python 03_gerar_trafego.py --cenario normal --total 60
python 03_gerar_trafego.py --cenario incidente --total 60
python 04_verificar_alerta.py
python -m pytest -q
```

6. Veja `/metrics` e `http://127.0.0.1:8000/painel`; capture prints no caderno e exporte PDF.

**Cuidado:** `http://127.0.0.1:8000/painel` é um *dashboard didático local* construído no kit; NÃO é o Grafana. O Grafana real roda em `localhost:3000` quando Docker estiver disponível.

## Extensão — Prometheus + Grafana com Docker

1. Pare o servidor local (Ctrl+C no Terminal 1) para liberar porta 8000.
2. Abra Docker Desktop, aguarde Engine/RUNNING e execute no terminal da pasta:

```powershell
docker compose up --build -d
docker compose ps
```

3. Endereços:
   - FastAPI: `http://localhost:8000/docs`
   - Métricas: `http://localhost:8000/metrics`
   - Prometheus: `http://localhost:9090/targets` e `/alerts`
   - Grafana: `http://localhost:3000` (usuário `admin`, senha `aula-mlops-12`). **Credenciais apenas para laboratório local**.
4. Gere tráfego no host com o `03_gerar_trafego.py`. Vá à pasta **MLOps** no Grafana e abra o dashboard já provisionado. Aguarde os scrapes; gráficos de `rate()` precisam de amostras no tempo.
5. O alerta Prometheus `LatenciaP95Elevada` tem limiar 200ms e `for: 30s`. Em condições de laboratório de ~5s por scrape e erro lento por ~40s, pode passar de pending a firing. **Não envia e-mail**; notificação precisa Alertmanager ou Grafana Alerting adicional.
6. Encerrar: `docker compose down` (não apaga o seu ZIP nem o caderno).

## Evidências, PDF e progresso

Abra o arquivo `CADERNO_ALUNO_SEMANA12.html` no Chrome/Edge. Preencha nome/turma, explique o que fez e anexe prints. As imagens são compactadas no navegador e incluídas no JSON e no PDF. Use **Baixar progresso JSON** para backup e **Carregar JSON** para recuperar. Para o PDF: **Imprimir / salvar PDF** → Destino: Salvar como PDF. Não feche antes de salvar/exportar.

## Questões técnicas que diferenciam esta prática

- `predicoes_total`: Counter por sucesso/erro; `rate()` deriva taxa a partir de amostras.
- `predicoes_em_andamento`: Gauge (sobe e desce).
- `latencia_inferencia_segundos`: Histogram com buckets; `histogram_quantile()` estima p95 a partir dos buckets.
- `modelo_carregado`: Gauge; não prova qualidade preditiva.
- `up`: métrica criada pelo Prometheus quando faz scrape; não faz parte do `/metrics` da API.
- Erros 422 rejeitados antes do handler não entram no Counter de inferência; erros didáticos 503 entram.
- O p95 do painel local é calculado sobre as últimas amostras individuais em memória, enquanto o Grafana utiliza aproximação dos buckets Prometheus.
- Alertas sinalizam sintomas. Não diagnosticam sozinhos a causa e não determinam retreino automático.

Consulte também `TROUBLESHOOTING.md`.
