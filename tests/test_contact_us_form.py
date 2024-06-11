import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="function", autouse=True)
def goto_page_url(page: Page):
    page.goto("https://webdriveruniversity.com/Contact-Us/contactus.html")
    yield


@pytest.fixture
def form_fields_content() -> dict:
    return {
        "First Name": "John",
        "Last Name": "Doe",
        "Email Address": "john_doe@mail.com",
        "Comments": "Just a test"
    }


def test_page_title(page: Page):
    expect(page).to_have_title("WebDriver | Contact Us")


def test_click_on_navbar_redirects_to_home_page(page: Page):
    page.get_by_role("link", name="WebdriverUniversity.com (New Approach To Learning)").click()

    expect(page).to_have_title("WebDriverUniversity.com")
    expect(page).to_have_url("https://webdriveruniversity.com/index.html")


@pytest.mark.parametrize("expected_empty_field", ["First Name", "Last Name", "Email Address", "Comments"])
def test_submit_form_missing_any_required_field_returns_an_error_message(
        page: Page, expected_empty_field, form_fields_content
):
    del form_fields_content[expected_empty_field]

    for placeholder, content in form_fields_content.items():
        page.get_by_placeholder(placeholder).fill(content)

    page.get_by_role("button", name="SUBMIT").click()

    expect(page.get_by_text("Error: all fields are required"), "should show empty field error message").to_be_visible()


def test_submit_form_with_an_invalid_email_returns_an_error_message(page: Page, form_fields_content):
    form_fields_content.update({"Email Address": "invalid_email"})

    for placeholder, content in form_fields_content.items():
        page.get_by_placeholder(placeholder).fill(content)

    page.get_by_role("button", name="SUBMIT").click()

    expect(page.get_by_text("Error: Invalid email address"), "should show invalid email error message").to_be_visible()


def test_reset_button_clears_all_fields(page: Page, form_fields_content):
    for placeholder, content in form_fields_content.items():
        page.get_by_placeholder(placeholder).fill(content)
        expect(page.get_by_placeholder(placeholder)).not_to_be_empty()

    page.get_by_role("button", name="RESET").click()

    for placeholder in form_fields_content.keys():
        expect(page.get_by_placeholder(placeholder)).to_be_empty()


def test_successfully_submits_a_form(page: Page, form_fields_content):
    for placeholder, content in form_fields_content.items():
        page.get_by_placeholder(placeholder).fill(content)

    page.get_by_role("button", name="SUBMIT").click()

    # But .not_to_be_visible() also passes :/ Why?
    expect(page.get_by_role("heading", name="Thank You for your Message!")).to_be_visible()

    # Using a xpath to locate the HTML tag and then making an assertion always gives a correct result tho
    expect(page.locator("xpath=//div[@id=\"contact_reply\"]/h1")).to_have_text("Thank You for your Message!")
