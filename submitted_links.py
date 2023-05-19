import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import random


# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
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
