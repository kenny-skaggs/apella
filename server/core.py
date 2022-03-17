from enum import Enum, auto
import functools

# Load environment configuration
from dotenv import load_dotenv
load_dotenv()

from tool_kit import external


# Configure database connection
db_connection = external.DatabaseConnection()


def needs_session(func):

    @functools.wraps(func)
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
            if isinstance(value, list) and len(value) > 0 and hasattr(value[0], 'to_dict'):
                result[field_name] = [item.to_dict() for item in value]
        return result


class Role(Enum):
    AUTHOR = auto()
    TEACHER = auto()
    STUDENT = auto()

    def __str__(self):
        return self.name.lower()


class Permission(Enum):
    VIEW = 1
    EDIT = 2
