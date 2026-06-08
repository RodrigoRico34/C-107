"""
Auteur : Rodrigo Silva Riço
Date : 08.06.2026
Desc : générer un hash de texte saisi ou d'un fichier existant
"""
import hashlib


def choice(text):
    while True:
        user_input = input(text)
        if user_input == "1":
            return 1
        if user_input == "2":
            return 2
        else:
            print("entrée invalide")


user_input = choice("1 Hachage d’un texte saisi.\n2 Hachage d'un fichier texte existant.\n")

if user_input == 1:
    try:
        print("Entrez votre texte (ligne vide pour terminer) :")

        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)

        hash_input = "\n".join(lines)
        hash_object = hashlib.sha256()

        hash_object.update(hash_input.encode('utf-8'))

        hash_hex = hash_object.hexdigest()

        print(f"\n{hash_hex}")

        # Si le fichier existe pas on le crée
        with open('hash_output', 'a') as f:
            pass

        with open('hash_output', 'r') as f:
            lines = f.readlines()

            if lines:
                last_line = lines[-1]
                first_char = last_line[0]

                number = int(last_line.split(')')[0]) + 1
            else:
                number = 1

        with open('hash_output', 'a') as f:
            f.write(f"{number}) {hash_hex}\n")

    except Exception as e:
        print(f"Erreur: {e}")

if user_input == 2:
    filepath = input("veuillez entrer le chemin d'accès du fichier : ")

    try:
        hash_object = hashlib.sha256()

        with open(filepath, 'rb') as f:
            data = f.read().replace(b'\r\n', b'\n')

        hash_object.update(data)

        hash_hex = hash_object.hexdigest()
        print(f"Hash SHA-256 du fichier: {hash_hex}")

        # si le fichier existe pas il est automatiquement créé
        with open('hash_output', 'a') as f:
            pass

        with open('hash_output', 'r') as f:

            lines = f.readlines()
            if lines:
                last_line = lines[-1]
                first_char = last_line[0]

                number = int(last_line.split(')')[0]) + 1
            else:
                number = 1

        with open('hash_output', 'a') as f:
            f.write(f"{number}) {hash_hex}\n")

    except FileNotFoundError:
        print("Erreur: Fichier introuvable!")
    except PermissionError:
        print("Erreur: Pas la permission de lire ce fichier!")
    except Exception as e:
        print(f"Erreur: {e}")
