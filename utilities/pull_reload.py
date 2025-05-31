import time

import winrm
from config.config_data import RemoteConnection as RC
from config.config_data import PersonData as pers_data

remote_address = RC.remote_address
username = pers_data.person_login
password = pers_data.person_password
app_pool_CTT = RC.app_pool_name_CTT
app_pool_admin = RC.app_pool_name_admin


class Session:
    session = winrm.Session(
        remote_address,
        auth=(username, password),
        transport='ntlm',
        server_cert_validation='ignore')

    @staticmethod
    def restart_pull_CTT():
        restart_cmd = f'Restart-WebAppPool {app_pool_CTT}'
        Session.session.run_ps(restart_cmd)
        time.sleep(2)

    @staticmethod
    def restart_pull_admin():
        restart_cmd = f'Restart-WebAppPool {app_pool_admin}'
        Session.session.run_ps(restart_cmd)
        time.sleep(2)

