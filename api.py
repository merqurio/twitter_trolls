from manual_model import troll_bot_analyzer
from connexion import NoContent

def get_user(user_id):
	print("Starting troll_bot_analyzer")
    u = troll_bot_analyzer(user_id)
	print("troll_bot_analyzer finished")
    if u:
        return u
    else:
        return NoContent, 500
