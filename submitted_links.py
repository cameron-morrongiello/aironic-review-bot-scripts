import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import random
import os

from dotenv import load_dotenv
load_dotenv()

service_account_key = {
    "type": os.environ.get("type"),
    "project_id": os.environ.get("project_id"),
    "private_key_id": os.environ.get("private_key_id"),
    "private_key": os.environ.get("private_key"),
    "client_email": os.environ.get("client_email"),
    "client_id": os.environ.get("client_id"),
    "auth_uri": os.environ.get("auth_uri"),
    "token_uri": os.environ.get("token_uri"),
    "auth_provider_x509_cert_url": os.environ.get("auth_provider_x509_cert_url"),
    "client_x509_cert_url": os.environ.get("client_x509_cert_url"),
    "universe_domain": os.environ.get("universe_domain")
}


# Initialize Firebase Admin SDK
cred = credentials.Certificate(service_account_key)
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()


def __get_random_product_link():

    # Get all documents from the "productLinks" collection
    collection_ref = db.collection("productLinks")
    documents = collection_ref.get()

    # Convert documents to a list of dictionaries
    data_list = [doc.to_dict() for doc in documents]

    # Randomly choose a link from the retrieved documents

    if not data_list:
        return None

    random_link = random.choice(data_list)["productLink"]

    return random_link


def __delete_product_links(product_link):

    # Get a reference to the "productLinks" collection
    collection_ref = db.collection("productLinks")

    # Query the collection to find documents with matching productLink
    query = collection_ref.where("productLink", "==", product_link)
    docs = query.stream()

    # Delete the matching documents, if found
    for doc in docs:
        doc.reference.delete()


def use_random_product_link():
    link = __get_random_product_link()
    __delete_product_links(link)
    return link


print(use_random_product_link())
