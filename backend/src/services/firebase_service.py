import firebase_admin
from firebase_admin import credentials, storage
from pathlib import Path
from src.core import settings

# Setup
cred = credentials.Certificate(settings.FIREBASE_PATH)
firebase_admin.initialize_app(
    cred, {"storageBucket": "fast-api-test-61466.firebasestorage.app"}
)

bucket = storage.bucket()

# Upload a file
blob = bucket.blob("uploads/my_file.txt")
local_file = Path(__file__).parent / "local_file.txt"
local_file.write_text("Hello World", encoding="utf-8")

print(local_file)
blob.upload_from_filename(str(local_file))
print("Uploaded to:", blob.name)

# Make it public
blob.make_public()
print("Public URL:", blob.public_url)

# Download it back
blob.download_to_filename("downloaded_my_file.txt")
print("Downloaded locally!")

# List files in 'uploads/' folder
print("Listing files in uploads/:")
for item in bucket.list_blobs(prefix="uploads/"):
    print("-", item.name)
