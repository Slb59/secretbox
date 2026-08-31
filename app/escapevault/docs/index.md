# Escapevault - Documentation

## version: 0.5.0

Cet outil est un espace de gestion des parcours et des lieux que nous avons visités où que nous souhaitons visiter. Les lieux sont apparents sur une carte, il est possible de filtrer les lieux par catégorie et par titre.

Les informations associées à un lieu sont:
- les coordonnées gps
- la ville
- l'adresse exacte
- la catégorie
- un titre
- une note (0 à 5 étoiles)
- une description
- un avis
- un état 'actif/inactif': sert de suppression d'un enregistrement.

Les catégories disponibles sont:
- maison
- camping
- parcours (dans ce cas l'adresse sera un point de départ)

La page d'accueil fait apparaître :
- la carte, avec les positions de la catégorie "maison" chargées par défaut 
- un bouton '+' pour ajouter une position,
- les options de filtre
	- catégorie
	- titre

L'ajout d'une position s'effectue par l'affichage d'un écran de saisie.

Le survol d'une position avec la souris fait apparaître une popup contenant la ville, le titre, la note, un bouton détail.

Le bouton détail donne accès à la page de modification des informations.


