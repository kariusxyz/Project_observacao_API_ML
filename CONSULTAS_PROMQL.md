# Consultas PromQL — explique antes de executar

```promql
# Requisições por segundo, sucesso + erro
sum(rate(predicoes_total[1m]))

# Taxa percentual de erros dentro do handler de inferência
100 * sum(rate(predicoes_total{resultado="erro"}[1m])) / clamp_min(sum(rate(predicoes_total[1m])), 0.000001)

# p95 estimado a partir do Histogram clássico, em SEGUNDOS
histogram_quantile(0.95, sum by (le) (rate(latencia_inferencia_segundos_bucket[1m])))

# Modelo carregado — gauge exposto pela aplicação
modelo_carregado

# Sucesso do scrape — métrica gerada pelo servidor Prometheus
up{job="api-observavel"}
```

Uma consulta rate() precisa de amostras em intervalos de tempo. Espere scrapes por 15–30s antes de concluir que há falha.

`sum by (le)` agrega séries preservando o limite cumulativo de cada bucket. O quantil é uma estimativa, não um percentil diretamente medido.

Fontes oficiais: https://prometheus.io/docs/prometheus/latest/querying/functions/ ; https://prometheus.github.io/client_python/ ; https://grafana.com/docs/grafana/latest/administration/provisioning/ .
