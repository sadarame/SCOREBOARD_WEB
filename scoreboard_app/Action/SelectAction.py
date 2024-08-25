# from FirestoreHandler import FirestoreHandler
from ..Logic.FireStore.FirestoreHandler import FirestoreHandler

class SelectAction:

    # 定数
    COLLECTION_NAME = "TB_TEAM_MST"

    #データ取得クラス
    def __init__(self):
        # FirestoreHandlerインスタンスを作成
        self.db = FirestoreHandler()

    # チームを取得
    def getTeams(self):
        # データをFirestoreから取得
        teamlist = self.db.getTeamList(self.COLLECTION_NAME)
        sortedList =self._sortTeamlist(teamlist)     
        return sortedList
    
    # カテゴリとリーグでソートしたリストを返却
    def _sortTeamlist(self, teamList):
        
        # カテゴリごとの辞書
        # カテゴリごとリーグごとの辞書を作成
        category_dict = {}

        for team in teamList:
            category = team['category']
            league = team['league']
            
            if category not in category_dict:
                category_dict[category] = {}
            
            if league not in category_dict[category]:
                category_dict[category][league] = []
            
            category_dict[category][league].append({
                'teamLongNM': team['teamLongNM'],
                'teamShortNM': team['teamShortNM']
        })
            
        return category_dict
    


