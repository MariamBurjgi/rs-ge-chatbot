import requests
import json

# წინა სკრიპტით ნაპოვნი ID
doc_id = "78ff496f-4141-4d48-93e2-5f46fce3f230"

# ვარაუდი: დეტალების ლინკი არის documents/ID
url = f"https://infohubapi.rs.ge/api/documents/{doc_id}"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
    "LanguageCode": "ka",
    "Origin": "https://infohub.rs.ge",
    "Referer": "https://infohub.rs.ge/",
    "Accept": "application/json, text/plain, */*"
}

try:
    print(f"ვამოწმებ ლინკს: {url}")
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        
        # ვეძებ მთავარ ტექსტს (სავარაუდო სახელები: 'body', 'content', 'text')
        keys = data.keys()
        print("\nნაპოვნი ველები:", list(keys))
        
        # ვბეჭდავ ტექსტის ნაწყვეტს, თუ ვიპოვე
        for field in ['body', 'content', 'text', 'description']:
            if field in data and data[field]:
                print(f"\n✅ ტექსტი ნაპოვნია ველში '{field}'!")
                print(f"ტექსტის დასაწყისი: {str(data[field])[:200]}...")
                break
    else:
        print("შეცდომა:", response.text)

except Exception as e:
    print("კრიტიკული შეცდომა:", e)