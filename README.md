# Discounts Finder
The application aggregates discounts from web shops. The idea is to find discounts pattern in a way that does not overfit to any particular web shop and integrate everything in one resource available through API.

## Details
- MongoDB for data storage.
- Celery worker for processing html pages.
- Web API for results and processing in Flask.
- React frontend for displaying results.
## Run project locally

### Backend
`docker-compose up`

### Run frontend locally
`npm run start`

[Demo Kubernetes deployment](deployments/README.md)

## Project status
- Current html parser is a placeholder and works only for some websites with PLN currency.
- Frontend allows processing single URL and displays result with CRUD operations.
- It's only an early prototype, I don't have time for it :(

