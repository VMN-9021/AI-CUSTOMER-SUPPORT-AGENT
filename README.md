# AI Customer Support Agent

An AI-powered customer support application that understands user queries, identifies the type of request, retrieves relevant information, and generates an appropriate response.

## Project Overview

This project uses LangGraph to create a structured workflow for handling customer support queries.

The agent classifies incoming queries into categories such as:

- Billing
- Technical Support
- Account
- General

Based on the query category, the workflow processes the request and generates a suitable response using an AI language model.

## Features

- Query classification
- Customer support response generation
- Structured workflow using LangGraph
- Context-based information retrieval
- Final response validation
- Interactive Streamlit interface

## Technologies Used

- Python
- LangGraph
- LangChain
- OpenAI
- Streamlit

## Project Structure

```text
ai-customer-support-agent/
│
├── agent.py
├── app.py
├── req.txt
└── README.md

## Workflow

```text
User Query
    ↓
Query Classification
    ↓
Information Retrieval
    ↓
Response Generation
    ↓
Final Validation
    ↓
Final Response
