# Minikube demo deployment

## Deploy app
Run minikube instance:

`minikube start`

Create secret for MONGO DB:

`kubectl create secret generic mongo-credentials --from-literal=mongo-uri=<yourMongoURI>`

Deploy app via Makefile:

`make discounts-app-deploy`

Run minikube backend service:

`minikube service backend`

## Removing resources

Delete app:

`make discounts-app-delete`

Delete MONGO DB secret:

`kubectl delete secret mongo-credentials`