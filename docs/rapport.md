# Rapport de synthèse — projet Aeria

**Aeria** — plateforme ouverte de surveillance de la qualité de l'air en Normandie
Auteur : BRINIS Aya — novembre 2026
Dépôt vitrine : <https://github.com/brinis-aya/aeria> · Tableau de bord : <https://brinis-aya.github.io/aeria-dashboard/>

---

## 1. Le projet en une page

**Question de départ** : *l'air sera-t-il bon demain au Havre ?* Y répondre sérieusement demande une chaîne
complète :

1. des mesures ;
2. leur validation ;
3. leur croisement avec les données officielles ;
4. un modèle de prévision ;
5. la maintenance des capteurs ;
6. la sécurité de l'ensemble ;
7. une interface lisible par tous.

Chaque maillon est un module, un dépôt GitHub public, un rapport.

| Module | Livrable principal | Résultat clé |
|---|---|---|
| 1. Capteurs IoT | simulateur et firmware ESP32, MQTT, ingestion Spring Boot validée | ingestion idempotente (QoS 1) ; mesures impossibles, incohérentes, hors délai ou malformées rejetées à l'entrée |
| 2. Pipeline | ETL pandas des données ouvertes LCSQA, entrepôt en étoile | 902 607 valeurs, 95,7 % exploitables, indice ATMO de 13 543 jours-stations |
| 3. Prévision | 5 modèles de gradient boosting, API FastAPI | 83,1 % d'indices exacts contre 79,6 % pour la persistance, sans fuite d'information |
| 4. Back-office | Merise, 16 règles de gestion en SQL, 3 processus BPMN, application Spring Boot | 24 tests sur base réelle, année de démonstration rejouée à travers les triggers |
| 5. Sécurité | EBIOS RM, audit, corrections re-testées, Wazuh, ISO 27001 | 6 constats corrigés avec preuve avant/après, 15/15 scénarios détectés |
| 6. Tableau de bord | étude UX, site React (carte, graphiques, prévision) | site statique publié, accessibilité vérifiée par axe-core en CI |
| 7. Vitrine | architecture, plateforme en une commande, CI d'intégration, script vidéo | plateforme reconstruite depuis les dépôts et testée de bout en bout |

## 2. Fil conducteur entre les modules

Les modules ne sont pas juxtaposés : chacun nourrit le suivant, et plusieurs résultats n'apparaissent qu'en
les croisant.

- **Les capteurs simulés ne suivent pas la météo réelle.** Le module 2 le montre en les comparant aux stations
  de référence (épisode de novembre 2026 manqué). Le module 3 en tire la conséquence : il est entraîné sur les
  mesures **réelles**.
- **Les données de maintenance confirment l'analyse de risques.** « Capteur muet » est l'incident n° 1 du
  module 4. Le module 5 désigne en conséquence les réseaux Wi-Fi des sites comme la partie prenante la plus
  dangereuse.
- **La sécurité a modifié les autres modules**, preuves à l'appui :
  - configuration MQTT de production (module 1) ;
  - écoute locale, verrouillage des comptes et journal de sécurité (module 4) ;
  - en-têtes HTTP (module 3) ;
  - mise à jour de Spring Boot (modules 1 et 4).
- **Le risque résiduel principal** (un capteur manipulé physiquement qui masque un épisode de pollution) se
  traite avec les autres modules : confrontation aux stations de référence (module 2) et à la valeur prévue
  (module 3).

## 3. Démarche et qualité

- **Données réelles** partout où c'est possible : open data officielles, prévisions météo réellement émises la
  veille. La simulation n'est utilisée que pour ce qui n'existe pas encore : les capteurs Aeria et l'année de
  maintenance. Elle est signalée comme telle.
- **Comparer à une référence simple** : persistance et climatologie pour la prévision ; avant/après pour
  chaque correction de sécurité.
- **Tester ce qui compte** : environ 140 tests automatisés. Ils couvrent les règles de gestion sur une vraie
  base PostgreSQL, l'absence de fuite d'information dans la prévision, les règles Wazuh sur un vrai manager,
  et l'accessibilité du site.
- **Intégration continue sur les 7 dépôts.** Le dépôt vitrine reconstruit toute la plateforme depuis GitHub et
  vérifie qu'elle fonctionne de bout en bout.
- **Honnêteté sur les limites** : chaque rapport consacre une section à ce qui ne marche pas ou n'a pas été
  fait.

## 4. Ce que j'en retiens

1. **Une règle métier dans la base vaut mieux qu'une règle dans le code.** Les triggers du module 4 ont même
   refusé, pendant la génération des données de démonstration, une intervention qui aurait mis un technicien
   à deux endroits à la fois.
2. **Un modèle doit être jugé contre la persistance, pas dans l'absolu.** Mes premiers résultats paraissaient
   bons, mais la persistance faisait presque aussi bien sur les particules. Le dire est plus utile que de
   l'omettre.
3. **Un outil de sécurité a des angles morts.** Varys, mon propre outil, n'a pas vu le back-office en HTTP sur
   un port non standard : seul nmap l'a révélé. Mes règles Wazuh semblaient correctes, mais trois erreurs ne
   sont apparues qu'en les testant réellement.
4. **Le design commence par une question d'utilisateur.** « Demain » plutôt qu'« aujourd'hui » a structuré
   tout le tableau de bord.

## 5. Limites d'ensemble

- **Environnement de développement.** Un seul poste ; pas d'hébergement de production, de proxy TLS ni de
  sauvegardes. Ces éléments sont au plan de traitement du module 5.
- **Capteurs simulés.** Le firmware ESP32 existe mais n'a pas été déployé physiquement.
- **Une seule année de données.** L'hiver n'est jamais en période de test pour la prévision, et les épisodes
  « Mauvais » sont rares.
- **Test utilisateur à mener.** Le protocole est prêt (module 6).
- **Formation.** Le MOOC SecNumacadémie de l'ANSSI et la vidéo de démonstration sont à réaliser par l'auteur.
  Le script et le plan de tournage sont fournis.

## 6. Documents

| Module | Rapport |
|---|---|
| 1 | <https://github.com/brinis-aya/aeria-iot-sensors/blob/main/docs/rapport.md> |
| 2 | <https://github.com/brinis-aya/aeria-data-pipeline/blob/main/docs/rapport.md> |
| 3 | <https://github.com/brinis-aya/aeria-forecast/blob/main/docs/rapport.md> |
| 4 | <https://github.com/brinis-aya/aeria-backoffice/blob/main/docs/rapport.md> et `docs/merise.md` |
| 5 | <https://github.com/brinis-aya/aeria-security/blob/main/docs/rapport.md>, `ebios-rm.md`, `audit.md`, `iso27001-soa.md` |
| 6 | <https://github.com/brinis-aya/aeria-dashboard/blob/main/docs/rapport.md> et `etude-ux.md` |
| 7 | ce document, `docs/video/script.md` |
