import streamlit as st
import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

# კონფიგურაცია 
load_dotenv()

st.set_page_config(page_title="InfoHub AI ასისტენტი", page_icon="🤖")

@st.cache_resource
def load_chain():
    if not os.getenv("OPENAI_API_KEY"):
        st.error("❌ API გასაღები ვერ ვიპოვე! გთხოვთ შეამოწმოთ .env ფაილი.")
        return None

    # შეცვალე სახელი
    embedding_function = OpenAIEmbeddings()
    vectorstore = Chroma(persist_directory="./chroma_fixed", embedding_function=embedding_function)
    #  k=10 (უფრო მეტ დოკუმენტს გადახედავს)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 50})

    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

    template = """
    შენ ხარ შემოსავლების სამსახურის (RS.GE) ვირტუალური ასისტენტი.
    შენი მიზანია დაეხმარო მომხმარებელს ინფორმაციის მოძიებაში.
    
    ინსტრუქცია:
    ქვემოთ მოცემულია დოკუმენტების ნაწყვეტები. მოძებნე პასუხი ამ ტექსტებში.
    თუ კითხვა ეხება კონკრეტულ ნომერს (მაგ: 2926), აუცილებლად მოძებნე ტექსტში, სადაც ეს ნომერი წერია.
    
    თუ ინფორმაცია კონტექსტში არ არის, თქვი: "სამწუხაროდ, ამ საკითხზე ინფორმაცია მოწოდებულ დოკუმენტებში არ იძებნება."
    
    კონტექსტი:
    {context}
    
    კითხვა: {question}
    
    პასუხი (ქართულად):
    """
    
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    
    return qa_chain

# --- UI ---

st.title("🤖 InfoHub AI კონსულტანტი")
st.markdown("დასვი კითხვა RS.GE-ს დოკუმენტებიდან.")

chain = load_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("დასვი კითხვა..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if chain:
            with st.spinner("ვეძებ ინფორმაციას..."):
                try:
                    response = chain.invoke({"query": prompt})
                    answer = response["result"]
                    source_docs = response["source_documents"]
                    
                    st.markdown(answer)
                    
                    if source_docs:
                        st.markdown("---")
                        st.caption("📚 **შესაძლო წყაროები:**")
                        unique_sources = set()
                        for doc in source_docs:
                            source_url = doc.metadata.get("source", "#")
                            source_title = doc.metadata.get("title", "დოკუმენტი")
                            
                            #  ფილტრი: მხოლოდ უნიკალური სათაურები გამოიტანოს
                            if source_title not in unique_sources:
                                st.markdown(f"- [{source_title}]({source_url})")
                                unique_sources.add(source_title)
                    
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                except Exception as e:
                    st.error(f"შეცდომა: {e}")
        else:
            st.error("სისტემა არ არის მზად.")