from flask import Flask


def init_app(app: Flask):
    @app.errorhandler(413)
    def max_lenght(error):
        return {'message': f"{str(error).split(': ')[-1]} Maximum upload limit: 1MB"}, 413
