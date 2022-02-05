
# Load environment configuration
from dotenv import load_dotenv
load_dotenv()

from tool_kit import external


# Configure database connection
db_connection = external.DatabaseConnection()
