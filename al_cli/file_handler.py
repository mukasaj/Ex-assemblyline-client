import configparser
import al_var


def create_settings_file():
    # Creating the config.ini file and getting some required info from the user
    configfile = open(al_var.CONFIG_FILE_PATH, "w")

    while True:  # hostname
        host = input("Please enter al host address (ex www.google.com/ 34.74.64.140): ")
        if host != "":
            break
    while True:  # timeout
        timeout = input("Please enter the request timeout[{}]: ".format(al_var.DEFAULT_TIMEOUT))
        if timeout.isdigit() or timeout == "":
            break
    while True:  # username
        username = input("Please enter your username: ")
        if username != "":
            break
    while True:  # apikey
        apikey = input("Please enter your apikey: ")
        if apikey != "":
            break

    configfile.writelines("[server]\n")  # server section
    configfile.writelines("host = {}\n".format(host))
    configfile.writelines("[requests]\n")  # Requests section
    configfile.writelines("timeout = {}\n".format(timeout if timeout != "" else str(al_var.DEFAULT_TIMEOUT)))
    configfile.writelines("[user]\n")  # user section
    configfile.writelines("username = {}\n".format(username))
    configfile.writelines("apikey = {}\n".format(apikey))

    configfile.close()


def update_server():
    config = configparser.ConfigParser()
    config.read(al_var.CONFIG_FILE_PATH)

    # getting new host address
    new_host = input(
        "Please enter the host address [{}]: ".format(
            config['server']['host'] if config.has_option('server', 'host') else ""
        )
    )
    if new_host != "":
        config.set('server', 'host', new_host)

    save_changes(config)


def update_requests():
    config = configparser.ConfigParser()
    config.read(al_var.CONFIG_FILE_PATH)

    while True:
        new_timeout = input(
            "Please enter the request timeout[{}]: ".format(
                config['requests']['timeout'] if config.has_option('requests', 'timeout') else ""
            )
        )
        if new_timeout.isdigit() or new_timeout == "":
            break
    if new_timeout != "":
        config.set('requests', 'timeout', new_timeout)

    save_changes(config)


def update_user():
    config = configparser.ConfigParser()
    config.read(al_var.CONFIG_FILE_PATH)

    # getting new username
    new_username = input(
        "Please enter your username[{}]: ".format(
            config['user']['username'] if config.has_option('user', 'username') else ""
        )
    )
    if new_username != "":
        config.set('user', 'username', new_username)

    # getting new apikey
    new_apikey = input(
        "Please enter your apikey[{}]: ".format(
            config['user']['apikey'] if config.has_option('user', 'apikey') else ""
        )
    )
    if new_apikey != "":
        config.set('user', 'apikey', new_apikey)

    save_changes(config)


def save_changes(config):
    with open(al_var.CONFIG_FILE_PATH, "w+") as configfile:
        config.write(configfile)
        configfile.close()


def update():
    update_server()
    update_requests()
    update_user()
