import random

board = [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]]


# 打印游戏界面
def display(board, score):
    print('{0:4} {1:4} {2:4} {3:4}'.format(board[0][0], board[0][1], board[0][2], board[0][3]))
    print('{0:4} {1:4} {2:4} {3:4}'.format(board[1][0], board[1][1], board[1][2], board[1][3]))
    print('{0:4} {1:4} {2:4} {3:4}'.format(board[2][0], board[2][1], board[2][2], board[2][3]))
    print('{0:4} {1:4} {2:4} {3:4}'.format(board[3][0], board[3][1], board[3][2], board[3][3]), '      分数:', score)


# 初始化游戏,在4*4里面随机生成两个2
def init(board):
    # 游戏先都重置为0
    for i in range(4):
        for j in range(4):
            board[i][j] = 0
    # 随机生成两个2保存的位置
    randomposition = random.sample(range(0, 15), 2)
    board[int(randomposition[0] / 4)][randomposition[0] % 4] = 2
    board[int(randomposition[1] / 4)][randomposition[1] % 4] = 2


def addSameNumber(boardList, direction):
    '''需要在列表中查找相邻相同的数字相加，返回增加的分数

    :param boardList: 经过对齐非零的数字处理过后的二维数组
    :param direction: direction == 'left'从右向左查找，找到相同且相邻的两个数字，左侧数字翻倍，右侧数字置0
                      direction == 'right'从左向右查找，找到相同且相邻的两个数字，右侧数字翻倍，左侧数字置0
    :return:
    '''
    addNumber = 0
    # 向左以及向上的操作
    if direction == 'left':
        for i in [0, 1, 2]:
            if boardList[i] == boardList[i+1] != 0:
                boardList[i] *= 2
                boardList[i + 1] = 0
                addNumber += boardList[i]
                return {'continueRun': True, 'addNumber': addNumber}
        return {'continueRun': False, 'addNumber': addNumber}
    # 向右以及向下的操作
    else:
        for i in [3, 2, 1]:
            if boardList[i] == boardList[i-1] != 0:
                boardList[i] *= 2
                boardList[i - 1] = 0
                addNumber += boardList[i]
                return {'continueRun': True, 'addNumber': addNumber}
        return {'continueRun': False, 'addNumber': addNumber}


def align(boardList, direction):
    '''对齐非零的数字

    direction == 'left'：向左对齐，例如[8,0,0,2]左对齐后[8,2,0,0]
    direction == 'right'：向右对齐，例如[8,0,0,2]右对齐后[0,0,8,2]
    '''
    # 先移除列表里面的0，如[8,0,0,2]->[8,2],1.先找0的个数，然后依照个数进行清理
    # boardList.remove(0)：移除列表中的某个值的第一个匹配项，所以[8,0,0,2]会移除两次0
    for x in range(boardList.count(0)):
        boardList.remove(0)
    # 移除的0重新补充回去,[8,2]->[8,2,0,0]
    if direction == 'left':
        boardList.extend([0 for x in range(4 - len(boardList))])
    else:
        boardList[:0] = [0 for x in range(4 - len(boardList))]


def handle(boardList, direction):
    '''
    处理一行（列）中的数据，得到最终的该行（列）的数字状态值, 返回得分
    :param boardList: 列表结构，存储了一行（列）中的数据
    :param direction: 移动方向,向上和向左都使用方向'left'，向右和向下都使用'right'
    :return: 返回一行（列）处理后加的分数
    '''
    addscore = 0
    # 先处理数据，把数据都往指定方向进行运动
    align(boardList, direction)
    result = addSameNumber(boardList, direction)
    # 当result['continueRun'] 为True，代表需要再次执行
    while result['continueRun']:
        # 重新对其，然后重新执行合并，直到再也无法合并为止
        addscore += result['addNumber']
        align(boardList, direction)
        result = addSameNumber(boardList, direction)
    # 直到执行完毕，及一行的数据都不存在相同的
    return {'addscore': addscore}


# 游戏操作函数，根据移动方向重新计算矩阵状态值，并记录得分
def operator(board):
    # 每一次的操作所加的分数，以及操作后游戏是否触发结束状态（即数据占满位置）
    addScore = 0
    gameOver = False
    # 默认向左
    direction = 'left'
    op = input("请输入您的操作:")
    if op in ['a', 'A']:
        # 方向向左
        direction = 'left'
        # 一行一行进行处理
        for row in range(4):
            addScore += handle(board[row], direction)['addscore']

    elif op in ['d', 'D']:
        direction = 'right'
        for row in range(4):
            addScore += handle(board[row], direction)['addscore']

    elif op in ['w', 'W']:
        # 向上相当于向左的转置处理
        direction = 'left'
        board = list(map(list, zip(*board)))
        # 一行一行进行处理
        for row in range(4):
            addScore += handle(board[row], direction)['addscore']
        board = list(map(list, zip(*board)))

    elif op in ['s', 'S']:
        # 向下相当于向右的转置处理
        direction = 'right'
        board = list(map(list, zip(*board)))
        # 一行一行进行处理
        for row in range(4):
            addScore += handle(board[row], direction)['addscore']
        board = list(map(list, zip(*board)))
    else:
        print("错误输入！请输入[W, S, A, D]或者对应小写")
        return {'gameOver': gameOver, 'addScore': addScore, 'board': board}

    # 每一次操作后都需要判断0的数量，如果满了，则游戏结束
    number_0 = 0
    for q in board:
        # count(0)是指0出现的个数,是扫描每一行的
        number_0 += q.count(0)
    # 如果number_0为0，说明满了
    if number_0 == 0:
        gameOver = True
        return {'gameOver': gameOver, 'addScore': addScore, 'board': board}
    # 说明还没有满，则在空的位置上加上一个2或者4，概率为3：1
    else:
        addnum = random.choice([2,2,2,4])
        position_0_list = []
        # 找出0的位置，并保存起来
        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    position_0_list.append(i*4 + j)
    # 在刚才记录的0的位置里面随便找一个，然后替换成生成的2或者4
    randomposition = random.sample(position_0_list, 1)
    board[int(randomposition[0] / 4)][randomposition[0] % 4] = addnum
    return {'gameOver': gameOver, 'addScore': addScore, 'board': board}


if __name__ == '__main__':
    print('输入：W(上) S(下) A(左) D(右).')
    # 初始化游戏界面，游戏分数
    gameOver = False
    init(board)
    score = 0
    # 游戏未结束，则一直运行
    while gameOver != True:
        display(board, score)
        operator_result = operator(board)
        board = operator_result['board']
        if operator_result['gameOver'] == True:
            print("游戏结束，你输了！")
            print("你的最终得分:", score)
            gameOver = operator_result['gameOver']
            break
        else:
            # 加上这一步的分
            score += operator_result['addScore']
            if score >= 2048:
                print("牛啊牛啊，你吊竟然赢了！")
                print("你的最终得分:", score)
                # 结束游戏
                gameOver = True
                break