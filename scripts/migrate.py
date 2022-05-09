import os

from dotenv import load_dotenv
import typer
load_dotenv()

from tool_kit.external import DatabaseConnection, SshTunnel


app = typer.Typer()


@app.command()
def curriculum():
    local_connection = DatabaseConnection()
    with local_connection.get_new_session() as local_session:
        result = local_session.execute("""
            select count(*) from course
        """).scalar()
        print(f'{result} courses locally')

    tunnel = SshTunnel(proxy_target_port=3306)
    server_connection = DatabaseConnection(
        host=os.environ['MIGRATION_DB_HOST'],
        username=os.environ['MIGRATION_DB_USERNAME'],
        password=os.environ['MIGRATION_DB_PASSWORD'],
        database_name=os.environ['MIGRATION_DB_NAME'],
        port=3306,
        db_protocol='mysql+mysqldb',
        ssl_tunnel=tunnel
    )
    with server_connection.get_new_session() as server_session:
        result = server_session.execute("""
            select count(*) from course
        """).scalar()
        print(f'{result} courses on the server')


if __name__ == '__main__':
    app()
