# WhatsApp Automation Web App

This project is a **WhatsApp automation tool** with a Web UI built using Flask and Selenium. It allows users to send **custom messages** to multiple contacts stored in an Excel file, including **unique role numbers in emoji style** and a **survey URL**.

---

## Features

- Upload `friends.xlsx` and optional `responded.xlsx` files.
- Custom message template with placeholders:
  - `{code}` → replaced with role number in emoji style.
  - `{survey_url}` → replaced with your mandatory survey URL.
- 2-stage messaging: first message to all, reminder to non-responders.
- Persistent WhatsApp login using a dedicated Chrome profile.
- Logs sent messages and errors via web interface.

---

## Prerequisites

- Python 3.10 or higher
- Google Chrome installed
- WhatsApp account logged in on Chrome

---

## Setup Instructions

1. **Clone the repository:**

```bash
git clone https://github.com/real-shabil/whatsapp-automation.git
cd whatsapp-automation
```

2. **Create and activate a virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Create a dedicated Chrome profile for WhatsApp:**

- Open Chrome and create a new profile.
- Scan the WhatsApp Web QR code once in that profile.
- Note the profile path and update `CHROME_PROFILE` in `app.py`.

5. **Prepare Excel files:**

- `friends.xlsx` should have columns: `Unique_ID`, `Name`, `Department`, `Mob_number`
- `responded.xlsx` should have column: `Mob_number` (optional, for reminders)

6. **Run the Flask app:**

```bash
python app.py
```

- Open browser at: `http://127.0.0.1:5000/`
- Upload Excel files, enter **custom message** with `{code}` and `{survey_url}`, then click **Start**.

---

## Notes

- Keep Chrome open while sending messages to preserve the session.
- `{code}` in the message will be replaced with emoji numbers.
- You can run the first round and second round separately.

---

## Git Usage

- To push future changes:

```bash
git add .
git commit -m "Your commit message"
git push
```

---

## License

MIT License
