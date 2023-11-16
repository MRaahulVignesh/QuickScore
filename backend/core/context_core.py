import jwt
import datetime

from backend.utils.errors import NotFoundError, AuthenticationError
from backend.dao.context_dao import ContextDao
from backend.schemas.context_schema import ContextResponse, CreateContext
from backend.config.config import config

class ContextCore:

    def __init__(self):
        self.context_dao = ContextDao()

    # Create a new context
    def create_context(self, input: CreateContext):
        context = self.context_dao.create_context(name= input.name, roll_no= input.roll_no, email= input.email, user_id=input.user_id)
        context = ContextResponse.model_validate(context).model_dump(mode="json")
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