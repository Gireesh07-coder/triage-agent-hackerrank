# Multi-Domain Support Triage Agent

## Overview
This project is a terminal-based support triage agent that processes support tickets across multiple domains (HackerRank, Claude, Visa).

## Features
- Ticket classification (request type & product area)
- Risk detection and escalation handling
- Retrieval-based response generation (RAG)
- Grounded responses using support corpus
- Structured CSV output

## Architecture
1. Classification layer
2. Risk detection
3. Retrieval (TF-IDF based)
4. Decision layer (answer vs escalate)
5. Response generation

## Safety
High-risk queries (fraud, payments, account access) are escalated instead of answered.

## How to Run

```bash
pip install -r requirements.txt
python main.py