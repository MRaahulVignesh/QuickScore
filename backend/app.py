from fastapi import FastAPI
from backend.utils.db_conn import postgres_conn
from backend.routes.user_router import user_router


def authorization_service_startup():
    print("Starting up -- Authorization server!!")
    postgres_conn.setup_server()


def authorization_service_shutdown():
    print("Shutting down -- Authorization server!!")
    postgres_conn.close_all_connections()


authorization_app = FastAPI(
    title="Authorization Server",
    description="This is the authorization server for security api",
)

# routers
authorization_app.include_router(user_router, prefix="/users")
