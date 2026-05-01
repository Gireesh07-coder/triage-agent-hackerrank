Multi-Domain Support Triage Agent
Overview
This project is a terminal-based support triage agent that processes support tickets across multiple domains (HackerRank, Claude, Visa).

Features
Ticket classification (request type & product area)
Risk detection and escalation handling
Retrieval-based response generation (RAG)
Grounded responses using support corpus
Structured CSV output
Architecture
Classification layer
Risk detection
Retrieval (TF-IDF based)
Decision layer (answer vs escalate)
Response generation
Safety
High-risk queries (fraud, payments, account access) are escalated instead of answered.

How to Run
pip install -r requirements.txt
python main.py
