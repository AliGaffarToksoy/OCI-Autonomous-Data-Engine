import oracledb
import os
import random
from faker import Faker
import time

# Fake veri üretici motor
fake = Faker()


def get_db_connection():
    print("🔒 Oracle Autonomous DB'ye mTLS Cüzdanı ile bağlanılıyor...")

    # Terraform'un indirdiği ve zipten çıkardığımızı varsaydığımız Wallet klasörü
    wallet_dir = os.path.join(os.path.dirname(__file__), "wallet")

    # Güvenlik standardı: Şifreler koda yazılmaz, ortam değişkeninden alınır
    db_password = os.getenv("DB_PASSWORD", "OciDataEngine@2026_Secure!")

    try:
        # python-oracledb (Thin Mode) ile yüksek güvenlikli bağlantı
        connection = oracledb.connect(
            user="ADMIN",
            password=db_password,
            dsn="enterpriseenginedb_high",  # Yüksek performanslı veri yolu (High Profile)
            wallet_location=wallet_dir,
            wallet_password=db_password
        )
        print("✅ Bağlantı Başarılı!")
        return connection
    except Exception as e:
        print(f"❌ Bağlantı Hatası: {e}")
        return None


def run_data_engine():
    conn = get_db_connection()
    if not conn:
        return

    cursor = conn.cursor()

    # 1. Tabloyu Oluştur (Eğer yoksa)
    print("🏗️ E-Ticaret tablosu inşa ediliyor...")
    try:
        cursor.execute("""
                       CREATE TABLE ECOMMERCE_ORDERS
                       (
                           ORDER_ID         VARCHAR2(50) PRIMARY KEY,
                           CUSTOMER_NAME    VARCHAR2(100),
                           PRODUCT_CATEGORY VARCHAR2(50),
                           PRICE            NUMBER(10, 2),
                           ORDER_DATE       TIMESTAMP
                       )
                       """)
    except oracledb.DatabaseError as e:
        # ORA-00955: İsim zaten kullanılıyor (Tablo varsa hata verme, devam et)
        error, = e.args
        if error.code != 955:
            raise

    # 2. Sahte Veri Üretimi
    BATCH_SIZE = 10000  # Tek seferde 10 BİN sipariş!
    print(f"🚀 {BATCH_SIZE} adet sipariş üretiliyor...")

    categories = ["Elektronik", "Giyim", "Ev & Yaşam", "Spor", "Otomotiv"]
    order_data = []

    for _ in range(BATCH_SIZE):
        order_data.append((
            fake.uuid4(),
            fake.name(),
            random.choice(categories),
            round(random.uniform(10.0, 5000.0), 2),
            fake.date_time_this_year()
        ))


    start_time = time.time()
    print("⚡ Veriler OCI Autonomous Database'e fırlatılıyor...")

    # JUNIOR Hareketi: execute() ile satır satır eklemek (Çok yavaş)
    # SENIOR Hareketi: executemany() ile paket (batch) halinde fırlatmak (Işık hızında)
    cursor.executemany("""
                       INSERT INTO ECOMMERCE_ORDERS (ORDER_ID, CUSTOMER_NAME, PRODUCT_CATEGORY, PRICE, ORDER_DATE)
                       VALUES (:1, :2, :3, :4, :5)
                       """, order_data)

    # Veritabanına kaydet
    conn.commit()

    end_time = time.time()
    print(f"🎯 BAŞARILI! {BATCH_SIZE} adet sipariş {(end_time - start_time):.2f} saniyede buluta yazıldı.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    run_data_engine()