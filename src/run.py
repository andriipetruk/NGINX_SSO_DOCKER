from microservice import create_app

app = create_app('settings.production')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
