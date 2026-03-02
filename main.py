from fastapi import FastAPI

app = FastAPI()

#define the route for our requests (get request)
@app.get('/')
def hello():
    return {'message': 'Hello world'}

@app.get('/about')
def about():
    return {'message':'i am learning fastapi'}

