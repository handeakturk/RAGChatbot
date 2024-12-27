# RAG Chatbot

RAG Chatbot, PDF belgelerini işlemek ve analiz etmek için tasarlanmış akıllı bir soru-cevaplama sistemidir. FastAPI, Azure OpenAI, Milvus ve SQLAlchemy kullanılarak geliştirilmiştir. Kullanıcıların **T. İş Bankası Temmuz 2023 Halka Arzı - İhraççı Bilgi Dokümanı** üzerinden sorular sormasına olanak tanır ve belgelerden bağlama duyarlı, doğru yanıtlar sağlar.

---

## Genel Bakış

Bu proje, önceden tanımlanmış PDF dosyalarını işleyen, vektör veri tabanına indeksleyen ve kullanıcıların içerikle ilgili sorular sormasına olanak tanıyan bir Retrieval-Augmented Generation (RAG) chatbotudur. Özellikle finansal belgeler, teknik kılavuzlar veya yasal sözleşmeler gibi büyük veri setlerini işlemek için idealdir.
![Arayüz Örneği](static/img/Screenshot%202024-12-27%20174840.png)
![Arayüz Örneği](static/img/Screenshot%202024-12-27%20174847.png)

### Temel Teknolojiler

1. **FastAPI**: API istekleri için yüksek performanslı bir backend sağlar.
2. **Azure OpenAI**: Embedding oluşturma ve doğal dil yanıtları için GPT modellerini kullanır.
3. **Milvus**: Benzerlik tabanlı aramalar için vektör veri tabanı.
4. **SQLAlchemy ve Alembic**: Yapılandırılmış veritabanı etkileşimleri ve geçişleri yönetir.
5. **Microsoft SQL Server**: Kullanıcı sorgularını, yanıtlarını ve performans metriklerini kaydeder.
6. **Streamlit**: Chatbot ile etkileşimli bir kullanıcı arayüzü sunar.

---

## Özellikler

1. **Önceden İndekslenmiş PDF**: Önceden tanımlı bir PDF (ör. T. İş Bankası'nın finansal raporu) üzerinden sorgu yanıtlar.
2. **Bağlam Duyarlı Soru-Cevaplama**: GPT ile belge embedding'lerini birleştirerek alakalı yanıtlar sağlar.
3. **Ölçeklenebilir Altyapı**: Milvus ile yüksek hızlı vektör benzerlik aramaları yapılır.
4. **Kapsamlı Kayıt Tutma**: MSSQL kullanarak kullanıcı sorgularını ve performans metriklerini takip eder.
5. **Streamlit Arayüzü**: Kullanıcı dostu bir etkileşim platformu sağlar.

---

## Kullanım Senaryoları

1. **Yatırım Kararları**
   - Detaylı finansal raporları analiz eder ve özel bilgiler sunar.
   - Örnek: "TSKB çevresel yönetim sistemi hakkında bilgi verir misin?"

2. **Kurumsal Araştırmalar**
   - Teknik kılavuzlar veya politika belgelerinden bilgi çıkarır.
   - Örnek: "Banka’nın sürdürülebilirlik stratejisi hakkında bilgi verir misin?"

3. **Hukuki ve Uyumluluk İncelemeleri**
   - Hukuki sözleşmelerde veya uyumluluk yönergelerinde kilit bölümleri hızlıca bulur.
   - Örnek: "Sözleşme ihlalleri için belirtilen cezalar nelerdir?"

---

## Mimari

### Güncellenmiş İş Akışı

1. **PDF**: Sistem, statik bir PDF dosyasını (ör. İş Bankası Halka Arzı) kullanır, bu dosya önceden işlenir ve indekslenir.
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
│   ├── main.py           # FastAPI giriş noktası
│   ├── config.py         # Uygulama yapılandırması
│   ├── models.py         # SQLAlchemy modelleri
│   ├── routes.py         # API rotaları
│   ├── services.py       # Çekirdek mantık ve yanıt oluşturma
│   ├── utils.py          # Yardımcı fonksiyonlar
│   ├── templates/        # Streamlit şablonları
│   └── wsgi.py           # WSGI üretim giriş noktası
├── migrations/           # Alembic geçişleri
├── requirements.txt      # Python bağımlılıkları
├── Dockerfile            # Docker yapılandırması
├── docker-compose.yml    # Milvus kurulumu
└── README.md             # Proje belgeleri
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
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Bağımlılıkları Yükleyin**
   ```bash
   pip install -r requirements.txt
   ```

4. **Milvus'u Başlatın**
   Terminalden `standalone.bat start`'i çalıştırın.

5. **Veritabanı Geçişlerini Uygulayın**
   Alembic geçişlerini başlatın ve uygulayın:
   ```bash
   alembic init migrations
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

6. **FastAPI Sunucusunu Başlatın**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

7. **Streamlit Arayüzünü Başlatın**
   ```bash
   streamlit run app/streamlit_app.py
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


## Lisans

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

