from basemodel import BaseModel
import common, constants

class MFlashcard(BaseModel):
    def __init__(self, config):
        super().__init__(config)

    def insert_flashcard(self, group_id, wordlist):
        '''
        作成したワードリストをDBに保存
        '''
        #バリデーション
        if type(group_id) != int or group_id < 1:
            return 'error'

        values = []
        for i in range(0, len(wordlist), 1):
            word = wordlist[i]['word']
            description = wordlist[i]['description']

            #要素ごとのバリデーション
            if not common.validate_string(word, constants.WORD_MAX_LENGTH):
                return 'error'
            if not common.validate_string(description, constants.DESCRIPTION_MAX_LENGTH):
                return 'error'
            
            value = [group_id, word, description]
            values.append(value)

        colmun = "`group_id`, `word`, `description`"
        return self.bulk_insert_records('flashcard', colmun, values)
    
    def select_flashcard(self, group_id):
        '''
        指定のグループidのワードリスト情報を取得
        '''
        
        #バリデーション
        if type(group_id) != int or group_id < 1:
            return 'error'
        
        result = self.select('flashcard', '`word`, `description`', ' WHERE group_id=' + str(group_id))

        data_list = []
        for i in range(0, len(result), 1):
            data = {'word': result[i]['word'], 'description':result[i]['description']}
            data_list.append(data)
        return data_list
    
    def select_flashcard_by_keyword(self, keyword):
        '''
        キーワードに一致する用語を含むワードリストを取得
        '''
        keyword = '"%' + str(keyword) + '%"'
        result = self.select('flashcard', '`group_id`', ' WHERE `word` LIKE ' + keyword + ' OR `description` LIKE ' + keyword)

        group_id_list = []

        for i in range(0, len(result), 1):
            group_id = result[i]['group_id']
            if not group_id in group_id_list:
                group_id_list.append(group_id)

        return group_id_list
    
    def delete_flashcard(self, group_id):
        return self.delete('flashcard', ' WHERE group_id=' + str(group_id))