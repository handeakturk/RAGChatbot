# RAG Chatbot

PDF belgelerini işlemek ve analiz etmek için tasarlanmış akıllı bir soru-cevaplama sistemidir. FastAPI, Azure OpenAI, Milvus ve SQLAlchemy kullanılarak geliştirilmiştir. Kullanıcıların **T. İş Bankası Temmuz 2023 Halka Arzı - İhraççı Bilgi Dokümanı** üzerinden sorular sormasına olanak tanır ve belgelerden bağlama duyarlı, doğru yanıtlar sağlar.

## Demo

Proje demosunu izlemek için [YouTube](https://www.youtube.com/watch?v=4-o1sY0wQM0).

---

## Genel Bakış

Bu proje, önceden tanımlanmış PDF dosyalarını işleyen, vektör veri tabanına indeksleyen ve kullanıcıların içerikle ilgili sorular sormasına olanak tanıyan bir Retrieval-Augmented Generation (RAG) chatbotudur.

**Şekil 1:** Streamlit Arayüzü
![Arayüz Örneği](chatbot_project/static/img/streamlit.png)


**Şekil 2:** PDF Belgesindeki İlgili Bölüm

![Arayüz Örneği](chatbot_project/static/img/dokuman.png)


### Temel Teknolojiler

1. **FastAPI**: API istekleri için yüksek performanslı bir backend sağlar.
2. **Azure OpenAI**: Embedding oluşturma ve doğal dil yanıtları için GPT modellerini kullanır.
3. **Milvus**: Benzerlik tabanlı aramalar için vektör veri tabanı.
4. **SQLAlchemy ve Alembic**: Yapılandırılmış veritabanı etkileşimleri ve geçişleri yönetir.
5. **Microsoft SQL Server**: Kullanıcı sorgularını, yanıtlarını ve performans metriklerini kaydeder.
6. **Streamlit**: Chatbot ile etkileşimli bir kullanıcı arayüzü sunar.

---

## Özellikler

1. **Önceden İndekslenmiş PDF**: Önceden tanımlı bir PDF üzerinden sorgu yanıtlar.
2. **Bağlam Duyarlı Soru-Cevaplama**: GPT ile belge embedding'lerini birleştirerek alakalı yanıtlar sağlar.
3. **Ölçeklenebilir Altyapı**: Milvus ile yüksek hızlı vektör benzerlik aramaları yapılır.
4. **Kapsamlı Kayıt Tutma**: MSSQL kullanarak kullanıcı sorgularını ve performans metriklerini takip eder.
5. **Streamlit Arayüzü**: Kullanıcı dostu bir etkileşim platformu sağlar.

---

## Kullanım Senaryoları

**Kurumsal Araştırmalar**

- Örnek: "Banka’nın sürdürülebilirlik stratejisi hakkında bilgi verir misin?"
- Örnek: "TSKB çevresel yönetim sistemi hakkında bilgi verir misin?"
- Örnek: "Sözleşme ihlalleri için belirtilen cezalar nelerdir?"

---

## Şema

1. **PDF**: Sistem, statik bir PDF dosyasını  kullanır, bu dosya önceden işlenir ve indekslenir.
2. **Embedding**: Belgeler daha küçük parçalara bölünür ve Azure OpenAI kullanılarak vektör embedding'lerine dönüştürülür.
3. **Vektör Database**: Embedding'ler, benzerlik tabanlı sorgular için Milvus'ta saklanır.
4. **Sorgu İşleme**: Kullanıcı sorguları işlenir, vektörleştirilir ve saklanan embedding'lerle eşleştirilir.
5. **Yanıt Oluşturma**: İlgili belge bölümleri alınır ve bağlam duyarlı yanıt oluşturmak için GPT'ye iletilir.
6. **Kayıt Tutma**: MSSQL kullanılarak kullanıcı etkileşimleri kaydedilir ve denetlenir.

### Mimari Diyagram

```
+----------------+       +------------------+       +----------------+       +-----------------+
| Kullanıcı Sorgusu| ----> | FastAPI Backend  | ----> | Milvus Vektör   | ----> | Azure OpenAI     |
| (Streamlit UI) |       | (Sorgu İşleme)   |       | (Veri Getirme)  |       | (Yanıt Oluşturma)|
+----------------+       +------------------+       +----------------+       +-----------------+
                     |                                                     |
                     v                                                     v
               +-------------+                                     +---------------+
               |   MSSQL     | <---------------------------------> |   Kayıt Tutma  |
               +-------------+                                     +---------------+
```

---

## Proje Yapısı

```
chatbot_project/
├── app/
│   ├── configs/
│   │   ├── config.py         # Uygulama yapılandırması
│   │   ├── database.py       # Veritabanı bağlantı mantığı
│   │   ├── embedEtcd.yaml    # Ek yapılandırma dosyaları
│   │   ├── user.yaml         # Kullanıcı yapılandırmaları
│   ├── doc/
│   │   └── banka.pdf         # İşlenen PDF dosyası
│   ├── logger/               # Loglama işlemleri
│   │   ├── logging.py        # Loglama işlevselliği
│   │   ├── logging_utils.py  # Loglama yardımcı işlevleri
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── search.py         # API arama rotası
│   ├── schemas/
│   │   ├── contextualize_q_prompt.jinja2
│   │   ├── qa_system_prompt.jinja2
│   ├── services/
│   │   ├── chains.py         # Zincirleme sorgu mantığı
│   │   ├── middleware.py     # Middleware işlemleri
│   │   ├── vectorstore.py    # Vektör depolama mantığı
├── scripts/
│   └── standalone_embed.bat  # Milvus başlatma betiği
├── static/                   # Statik dosyalar (img, css vb.)
├── .env                      # Ortam değişkenleri
├── alembic.ini               # Alembic yapılandırması
├── app.py                    # WSGI giriş noktası
├── main.py                   # FastAPI giriş noktası
├── README.md                 # Proje belgeleri
├── requirements.txt          # Python bağımlılıkları
├── wsgi.py                   # WSGI dağıtım ayarları
```

---

## Kurulum ve Yükleme

### Ön Koşullar

- **Python 3.9+**
- **Docker ve Docker Compose**
- **Microsoft SQL Server**
- **Milvus Standalone**

### Kurulum ve Yapılandırma

1. **Depoyu Klonlayın**
   ```bash
   git clone https://github.com/handeakturk/RAGChatbot.git
   cd chatbot_project
   ```

2. **Python Sanal Ortamı Oluşturun**
   ```bash
   python -m venv venv
   Windows: venv/Scripts/activate
   ```

3. **Bağımlılıkları Yükleyin**
   ```bash
   pip install -r requirements.txt
   ```

4. **Milvus'u Başlatın**
   ```bash
   https://milvus.io/docs/install_standalone-windows.md dökümanını takip ederek milvus standalone.bat dosyasını indirin.
   Terminalden `standalone.bat start`'i çalıştırın.
   ```

5. **Veritabanı Geçişlerini Uygulayın**
   Alembic geçişlerini başlatın ve uygulayın:
   ```bash
   alembic init migrations
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

6. **FastAPI Sunucusunu Başlatın**
   ```bash
   uvicorn main:app --reload
   ```

7. **Streamlit Arayüzünü Başlatın**
   ```bash
   streamlit run app.py
   ```
   Streamlit arayüzüne erişmek için: `http://localhost:8501`

---

## Nasıl Kullanılır

1. **Belgeye Erişim**: Sistem, İş Bankası Halka Arzı PDF'ini otomatik olarak kullanır.
2. **Soru Sorun**: 
   - Örnek: "TSKB çevresel yönetim sistemi hakkında detaylı ve uzun bilgi verir misin?"
3. **Yanıt Alın**: Belgeye dayalı bağlam duyarlı yanıtlar alın.
4. **Kayıtları Takip Edin**: Kullanıcı sorgularını ve yanıtlarını MSSQL üzerinden izleyin.

---

## Sorun Giderme

### Yaygın Sorunlar

- **Milvus Bağlantı Hatası**: `standalone.bat`'in çalıştığından ve `http://localhost:19530` üzerinden erişilebilir olduğundan emin olun.
- **Veritabanı Hataları**: `.env` dosyasının doğru yapılandırıldığından ve veritabanı sunucusunun çalıştığından emin olun.
- **Dosya Yolu Hataları**: `.env` dosyasındaki `FILEPATH` değişkeninin İş Bankası PDF'ini doğru gösterdiğinden emin olun.

---

## .env Dosyası İçeriği

`.env` dosyasını aşağıdaki şekilde oluşturup doldurun:

```env
AZURE_OPENAI_ENDPOINT=<Azure OpenAI endpoint URL>
AZURE_MODEL_NAME=<Kullanılan model adı>
AZURE_DEPLOYMENT_NAME=<Azure'deki dağıtım adı>
AZURE_OPENAI_API_VERSION=<API versiyonu örn: "2023-03-15">
AZURE_OPENAI_API_KEY=<Azure API anahtarınız>
```

Değerleri, Azure OpenAI hesabınızdan alabilirsiniz. Bu bilgiler API ile doğru iletişim kurmak için gereklidir.

---

### Örnek Girdi ve Çıktı

**Search Endpoint'i Kullanımı:**
Postman uygulamasında yeni bir POST request oluşturarak http://127.0.0.1:8000/search/ adresinden json formatında aşağıdaki gibi sorgu yapabilirsiniz.

İstek:
```json
{
    "query": "İş Bankası belgesinde belirtilen risk faktörleri nelerdir?"
}
```

Yanıt:
```json
{
    "query": "İş Bankası belgesinde belirtilen risk faktörleri nelerdir?",
    "answer": "İş Bankası Temmuz 2023 belgesinde aşağıdaki risk faktörleri belirtilmiştir: ..."
}
```

**Streamlit Arayüzü Kullanımı:**

Arayüzde sorunuzu girerek hızlı bir şekilde yanıt alabilirsiniz. Örnek soru:
- "Belgede belirtilen anahtar stratejiler nelerdir?"
---


# Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.

---

## Katkıda Bulunma

Katkıda bulunmaktan memnuniyet duyarız! Şu adımları izleyin:

1. Depoyu çatallayın.
2. Yeni bir dal oluşturun:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Değişikliklerinizi işleyin:
   ```bash
   git commit -m "Add your feature description"
   ```
4. Dalınızı iterek gönderin:
   ```bash
   git push origin feature/your-feature-name
   ```
5. İnceleme için bir pull request oluşturun.

---

