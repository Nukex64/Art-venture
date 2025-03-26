# Projet : Art'Venture
# Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure

import json


class sauvegarde:
    """
    Classe permettant de gérer la sauvegarde du jeu en chargeant et en modifiant un fichier JSON.

    Permet de charger des données sauvegardées, de les modifier et de les enregistrer à nouveau.
    """

    def __init__(self, nb):
        """
        Initialise l'objet `sauvegarde` avec un fichier de sauvegarde spécifié par son numéro.

        Args:
            nb (int): Le numéro de la sauvegarde, utilisé pour localiser le fichier de sauvegarde (ex: 'save_1.json').
        """
        self.nb = nb
        with open(f"save_{nb}.json", "r+") as f:
            self.save = json.load(f)

    def changer_json(self, key, item=None):
        """
        Modifie une entrée spécifique dans le fichier de sauvegarde et l'enregistre.

        Args:
            key (str): La clé de l'entrée à modifier dans le fichier JSON.
            item (obj, optional): La nouvelle valeur à attribuer à cette clé. Si `item` est `None`, la valeur actuelle est retournée.

        Returns:
            obj: La valeur de la clé spécifiée après modification (ou la valeur existante si `item` est `None`).
        """
        if item is not None:
            self.save[key] = item
            with open(f"save_{self.nb}.json", "w") as f:
                json.dump(self.save, f, indent=2)
        return self.save[key]

    def liste_changer_json(self, name, key, x):
        """
        Modifie une valeur dans une liste contenue dans le fichier de sauvegarde et l'enregistre.

        Cette méthode modifie une entrée dans un sous-ensemble de données du fichier JSON, plus précisément
        dans un tableau qui est référencé par la clé `name`, puis la valeur de la clé `key` est modifiée avec la valeur `x`.

        Args:
            name (str): Le nom de la liste (la clé principale dans le fichier JSON).
            key (str): La clé de l'élément à modifier dans la liste.
            x (obj): La nouvelle valeur à attribuer à la clé spécifiée dans la liste.

        """
        self.save[name][key] = x
        with open(f"save_{self.nb}.json", "w") as f:
            json.dump(self.save, f, indent=2)

    def reload_json(self, nb=0):
        """
        Recharge le fichier de sauvegarde en utilisant un nouveau numéro de sauvegarde.

        Args:
            nb (int, optional): Le nouveau numéro de la sauvegarde. Si `0`, le fichier actuel est rechargé.
        """
        if nb:
            self.nb = nb
        with open(f"save_{self.nb}.json", "r+") as f:
            self.save = json.load(f)
