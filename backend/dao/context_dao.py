from sqlalchemy.orm import Session
from sqlalchemy import exc

from backend.utils.db_conn import conn  
from backend.utils.errors import DatabaseError, DuplicateError, NotFoundError
from backend.models.models import ContextModel, ExamModel

class ContextDao:
    def __init__(self):
        self.db = conn.get_db()

    # Create a new user
    def create_context(self, name: str, comments: str, user_id: int, context_key: str, filename: str,):
        try:
            context = ContextModel(name=name, comments=comments, user_id=user_id, context_key=context_key, file_name=filename)
            self.db.add(context)
            self.db.commit()
            self.db.refresh(context)
        except exc.IntegrityError as error:
            print(error)
            raise DuplicateError("Similar Record already exists!")
        except Exception as error:
            print(error)
            raise DatabaseError("DB operation Failed: Create_Context")
        finally:
            self.db.close()
        return context

    # Retrieve a context by ID
    def get_context_by_id(self, id: int):
        try:
            context = self.db.query(ContextModel).filter(ContextModel.id == id).first()
            if context is None:
                raise NotFoundError("Context doesnot exist!")
        except Exception as error:
            print(error)
            raise DatabaseError("DB operation Failed: Get_Context_By_Id")
        return context

    # Retrieve a context by email
    def get_contexts_by_user_id(self, user_id: str):
        try:
            contexts = self.db.query(ContextModel).filter(ContextModel.user_id == user_id).all()
        except Exception as error:
            raise DatabaseError("DB operation Failed: Get_Context_By_User_Id")
        return contexts


    def delete_context(self, id: int):
        try:
            with self.db.begin() as transaction:
                context = self.db.query(ContextModel).filter(ContextModel.id == id).first()
                if context is None:
                    transaction.rollback()
                    raise NotFoundError("Context doesnot exist!")
                self.db.query(ExamModel).filter(ExamModel.context_id == context.id).update({ExamModel.context_id: None})
                self.db.delete(context)
                transaction.commit()
        except NotFoundError as error:
            raise error
        except Exception as error:
            print(error)
            transaction.rollback()
            raise DatabaseError("DB operation Failed: Delete_Context")
        finally:
            self.db.close()
        return True
