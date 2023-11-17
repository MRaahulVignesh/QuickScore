import jwt
import datetime
import uuid
from backend.utils.errors import NotFoundError, AuthenticationError, ModelError
from backend.dao.context_dao import ContextDao
from backend.schemas.context_schema import ContextResponse, CreateContext
from backend.config.config import config
from backend.rag_models.vector_store import VectorDB

class ContextCore:

    def __init__(self):
        self.context_dao = ContextDao()

    # Create a new context
    def create_context(self, input: CreateContext, filename, context_pdf = None):
        if context_pdf is None:
            raise BadRequestError("Could not parse the pdf")
        uuid_str = str(uuid.uuid4()).replace('-', '')
        context_unique_key = "CONTEXT"+uuid_str[0].upper() + uuid_str[1:]

        vector_db = VectorDB()
        result = vector_db.embed_and_store(context_pdf, context_unique_key)
        if result:
            context = self.context_dao.create_context(name= input.name, comments=input.comments, context_key=context_unique_key, user_id=input.user_id, filename=filename)
            context = ContextResponse.model_validate(context).model_dump(mode="json")
        else:
            raise ModelError("Could Process the context pdf!")
        return context

    # Retrieve a context by id
    def get_context_by_id(self, id: int):
        context = self.context_dao.get_context_by_id(id)
        context = ContextResponse.model_validate(context).model_dump(mode="json")
        return context

    # Retrieve a context by user_id
    def get_contexts_by_user_id(self, user_id: int):
        contexts = self.context_dao.get_contexts_by_user_id(user_id)
        new_contexts = []
        for context in contexts:
            tmp = ContextResponse.model_validate(context).model_dump(mode="json")
            new_contexts.append(tmp)
        return new_contexts

    # Delete a context
    def delete_context(self, id: int):
        print("hello")
        self.context_dao.delete_context(id)
        return True