import requests
import json
import time
from bs4 import BeautifulSoup

# --- კონფიგურაცია ---
BASE_URL = "https://infohubapi.rs.ge/api/documents"

# სულ გვინდა 100 დოკუმენტი
TARGET_TOTAL = 100
# ერთ ჯერზე ვითხოვთ 20-ს (რომ სერვერი არ გაბრაზდეს - 422 შეცდომა არ ამოაგდოს)
BATCH_SIZE = 20

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "LanguageCode": "ka",
    "Origin": "https://infohub.rs.ge",
    "Referer": "https://infohub.rs.ge/",
    "Accept": "application/json, text/plain, */*"
}

def clean_html(html_content):
    if not html_content:
        return ""
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.get_text(separator="\n").strip()
    except:
        return str(html_content)

def get_document_list():
    all_documents = []
    skip = 0
    
    print(f"⏳ ვიწყებ {TARGET_TOTAL} დოკუმენტის შეგროვებას ნაწილ-ნაწილ...")

    while len(all_documents) < TARGET_TOTAL:
        print(f"   ↳ ვითხოვ დოკუმენტებს {skip}-დან {skip + BATCH_SIZE}-მდე...")
        
        params = {
            "skip": skip,
            "take": BATCH_SIZE,
            "species": "NewDocument"
        }
        
        try:
            response = requests.get(BASE_URL, headers=HEADERS, params=params)
            if response.status_code == 200:
                data = response.json().get("data", [])
                if not data:
                    print("   ⚠️ მეტი დოკუმენტი აღარ არის.")
                    break
                
                all_documents.extend(data)
                skip += BATCH_SIZE # შემდეგ ჯერზე შემდეგი 20-ის წამოღება
                time.sleep(0.5) # შესვენება
            else:
                print(f"❌ შეცდომა: {response.status_code}")
                break
        except Exception as e:
            print(f"❌ კრიტიკული შეცდომა: {e}")
            break
            
    return all_documents[:TARGET_TOTAL] # ზუსტად იმდენს ვაბრუნებთ, რამდენიც გვინდოდა

def get_document_details(doc_id):
    url = f"{BASE_URL}/{doc_id}/details-by-key?openFromSearch=false"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            raw_html = data.get("body") or data.get("description") or data.get("content") or ""
            return clean_html(raw_html)
        return None
    except:
        return None

def main():
    documents = get_document_list()
    
    if not documents:
        print("❌ სია ცარიელია.")
        return

    print(f"\n✅ სულ შეგროვდა {len(documents)} დოკუმენტის სათაური. ვიწყებ შინაარსის წამოღებას...\n")

    final_data = []

    for i, doc in enumerate(documents):
        doc_id = doc.get("uniqueKey")
        title = doc.get("title")
        doc_number = doc.get("documentNumber")
        
        if not title:
            if doc_number:
                title = f"ბრძანება №{doc_number}"
            else:
                title = "დოკუმენტი (სათაურის გარეშე)"
            
        print(f"[{i+1}/{len(documents)}] ვამუშავებ: {str(title)[:50]}...")
        
        if not doc_id:
            continue

        full_text = get_document_details(doc_id)
        
        if full_text and len(full_text) > 10: 
            if title == "დოკუმენტი (სათაურის გარეშე)":
                title = full_text[:60].replace("\n", " ") + "..."

            entry = {
                "id": doc_id,
                "title": title,
                "date": doc.get("receiptDate", ""),
                "content": full_text,
                "url": f"https://infohub.rs.ge/ka/workspace/document/{doc_id}",
                "type": doc.get("typeName", "დოკუმენტი")
            }
            final_data.append(entry)
        
        time.sleep(0.1)

    if final_data:
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print(f"\n🎉 გილოცავ! {len(final_data)} დოკუმენტი შენახულია!")
    else:
        print("\n⚠️ სამწუხაროდ, ვერცერთი დოკუმენტის ტექსტი ვერ ამოვიღე.")

if __name__ == "__main__":
    main()