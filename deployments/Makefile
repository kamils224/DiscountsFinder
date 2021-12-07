discounts-app-deploy:
	# config
	kubectl apply -f minikube/config-map.yaml
	# celery
	kubectl apply -f minikube/redis-deployment.yaml
	kubectl apply -f minikube/redis-service.yaml
	# redis
	kubectl apply -f minikube/celery-deployment.yaml

	# flask backend
	kubectl apply -f minikube/backend-deployment.yaml
	kubectl apply -f minikube/backend-service.yaml

discounts-app-delete:
	# config
	kubectl delete -f minikube/config-map.yaml
	# celery
	kubectl delete -f minikube/redis-deployment.yaml
	kubectl delete -f minikube/redis-service.yaml
	# redis
	kubectl delete -f minikube/celery-deployment.yaml

	# flask backend
	kubectl delete -f minikube/backend-deployment.yaml
	kubectl delete -f minikube/backend-service.yaml
