import xml.etree.ElementTree as ET
from pathlib import Path
import os
NON PAS UTILISER
# Liste des fichiers à modifier
liste_file = [
    "map/tileset_tsx/Musée.tsx", "map/tileset_tsx/autre.tsx", "map/tileset_tsx/tilemap.tsx",
    "map/tileset_tsx/tilemap-backgrounds_packed.tsx", "map/tileset_tsx/tilemap_jump.tsx",
    "map/tileset_tsx/tileset_ville.tsx", "map/museum/musée_couloir_1.tmx", "map/museum/musée_Hall.tmx",
    "map/museum/musée_couloir_2.tmx", "map/eau.tmx", "map/laby.tmx", "map/road.tmx",
    "map/maptresortest.tmx", "map/map.tmx", "map/jump.tmx"
]

def transformer_chemin(source):
    """ Transforme un chemin en format relatif et correct selon l'OS """
    if not source:  # Vérifie que le chemin n'est pas vide
        return None

    path = Path(source).resolve()

    # Convertir en chemin relatif par rapport au projet
    try:
        relative_path = path.relative_to(Path().resolve())
    except ValueError:
        relative_path = path  # Si impossible, garder tel quel

    # Adapter au format Windows ou Unix
    return str(relative_path).replace("\\", "/")  # Toujours en format portable `/`

def transform_to():
    for file in liste_file:
        input_file = Path(file)

        # Vérifie que le fichier existe
        if not input_file.exists():
            print(f"⚠️ Fichier introuvable : {input_file}")
            continue

        tree = ET.parse(input_file)
        root = tree.getroot()

        # Appliquer la modification sur toutes les balises contenant un attribut `source`
        for element in root.findall(".//*[@source]"):
            new_path = transformer_chemin(element.get("source"))
            if new_path:
                element.set("source", new_path)

        # Sauvegarder le fichier modifié
        tree.write(input_file, encoding="UTF-8", xml_declaration=True)
        print(f"✅ Fichier modifié et sauvegardé sous : {input_file}")

# Exécuter la fonction
#transform_to()
NE LE FAIS PAS
