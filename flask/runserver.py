from notejam import app
import os

username_env_var = os.environ.get('username', 'defaultuser')
password_env_var = os.environ.get('password', 'defaultpassword')
server_env_var = os.environ.get('server', 'defaultserver')

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://{username_env_var}:{password_env_var}@{server_env_var}/testdb".format(username, password, server)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
