.PHONY: run-backend run-frontend run-all

run-backend:
	cd backend && uvicorn app.main:app --reload

run-frontend:
	cd frontend && streamlit run main.py

run-all:
	make run-backend & make run-frontend