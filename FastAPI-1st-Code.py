from fastapi import FastAPI

app = FastAPI() # making object

# if you want data from server Use get
# If you want to send data to server use post

# / is decorater
@app.get('/') #  creating route using '/' decorater
def hello():
    return {'message':'Hello World'} # returns dictionary

@app.get('/aboutMe')
def Me():
    return {'Me':'I am Jugal learning FastAPI'}

# Tip using -- reload for automaticly updating
# FastAPI make documentation automaticly use /docs