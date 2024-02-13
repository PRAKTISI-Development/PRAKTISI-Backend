import uvicorn 

config = {
  'app' : 'apps.main:app',
  'host': '127.0.0.1',
  'port': 8888
}

if __name__ == '__main__':
    uvicorn.run(config['app'], 
                host=config['host'], 
                port=config['port'], 
                reload=True 
                )

