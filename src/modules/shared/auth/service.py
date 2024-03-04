from src.core.security import verify_password
from src.modules.shared.user.model import User


def root_service():
    return 'Hello core auth router!'


def hello_service():
    return 'Hello service !!'

async def login_service(session, form_data):
    user = await User.get(session, username = form_data.username)
    if user and verify_password(form_data.password, user.hashed_password):
        return user
    
    return None