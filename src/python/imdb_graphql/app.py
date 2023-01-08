from flask import Flask
from graphql_server.flask import GraphQLView

from .database import engine, init_db, session
from .schema import schema

app = Flask(__name__)
app.Debug = True

default_query = '''
{
  movie(imdbID: "tt0892769") {
    imdbID
  }
}
'''.strip()


app.add_url_rule(
    '/imdb',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        enable_async=True,
        context={'session': session},
        default_query=default_query,
        graphiql=True,
    ),
)


@app.teardown_appcontext
async def shutdown_session(exception=None):
    await engine.dispose()


if __name__ == '__main__':
    init_db()
    app.run()
