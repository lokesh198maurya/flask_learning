from user import User

def authentication(username, password):
    user = User.find_by_username(username)

    if user and user.password == password:
        return user

def idenity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)