from fastapi import FastAPI, Request, HTTPException

from routes import tour_routes, user_routes

app = FastAPI()


@app.middleware("http")
async def add_some_middleware(request: Request, call_next):
    response = await call_next(request)
    print(f"hello from middleware 🧸")
    return response


app.include_router(tour_routes.router, prefix="/api/v1/tours", tags=["tours"])
app.include_router(user_routes.router, prefix="/api/v1/users", tags=["users"])


@app.get("/")
async def heart_beat():
    
    return {"I ❤️ FastAPI": "🙋🏽‍♂️"
      }

