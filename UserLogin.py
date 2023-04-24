from data.users import User
from data import db_session

class UserLogin():

    def fromDB(self, user_id):
        db_sess = db_session.create_session()
        self.__user = db_sess.query(User).filter(User.id == user_id).first()
        return self
    
    def create(self, user):
        self.__user = user
        return self
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.__user.id)
    
    def get_name(self):
        return str(self.__user.name)
    
    def get_courses(self):
        return str(self.__user.courses)
    

