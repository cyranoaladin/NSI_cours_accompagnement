# 🔧 Guide de Dépannage - Nexus Réussite Backend

## ❌ Erreur : "Impossible de résoudre l'importation flask"

### Symptômes
- L'IDE affiche une erreur d'importation pour Flask
- Les modules Python ne sont pas reconnus
- Code d'erreur : `Warning - [object Object]`

### 🎯 Causes Principales
1. **Environnement virtuel non activé**
2. **Dépendances non installées**
3. **IDE pointant vers le mauvais interpréteur Python**

### ✅ Solutions

#### Solution 1 : Script Automatique (Recommandé)
```bash
cd nexus-reussite/backend
./setup_env.sh
```

#### Solution 2 : Configuration Manuelle

1. **Activer l'environnement virtuel**
   ```bash
   cd nexus-reussite/backend
   source venv/bin/activate
   ```

2. **Installer les dépendances**
   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

3. **Vérifier l'installation**
   ```bash
   python -c "import flask; print('Flask OK:', flask.__version__)"
   ```

#### Solution 3 : Configuration IDE

**Pour VSCode :**
1. Ouvrir la palette de commandes (`Ctrl+Shift+P`)
2. Chercher "Python: Select Interpreter"
3. Sélectionner `./venv/bin/python`

**Pour PyCharm :**
1. File → Settings → Project → Python Interpreter
2. Sélectionner l'environnement virtuel : `nexus-reussite/backend/venv/bin/python`

### 🧪 Tests de Vérification

1. **Test d'importation**
   ```bash
   python -c "from flask import Flask; print('✅ Flask importé avec succès')"
   ```

2. **Test du serveur**
   ```bash
   python src/main_simple.py
   ```
   Devrait afficher :
   ```
   🚀 Lancement du serveur Flask Nexus Réussite
   📡 API disponible sur http://localhost:5000
   ```

### 📋 Checklist Complète

- [ ] L'environnement virtuel est activé (prompt `(venv)`)
- [ ] Flask est installé (`pip list | grep -i flask`)
- [ ] L'IDE pointe vers le bon interpréteur Python
- [ ] Le fichier `.vscode/settings.json` existe
- [ ] Le serveur démarre sans erreur

### 🆘 Problèmes Persistants

Si le problème persiste après avoir suivi ces étapes :

1. **Recréer l'environnement virtuel**
   ```bash
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Vérifier les versions Python**
   ```bash
   python --version
   which python
   ```

3. **Nettoyer le cache pip**
   ```bash
   pip cache purge
   ```

### 📞 Support
Pour d'autres problèmes, consultez :
- Documentation Flask : https://flask.palletsprojects.com/
- Issues GitHub du projet
- Logs dans `logs/` directory

---
*Dernière mise à jour : $(date)*
