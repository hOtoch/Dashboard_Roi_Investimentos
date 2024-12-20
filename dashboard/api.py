import requests

BACKEND_URL = 'https://dashboard.roiinvestimentos.com/api'

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
    
def create_user(token, user_data):
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    try:
        response = requests.post(f"{BACKEND_URL}/usuarios", headers=headers, json=user_data)
        response.raise_for_status()

        if response.status_code == 201:
            return response

    except requests.exceptions.HTTPError as http_err:
       
        try:            
            error_message = response.json().get('erro', 'Erro desconhecido')
            return {"erro": f"Erro {response.status_code}: {error_message}"}
        except ValueError:
           
            return {"erro": f"HTTP error occurred: {http_err}, código: {response.status_code}"}
    except Exception as err:
        return {"erro": f"Other error occurred: {err}"}
    
    
def getall_users(token):
    headers = {'Authorization':f'Bearer {token}'}
    try:
        
        response = requests.get(f"{BACKEND_URL}/usuarios", headers=headers)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        return {"erro": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"erro": f"Other error occurred: {err}"}
    
def edit_user(token, user_id, user_data):
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    try:
        response = requests.put(f"{BACKEND_URL}/usuarios/{user_id}", headers=headers, json=user_data)
        response.raise_for_status()

        if response.status_code == 200:
            return response

    except requests.exceptions.HTTPError as http_err:
       
        try:            
            error_message = response.json().get('erro', 'Erro desconhecido')
            return {"erro": f"Erro {response.status_code}: {error_message}"}
        except ValueError:
           
            return {"erro": f"HTTP error occurred: {http_err}, código: {response.status_code}"}
    except Exception as err:
        return {"erro": f"Other error occurred: {err}"}
    
def delete_user(token, user_id):
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.delete(f"{BACKEND_URL}/usuarios/{user_id}", headers=headers)
        response.raise_for_status()

        if response.status_code == 200:
            return response

    except requests.exceptions.HTTPError as http_err:
       
        try:            
            error_message = response.json().get('erro', 'Erro desconhecido')
            return {"erro": f"Erro {response.status_code}: {error_message}"}
        except ValueError:
           
            return {"erro": f"HTTP error occurred: {http_err}, código: {response.status_code}"}
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
    
def create_conta(token, conta_data):
    headers = {'Authorization':f'Bearer {token}','Content-Type': 'application/json'}
    
    try:
        response = requests.post(f"{BACKEND_URL}/contas", headers=headers, json=conta_data)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        return {"erro": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"erro": f"Other error occurred: {err}"}
    
def listar_contas_user_admin(token, user_id):
    headers = {'Authorization':f'Bearer {token}'}
    
    try:
        response = requests.get(f"{BACKEND_URL}/contas/user/{user_id}", headers=headers)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        return {"erro": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"erro": f"Other error occurred: {err}"}


def listar_contas_user(token):
    headers = {'Authorization':f'Bearer {token}'}
    
    try:
        response = requests.get(f"{BACKEND_URL}/contas/user", headers=headers)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        return {"erro": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"erro": f"Other error occurred: {err}"}
    
def edit_conta(token,conta_id, conta_data):
    headers = {'Authorization':f'Bearer {token}','Content-Type': 'application/json'}
    
    try:
        response = requests.put(f"{BACKEND_URL}/contas/{conta_id}", headers=headers, json=conta_data)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        return {"erro": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"erro": f"Other error occurred: {err}"}
    
def delete_conta(token, conta_id):
    headers = {'Authorization':f'Bearer {token}','Content-Type': 'application/json'}
    
    try:
        response = requests.delete(f"{BACKEND_URL}/contas/{conta_id}", headers=headers)
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
    

    
def create_ciclomes(token, ciclomes_data):
    headers = {'Authorization':f'Bearer {token}','Content-Type': 'application/json'}
    
    try:
        response = requests.post(f"{BACKEND_URL}/ciclomes", headers=headers, json=ciclomes_data)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        return {"erro": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"erro": f"Other error occurred: {err}"}
    
def edit_ciclomes(token, ciclomes_id, ciclomes_data):
    headers = {'Authorization':f'Bearer {token}','Content-Type': 'application/json'}
    
    try:
        response = requests.put(f"{BACKEND_URL}/ciclomes/{ciclomes_id}", headers=headers, json=ciclomes_data)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        return {"erro": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"erro": f"Other error occurred: {err}"}

def delete_ciclomes(token, ciclomes_id):
    headers = {'Authorization':f'Bearer {token}'}
    
    try:
        response = requests.delete(f"{BACKEND_URL}/ciclomes/{ciclomes_id}", headers=headers)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        return {"erro": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"erro": f"Other error occurred: {err}"}
    
def ativar_ciclomes(token, ciclomes_id):
    headers = {'Authorization':f'Bearer {token}'}
    
    try:
        response = requests.put(f"{BACKEND_URL}/ciclomes/ativar/{ciclomes_id}", headers=headers)
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
    
def edit_dia(token, dia_id, dia_data):
    headers = {'Authorization':f'Bearer {token}','Content-Type': 'application/json'}
    
    try:
        response = requests.put(f"{BACKEND_URL}/dias/{dia_id}", headers=headers, json=dia_data)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        return {"erro": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"erro": f"Other error occurred: {err}"}

