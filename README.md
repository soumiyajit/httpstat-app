# Application for Monitor External URLs

This is an application designed to run in a Kubernetes cluster which can be used to monitor external URL. The state of the external URL and the response time in millisecond can be seen from Promethues. Also the metrics ingested by Prometheus Server should be visualized form the Grafana Dashboard.

#####The following URLs are used for the sample application:
	1. [https://httpstat.us/200](https://httpstat.us/200)
	2. [https://httpstat.us/503](https://httpstat.us/503)

#####Expected response format:

	httpstat_url_up{url="https://httpstat.us/503 "}  = 0
	httpstat_url_resp_ms{url="https://httpstat.us/503 "}  = [value]
	httpstat_url_up{url="https://httpstat.us/200 "}  = 1
	httpstat_url_resp_ms{url="https://httpstat.us/200 "}  = [value]
	
#### Application Developement:

1. ##### Clone the git repository:
	```
	https://soumiyajit.github.com
	```

2. ##### Install the required package:
	```
	pip install -r src/requirement.txt
	```

3. ##### Export the environment variables:
	```
	export URLS='https://httpstat.us/503','https://httpstat.us/200' 
   export TIMEOUT=2
   export PORT=8080
   ```
   
4. ##### Run the Python Application:
	```
	python src/app.py
	```
	
5. ##### Verify the application from browser:
	```
	http://localhost:8080 
	http://localhost:8080/metrics
	```

#### Create a Docker image:

1. ##### Build docker image: 

   ```
	docker build -t httpstat_url .
	```
	
2. ##### Run the docker image:
	```
	docker run -d -p 8080:8080 --env-file ./env-vars --name httpstat httpstat_url
	```
3. ##### Verify the application from the browser again:
	```
	http://localhost:8080 
	http://localhost:8080/metrics
	```
	
3. ##### Login to your docker account and push the image to your repository:

	```
	docker build -t httpstat_url .
   docker run -d -p 8080:8080 --env-file ./env-vars --name httpstat httpstat_url
	```
	
#### Deploy the Application on the target Kubernetes Cluster:

1. ##### The manifests folder contains the deployment and service file for the application. Deploy the same in the target cluster

	```
	kubectl create -f src/manifests/
	```

2. ##### Verify all the pods, services, deployment and replicasets:
	```
	kubectl get all
	```

Make a note of the NodePort to access the application.

3. ##### Verify the NodePort for the httpstat-url-svc service and access the application from the browser:

	```
	http://<NodeIP>:<Node Port>
	http://<NodeIP>:<Node Port>/metrics
	```
#### Configure Prometheus and Grafana:

1. ##### Install Prometheus using Helm:
	```
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
	helm repo add kube-state-metrics https://kubernetes.github.io/kube-state-metrics
	helm repo update
	helm install prometheus prometheus-community/prometheus
	```
	Now configure the service of the Prometheus to make the prometheus-server available over Node Port.

2. ##### Install Grafana using Helm:

	```
	helm repo add grafana https://grafana.github.io/helm-charts
	helm repo update
	helm install -f grafana-values.yml grafana grafana/grafana
	```
	Now configure the service of the Grafana to make the prometheus server available over Node Port.

3. ##### Update the prometheus-server configuration to scrape metrics of the application:

	```
	- job_name: 'httpstat-url'
      static_configs:
      - targets: ['<NodeIP>:<Node Port>']
	```

4. ##### Now we can verify our application from the Prometheus dashboard:

5. ##### Now access the Grafana dashboard using the NodeIP and Node Port:

	Add the Prometheus data source
	
	Import the Grafana Dashboard
	
	Click the upload and select the grafana.json file.
	
	When the import is successful we can see the application metrics in Grafana.
	

#### Reference:

1. https://github.com/prometheus/client_python
2. https://sysdig.com/blog/prometheus-metrics/
3. https://tomgregory.com/how-and-when-to-use-a-prometheus-gauge/
4. https://codeburst.io/prometheus-by-example-4804ab86e741
5. https://tanzu.vmware.com/developer/guides/kubernetes/observability-prometheus-grafana-p1/
6. https://grafana.com/docs/grafana/latest/getting-started/getting-started-prometheus/
7. https://devopscube.com/setup-prometheus-monitoring-on-kubernetes/#:~:text=Exposing%20Prometheus%20as%20a%20Service,node%20IP's%20on%20port%2030000%20.
8. https://artifacthub.io/packages/helm/prometheus-community/prometheus













