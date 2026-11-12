# Vidéo de démonstration Aeria — script, plan de tournage et montage CapCut

Durée cible : **2 min 00** (± 5 s). Format : 1920 × 1080, 30 i/s. Voix off en français, sous-titres
incrustés (beaucoup de vidéos sont regardées sans le son).

## Storyboard

| # | Temps | À l'écran | Voix off | Texte incrusté |
|---|---|---|---|---|
| 1 | 0:00–0:08 | Plan large du Havre (photo libre de droits ou capture de la carte zoomée sur le port), puis le logo Aeria | « Au Havre, entre le port et la zone industrielle, l'air change d'heure en heure. » | **Aeria** · qualité de l'air en Normandie |
| 2 | 0:08–0:20 | Tableau de bord, page d'accueil : barres « observé » et « prévu demain » | « Aeria répond à une question simple : est-ce que l'air sera bon demain ? » | Indice observé et prévu à J+1 |
| 3 | 0:20–0:38 | Carte : bascule « Observé / Prévu demain », survol d'une station, clic vers la page station, calendrier et graphique | « Trente-six stations officielles, six capteurs Aeria. Chaque indice est écrit en toutes lettres, avec le polluant responsable. » | 902 607 mesures · 36 stations |
| 4 | 0:38–0:55 | Schéma d'architecture (`docs/architecture.svg`), zoom progressif module par module | « Derrière, sept modules : des capteurs MQTT, un pipeline de données ouvertes, un modèle de prévision, un back-office de maintenance, la sécurité et ce tableau de bord. » | 7 modules · 7 dépôts GitHub |
| 5 | 0:55–1:12 | Page Prévision, puis graphique du backtest (`aeria-forecast/docs/figures/01_precision_mensuelle.png`) | « Le modèle prévoit l'indice du lendemain avec la météo prévue la veille. Il trouve le bon indice 83 % du temps, mieux que la simple persistance. » | 83,1 % vs 79,6 % |
| 6 | 1:12–1:32 | Back-office : tableau de bord, un ticket « capteur muet » créé par la supervision, planification, l'historique | « Un capteur se tait ? La supervision ouvre un ticket, propose le bon technicien, et chaque étape est tracée. Les règles de gestion sont dans la base de données elle-même. » | Merise · SQL · BPMN |
| 7 | 1:32–1:50 | Terminal : `wazuh-logtest` avec la règle 100705 (niveau 12), puis le scan nmap avant/après (8084 open → closed) | « La sécurité a été auditée : six failles trouvées, corrigées et re-testées, et des règles Wazuh détectent les attaques que l'on ne peut pas empêcher. » | EBIOS RM · nmap · Wazuh |
| 8 | 1:50–2:00 | Page GitHub du dépôt `aeria`, badges verts, puis URL du site | « Tout est ouvert et testé en continu. Aeria : respirer, ça se mesure. » | github.com/brinis-aya/aeria |

## Ce qu'il faut enregistrer

Captures d'écran vidéo avec la Xbox Game Bar (Win + Alt + R) ou OBS Studio, navigateur en plein écran à
1920 × 1080, zoom à 110 %. Ces captures sont souvent plus longues que nécessaire : on coupera au montage.

1. **Site** <https://brinis-aya.github.io/aeria-dashboard/> : l'accueil, puis la carte (cliquer « Prévu
   demain », survoler 2 ou 3 stations, cliquer « Le Havre ville-haute »), puis la page station (faire défiler
   lentement), puis la page Prévision.
2. **Back-office** : `docker compose up --build` dans le dépôt `aeria`, puis <http://127.0.0.1:8084>. Se
   connecter en `responsable`, ouvrir Tickets, puis un ticket « Aucune mesure reçue ». Montrer la liste
   « Technicien (compétents, même zone…) », cliquer « Planifier », montrer l'historique.
3. **Terminal** (police 18 pt, thème sombre) :
   - `python scripts/test_wazuh_rules.py --container <manager>` dans `aeria-security` ;
   - `type docs\audit\raw\03-nmap-poste-lan-avant.txt` puis `…08-…-apres.txt`.
4. **Images fixes** : `docs/architecture.svg` (ouvert dans le navigateur, zoom), graphique de précision
   mensuelle du module 3, matrice des risques du module 5.

## Montage dans CapCut (bureau)

1. **Nouveau projet** → format 16:9, 1080p, 30 i/s. Importer toutes les captures et images.
2. **Voix off** : `Audio` → `Enregistrer`, lire le texte du storyboard scène par scène, avec 1 s de silence
   entre les scènes. Ou bien utiliser `Texte → Lecture vocale`, voix française naturelle.
3. **Découpe** : placer chaque scène sous sa voix off. Couper avec `Ctrl + B`, supprimer les temps morts.
   Accélérer à ×1,5 les défilements trop longs (`Vitesse`).
4. **Zooms** : sur les captures, `Animation` → `Zoom avant` léger (105 → 115 %), pour guider l'œil vers la
   zone importante (bascule de la carte, règle niveau 12, port 8084).
5. **Textes incrustés** : `Texte` → style simple, police sans empattement, blanc sur bandeau semi-opaque,
   en bas à gauche, 3 s par carton (colonne « Texte incrusté »).
6. **Sous-titres** : `Texte` → `Sous-titres automatiques` → français, puis corriger les noms propres (Aeria,
   ATMO, Wazuh, nmap, EBIOS).
7. **Musique** : `Audio` → bibliothèque libre de droits, ambiance calme. Volume à -22 dB sous la voix ;
   activer « Réduction automatique » si disponible.
8. **Transitions** : fondu court (0,3 s) entre les scènes 1→2, 4→5 et 7→8 seulement. Pas d'effets
   tape-à-l'œil.
9. **Contrôle** : durée totale 2:00 ± 5 s, voix intelligible, aucun mot de passe visible à l'écran (le mot de
   passe de démonstration ne doit pas apparaître dans le champ, utiliser l'autoremplissage ou couper).
10. **Export** : 1080p, 30 i/s, H.264, débit « Recommandé » → `aeria-demo.mp4`.

## Publication

- Mettre la vidéo en ligne (YouTube en « non répertoriée », ou une *release* GitHub du dépôt `aeria`).
- Remplacer le lien `VIDEO_URL` dans le README du dépôt `aeria`.
- Ajouter une miniature : capture de la carte et titre « Aeria · 2 min ».
