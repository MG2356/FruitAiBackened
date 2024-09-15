from pymongo import MongoClient

# MongoDB Atlas connection string
client = MongoClient('mongodb+srv://munishgoel45698:9r3jwSuO1CzegsfD@cluster0.9r9br1c.mongodb.net/healthmanager')
db = client['healthmanager']  # Use the same name as your database in MongoDB Atlas
faqs_collection = db['faqs']  # Use the collection name you want for your FAQs
users_collection = db['users']