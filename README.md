# GrzybNet - Michał Wirkowski 4 grupa

**GrzybNet** is a web application based on a microservices architecture. It allows users to share information about mushrooms, publish posts, and comment on findings – with full support for authentication via OAuth 2.0 (Keycloak).

It's build on such microservices as:
- Flask api
- Mongodb
- Keycloak
---

## 🛠️ Technologies

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)  
![Flask](https://img.shields.io/badge/Flask-2.3-black?logo=flask)  
![MongoDB](https://img.shields.io/badge/MongoDB-4.4-green?logo=mongodb)  
![Keycloak](https://img.shields.io/badge/Keycloak-OAuth2-7c4dff?logo=keycloak)  
![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker)  
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326ce5?logo=kubernetes)

---

## 🔐 Security

The application uses **OAuth 2.0** for user authentication via **Keycloak**.

- Registration and login via Keycloak  
- Access tokens (JWT) are required to use the API  
- Roles and permissions are managed through the Keycloak Realm

---

## 🏗️ Running the Project Locally

### 🔧 Requirements

- Docker Dekstop  
- Git  
- Kubernetes

### 📦 Installation

```bash
[turn on docker desktop first]
git clone https://github.com/mwirk/Grzybnet.git grzybnet
cd grzybnet
kubectl apply -f k8s/
```
