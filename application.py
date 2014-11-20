from wsgiref.simple_server import make_server
from pyramid.session import SignedCookieSessionFactory
from pyramid.config import Configurator

def main():
    my_session_factory = SignedCookieSessionFactory('C8TWB9q1H16jkFCThU4i')
    config = Configurator()
    config.set_session_factory(my_session_factory)
    config.include('pyramid_chameleon')
    config.scan("views")
    config.add_static_view('static', 'static/',
                           cache_max_age=86400)
    app = config.make_wsgi_app()
    return app

if __name__ == '__main__':
    app = main()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()