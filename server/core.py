
# Load environment configuration
from dotenv import load_dotenv
load_dotenv()

from tool_kit import external


# Configure database connection
db_connection = external.DatabaseConnection()


def needs_session(func):
    def wrapper(*args, **kwargs):
        if 'session' not in kwargs:
            with db_connection.get_new_session() as session:
                kwargs['session'] = session
                return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return wrapper


class Serializable:
    def to_dict(self):
        result = self.__dict__
        for field_name, value in result.items():
            if isinstance(value, list):
                result[field_name] = [item.to_dict() for item in value]
        return result
