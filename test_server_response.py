import requests

def check_server_response():
    try:
        response = requests.get('http://127.0.0.1:8003')
        return response.status_code, response.text
    except Exception as e:
        return None, str(e)


status, text = check_server_response()
print(f'Status: {status}, Response: {text}')
