# 🍄 GrzybNet 🍄 

**GrzybNet** to aplikacja webowa oparta na architekturze mikroserwisowej. Umożliwia użytkownikom dzielenie się informacjami o grzybach, publikowanie postów i komentowanie znalezisk – z pełnym wsparciem autoryzacji za pomocą OAuth 2.0 (Keycloak).

---

## 🛠️ Technologie

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3-black?logo=flask)
![MongoDB](https://img.shields.io/badge/MongoDB-4.4-green?logo=mongodb)
![Keycloak](https://img.shields.io/badge/Keycloak-OAuth2-7c4dff?logo=keycloak)
![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326ce5?logo=kubernetes)

---

## 🔐 Bezpieczeństwo

Aplikacja wykorzystuje **OAuth 2.0** do uwierzytelniania użytkowników za pomocą **Keycloak**.

- Rejestracja i logowanie przez Keycloak
- Tokeny dostępu (JWT) są wymagane do korzystania z API
- Role i uprawnienia kontrolowane przez Realm Keycloak

---

## 🏗️ Uruchomienie projektu lokalnie

### 🔧 Wymagania

- Docker + Docker Compose
- Git
- Kubernetes

### 📦 Instalacja

```bash
git clone https://github.com/twoj-login/forum-grzybiarzy.git
cd forum-grzybiarzy
kubectl apply -f k8s/

