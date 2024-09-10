import requests

BACKEND_URL = 'http://localhost:5000'

def get_user(token, user_id):
    headers = {'Authorization':f'Bearer {token}'}
    try:
        
        response = requests.get(f"{BACKEND_URL}/usuarios/{user_id}", headers=headers)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        return {"erro": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"erro": f"Other error occurred: {err}"}
    
def get_contas(token):
    headers = {'Authorization':f'Bearer {token}'}
        
    try:
        
        response = requests.get(f"{BACKEND_URL}/contas", headers=headers)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        return {"erro": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"erro": f"Other error occurred: {err}"}
    
def get_ciclomeses(token):
    headers = {'Authorization':f'Bearer {token}'}
    
    try:
        response = requests.get(f"{BACKEND_URL}/ciclomes", headers=headers)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        return {"erro": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"erro": f"Other error occurred: {err}"}
    
def get_dias(token, mes_id):
    headers = {'Authorization':f'Bearer {token}'}
    
    try:
        response = requests.get(f"{BACKEND_URL}/dias/{mes_id}", headers=headers)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        return {"erro": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"erro": f"Other error occurred: {err}"}