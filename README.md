https://rs-ge-chatbot-kaedenvn9wy9eu3t24asfl.streamlit.app/
##  ფუნქციონალი
*   **Scraping:** ავტომატურად იღებს დოკუმენტებს საჯარო წყაროდან.
*   **Vector Database:** ინახავს ტექსტებს ვექტორულ ფორმატში (ChromaDB) სწრაფი ძებნისთვის.
*   **AI Integration:** იყენებს OpenAI GPT-4o მოდელს პასუხების გენერაციისთვის.
*   **Citations:** პასუხს ყოველთვის ახლავს წყაროს ბმული.
##  გამოყენებული ტექნოლოგიები
*   **Python 3.11**
*   **LangChain** (Orchestration framework)
*   **ChromaDB** (Vector Store)
*   **OpenAI API** (LLM & Embeddings)
*   **Streamlit** (Frontend)
*   **BeautifulSoup4** (Web Scraping)

##  ლოკალურად გაშვების ინსტრუქცია

თუ გსურთ პროექტის თქვენს კომპიუტერში გაშვება:

1. **დააკლონეთ რეპოზიტორი:**
   ```bash
   git clone https://github.com/MariamBurjgi/rs-ge-chatbot.git
   cd rs-ge-chatbot
2. **დააინსტალირეთ საჭირო ბიბლიოთეკები:**
   ```bash
   pip install -r requirements.txt
 3. **გაიმზადეთ გარემო (.env):**
   პროექტის მთავარ საქაღალდეში შექმენით ფაილი სახელად `.env` და შიგნით ჩაწერეთ თქვენი OpenAI გასაღები:
   ```text
   OPENAI_API_KEY=sk-თქვენი-გასაღები-აქ
4. **მონაცემების განახლება :**
   თუ გსურთ დოკუმენტების თავიდან წამოღება და ბაზის განახლება, გაუშვით ეს ბრძანებები:
   ```bash
   python scraper.py   # დოკუმენტების წამოღება
   python create_db.py # ბაზის შექმნა
5. **აპლიკაციის გაშვება:**
   ```bash
   streamlit run app.py
---
*შენიშვნა: სისტემა ამ ეტაპზე სატესტო რეჟიმშია და დამუშავებული აქვს ბოლო 100 დოკუმენტი.*