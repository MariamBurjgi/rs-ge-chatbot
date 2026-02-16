import json
import os
import time
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# გარემოს ცვლადების წაკითხვა
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    print("❌ შეცდომა: OPENAI_API_KEY ვერ ვიპოვე .env ფაილში!")
    exit()

# დამხმარე ფუნქცია, რომელიც სიას პატარა ნაწილებად (Batches) ყოფს
def batch_process(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

def create_vector_db():
    print("📂 ვიწყებ data.json-ის წაკითხვას...")
    
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ data.json ვერ ვიპოვე!")
        return

    documents = []
    
    # ტექსტის მომზადება
    for entry in data:
        content = entry.get("content", "")
        metadata = {
            "source": entry.get("url", ""),
            "title": entry.get("title", "სათაურის გარეშე"),
            "date": entry.get("date", "")
        }
        if content:
            doc = Document(page_content=content, metadata=metadata)
            documents.append(doc)

    print(f"✅ წავიკითხე {len(documents)} დოკუმენტი.")

    # ტექსტის დაჭრა
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    splits = text_splitter.split_documents(documents)
    print(f"🔪 ტექსტი დავჭერი {len(splits)} პატარა ნაწილად.")

    # --- აქ არის ცვლილება: ნაწილ-ნაწილ გაგზავნა ---
    print("🧠 ვიწყებ ბაზის შევსებას (ნაწილ-ნაწილ)...")
    
    persist_directory = "./chroma_fixed"
    embedding_function = OpenAIEmbeddings()
    
    # ვქმნით ცარიელ ბაზას ან ვიღებთ არსებულს
    vectorstore = Chroma(
        persist_directory=persist_directory, 
        embedding_function=embedding_function
    )
    
    # მონაცემებს ვუშვებთ 40-40 ნაწილად (რომ ლიმიტს არ გადავცდეთ)
    batch_size = 40
    total_batches = (len(splits) + batch_size - 1) // batch_size

    for i, batch in enumerate(batch_process(splits, batch_size)):
        print(f"   ⏳ ვამუშავებ ნაწილს {i+1}/{total_batches}...")
        try:
            vectorstore.add_documents(documents=batch)
            time.sleep(0.5) # პატარა პაუზა სუნთქვისთვის
        except Exception as e:
            print(f"⚠️ შეცდომა ამ ნაწილზე: {e}")

    print(f"🎉 ბაზა წარმატებით შეიქმნა/განახლდა '{persist_directory}' საქაღალდეში!")

if __name__ == "__main__":
    create_vector_db()