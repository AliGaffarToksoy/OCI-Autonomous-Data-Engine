terraform {
  required_providers {
    oci = {
      source  = "oracle/oci"
      version = "~> 5.20.0"
    }
  }
}

# Gerçek ortamda bu kimlik bilgileri ortam değişkenlerinden (Environment Variables) gelir
provider "oci" {
  tenancy_ocid     = "MOCK_TENANCY_OCID"
  user_ocid        = "MOCK_USER_OCID"
  fingerprint      = "MOCK_FINGERPRINT"
  private_key_path = "/path/to/mock/key.pem"
  region           = "eu-frankfurt-1" # Avrupa'nın kalbi
}