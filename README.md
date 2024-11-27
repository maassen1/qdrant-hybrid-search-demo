# qdrant-hybrid-search-demo

This repo is a barebones demo of an application using Qdrant hybrid search running on Qdrant Hybrid Cloud for effieciently obtaining information from PDFs. The demo loads data from this repo's `data` directory into Qdrant and prompts the user for a question continuously until `exit` is input. 

### Assumptions
1. Qdrant v1.12.4
2. Python v3.11.7
3. Kubernetes info:
  * Client Version\: v1.24.11-dispatcher
  * Kustomize Version\: v4.5.4
  * Server Version\: v1.31.0
4. Minikube v1.34.0
5. MacOS Ventura v13.3, M1 2020
6. Auxiliary features (such as TLS) not necessary for demo. 

### Process

The following steps were taken to complete this assessment.

1. Setup Kubernetes cluster via minikube on my local machine
2. Setup Qdrant Hybrid Cloud
3. Deploy Qdrant cluster on Hybrid Cloud
4. Configure API Key auth for Qdrant
5. Follow [Chat With Product PDF Manuals Using Hybrid Search](https://qdrant.tech/documentation/examples/hybrid-search-llamaindex-jinaai/#chat-with-product-pdf-manuals-using-hybrid-search) to create Python application that implements Qdrant Hybrid Search with both Sparse and Dense vectors


### Results
1. [Qdrant Hybrid Cloud Deployment](https://github.com/maassen1/qdrant-hybrid-search-demo/blob/main/qdrant_cloud_ui.png)
2. [Local Qdrant UI](https://github.com/maassen1/qdrant-hybrid-search-demo/blob/main/qdrant_localhost_ui.png)
3. [demo behavior](https://github.com/maassen1/qdrant-hybrid-search-demo/blob/main/main_output.png)
