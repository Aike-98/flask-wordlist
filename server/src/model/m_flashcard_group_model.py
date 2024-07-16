from basemodel import BaseModel
import common, constants

class MFlashcardGroup(BaseModel):
    def __init__(self, config):
        super().__init__(config)
        self.table = 'flashcard_group'

    ### flashcard_group へのINSERT ###
    def insert_flashcard_group(self, title, user_id):
        '''
        作成したflashcardのgroup情報をDBに登録
        '''
        #バリデーション
        if not common.validate_string(title, constants.TITLE_MAX_LENGTH) :
            return 'error'
        values = (title, user_id)
        return self.insert_single_record(self.table, '`name`, `user_id`', values)
    
    def select_latest_flashcard_group(self):
        '''
        TOP表示する最新5件の単語帳グループを取得
        '''
        return self.select('flashcard_group', '`id`, `name`', ' ORDER BY `lastdate` DESC LIMIT 5')
    
    def select_flashcard_group_by_id(self, group_id_list):
        where = ' WHERE '
        for i in range(0, len(group_id_list), 1):
            group_id_list[i] = 'id=' + str(group_id_list[i])
        ids = ' OR '.join(group_id_list)
        where = where + ids
            
        return self.select_by_id(self.table, '`id`, `name`', where)
    
    def select_flashcard_group_by_keyword(self, keyword):
        keyword = '"%' + str(keyword) + '%"'
        result = self.select(self.table, '`id`', ' WHERE `name` LIKE ' + keyword)

        group_id_list = []
        for i in range(0, len(result), 1):
            group_id = result[i]['id']
            if not group_id in group_id_list:
                group_id_list.append(group_id)

        return group_id_list
    
    def select_flashcard_group_by_userid(self, user_id):
        where = ' WHERE user_id=' + str(user_id)
        return self.select(self.table, '`id`, `name`', where)
    
    def delete_flashcard_group(self, group_id):
        '''
        削除
        '''
        return self.delete('flashcard_group', ' WHERE id=' + str(group_id))
    