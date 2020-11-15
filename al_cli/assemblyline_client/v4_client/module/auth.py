from assemblyline_client.v4_client.common.utils import api_path


class Auth(object):
    def __init__(self, connection):
        self._connection = connection

    def logout(self):
        # Requires that the signup process be enabled on Assemblyline's config.yml
        return self._connection.get(api_path('auth/logout'))

    def signup(self, data):
        return self._connection.post(api_path('auth/signup'), data=data)

    def generate_apikey(self, name, priv):
        return self._connection.get(api_path("auth/apikey/{}/{}".format(name, priv)))

    def delete_apikey(self, name):
        return self._connection.delete(api_path("auth/apikey/{}".format(name)))

