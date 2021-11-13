
from fastapi import FastAPI, Request

from routes import tour_routes, user_routes


app = FastAPI()


# added midddleware

@app.middleware("http")
async def add_some_middleware(request: Request, call_next):
    response = await call_next(request)
    print(f"hello from middleware 🧸")
    return response

app.include_router(tour_routes.router)
app.include_router(user_routes.router)



