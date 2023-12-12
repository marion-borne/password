# Importation des bibliothèques nécessaires
import random
import hashlib
import string
import json
import re
import os

# Nom du fichier où les mots de passe seront stockés
FILE_NAME = "passwords.json"

# Cette fonction demande à l'utilisateur d'entrer un mot de passe et le renvoie
def affichage_mdp():
    mdp = input("Veuillez entrer un mot de passe : ")
    return mdp

# Cette fonction vérifie la sécurité du mot de passe en fonction de plusieurs critères
def verification_mdp(password):
    while True:
        if len(password) < 8:
            print("Le mot de passe doit contenir au moins huit caractères.")
        elif not re.search("[a-z]", password):
            print("Le mot de passe doit contenir au moins une lettre minuscule.")
        elif not re.search("[A-Z]", password):
            print("Le mot de passe doit contenir au moins une lettre majuscule.")
        elif not re.search("[0-9]", password):
            print("Le mot de passe doit contenir au moins un chiffre.")
        elif not re.search("[!@#$%^&*]", password):
            print("Le mot de passe doit contenir au moins un caractère spécial (!, @, #, $, %, ^, &, *).")
        else:
            print("Le mot de passe est sécurisé.")
            break
        # Si le mot de passe ne respecte pas les critères, on demande à l'utilisateur d'en entrer un nouveau
        password = affichage_mdp()
    return password

# Cette fonction prend un mot de passe en entrée, le convertit en bytes, puis utilise la fonction sha256 de la bibliothèque hashlib pour le hacher
def cryptage_mdp(password):
    password = password.encode()
    hashed_password = hashlib.sha256(password).hexdigest()
    return hashed_password

# Cette fonction sauvegarde le mot de passe haché dans un fichier JSON
def save_password(hashed_password):
     # Vérifie si le fichier existe déjà
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r') as file:
            data = json.load(file)
    else:
        data = {}

    password_name = input("Veuillez entrer un nom pour ce mot de passe : ")
    # Vérifie si le mot de passe existe déjà
    if hashed_password in data.values():
        print("Ce mot de passe existe déjà.")
    else:
        # Si le mot de passe n'existe pas déjà, on l'ajoute au dictionnaire data
        data[password_name] = hashed_password
         # On ouvre le fichier en mode écriture et on y enregistre le dictionnaire data au format JSON
        with open(FILE_NAME, 'w') as file:
            json.dump(data, file)

# Cette fonction affiche tous les mots de passe stockés dans le fichier
def display_passwords():
    # Vérifie si le fichier existe
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r') as file:
            data = json.load(file)
        # Parcourt tous les éléments du dictionnaire data et les affiche
        for password_name, hashed_password in data.items():
            print(f"Nom: {password_name}, Mot de passe haché: {hashed_password}")
    else:
        print("Aucun mot de passe n'a été enregistré.")
        
# Cette fonction génère un mot de passe aléatoire de 10 caractères qui respecte les critères de sécurité
def generate_random_password():
    length = 10
    password_characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(password_characters) for i in range(length))
    return password

# Fonction principale qui gère le menu du programme
def main():
    while True:
        print("1. Ajouter un nouveau mot de passe")
        print("2. Afficher les mots de passe")
        print("3. Générer un mot de passe aléatoire")
        print("4. Quitter")
        choice = input("Veuillez choisir une option : ")
        if choice == '1':
            password = verification_mdp(affichage_mdp())
            hashed_password = cryptage_mdp(password)
            save_password(hashed_password)
        elif choice == '2':
            display_passwords()
        elif choice == '3':
            password = generate_random_password()
            print("Votre mot de passe aléatoire est : ", password)
            hashed_password = cryptage_mdp(password)
            save_password(hashed_password)
        elif choice == '4':
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

# Exécute la fonction principale qui elle même va executer les autres fonctions selons les choix de l'utilisateur
if __name__ == "__main__":
    main()
    
