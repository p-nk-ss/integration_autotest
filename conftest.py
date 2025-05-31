import time
from playwright.sync_api import Playwright, Page
import pytest
from config.config_data import PersonData
from sql.sql_for_conftest import Conftest
from config import env_config as env

user_mail = PersonData.person_email
password = PersonData.person_password

ctt_personal_url = env.config['ctt_personal']
cbp_absence_url = env.config['cbp_absence_type']
cbp_work_types_url = env.config['cbp_work_types']
cbp_compackage_url = env.config['cbp_compackage']
admin_settings_url = env.config['admin_ctt_settings']
admin_hours_off_url = env.config['admin_hours_off']
admin_compackage_url = env.config['admin_compackage']



@pytest.fixture
def setup_page(page: Page):
    def setup_url(url, max_retries=3, goto_timeout=180000, load_state_timeout=120000):
        test_page = page.context.new_page()
        retries = 0
        while retries < max_retries:
            try:
                test_page.goto(url, timeout=goto_timeout)
                break
            except TimeoutError:
                retries += 1
                test_page.reload()
        else:
            raise Exception(f"Failed to load the URL {url} after {max_retries} retries.")

        test_page.wait_for_load_state("networkidle", timeout=load_state_timeout)
        sql.delete_tt()
        try:
            yield test_page
        finally:
            test_page.close()
            sql.delete_tt()
    return setup_url


@pytest.fixture
def setup_browser(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    yield browser
    browser.close()

def open_authenticated_page(browser, url: str):
    context = browser.new_context(http_credentials={
        "username": user_mail,
        "password": password
    })
    page = context.new_page()
    page.goto(url)
    page.wait_for_load_state(state="networkidle", timeout=30000)
    return page, context

@pytest.fixture
def setup_cbp_counters(setup_browser):
    sql_tt = Conftest()
    sql_tt.delete_person_TT()

    page, context = open_authenticated_page(setup_browser, cbp_absence_url)
    yield page

    context.close()
    sql_tt.delete_person_TT()

@pytest.fixture
def setup_cbp_work_types(setup_browser):
    page, context = open_authenticated_page(setup_browser, cbp_work_types_url)
    yield page
    context.close()

@pytest.fixture
def setup_cbp_compackage(setup_browser):
    page, context = open_authenticated_page(setup_browser, cbp_compackage_url)
    yield page
    context.close()


@pytest.fixture
def setup_ctt(setup_page):
    sql_tt = Conftest()
    sql_tt.delete_person_TT()
    yield from setup_page(ctt_personal_url)
    sql_tt.delete_person_TT()

