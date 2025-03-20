# Projet : Art'Venture
# Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure

import json

class sauvegarde:
    def __init__(self):
        with open("save.json", "r+") as f:
            self.save = json.load(f)
        print(self.save)

    def changer_json(self, key, item = None):
        if item != None:
            self.save[key] = item
            with open("save.json", "w") as f:
                json.dump(self.save, f, indent=2)
        return self.save[key]

    def reload_json(self):
        with open("save.json", "r+") as f:
            self.save = json.load(f)