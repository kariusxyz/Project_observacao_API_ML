"""Verificação local imediata — não é alerta persistente do Prometheus."""
import httpx
try:
 r=httpx.get('http://127.0.0.1:8000/api/snapshot',timeout=10);r.raise_for_status();dados=r.json()
except Exception as exc:
 print('Falha de conexão. Confira o servidor: ',exc);raise SystemExit(2)
print('=== LEITURA LOCAL DOS ÚLTIMOS 60 s ===')
for campo in ['total_ultimos_60s','taxa_erro_pct','p50_ms','p95_ms','alerta_p95']:
 print(f'{campo}: {dados[campo]}')
print('ALERTA LOCAL' if dados['alerta_p95'] else 'SEM ALERTA LOCAL', '— p95>200ms com >=10 amostras')
print('Diferença importante: o Prometheus consulta métricas por janela; o alerta local usa amostras desta instância.')
