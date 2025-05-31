

class EnvironmentQA:
    env_name = "QA"
    admin_qa_hours_off = 'https://cttqa-admin/hours-off-counters'
    admin_qa_compackage = "https://cttqa-admin/compensation-packages"
    cbp_qa_absence_type = "https://cbp.qa.ds.infopulse.local/services/time-tracking-absence-types"
    cbp_qa_work_types = "https://cbp.qa.ds.infopulse.local/subtypes"
    cbp_qa_compackage = "https://cbp.qa.ds.infopulse.local/packages/packages"
    ctt_qa_personal = 'https://cttqa-ext/content/personalview'

    DataBase_ESD_QA = 'CI1-TST\\QA'
    DataBase_CTTQA1438 = 'CI6-TST\\QA,1438'
    Table_CTT_QA = 'QA'
    Table_ESD = 'ESD'

    remote_address = 'qa-vm'
    app_pool_name_ctt_qa = 'QA_WebApi'
    app_pool_name_admin_qa = "QA_Admin_WebApi"


class EnvironmentQAPROD:
    env_name = "QAPROD"
    cbp_qaprod_absence_type = 'https://cbp.qaprod.ds.infopulse.local/services/time-tracking-absence-types'
    cbp_qaprod_work_types = 'https://cbp.qaprod.ds.infopulse.local/subtypes'
    cbp_qaprod_compackage = "https://cbp.qaprod.ds.infopulse.local/packages/packages"
    admin_qaprod_hours_off = 'https://cttqaprod-admin/hours-off-counters'
    admin_qaprod_compackage = 'https://cttqaprod-admin/compensation-packages'
    ctt_qaprod_personal = 'https://cttqaprod-ext/content/personalview'

    DataBase_CTT_QAPROD = 'CI6-TST\\CTTQA,1438'
    DataBase_ESD_QAPROD = 'CI4-TST\\qaprod'
    Table_ESD = 'ESD'
    Table_CTT_QAPROD = 'QAPROD'

    remote_address = '01-qa-vm'
    app_pool_name_ctt_qaprod = 'QAPROD_WebApi'
    app_pool_name_admin_qaprod = 'QAPROD_Admin_WebApi'



