# Checklist antes de projetar

1. Abra o deck HTML offline e avance 1→15, teste os botões Counter/Gauge/p95/status da API.
2. Garanta Python 3.10+, VS Code, acesso à instalação via pip; Docker é opcional.
3. Para demonstração, instale requirements, rode treino e uvicorn; abra `/docs`, `/metrics`, `/painel`.
4. Colete as evidências no caderno do aluno; ele gera PDF e backup JSON.
5. Se a turma não tiver Docker: não bloquear. Conteúdos de Prometheus/Grafana são trabalhados com os arquivos reais YAML/JSON do kit, e o aluno observa o painel local de eventos reais.
6. Se a turma tiver Docker: execute `docker compose up --build -d`, consulte `/targets`, `/alerts`, Grafana, gere tráfego via Python.
7. Não confunda latência p95 com média; Counter com taxa; monitoramento operacional com verificação de drift.
8. Não prometer notificação e-mail/Slack: kit não inclui Alertmanager.
