# Setup Guide

## 1. Clone

git clone --branch day-19 <repository-url>

## 2. Enter project

cd genai-assistant

## 3. Create virtual environment

python -m venv venv

## 4. Activate

.\venv\Scripts\Activate.ps1

## 5. Install dependencies

pip install -r requirements.txt

## 6. Configure environment

Copy `.env.example` to `.env`.

Do not commit `.env`.

## 7. Verify

pytest -v