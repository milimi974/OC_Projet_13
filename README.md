# OC_Projet_13

Les livrables du projets se trouvent dans le dossier Documents.   
Les test unitaires sont réalisés sur le module bugs_api.   
L'addons finalisé est le module ui_panel_bugs_studio.py.

### Installation 

1. ouvrir Blender
2. File > users preferences
3. Addons 
4. Install Add-on from file
5. Cocher la check box puis clicker sur la petite flèche 
6. Renseigner les champs
7. Save User Settings 

### Description
L’add-on permet de mettre en ligne des fichiers *.blend et *.obj sur un   
serveur par le biais d’une connexion FTP.  
Les fichiers peuvent être récupérés par les personnes ayant un accès au service.   
Le fichier ***.blend** remplacera la scène sur laquelle vous travaillez.   
**Penser à sauvegarder avant toute manipulation.**   
Le fichier ***.obj** insert dans la scène courante l’objet téléchargé.   
Un autre fonctionnalité permet d’afficher les dates des réunions,   
en récupérant un fichier *.json depuis le serveur.   
Le format du fichier devra être $var = {index(int): value(string), ...}    
et dont la value est une chaine de caractère correspondant à une date sous format EN.
Exp. Date : 
"%d %m %Y"


