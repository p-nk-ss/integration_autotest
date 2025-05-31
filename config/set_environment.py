import json
import sys
import environment

environmentQA = "QA"
environmentQAPROD = "QAPROD"


def set_environment(env_name):
    env = {}

    if env_name == 'QA':
        env = {
            "env_name": environment.EnvironmentQA.env_name,
            "admin_hours_off": environment.EnvironmentQA.admin_qa_hours_off,
            "admin_compackage": environment.EnvironmentQA.admin_qa_compackage,
            "cbp_absence_type": environment.EnvironmentQA.cbp_qa_absence_type,
            "cbp_work_types": environment.EnvironmentQA.cbp_qa_work_types,
            "cbp_compackage": environment.EnvironmentQA.cbp_qa_compackage,
            "ctt_personal": environment.EnvironmentQA.ctt_qa_personal,

            "dataBase_ESD": environment.EnvironmentQA.DataBase_ESD_QA,
            "dataBase_CTT": environment.EnvironmentQA.DataBase_CTTQA1438,
            "table_CTT": environment.EnvironmentQA.Table_CTT_QA,
            "table_ESD": environment.EnvironmentQA.Table_ESD,
            "remote_address": environment.EnvironmentQA.remote_address,
            "app_pool_name_ctt": environment.EnvironmentQA.app_pool_name_ctt_qa,
            "app_pool_name_admin": environment.EnvironmentQA.app_pool_name_admin_qa
        }


    elif env_name == 'QAPROD':
        env = {
            "env_name": environment.EnvironmentQAPROD.env_name,
            "admin_hours_off": environment.EnvironmentQAPROD.admin_qaprod_hours_off,
            "admin_compackage": environment.EnvironmentQAPROD.admin_qaprod_compackage,
            "cbp_absence_type": environment.EnvironmentQAPROD.cbp_qaprod_absence_type,
            "cbp_work_types": environment.EnvironmentQAPROD.cbp_qaprod_work_types,
            "cbp_compackage": environment.EnvironmentQAPROD.cbp_qaprod_compackage,
            "ctt_personal": environment.EnvironmentQAPROD.ctt_qaprod_personal,

            "dataBase_ESD": environment.EnvironmentQAPROD.DataBase_ESD_QAPROD,
            "dataBase_CTT": environment.EnvironmentQAPROD.DataBase_CTT_QAPROD,
            "table_CTT": environment.EnvironmentQAPROD.Table_CTT_QAPROD,
            "table_ESD": environment.EnvironmentQAPROD.Table_ESD,
            "remote_address": environment.EnvironmentQAPROD.remote_address,
            "app_pool_name_ctt": environment.EnvironmentQAPROD.app_pool_name_ctt_qaprod,
            "app_pool_name_admin": environment.EnvironmentQAPROD.app_pool_name_admin_qaprod
        }
    with open('env_config.py', 'w') as outfile:
        outfile.write("config = ")
        json.dump(env, outfile, indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid environment name. Usage: python SetEnvironment.py <environment_name>."
              " Available environments: QA, QAPROD")
        sys.exit(1)

    env_name = sys.argv[1]
    set_environment(env_name)
