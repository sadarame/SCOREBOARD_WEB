#!/usr/local/bin/python3.7
from FirestoreHandler import FirestoreHandler
from nba_api.live.nba.endpoints import scoreboard
from bs4 import BeautifulSoup
import datetime
import requests
import pytz

class Game:

    # 試合情報を格納するリスト
    game_list = []
    collection_name_NBA = "TB_NBA_LIVE_SCORE"
    collection_name_NPB = "TB_NPB_LIVE_SCORE"

    def __init__(self):

        #firestore用のインスタンス
        self.firestoreHandler = FirestoreHandler()

    def getNBALiveInfo(self):

        # 試合情報を格納するリストの初期化
        self.game_list = []

        # NBAの試合情報を取得
        games = scoreboard.ScoreBoard()
        scoreDict = games.get_dict()

        # 各試合の情報を抜き出す
        for game in scoreDict['scoreboard']['games']:
            home_team = game['homeTeam']['teamCity']
            home_team_abbreviation = game['homeTeam']['teamTricode']
            away_team = game['awayTeam']['teamCity']
            away_team_abbreviation = game['awayTeam']['teamTricode']
            home_score = game['homeTeam']['score']
            away_score = game['awayTeam']['score']
            game_status = game['gameStatusText']

            # 試合情報を辞書に格納し、リストに追加
            game_info = {
                'home_team': home_team,
                'home_team_abbreviation': home_team_abbreviation,
                'away_team': away_team,
                'away_team_abbreviation': away_team_abbreviation,
                'home_score': home_score,
                'away_score': away_score,
                'game_status': game_status,
                'update_date':datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
            }

            self.game_list.append(game_info)

        for game_info in self.game_list:
            print(game_info)

        # 試合情報を保存
        self.saveLiveInfo(self.game_list,self.collection_name_NBA)    

    ##ライブ情報を返却
    def getNPBLiveInfo(self):
        # NBAの試合情報を取得
        #ターゲットのURL
        url = "https://baseball.yahoo.co.jp/npb/schedule/"
        # ページの取得
        # ページの取得
        response = requests.get(url)

        # ページの解析
        soup = BeautifulSoup(response.text, 'html.parser')

        # 試合情報を格納するリスト
        self.game_list = []

        # 試合情報の取得
        games = soup.find_all('li', class_='bb-score__item')

        for game in games:
            venue = game.select_one('.bb-score__venue').text.strip()
            home_team = game.select_one('.bb-score__homeLogo').text.strip()
            away_team = game.select_one('.bb-score__awayLogo').text.strip()
            status = game.select_one('.bb-score__link').text.strip()
            link = game.select_one('.bb-score__content')['href']

            # スコアの取得            
            score_left_element = game.select_one('.bb-score__score--left')
            score_left = score_left_element.text.strip() if score_left_element else ""

            score_center_element = game.select_one('.bb-score__score--center')
            score_center = score_center_element.text.strip() if score_center_element else ""

            score_right_element = game.select_one('.bb-score__score--right')
            score_right = score_right_element.text.strip() if score_right_element else ""
        
            # すでに同じ試合情報がリストに存在するかどうかを確認
            existing_game_info = next((game_info for game_info in self.game_list if game_info['venue'] == venue and
                                                                game_info['home_team'] == home_team and
                                                                game_info['away_team'] == away_team), None)

            # 試合情報を辞書にまとめてリストに追加
            if existing_game_info is None:
                game_info = {
                    'venue': venue,
                    'home_team': home_team,
                    'away_team': away_team,
                    'status': status,
                    'link': link,
                    'score': {
                        'left': score_left,
                        'center': score_center,
                        'right': score_right
                    },
                    'update_date':datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
                }

            self.game_list.append(game_info)

        # 取得した試合情報の表示
        for game_info in self.game_list:
            print(game_info)

        # 試合情報を保存
        self.saveLiveInfo(self.game_list,self.collection_name_NPB)   
    
    # FireStoreに洗いがえで保存
    def saveLiveInfo(self,game_list,collection_name):
        self.firestoreHandler.setLiveScoer(game_list,collection_name)