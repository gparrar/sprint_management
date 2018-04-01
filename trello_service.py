from trello import TrelloClient
from collections import Counter
from constants import TRELLO_API_KEY, TRELLO_API_SECRET, TRELLO_TOKEN, TRELLO_TOKEN_SECRET

client = TrelloClient(
    api_key= TRELLO_API_KEY,
    api_secret= TRELLO_API_SECRET,
    token= TRELLO_TOKEN,
    token_secret= TRELLO_TOKEN_SECRET
)

def my_board(name):
    board_id = ''
    all_boards = client.list_boards()
    for board in all_boards:
        if board.name == name:
            board_id = board.id
            pass
    board = client.get_board(board_id)
    return board

def my_list(board, my_list):
    list_id = ''
    origin_lists = board.list_lists()
    for lista in origin_lists:
        if lista.name == my_list:
            list_id = lista.id
            pass
    list = board.get_list(list_id)
    return list

def member_name(member_id):
	member_name = client.get_member(member_id).fetch().full_name
	return member_name

def get_list_info(list):
    tasks = []
    labels =  []
    members =  []
    card_list = list.list_cards()
    for card in card_list:
        tasks.append(card.name)
        for label in card.labels:
            labels.append(label.name)
        for member in card.member_id:
            members.append(member_name(member))
    return Counter(labels), Counter(members), len(card_list), tasks

def prepare_next_sprint(sprint_name, board):
    name = 'Done %s' % (sprint_name)
    board.add_list(name, pos='bottom')
    new_list = my_list(board, name)
    done = my_list(board, 'Done')
    done.move_all_cards(new_list)
