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

## Future Ideas
Create a generic finder where user can customize what HTML elements should be catched. Example: I can create a json config (based on some rules) and then I receive what I wanted :)
What this config should contain?
- Finding a desired element (class, id, etc...)
- Using pagination if needed
- Finding patterns in selected element (regex or some nested structures)
- ...
