
# 🌍 QUIZ DRAPEAUX

[![GitHub stars](https://img.shields.io/github/stars/PhilippeHim/quizz_drapeau?style=social)](https://github.com/PhilippeHim/quizz_drapeau)
[![GitHub repo size](https://img.shields.io/github/repo-size/PhilippeHim/quizz_drapeau)](https://github.com/PhilippeHim/quizz_drapeau)
![Python version](https://img.shields.io/badge/Python-3.x-blue)
![Framework](https://img.shields.io/badge/Framework-Streamlit-red)

## 🎯 Aperçu du Projet

Ce projet est une application de quiz interactive développée avec **Streamlit** en Python. Le but est de tester et d'améliorer vos connaissances en **vexillologie** (l'étude des drapeaux) en identifiant les drapeaux des pays du monde.

Les drapeaux utilisés ont été scrapés depuis la page Wikipédia : [Galerie des drapeaux des pays du monde](https://fr.wikipedia.org/wiki/Galerie_des_drapeaux_des_pays_du_monde).

### ⚙️ Fonctionnalités

* Affichage aléatoire d'un drapeau du monde.
* Affichage du nom du pays (la réponse) en cliquant sur le bouton (simulant la touche `Entrée`).
* Passage au drapeau suivant pour une nouvelle manche.
* Interface utilisateur simple et réactive grâce à Streamlit.

---

## 🚀 Démarrage Rapide

Ces instructions vous permettront d'obtenir une copie du projet opérationnelle sur votre machine locale à des fins de développement et de test.

### Prérequis

Vous devez avoir `Python 3` installé sur votre système.

### 1. Cloner le dépôt

Ouvrez votre terminal et clonez le dépôt :

```bash
git clone [https://github.com/PhilippeHim/quizz_drapeau.git](https://github.com/PhilippeHim/quizz_drapeau.git)
cd quizz_drapeau
````

### 2\. Créer et Activer l'Environnement Virtuel

Il est fortement recommandé d'utiliser un environnement virtuel pour isoler les dépendances du projet.

**Sur Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Sur Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3\. Installer les Dépendances

Toutes les bibliothèques requises sont listées dans `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4\. Lancer l'Application

Une fois les dépendances installées, lancez l'application Streamlit :

```bash
streamlit run quizz.py
```

L'application devrait s'ouvrir automatiquement dans votre navigateur par défaut (généralement sur `http://localhost:8501`).

-----

## 📁 Structure du Projet

Le projet est organisé comme suit :

```
quizz_drapeaux/
├── drapeaux/             # Contient les images des drapeaux renommées (ex: "France.png")
├── drapeaux_orig/        # Contient les images brutes scrapées avant renommage
├── venv/                 # Environnement virtuel (ignoré par Git)
├── .gitignore            # Fichiers à ignorer (venv, .DS_Store, etc.)
├── quizz.py              # Le script principal de l'application Streamlit
├── renommer.py           # Script (probablement utilisé) pour nettoyer et renommer les drapeaux
├── requirements.txt      # Liste des dépendances Python
└── README.md             # Ce fichier
```

-----

## 🛠️ Dépendances Techniques

Ce projet nécessite les bibliothèques Python suivantes :

  * `streamlit` : Pour le développement rapide de l'application web.
  * `Pillow` (ou `PIL`) : Souvent utilisé pour le traitement d'images (redimensionnement, etc.).
  * `os` / `random` : Pour la gestion des fichiers et la sélection aléatoire.
    *(Note : Assurez-vous que votre `requirements.txt` contient toutes les dépendances exactes).*

-----

## 💡 Comment Jouer

1.  Lancez l'application comme indiqué ci-dessus.
2.  Un drapeau s'affiche. Essayez de deviner le pays.
3.  Cliquez sur le bouton **"Afficher la réponse / Changer de drapeau"** (ou le nom exact que vous avez donné à votre bouton) pour voir le nom du pays.
4.  Cliquez à nouveau pour passer au drapeau suivant \!

-----

## 🧑 Auteur

**Philippe Him**

  * [GitHub Profile](https://www.google.com/search?q=https://github.com/PhilippeHim)

-----

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` (si vous en créez un) pour plus de détails.


```