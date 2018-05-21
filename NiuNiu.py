# -*- coding:utf-8 -*-

class Base(object):
    num_dict = {"1":1,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":11,"Q":12,"K":13}
    color_dict = {"黑桃":4, "红桃":3, "梅花":2, "方片":1}


class Card(Base):
    """一张卡"""

    def __init__(self,num,color):
        self.num = num
        self.color = color
        self.ori_value = self.num_dict[self.num]
        self.num_value = self.num_dict[self.num]  # 根据其他规则设置value值
        self.color_value = self.color_dict[self.color]

    def __repr__(self):
        return "{color}{num}".format(color=self.color,num=self.num)


class Pokers(Base):
    """整副扑克"""
    _instance = None  # 使用单例模式

    def __new__(cls, *args, **kwargs):
        """
        单例模式
        :param args:
        :param kwargs:
        :return:
        """
        # return 真实的去创建对象
        if cls._instance:
            return cls._instance
        else:
            # obj = '真实的去创建对象'
            obj = object.__new__(cls, *args, **kwargs)
            cls._instance = obj
            return obj

    @classmethod
    def cards(cls):
        cards = []
        for color in cls.color_dict:
            for num in cls.num_dict:
                cards.append(Card(num,color))
        return cards


class NiuNiu(Base):
    """根据牛牛的规则处理5张牌"""

    niuniu_num_dict = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10,
                "K": 10}

    def __init__(self,fiveCards):
        self.fiveCards = self.initial(fiveCards) if hasattr(self,"initial") else fiveCards


    def initial(self,fiveCards):
        for card_obj in fiveCards:
            card_obj.num_value = self.niuniu_num_dict[card_obj.num]  # 根据牛牛的规则，修改其num_value
        return fiveCards


    @property
    def result(self):
        fiveCards = self.fiveCards
        result = {"status":False,"point":0,"maxCard":None,"doubling":1,"text":"无牛"}

        result["maxCard"] = self.max_in_somecards(fiveCards)
        if self.haveNiu(fiveCards):
            result["status"] = True

            point = sum(map(lambda x:x.num_value,fiveCards)) % 10
            result["point"] = point if point else 10
            result["text"] = "牛{n}".format(n=point if point else "牛" )
            result["doubling"] = self.rule(point)

        return result


    def rule(self,point):
        if point == 7 or point == 8:
            res = 2
        elif point == 9:
            res = 3
        elif point == 10:
            res = 4
        else:
            res = 1

        return res


    def haveNiu(self,fiveCards):
        """
        检查有牛没牛
        :param FiveCards: 5张牌[obj1,obj2,obj3,obj4,obj5]
        :return: True/False 有牛或没牛
        """
        from itertools import combinations
        threeCards = list(combinations(fiveCards, 3))
        for three_card in threeCards:
            if sum(map(lambda x:x.num_value,three_card)) % 10 == 0:
                # 3张牌的和是10的倍数，有牛
                # res = sum(set(fiveCards).difference(set(threeCards))) % 10
                return True
        # 无牛
        return False

    def biger_in_2card(self,card1_obj,card2_obj):
        """
        比较两张牌的大小（点数、花色）
        :param card1:
        :param card2:
        :return: 两张牌中较大的那张牌obj
        """
        if card1_obj.ori_value == card2_obj.ori_value:
            if card1_obj.color_value > card1_obj.color_value:
                return card1_obj
            else:
                return card2_obj
        else:
            if card1_obj.ori_value > card2_obj.ori_value:
                return card1_obj
            else:
                return card2_obj

    def max_in_somecards(self, somecards_list):
        """
        比较多张牌obj的最大值
        :param somecards_list: [obj1,obj2,obj3....]
        :return: 最大值
        """
        from functools import reduce
        max_obj = reduce(self.biger_in_2card,somecards_list)
        return max_obj

    def __repr__(self):
        base_ret = """
        我的牌组：{fiveCards}
        结果：{result}
        倍数：{doubling}
        最大牌：{maxCard}
        """
        ret = base_ret.format(
            fiveCards=self.fiveCards,
            result=self.result["text"],
            doubling=self.result["doubling"],
            maxCard=self.result["maxCard"],
        )

        return ret


class Player(object):
    def __init__(self,name,wager=10,role="玩家",money=0):
        self.name = name
        self.role = role
        self.cards = []
        self.niuniu_result = {}  # {"status":False,"point":0,"maxCard":None,"doubling":1,"text":"无牛"}
        self.money = money
        self.wager = wager

    def __repr__(self):
        return self.name


class Game(NiuNiu):
    pokers = Pokers.cards()

    def __init__(self,zhuang_obj,player_obj_list):
        self.zhuang = zhuang_obj
        self.player_objs = player_obj_list
        self.all_players = [zhuang_obj] + player_obj_list
        self.n_cards = 5


    def giveCards(self,pokers):
        import random
        ALL = random.sample(pokers, len(pokers))
        player_objs = self.all_players
        n_players = len(player_objs)
        n_cards = self.n_cards

        for idx,player in enumerate(player_objs):
            tmp_l = []
            for n in range(n_cards):
                card = ALL[n*n_players+ idx]
                tmp_l.append(card)
            player.cards = tmp_l
            player.niuniu_result = NiuNiu(tmp_l).result


    def compare_2_player(self,zhuang,player):
        """
        比较 庄家 和 闲家 的大小
        :param zhuang:
        :param player:
        :return: True庄赢，False闲赢
        """
        Flag = False
        zhuang_niuniu = zhuang.niuniu_result
        player_niuniu = player.niuniu_result

        if zhuang_niuniu["point"] == player_niuniu["point"]:
            bigerCard = self.max_in_somecards([zhuang_niuniu["maxCard"],player_niuniu["maxCard"]])
            if bigerCard is zhuang_niuniu["maxCard"]:
                Flag = True
        elif zhuang_niuniu["point"] > player_niuniu["point"]:
            Flag = True




        if Flag:
            # 庄家赢了
            money_change = zhuang.niuniu_result["doubling"] * player.wager
            zhuang.money += money_change
            player.money -= money_change
            base_res = "\033[1;31m{zhuang}赢了{money_change}，余额：{money}【{text}，倍数：{doubling}，最大：{maxCard}，牌组：{cards}】\033[0m；{player}输了{money_change}，余额：{money2}【{text2}，赌注：{wager}，倍数：{doubling2}，最大：{maxCard2}，牌组：{cards2}】"
        else:
            # 庄家输了
            money_change = player.niuniu_result["doubling"] * player.wager
            zhuang.money -= money_change
            player.money += money_change
            base_res = "{zhuang}输了{money_change}，余额：{money}【{text}，倍数：{doubling}，最大：{maxCard}，牌组：{cards}】；\033[1;31m{player}赢了{money_change}，余额：{money2}【{text2}，赌注：{wager}，倍数：{doubling2}，最大：{maxCard2}，牌组：{cards2}】\033[0m"


        res = base_res.format(
            zhuang = zhuang,
            money_change = money_change,
            money = zhuang.money,
            text = zhuang.niuniu_result["text"],
            doubling = zhuang.niuniu_result["doubling"],
            maxCard = zhuang.niuniu_result["maxCard"],
            cards = zhuang.cards,
            player = player,
            money2 = player.money,
            text2 = player.niuniu_result["text"],
            wager = player.wager,
            doubling2 = player.niuniu_result["doubling"],
            maxCard2 = player.niuniu_result["maxCard"],
            cards2 = player.cards,
        )



        return res


    def start(self):
        self.giveCards(self.pokers)

        zhuang = self.zhuang
        players = self.player_objs
        for player in players:
            res = self.compare_2_player(zhuang,player)
            print(res)




zhuang = Player("玩家1（庄家）")
l_players = [
    Player("玩家2"),
    Player("玩家3"),
]

game = Game(zhuang,l_players)
for i in range(5):
    print("【第{}局】".format(i+1))
    game.start()
    print("################################")

