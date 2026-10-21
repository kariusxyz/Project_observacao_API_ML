# Soluções rápidas — Semana 12

**`py` não é reconhecido** → tente `python --version`; use Python 3.10+ (recomendado 3.11/3.12). Se necessário, reabra o VS Code após a instalação.

**Ativação PowerShell bloqueada** → `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`; depois `.\.venv\Scripts\Activate.ps1`. Isso NÃO altera a política permanentemente.

**`ModuleNotFoundError`** → verifique `(.venv)` e execute `python -m pip install -r requirements.txt`, depois `python 00_preflight.py`.

**`api.py` não acha modelo** → antes de iniciar API: `python 01_treinar_modelo.py`. Confira `modelos/churn.joblib`.

**Erro de conexão com 127.0.0.1:8000** → no Terminal 1 execute `python -m uvicorn api:app --reload` e deixe aberto. Se a porta 8000 estiver ocupada, encerre o servidor anterior ou o `docker compose` anterior.

**`/metrics` exibe texto e não gráfico** → comportamento esperado. Abra `/painel` para o gráfico local, ou Prometheus/Grafana se Docker estiver disponível.

**Counter de erros não aparece** → execute `python 03_gerar_trafego.py --cenario incidente --total 60` para gerar erros HTTP 503 instrumentados.

**O p95/alerta local continua zero** → os indicadores usam janela de 60 segundos: gere tráfego de novo e consulte imediatamente. O threshold usa pelo menos dez amostras.

**Prometheus target DOWN** → `docker compose ps` e `docker compose logs modelo`; confirme que o serviço interno é `modelo:8000` e que `/metrics` responde no navegador host. Dentro do container Prometheus, `localhost` não representa a API.

**Grafana sem painéis** → confirme `docker compose ps`, abra Grafana, Dashboards → pasta `MLOps`; aguarde scrape do Prometheus e faça tráfego. Verifique a fonte `Prometheus` provisionada.

**Alerta permanece pending** → os 30 segundos devem decorrer enquanto a condição continua verdadeira. Gere tráfego lento por mais tempo. Sem tráfego, `rate()` pode ficar vazio.

**Docker indisponível ou sem permissão** → não impede a prática. Siga o caminho sem Docker, use `/painel` e `/metrics` e colete a evidência alternativa.

**Comandos bash do arquivo antigo** → foram substituídos por Python/PowerShell, compatíveis com Windows.

**O caderno não conserva o print depois da atualização** → o armazenamento do navegador pode ter quota/política específica. Use `Baixar progresso JSON` e confira o arquivo antes de sair. Para entregar, gere o PDF com o navegador enquanto os prints estão anexados.

**Senha Grafana** → `admin / aula-mlops-12` é apenas para ambiente local didático. Nunca use esse segredo em serviço publicado.
