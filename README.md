# FruitAiBackened
FruitAiBackened/
│
├── app.py
├── db.py
├── requirements.txt
│
└── README.md

Endpoints
POST /signup - User registration
POST /login - User login
GET /faqs - Get all FAQs
GET /faqs/<id> - Get FAQ by ID
POST /faqs - Create new FAQ (Requires authentication)
PUT /faqs/<id> - Update FAQ by ID (Requires authentication)
DELETE /faqs/<id> - Delete FAQ by ID (Requires authentication)
POST /api/detect - Detect language of text
POST /api/translate - Translate text
