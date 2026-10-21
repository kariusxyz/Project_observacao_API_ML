import httpx
base='http://127.0.0.1:8000'
entrada={'idade':34,'meses_cliente':18,'chamados_suporte':3,'dias_sem_login':25,'valor_mensal':119}
with httpx.Client(timeout=10) as client:
    for route in ['/health','/metrics','/painel']:
        r=client.get(base+route); print(route,r.status_code);r.raise_for_status()
    r=client.post(base+'/predict',json=entrada); r.raise_for_status();print('Previsão:',r.json())
    texto=client.get(base+'/metrics').text
    for nome in ['predicoes_total','latencia_inferencia_segundos_bucket','modelo_carregado']:
        assert nome in texto,nome
        print('[OK] Métrica',nome)
print('TESTE MANUAL DA API: PASSOU')
