from dependency_injector import containers, providers, resources

from exchange.datasource import Database


class DatabaseResource(resources.Resource):
    def init(self, username: str, password: str, host: str, port: int, database: str) -> Database:
        db = Database(username=username, password=password, host=host, port=port, database=database)
        db.connect()
        return db

    def shutdown(self, resource: Database) -> None:
        resource.close()


class Core(containers.DeclarativeContainer):
    config = providers.Configuration()


class Datasources(containers.DeclarativeContainer):
    config = providers.Configuration()

    postgres: providers.Provider[Database] = providers.Resource(
        DatabaseResource,
        username=config.user,
        password=config.password,
        host=config.host,
        port=config.port,
        database=config.db,
    )


class Application(containers.DeclarativeContainer):
    config = providers.Configuration()
    core: providers.Container[Core] = providers.Container(Core, config=config)
    datasources: providers.Container[Datasources] = providers.Container(Datasources, config=config.database)
