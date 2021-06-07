from fastapi import FastAPI, HTTPException
from .database import database_connection
from .routes import user_router
from .routes import review_router
from .models import *

app = FastAPI(
    title='Python Movie API',
    description="In this project we'll do movie reviews",
    version='1'
    )

app.include_router(user_router)
app.include_router(review_router)

@app.get('/')
async def index():
    return 'Hello world from FastApi server'


# startup: evento para iniciar el servidor
@app.on_event('startup')
def start_server():
    if database_connection.is_closed():
        database_connection.connect()
    
    database_connection.create_tables([User, Movie, UserReview])

# shutdown: evento para apagar el servidor
@app.on_event('shutdown')
def kill_server():
    if not database_connection.is_closed():
        database_connection.close()
        print('Closing...')


