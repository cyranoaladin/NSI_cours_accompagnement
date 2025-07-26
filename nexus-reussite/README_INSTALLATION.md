# 🚀 Nexus Réussite - Guide de Démarrage

## ✅ Installation Terminée

La plateforme Nexus Réussite est maintenant opérationnelle avec :

- **Backend Flask** en mode minimal fonctionnel
- **Frontend React** avec Vite
- **Communication API** configurée
- **CORS** activé pour les requêtes cross-origin

## 🌐 Accès à l'Application

### URLs d'accès
- **Frontend (Interface utilisateur)** : http://localhost:3002 (port adaptatif)
- **Backend (API)** : http://localhost:5002
- **API de configuration** : http://localhost:5002/api/config
- **Check de santé** : http://localhost:5002/health
- **API d'authentification** : http://localhost:5002/api/auth/login

## 🔧 Démarrage des Serveurs

### Option 1 : Script automatique (Recommandé)
```bash
cd /home/alaeddine/Documents/NSI_cours_accompagnement/nexus-reussite
./start_nexus.sh
```

### Option 2 : Démarrage manuel

#### Backend
```bash
cd backend
FLASK_PORT=5002 python start_server.py
```

#### Frontend
```bash
cd frontend  
npm run dev
```

## 📊 État Actuel

### Backend
- ✅ Serveur Flask fonctionnel sur le port 5002
- ✅ Routes API basiques configurées :
  - `/health` - Check de santé
  - `/api/config` - Configuration de l'application
  - `/api/auth/login` - Authentification simulée
  - `/api/students/profile` - Profil étudiant de démonstration
- ✅ CORS configuré pour le frontend
- ⚠️ Mode minimal (certains modules avec imports relatifs désactivés)

### Frontend
- ✅ Application React/Vite fonctionnelle
- ✅ Configuration proxy vers le backend
- ✅ Prête à communiquer avec l'API
- ✅ Interface utilisateur complète

## 🔧 Commandes Utiles

### Arrêter tous les serveurs
```bash
pkill -f "python.*start_server"
pkill -f "vite.*--host"
```

### Vérifier le statut des serveurs
```bash
# Backend
curl http://localhost:5002/health

# API de test
curl http://localhost:5002/api/config

# Frontend (retourne du HTML)
curl http://localhost:3002/
```

### Logs des serveurs
- Les logs du backend s'affichent dans le terminal
- Les logs du frontend sont visibles via l'interface Vite

## 🚀 Prochaines Étapes

1. **Accéder à l'interface** : Ouvrez http://localhost:3002 dans votre navigateur
2. **Tester l'authentification** : Utilisez le système de login de démonstration
3. **Explorer les fonctionnalités** : Naviguez dans les différentes sections de l'application

## 🐛 Résolution de Problèmes

### Si le backend ne démarre pas
- Vérifiez que le port 5002 est libre
- Vérifiez que l'environnement virtuel Python est activé
- Consultez les messages d'erreur dans le terminal

### Si le frontend ne démarre pas
- Vérifiez que Node.js et npm sont installés
- Assurez-vous que les dépendances sont installées (`npm install`)
- Le frontend utilisera automatiquement un port alternatif si 3000 est occupé

### Si la communication API ne fonctionne pas
- Vérifiez que les deux serveurs sont démarrés
- Testez l'accès direct à l'API : http://localhost:5002/api/config
- Vérifiez les paramètres CORS dans le backend

## 📝 Notes Techniques

- Le backend fonctionne en **mode minimal** pour contourner les problèmes d'imports relatifs
- Les **routes API essentielles** sont opérationnelles
- Le **système d'authentification** est simulé pour les tests
- La **base de données** n'est pas encore initialisée (fonctionne en mode mémoire)

## ✨ Félicitations !

Votre plateforme Nexus Réussite est maintenant opérationnelle et prête à être utilisée pour le développement et les tests ! 🎉
