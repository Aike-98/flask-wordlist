from basemodel import BaseModel
import common, constants

class MUser(BaseModel):
    def __init__(self, config):
        super().__init__(config)
        self.table = 'user'

    def insert_user(self, user_name, password):
        '''
        ユーザー情報をDBに保存
        '''
        #バリデーション
        values = (user_name, password)
        return self.insert_single_record(self.table, '`name`, `password`', values)
    
    def select_user_by_username(self, user_name):
        where = ' WHERE name="' + str(user_name) +'"'
        return self.select(self.table, '*', where)