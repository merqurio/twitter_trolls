import dataset

sql = dataset.connect('sqlite:///test.sql')
table = sql["users"]


def process_cursor(cursor):
    pass
