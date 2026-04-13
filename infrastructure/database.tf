# 1. Autonomous Transaction Processing (ATP) Veritabanı Yaratıyoruz
resource "oci_database_autonomous_database" "enterprise_atp" {
  compartment_id           = "MOCK_COMPARTMENT_OCID"
  db_name                  = "EnterpriseEngineDB"
  display_name             = "High-Performance Data Engine"
  cpu_core_count           = 1
  data_storage_size_in_tbs = 1

  # OLTP (Online Transaction Processing) - E-ticaret / Anlık işlem yükleri için
  db_workload              = "OLTP"

  # Mülakatçıya "Güvenliği biliyorum" deme satırı: Sadece mTLS (Cüzdanlı) bağlantıya izin ver!
  is_mtls_connection_required = true

  # Admin Şifresi (Normalde HashiCorp Vault veya Secrets ile verilir)
  admin_password           = "OciDataEngine@2026_Secure!"

  # Veritabanı otomatik yedeklensin ve yama alsın
  is_auto_scaling_enabled  = true
}

# 2. Senior Dokunuşu: Kurulan veritabanının güvenlik cüzdanını (Wallet) otomatik indir!
resource "oci_database_autonomous_database_wallet" "atp_wallet" {
  autonomous_database_id = oci_database_autonomous_database.enterprise_atp.id
  password               = "OciDataEngine@2026_Secure!" # Cüzdan şifresi
  base64_encode_content  = true
}

# 3. İndirilen cüzdanı bizim Python kodlarımızın yanına (src/wallet) aç ve kaydet
resource "local_file" "wallet_file" {
  content_base64 = oci_database_autonomous_database_wallet.atp_wallet.content
  filename       = "../src/wallet/wallet_EnterpriseEngineDB.zip"
}