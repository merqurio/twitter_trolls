from manual_model import troll_bot_analyzer
from connexion import NoContent


def get_user(user_id):
    u = troll_bot_analyzer(user_id)
    if u:
        return u
    else:
        return NoContent, 500
