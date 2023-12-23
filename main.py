from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from database import Database
from psycopg2 import sql
from clases import *
from datetime import date
from fastapi.responses import JSONResponse

db_params = {
    'dbname': 'wakala',
    'user': 'postgres',
    'password': '',
    'host': 'localhost',
    'port': '5432'
}

app = FastAPI()

@app.post('/addUser/')
async def add_user(user: User):
    db = Database(db_params)
    query = sql.SQL("INSERT INTO users (username, password) VALUES (%s, %s);")
    values = (user.username, user.password)
    try:
        db.execute_insert(query, values)
        return {"StatusCode": 200}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al ejecutar query: {str(e)}")
    finally:
        db.close_connection()


@app.get("/login/{username}/{password}")
def login(username: str, password: str):
    db = Database(db_params)
    query = sql.SQL('SELECT id_user, password FROM users WHERE username=%s;')
    values = (username, )
    try:
        user_data = db.execute_query(query, values)
        print(user_data)
        if user_data[0]:
            if user_data[0][1] == password:
                return {"StatusCode": 200, "id_user": user_data[0][0]}
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al ejecutar query: {str(e)}")
    finally:
        db.close_connection()

@app.get("/username/{id_user}")
async def get_username(id_user: int):
    db = Database(db_params)
    query = sql.SQL('SELECT username FROM users WHERE id_user=%s;')
    values = (id_user,)
    try:
        username = db.execute_query(query, values)
        formatted_username = [
            {
                'username': row[0]
            }
            for row in username
        ]
        return JSONResponse(content=formatted_username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al ejecutar query: {str(e)}")
    finally:
        db.close_connection()

@app.get("/locations/", response_model=list[LocationsList])
async def get_locations():
    db = Database(db_params)
    query = sql.SQL("""SELECT id_location, sector, username, registration_date 
                    FROM public.locations loc
                    JOIN public.users us
                    ON loc.id_user = us.id_user;""")
    try:
        locations = db.execute_query(query)
        formatted_locations = [
            {
                'id_location': row[0],
                'sector': row[1],
                'username': row[2],
                'registration_date': row[3].isoformat()
            }
            for row in locations
        ]
        return JSONResponse(content=formatted_locations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al ejecutar query: {str(e)}")
    finally:
        db.close_connection()

@app.get("/detailsLocations/{id_location}", response_model=list[LocationsList])
async def get_locations(id_location: int):
    db = Database(db_params)
    query = sql.SQL("""SELECT sector, description, photo1, photo2, username, registration_date, still_there, not_still_there
                    FROM public.locations loc
                    JOIN public.users us
                    ON loc.id_user = us.id_user
                    WHERE loc.id_location = %s;""")
    values = (id_location, )
    try:
        locations = db.execute_query(query, values)
        formatted_locations = [
            {
                'sector': row[0],
                'description': row[1],
                'photo1': row[2],
                'photo2': row[3],
                'username': row[4],
                'registration_date': row[5].isoformat(),
                'still_there': row[6],
                'not_still_there': row[7]
            }
            for row in locations
        ]
        return JSONResponse(content=formatted_locations)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al ejecutar query: {str(e)}")
    finally:
        db.close_connection()

@app.post("/addLocation/")
def create_location(location: NewLocation, id_user: int):
    db = Database(db_params)
    query = sql.SQL("INSERT INTO locations (sector, description, photo1, photo2, registration_date, id_user, still_there, not_still_there) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);")
    today = date.today()
    values = (location.sector, location.description, location.photo1, location.photo2, today, id_user, 0, 0)
    try:
        db.execute_insert(query, values)
        return {"StatusCode": 200}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al ejecutar query: {str(e)}")
    finally:
        db.close_connection()

@app.put("/stillThere/{location_id}")
async def like_location(location_id: int):
    db = Database(db_params)
    query = sql.SQL("UPDATE locations SET still_there = still_there + 1 WHERE id_location = %s;")
    values = (location_id, )
    try:
        db.execute_insert(query, values)
        return {"StatusCode": 200}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al ejecutar query: {str(e)}")
    finally:
        db.close_connection()

@app.put("/notStillThere/{location_id}")
async def dislike_location(location_id: int):
    db = Database(db_params)
    query = sql.SQL("UPDATE locations SET not_still_there = not_still_there + 1 WHERE id_location = %s;")
    values = (location_id, )
    try:
        db.execute_insert(query, values)
        return {"StatusCode": 200}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al ejecutar query: {str(e)}")
    finally:
        db.close_connection()
    
@app.post("/comment/{id_location}")
async def add_comment(id_location: int, id_user: int, comment: Comment):
    db = Database(db_params)
    query = sql.SQL("INSERT INTO comments (id_location, id_user, comment) VALUES (%s, %s, %s);")
    values = (id_location, id_user, comment.text)
    try:
        db.execute_insert(query, values)
        return {"StatusCode": 200}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al ejecutar query: {str(e)}")
    finally:
        db.close_connection()

@app.get("/getComments/{id_location}")
async def get_comments(id_location: int):
    db = Database(db_params)
    query = sql.SQL("""SELECT username, comment 
                    FROM public.comments com
                    JOIN public.users us
                    ON com.id_user = us.id_user
                    WHERE com.id_location=%s;""")
    values = (id_location, )
    try:
        comments = db.execute_query(query, values)
        formatted_comments = [
            {
                'username': row[0],
                'comment': row[1]
            }
            for row in comments
        ]
        return JSONResponse(content=formatted_comments)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al ejecutar query: {str(e)}")
    finally:
        db.close_connection()