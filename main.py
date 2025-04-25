from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from transformers import pipeline
import time

# 🧠 Load open-source summarizer from Hugging Face
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# 🔧 Setup WebDriver
service = Service("path/to/chromedriver")  # <- Replace with your local chromedriver path
driver = webdriver.Chrome(service=service)

# 🌐 Open WhatsApp Web
driver.get("https://web.whatsapp.com")
input("📱 Scan the QR code and press Enter once you're in...\n")

time.sleep(5)

# 🔍 Find chats with unread messages
unread_chats = driver.find_elements(By.XPATH, '//span[@aria-label=" unread message"]')

for i, badge in enumerate(unread_chats[:3]):  # Limit for demo
    try:
        parent = badge.find_element(By.XPATH, './../../..')
        parent.click()
        time.sleep(2)

        # Extract last 10 messages from the chat
        messages = driver.find_elements(By.XPATH, '//div[contains(@class,"message-in")]//span[@class="_11JPr"]')
        text = "\n".join([m.text for m in messages[-10:] if m.text.strip() != ""])

        if not text:
            print(f"\n📭 Chat {i+1} has no readable text.")
            continue

        # Summarize the chat text
        summary = summarizer(text, max_length=60, min_length=15, do_sample=False)[0]['summary_text']

        print(f"\n🧵 Chat {i+1} Summary:\n{summary}")

    except Exception as e:
        print(f"❌ Error with chat {i+1}: {e}")

driver.quit()
