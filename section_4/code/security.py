from user import User

users = [User(1, 'loki', 'afsd8520')]

username_mapping = {ele.username: ele for ele in users}
  
userid_mapping = {ele.id: ele for ele in users}

def authentication(username, password):
    user = username_mapping.get(username, None)

    if user and user.password == password:
        return user

def idenity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)