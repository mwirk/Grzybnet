# 🍄 GrzybNet 🍄 

**GrzybNet** to aplikacja webowa oparta na architekturze mikroserwisowej. Umożliwia użytkownikom dzielenie się informacjami o grzybach, publikowanie postów i komentowanie znalezisk – z pełnym wsparciem autoryzacji za pomocą OAuth 2.0 (Keycloak).

---

## 🧩 Architektura

Projekt składa się z trzech głównych mikroserwisów:

| Serwis       | Technologia | Opis |
|--------------|-------------|------|
| **API**      | Flask       | Główna logika aplikacji – obsługa użytkowników, postów, komentarzy |
| **Baza Danych** | MongoDB     | Przechowuje dane użytkowników i postów w formacie dokumentowym |
| **Auth**     | Keycloak    | Służy jako serwer autoryzacji i zarządzania tożsamością (OAuth 2.0 / OpenID Connect) |

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

