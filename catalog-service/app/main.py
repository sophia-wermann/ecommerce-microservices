from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import connect_to_mongo, close_mongo_connection
from app.routes.products import router as products_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(
    title="Catalog Service",
    description="Product catalog microservice with flexible schema per category. "
                "Part of a polyglot microservices e-commerce system.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(products_router)


@app.get("/health", tags=["Health"])
async def health_check():
    """Returns service health status."""
    return {"status": "healthy", "service": "catalog-service"}
