# N11 E-commerce Automation Project

## 🎯 Proje Genel Bakışı
Bu proje, N11 e-ticaret web sitesi için Python, Selenium ve Pytest kullanarak geliştirilmiş otomatik test projesidir. Page Object Model (POM) ve SOLID prensipleri kullanılarak sürdürülebilir ve ölçeklenebilir kod yapısı oluşturulmuştur.

## 🏗️ Proje Yapısı

```
n11/
├── pages/                       # Page Objects
│   ├── __init__.py
│   ├── base_page.py            # Temel sayfa sınıfı
│   ├── home_page.py            # Ana sayfa
│   ├── product_listing_page.py # Ürün listesi sayfası
│   ├── search_result_page.py   # Arama sonuçları sayfası
│   └── stores_page.py          # Mağazalar sayfası
├── tests/                       # Test Cases
│   ├── __init__.py
│   ├── conftest.py             # Pytest konfigürasyonu
│   ├── test_search.py          # Arama testleri
│   └── test_stores.py          # Mağaza testleri
├── utils/                       # Yardımcı Araçlar
│   ├── __init__.py
│   └── wait_helper.py          # Bekleme yardımcıları
├── reports/                     # Test Raporları
├── screenshots/                 # Hata ekran görüntüleri
├── .env                         # Ortam değişkenleri
├── pytest.ini                  # Pytest konfigürasyonu
├── requirements.txt             # Bağımlılıklar
└── README.md                   # Proje dokümantasyonu
```

## 🚀 Kurulum Talimatları

### Ön Gereksinimler
- Python 3.8+
- Chrome Browser
- Git

### Kurulum Adımları

1. **Repository'yi klonlayın:**
```bash
git clone <repository-url>
cd n11
```

2. **Virtual environment oluşturun:**
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows
```

3. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

## 🧪 Testleri Çalıştırma

### Tüm testleri çalıştırın:
```bash
pytest
```

### Sadece smoke testleri:
```bash
pytest -m smoke
```

### Belirli bir test dosyası:
```bash
pytest tests/test_stores.py
```

### Detaylı çıktı ile:
```bash
pytest -v -s
```

### HTML raporu oluşturun:
```bash
pytest --html=reports/report.html
```

## 📊 Test Raporları
- HTML raporları `reports/` dizininde oluşturulur
- Hata durumunda ekran görüntüleri `screenshots/` dizininde saklanır
- JSON raporları CI/CD entegrasyonu için kullanılabilir

## 🏷️ Test Kategorileri
- **Smoke Tests**: Kritik fonksiyonalite testleri
- **Regression Tests**: Kapsamlı fonksiyonalite testleri
- **Slow Tests**: Zaman alan testler

## 🔧 Konfigürasyon
- Ortam değişkenleri `.env` dosyasında yönetilir
- Pytest konfigürasyonu `pytest.ini` dosyasında bulunur
- WebDriver kurulumu `conftest.py` dosyasında yapılır

## 📝 Kod Standartları

### SOLID Prensipleri
- **Single Responsibility**: Her fonksiyon sadece 1 iş yapar
- **Open/Closed**: Kod genişletmeye açık, değiştirmeye kapalı
- **Liskov Substitution**: Türetilmiş sınıflar temel sınıfların yerine geçebilir
- **Interface Segregation**: Gereksiz metod imzalarından kaçın
- **Dependency Inversion**: Bağımlılıklar soyutlamalara bağlı olmalı

### POM (Page Object Model)
- Sayfa elementleri test mantığından ayrılır
- Her sayfa kendi fonksiyonlarını içerir

### DRY & KISS
- **DRY**: Kendini Tekrarlama
- **KISS**: Basit Tut
- **Single Purpose Functions**: Fonksiyonlar net ve tek amaçlı olmalı

## 🛠️ Geliştirme Rehberi

### Fonksiyon Tasarımı
- Fonksiyon isimleri fiil ile başlar (click_, enter_, get_, select_)
- Her fonksiyon sadece 1 iş yapar
- Fonksiyon docstring formatı:

```python
def click_filter(self, index: int) -> None:
    """
    Belirtilen indeksteki filtreyi tıklar.

    Args:
        index: Tıklanacak filtre elementinin indeksi
    """
    self.click_element_by_index(self.FILTERS, index)
```

### Page Object Model Kuralları
- Her sayfa tek bir sınıf olmalı
- Locator'lar sınıf içinde private (_locator_name) olarak tanımlanmalı
- Public metodlar sadece iş mantığı içermeli
- BasePage tüm sayfalar için ortak fonksiyonları içermeli

### Hata Yönetimi
- Kritik olmayan işlemler için try/except kullanın
- Hataları loglayın ve hata durumunda ekran görüntüsü alın
- Test başarısızlıklarında net hata mesajları verin

### Bekleme Stratejileri
- Mümkün olduğunca time.sleep() kullanmayın
- Tüm explicit wait metodları WaitHelper'da olmalı

## 🚫 Kaçınılması Gereken Anti-Pattern'ler
- Büyük fonksiyonlar (>20 satır)
- Hard-coded değerler
- Test case'lerde locator tanımlama
- Thread.sleep() kullanımı

## 🔍 Kod İnceleme Kontrol Listesi
- [ ] Fonksiyonlar single responsibility mi?
- [ ] POM yapısı takip ediliyor mu?
- [ ] Kod tekrarı önlenmiş mi?
- [ ] Hatalar loglanıyor mu?
- [ ] Bekleme stratejisi doğru kullanılıyor mu?

## 📞 Destek
Sorular veya sorunlar için otomasyon ekibi ile iletişime geçin.

## 📄 Lisans
Bu proje MIT lisansı altında lisanslanmıştır.
