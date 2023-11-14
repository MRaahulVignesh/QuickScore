from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from backend.utils.db_conn import postgres_conn
from backend.routes.user_router import user_router
from backend.routes.exam_router import exam_router
from backend.routes.student_router import student_router
from backend.routes.answer_router import answer_router

def authorization_service_startup():
    print("Starting up -- Authorization server!!")
    postgres_conn.setup_server()

def authorization_service_shutdown():
    print("Shutting down -- Authorization server!!")
    postgres_conn.close_all_connections()

@asynccontextmanager
async def lifespan(app: FastAPI):
    authorization_service_startup()
    yield
    authorization_service_shutdown()

server = FastAPI(
    title="Authorization Server",
    description="This is the authorization server for security api",
    lifespan=lifespan
)

server.include_router(user_router, prefix="/quick-score/users")
server.include_router(exam_router, prefix="/quick-score/exams")
server.include_router(student_router, prefix="/quick-score/students")
server.include_router(answer_router, prefix="/quick-score/answers")