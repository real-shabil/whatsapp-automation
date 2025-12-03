from flask import Flask, render_template, request, redirect, url_for, flash
import openpyxl
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Persistent Chrome profile path for WhatsApp Web login
CHROME_PROFILE = "/Users/shabilk/Desktop/whatsapp_profile"

# ----- DIGIT ➜ NUMBER EMOJI -----
DIGIT_TO_EMOJI = {
    "0": "0️⃣",
    "1": "1️⃣",
    "2": "2️⃣",
    "3": "3️⃣",
    "4": "4️⃣",
    "5": "5️⃣",
    "6": "6️⃣",
    "7": "7️⃣",
    "8": "8️⃣",
    "9": "9️⃣",
}

def to_emoji_number(num_str):
    return ''.join(DIGIT_TO_EMOJI.get(d, '') for d in str(num_str))

# ----------------------
# Flask Routes
# ----------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Upload files
        friends_file = request.files.get('friends_file')
        responded_file = request.files.get('responded_file')
        custom_message = request.form.get('custom_message')
        survey_url = request.form.get('survey_url')

        if not friends_file or not custom_message or not survey_url:
            flash("Please provide friends file, custom message, and survey URL.")
            return redirect(request.url)

        # Save uploaded files temporarily
        friends_file.save("friends.xlsx")
        if responded_file:
            responded_file.save("responded.xlsx")

        try:
            # Selenium setup with persistent profile
            chrome_options = Options()
            chrome_options.add_argument(f"user-data-dir={CHROME_PROFILE}")

            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.get("https://web.whatsapp.com")
            flash("WhatsApp Web loaded. Ensure you are logged in.")
            sleep(10)  # Wait for page to load

            # Send first round messages
            wb = openpyxl.load_workbook("friends.xlsx")
            ws = wb.active

            for row in ws.iter_rows(min_row=2, values_only=True):
                try:
                    unique_id, name, _, number = row
                    role_emoji = to_emoji_number(unique_id)

                    # Replace placeholder {code} and {survey_url} in custom message
                    message = custom_message.replace('{code}', role_emoji).replace('{survey_url}', survey_url)

                    url = f"https://web.whatsapp.com/send?phone={number}&text={message}"
                    driver.get(url)
                    sleep(5)
                    send_btn = driver.find_element(By.XPATH, "//span[@data-icon='send']")
                    send_btn.click()
                    sleep(3)
                except Exception as e:
                    print(f"Failed to send to {row}: {e}")

            flash("Messages sent successfully!")

        except Exception as e:
            flash(f"Error initializing WhatsApp Web: {e}")
        finally:
            try:
                driver.quit()
            except:
                pass

        return redirect(request.url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
