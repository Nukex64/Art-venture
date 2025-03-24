# Projet : Art'Venture
# Auteurs : Anthony Ibanez-Esteban, Raphaël Prost, Aëlys-Coleen Surma Valtaer, Louis Gagne, Mathéo Faure

import json

class sauvegarde:
    def __init__(self, nb):
        self.nb = nb
        with open(f"save_{nb}.json", "r+") as f:
            self.save = json.load(f)
            f.close()

    def changer_json(self, key, item = None):
        if item != None:
            self.save[key] = item
            with open(f"save_{self.nb}.json", "w") as f:
                json.dump(self.save, f, indent=2)
                f.close()
        return self.save[key]


    def reload_json(self, nb=0):
        if nb : self.nb = nb
        with open(f"save_{self.nb}.json", "r+") as f:
            self.save = json.load(f)