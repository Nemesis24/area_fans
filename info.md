# Area Fans

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

## Description

L'intégration **Area Fans** permet de gérer les ventilateurs par zone dans Home Assistant. Vous pouvez exclure certains ventilateurs de chaque zone et surveiller l'état des ventilateurs dans chaque zone. De plus, vous pouvez allumer ou éteindre tous les lumières d'une zone à l'aide d'un switch.

## Installation

### Via HACS (Home Assistant Community Store) 

1. Ajoutez ce dépôt à HACS en tant que dépôt personnalisé.
2. Recherchez "Area Fans" dans HACS et installez l'intégration.
3. Redémarrez Home Assistant.

### Manuel

1. Téléchargez les fichiers de ce dépôt.
2. Copiez le dossier `area_fans` dans le répertoire `custom_components` de votre configuration Home Assistant.
3. Redémarrez Home Assistant.

## Configuration

### Via l'interface utilisateur

1. Allez dans `Configuration` > `Intégrations`.
2. Cliquez sur le bouton `+ Ajouter une intégration`.
3. Recherchez "Area Fans" et suivez les instructions à l'écran pour configurer l'intégration.

### Via YAML

Non supporté.

## Utilisation

### Switch

L'intégration crée un switch pour chaque zone ainsi qu'un switch pour toute la maison avec les attributs suivants :

- `count`: Nombre de ventilateurs allumés.
- `total`: Nombre total de ventilateurs.
- `count_of`: Nombre de ventilateurs allumés sur le total.
- `fans_on`: Liste des ventilateurs allumés.
- `fans_off`: Liste des ventilateurs éteints.
- `excluded_fans`: Liste des ventilateurs exclus.

### Exclusion de ventilateurs

Vous pouvez exclure des ventilateurs spécifiques de chaque zone via l'interface de configuration de l'intégration.

## Support

Pour toute question ou problème, veuillez utiliser le [suivi des problèmes](https://github.com//Nemesis24/area_fans/issues).

## Contribuer

Les contributions sont les bienvenues ! Veuillez lire le fichier [CONTRIBUTING.md](https://github.com//Nemesis24/area_fans/blob/main/CONTRIBUTING.md) pour plus d'informations.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](https://github.com//Nemesis24/area_fans/blob/main/LICENSE) pour plus de détails.