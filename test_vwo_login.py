import random
import string
import os
from playwright.sync_api import sync_playwright


def generate_random_email():
    """Generate a random email address."""
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    domains = ["test.com", "example.com", "random.org", "fake.io"]
    domain = random.choice(domains)
    return f"{username}@{domain}"


def generate_random_password():
    """Generate a random password."""
    chars = string.ascii_letters + string.digits + "!@#$%"
    return ''.join(random.choices(chars, k=14))


def test_vwo_invalid_login():
    """
    Test VWO login with invalid credentials and verify error message.
    Steps:
        1. Open https://app.vwo.com/
        2. Enter a random email in the Email ID field
        3. Enter a random password in the Password field
        4. Click the Sign In button
        5. Wait for and verify the error message
        6. Take a screenshot
        7. Close the browser
    """
    random_email = generate_random_email()
    random_password = generate_random_password()

    print(f"\n{'='*60}")
    print("VWO Login Test - Invalid Credentials")
    print(f"{'='*60}")
    print(f"Email    : {random_email}")
    print(f"Password : {random_password}")
    print(f"{'='*60}\n")

    # Create screenshots directory if it doesn't exist
    screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshots_dir, "vwo_login_error.png")

    with sync_playwright() as p:
        # Launch Chromium browser (headless=False to see the browser)
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        try:
            # Step 1: Navigate to VWO login page
            print("Step 1: Navigating to https://app.vwo.com/ ...")
            page.goto("https://app.vwo.com/", wait_until="domcontentloaded")
            page.wait_for_load_state("networkidle")
            print("        ✅ Page loaded successfully")

            # Step 2: Enter random email
            print(f"Step 2: Entering email: {random_email}")
            email_input = page.locator("input[type='email'], input[placeholder*='email' i], input[placeholder*='Email' i]").first
            email_input.wait_for(state="visible")
            email_input.click()
            email_input.fill(random_email)
            print("        ✅ Email entered")

            # Step 3: Enter random password
            print(f"Step 3: Entering password: {random_password}")
            password_input = page.locator("input[type='password']").first
            password_input.wait_for(state="visible")
            password_input.click()
            password_input.fill(random_password)
            print("        ✅ Password entered")

            # Step 4: Click Sign In button
            print("Step 4: Clicking Sign In button ...")
            sign_in_button = page.locator("button:has-text('Sign in'), button[type='submit']").first
            sign_in_button.wait_for(state="visible")
            sign_in_button.click()
            print("        ✅ Sign In button clicked")

            # Step 5: Wait for error message
            print("Step 5: Waiting for error message ...")
            error_locator = page.locator("text=did not match").or_(
                page.locator("text=Invalid credentials")
            ).or_(
                page.locator("[class*='error'], [class*='alert'], [class*='danger']")
            ).first
            error_locator.wait_for(state="visible", timeout=10000)
            error_message = error_locator.inner_text().strip()
            print(f"        ✅ Error message received!")
            print(f"\n{'='*60}")
            print(f"  ERROR MESSAGE: {error_message}")
            print(f"{'='*60}\n")

            # Step 6: Take screenshot
            print(f"Step 6: Taking screenshot → {screenshot_path}")
            page.screenshot(path=screenshot_path, full_page=False)
            print(f"        ✅ Screenshot saved to: {screenshot_path}")

        except Exception as e:
            # Take a failure screenshot if anything goes wrong
            failure_path = os.path.join(screenshots_dir, "vwo_login_failure.png")
            page.screenshot(path=failure_path)
            print(f"        ❌ Test failed: {e}")
            print(f"        Failure screenshot saved to: {failure_path}")
            raise

        finally:
            # Step 7: Close browser
            print("Step 7: Closing browser ...")
            context.close()
            browser.close()
            print("        ✅ Browser closed")
            print("\nTest completed successfully! ✅\n")


if __name__ == "__main__":
    test_vwo_invalid_login()
