import uvicorn as uc

try:
    if __name__ == "__main__":
        uc.run(
            'apps.main:app',  
            host="127.0.0.1", 
            port=8888,
            reload=True
        )
except Exception as e:
    print(f'Error: {e}')