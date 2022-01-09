import uuid
import os
from io import BytesIO
from PIL import Image

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobClient
from fastapi.exceptions import HTTPException

from natours.models.database import engine as db
from natours.config import settings

def create_blob_client(file_name):

    default_credential = DefaultAzureCredential()

    secret_client = SecretClient(
        vault_url=settings.AZURE_VAULT_ACCOUNT,
        credential= default_credential
    )

    storage_credentials = secret_client.get_secret(name="storage-key")

    return BlobClient(account_url=settings.AZURE_STORAGE_ACCOUNT, container_name=settings.AZURE_APP_BLOB_NAME, blob_name=file_name,  credential=storage_credentials.value)

 
def check_image_ext(path):

    _ , ext = os.path.splitext(path)

    return ext in [".png", ".jpeg", ".jpg", ".tif"]


def delete_blob(file):
    blob = create_blob_client(file)
    if not blob.exists():
        return
    blob.delete_blob()

async def update_user_photo_name(user, photo_url):
    current_photo = user.photo
    blob_name = "/".join(current_photo.split("/")[-3:])
    delete_blob(blob_name)
    user.photo = photo_url
    await db.save(user)


def resize_picture(image:BytesIO):
    output_size = (125, 125)
    i = Image.open(image)
    i.thumbnail(output_size)
    img_byte_arr = BytesIO()
    i.save(img_byte_arr, format=i.format)
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

async def upload_image_to_blob(file, user):
    
    file_suffix = uuid.uuid4().hex

    _, ext = os.path.splitext(file.filename)
    
    file_name = f"{settings.AZURE_BLOG_USER_IMAGE_PATH}user-{file_suffix}{ext}"
    
    user_photo_url = f"{settings.AZURE_STORAGE_ACCOUNT}/{settings.AZURE_APP_BLOB_NAME}/{file_name}"
    
    await update_user_photo_name(user, user_photo_url)
    
    if not check_image_ext(file_name):
        raise HTTPException(
            404, "image file extention allowed only .png .jpg .jpeg .tif"
        )
    
    file_content = await file.read()

    image_io = BytesIO(file_content)

    image_resized = resize_picture(image_io)

    blob_client = create_blob_client(file_name=file_name)
    
    blob_client.upload_blob(data=image_resized)

    return file.filename