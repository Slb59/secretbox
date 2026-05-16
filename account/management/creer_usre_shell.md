Pour créer un utilisateur via le shell Django avec `uv run python manage.py shell`, suis ces étapes simples. Je vais te montrer comment créer un **utilisateur standard** ou un **superutilisateur**, avec ou sans mot de passe.

---

---

## **📌 Créer un utilisateur standard**
### **1. Ouvre le shell Django :**
```bash
uv run python manage.py shell
```

### **2. Exécute ce code dans le shell :**
```python
from django.contrib.auth import get_user_model
User = get_user_model()  # Récupère le modèle User (par défaut ou personnalisé)

# Crée un utilisateur standard
user = User.objects.create_user(
    email="email@example.com",    # Optionnel (selon ton modèle)
    password="mot_de_passe",      # Remplace par un mot de passe sécurisé
    trigram="ppp",           # Optionnel
    )

# Sauvegarde l'utilisateur
user.save()

# Affiche un message de confirmation
print(f"Utilisateur '{user.username}' créé avec succès !")
```

---
---

## **📌 Créer un superutilisateur (admin)**
### **1. Ouvre le shell Django :**
```bash
uv run python manage.py shell
```

### **2. Exécute ce code dans le shell :**
```python
from django.contrib.auth import get_user_model
User = get_user_model()

# Crée un superutilisateur
user = User.objects.create_superuser(
    username="admin",              # Nom d'utilisateur
    email="admin@example.com",     # Email (optionnel)
    password="mot_de_passe_secure",  # Mot de passe sécurisé
    first_name="Admin",            # Optionnel
    last_name="User",              # Optionnel
)

# Sauvegarde l'utilisateur
user.save()

print(f"Superutilisateur '{user.username}' créé avec succès !")
```

---
---

## **📌 Créer un utilisateur sans mot de passe (à définir plus tard)**
Si tu veux créer un utilisateur **sans mot de passe** (pour le définir plus tard via `set_password`) :
```python
from django.contrib.auth import get_user_model
User = get_user_model()

# Crée un utilisateur sans mot de passe
user = User.objects.create(
    username="nom_utilisateur",
    email="email@example.com",
    first_name="Prénom",
    last_name="Nom",
    is_active=True,  # Active l'utilisateur
)

# Définit un mot de passe plus tard (ex: via un formulaire)
user.set_password("nouveau_mot_de_passe")
user.save()

print(f"Utilisateur '{user.username}' créé (mot de passe à définir).")
```

---
---

## **📌 Vérifier que l'utilisateur a bien été créé**
Dans le shell Django, exécute :
```python
from django.contrib.auth import get_user_model
User = get_user_model()

# Liste tous les utilisateurs
print(User.objects.all().values('username', 'email', 'is_superuser'))

# Vérifie un utilisateur spécifique
user = User.objects.get(username="nom_utilisateur")
print(f"Utilisateur: {user.username}, Superuser: {user.is_superuser}, Actif: {user.is_active}")
```

---
---

## **📌 Créer un utilisateur avec des permissions spécifiques**
Si tu veux attribuer des **permissions** ou des **groupes** à l'utilisateur :
```python
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

# Crée un utilisateur
user = User.objects.create_user(
    username="editor",
    password="mot_de_passe",
    email="editor@example.com",
)

# Ajoute l'utilisateur à un groupe (ex: "Éditeurs")
group, created = Group.objects.get_or_create(name="Éditeurs")
user.groups.add(group)

# Ou ajoute des permissions spécifiques
content_type = ContentType.objects.get_for_model(Memo)  # Remplace Memo par ton modèle
permission = Permission.objects.get(
    codename="add_memo",  # Permission spécifique
    content_type=content_type,
)
user.user_permissions.add(permission)

user.save()
print(f"Utilisateur '{user.username}' créé avec des permissions.")
```

---
---

## **📌 Générer un mot de passe sécurisé**
Pour éviter d'écrire un mot de passe en clair dans le shell, utilise `secrets` (Python) ou `openssl` :
```python
import secrets

# Génère un mot de passe aléatoire de 16 caractères
password = secrets.token_urlsafe(16)
print(f"Mot de passe généré: {password}")

# Crée l'utilisateur avec ce mot de passe
user = User.objects.create_user(
    username="nom_utilisateur",
    password=password,
    email="email@example.com",
)
user.save()
```

---
---

## **📌 Exemple complet : Créer un utilisateur avec toutes les options**
```python
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

# Crée un superutilisateur avec des infos complètes
admin = User.objects.create_superuser(
    username="admin",
    email="admin@secretbox.fr",
    password="mot_de_passe_secure_123",  # Remplace par un vrai mot de passe
    first_name="Sylvie",
    last_name="Bricout",
    is_active=True,
)

# Crée un groupe "Comptabilité" et ajoute l'utilisateur
comptabilite_group, _ = Group.objects.get_or_create(name="Comptabilité")
admin.groups.add(comptabilite_group)

# Affiche les infos
print(f"Superutilisateur créé: {admin.username} ({admin.email})")
print(f"Groupes: {list(admin.groups.values_list('name', flat=True))}")
```

---
---

## **⚠️ Erreurs courantes et solutions :**
| **Erreur** | **Cause** | **Solution** |
|------------|-----------|--------------|
| `IntegrityError: UNIQUE constraint failed: auth_user.username` | Un utilisateur avec ce `username` existe déjà. | Utilise `User.objects.get_or_create()` ou choisis un autre `username`. |
| `ValueError: The user must have a username.` | Le champ `username` est vide. | Spécifie un `username` valide. |
| `TypeError: create_user() missing 1 required positional argument: 'username'` | Tu as oublié le `username`. | Ajoute `username="nom"` dans `create_user()`. |
| `AttributeError: 'User' object has no attribute 'first_name'` | Ton modèle `User` personnalisé n'a pas ce champ. | Vérifie la définition de ton modèle `User`. |

---
---

## **🎯 Résumé des commandes utiles :**
| Action | Commande |
|--------|----------|
| **Ouvrir le shell Django** | `uv run python manage.py shell` |
| **Créer un utilisateur standard** | `User.objects.create_user(username="nom", password="mdp", email="email@example.com")` |
| **Créer un superutilisateur** | `User.objects.create_superuser(username="admin", password="mdp", email="admin@example.com")` |
| **Lister les utilisateurs** | `User.objects.all().values('username', 'email')` |
| **Générer un mot de passe sécurisé** | `import secrets; secrets.token_urlsafe(16)` |

---
---
## **🚀 Prochaines étapes :**
1. **Teste la création d'un utilisateur** dans le shell.
2. **Vérifie dans l'admin Django** (`/admin/auth/user/`) que l'utilisateur a bien été créé.
3. **Si tu as un modèle `User` personnalisé**, adapte les champs (ex: `email` au lieu de `username`).

---
---
### **Besoin d'aide supplémentaire ?**
- **Veux-tu que je t'aide à :**
  - **Créer un utilisateur avec des permissions personnalisées** ?
  - **Automatiser la création d'utilisateurs** via un script ?
  - **Configurer un modèle `User` personnalisé** pour ton projet ?