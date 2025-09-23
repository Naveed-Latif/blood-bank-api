from fastapi import FastAPI,  Depends
from contextlib import asynccontextmanager
from .routers import signup, auth, user

# Import local modules
from .database import create_tables
from fastapi.middleware.cors import CORSMiddleware

# Use FastAPI lifespan event for table creation


@asynccontextmanager
async def lifespan(app):
    create_tables()
    yield

app = FastAPI(title='Blood Donation API',
              description='API for blood donation signup', lifespan=lifespan)

origins = [
    "http://localhost:3000",  # Next.js dev server
    "http://127.0.0.1:3000",
    "https://blood-donation-bank-ten.vercel.app",  # Vercel production frontend
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint - welcome message


@app.get("/")
async def root():
    return {"message": "Blood Donation API - Welcome!"}


# Signup endpoint - register new blood donor
app.include_router(signup.router)


# Login endpoint
app.include_router(auth.router)


# User endpoints
app.include_router(user.router)


# Run the application when script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
