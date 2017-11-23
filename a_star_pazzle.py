# -*- coding: utf-8 -*-

from itertools import product
import copy
import time

start = time.time()

# 0 の位置を見つける
def space_founder(board):
    for x, y in product(range(3), range(3)):
        if board[x][y] is 0:
            return x, y

# マンハッタン距離を求める
def manhattan(board_now, board_goal):
    cost = 0
    for x, y, goal_x, goal_y in product(range(3), range(3), range(3), range(3)):
        if board_now[x][y] == board_goal[goal_x][goal_y]:
            cost += abs(x - goal_x) + abs(y - goal_y)
    return int(cost/2)            

# 上下左右の方向をリストで管理している。
directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

# spaceと隣接したノードを入れ替えたノードを作る
def replace(node, direction):
    n = copy.deepcopy(node)
    x, y = n.space
    try: n.board[x][y], n.board[x + direction[0]][y + direction[1]] = n.board[x + direction[0]][y + direction[1]], n.board[x][y]
    except: pass
    # 移動方向が範囲外だった場合、continue
    return n.board

def list_matcher(list1, list2):
    for x, y in product(range(3), range(3)):
        if list1[x][y] != list2[x][y]: return False
    return True

# 結果のリストを表示する
def print_answer(x, num):
    if x is not None:
        num += 1
        print_answer(x.parent_node, num)
        if num > 0:
            print("ゴールまで：", num, "手")
        else:
            print("ーーーゴールですーーー")
        print(x.board[0])
        print(x.board[1])
        print(x.board[2])
        print("")
        print("")



# 全ての状態はこのクラスによって生成される
class Node():
    start = None
    goal = None
    def __init__(self, board):
        self.board = board
        self.space = space_founder(self.board)
        self.parent_node = None
        self.h_star = manhattan(self.board, self.goal)
        self.f_star = 0

    def __getitem__(self, item):
        return self.board[item]

# リスト「OPEN」とリスト「CLOSE」から、メソッド「find」で指定された状態「n」を探し、
# メソッド「remove」で、指定された状態「node」を消去する。
# 「OPEN」  -> 展開可能なノードのリスト
# 「CLOSE」 -> 展開されたノードのリスト
class NodeList(list):
    # リスト「self」の中で0番目から順に見ていって渡されたノードと同じノードがあったらNodeオブジェクト、
    # なかったらNoneを返す。
    def find(self, n):
        for t in range(len(self)):
            if list_matcher(self[t].board, n.board):
                l = self[t]
                if l != []: return l
            else: return None

    def remove(self,node):
        del self[self.index(node)]

# 上下左右の方向をリストで管理している。
directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

# スタートとゴールの設定

Node.start = [
    [0, 2, 3],
    [1, 5, 6],
    [4, 7, 8]
]
'''
Node.start = [
    [8, 6, 7],
    [2, 5, 4],
    [3, 0, 1]
]
#[8, 6, 7, 2, 5, 4, 3, 0, 1]
'''

Node.goal = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

Start = Node(copy.deepcopy(Node.start))
Goal = Node(Node.goal)

# f(n) の初期値は g(n) = 0 なので h(n) と一致する。
Start.f_star = Start.h_star

# リスト「OPEN」とリスト「CLOSE」の初期宣言
openList = NodeList()
closeList = NodeList()

# 第一引数が現在の状態、第二引数が次の状態としてコスト計算
def fPrime(n, m):    
    # 現在の状態からg*(n)=f*(n)-h*(n)を求めることが出来る。
    gStar = lambda n, m: n.f_star - n.h_star
    hStar = lambda m: m.h_star
    cost = 1
    '''
    gStar -> 現在の状態に至るまでに実際にかかったコスト
    hStar -> 次の状態に遷移した時の、ゴールまでの予測コスト
    cost  -> 現在の状態から次の状態に移るまでにかかるコスト
    つまり、

    -> gStar -> 「現在の状態」 -> cost -> 「次の状態」 -> hStar
    
    になる。最後に全部の総和を返している。
    '''
    return gStar(n, m) + hStar(m) + cost

# 「OPEN」にスタートノードを入れて探索開始
openList.append(Start)

while openList:
    # 「OPEN」の中から f*(n) の値が一番小さいノードを n とする。
    n = min(openList, key=lambda x: x.f_star)

    # 見つかったノード n を「OPEN」から消し、「CLOSE」に入れる。
    openList.remove(n)
    closeList.append(n)

    # もし「OPEN」リストに含まれていたノード n がゴールなら探索終了
    if list_matcher(n.board, Node.goal):
        end_node = n
        break
    
    # それ以外なら次に移動可能な方向を探して最大４個のノードを新規に作成する。
    # ここでspaceと隣接している数字とを入れ替える -> 枠外にspaceが出てしまうような場合にはcontinue
    for direction in directions:
        m = Node(replace(n, direction))

        # ノードが「OPEN」と「CLOSE」に含まれているかを確認する。
        om = openList.find(m)
        cm = closeList.find(m)
        
        # 「OPEN」にも「CLOSE」にも含まれていない新規ノード
        fp = fPrime(n, m)

        # m が「OPEN」に含まれていたら上を、m が「CLOSE」に含まれていたら下を実行する。
        om_fp = fPrime(n, om) if om else None
        cm_fp = fPrime(n, cm) if cm else None

        '''
        n  -> 現在の状態
        m  -> 次の状態
        om -> 「OPEN」に m が含まれていた時の状態
        cm -> 「CLOSE」に m が含まれていた時の状態

        fp    -> 現在の状態と次の状態から計算されたコスト
        om_fp -> 現在の状態と「OPEN」に m が含まれていた時の状態から計算されたコスト
        cm_fp -> 現在の状態と「CLOSE」に m が含まれていた時の状態から計算されたコスト
        '''
        # m が「OPEN」にも「CLOSE」にも含まれていなかった時
        if om is None and cm is None:
            m.parent_node = n
            m.f_star = fp
            openList.append(m)

        # m が「OPEN」に含まれていて、元々計算されていた m より今回計算した m の方がコストが小さい時
        elif not om is None and om_fp < om.f_star:
            om.parent_node = n
            om.f_star = om_fp

        # m が「CLOSE」に含まれていて、元々計算されていた m より今回計算した m の方がコストが小さい時
        elif not cm is None and cm_fp < cm.f_star:
            cm.f_star = cm_fp
            closeList.remove(cm)
            openList.append(cm)
        m = Node(replace(n, direction))
        # 最後にdirectionから新たにノードを作成するためにもう一度入れ替える必要がある
else:
    print("入力された盤は解くことが不可能な盤です。偶奇性に注意してもう一度入力してください")


print_answer(n, -1)

print("End Time:",time.time() - start)
