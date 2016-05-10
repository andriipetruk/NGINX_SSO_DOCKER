from flask.ext.script import Manager, Server
from microservice import create_app

app = create_app()
manager = Manager(app)

manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0')
)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=3).run(tests)


if __name__ == "__main__":
    manager.run()
