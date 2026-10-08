# Carte LogWatch v0 - v1 du 2026-09-24 (étape 1)

## Entrées et sorties
lit : le fichier de logs (--log, .env LOGWATCH_LOG, défaut sample-logs.log),
      config.json (--config, .env LOGWATCH_CONFIG, défaut config.json), .env
écrit : le rapport JSON daté dans reports/ (--reports, .env LOGWATCH_REPORTS, défaut reports)
supprime : les vieux rapports du dossier reports/, dans d6_purger_rapports

## Les fonctions, dans l'ordre du fichier

| fonction | rend |
|---|---|
| charger_env(chemin=".env") | Rien. Elle pose les variables absentes de l'environnement. |
| charger_config(chemin) | un dictionnaire des seuils : les valeurs par défaut (DEFAUTS), écrasées par celles présentes dans config.json |
| parser_ligne(ligne) | un dictionnaire à onze clés, ou None si la ligne n'a pas la forme attendue ou si la date est illisible |
| lire_log(chemin, encodage="utf-8") | un tuple (liste des entrées parsées, nombre de lignes ignorées) |
| anonymiser_ip(ip) | l'IP avec son dernier octet remplacé par "x" si elle a 4 morceaux, sinon l'IP telle quelle |
| d1_requetes_par_ip(entrees, top_ips) | un dictionnaire : par_ip (les top_ips IP anonymisées les plus actives) et somme (total compté) |
| d2_brute_force(entrees, url_login, seuil) | une liste de dictionnaires (ip anonymisée, tentatives, gravité) pour les IP au-dessus du seuil |
| d3_scan(entrees, seuil) | une liste de dictionnaires (ip anonymisée, nb_urls, urls, gravité), triée par nb_urls décroissant |
| d4_pic_trafic(entrees, seuil_pic, fenetre_minutes) | un dictionnaire (alerte, charge, max_par_minute, minute_pic) |
| d5_erreurs_5xx(entrees, seuil) | un dictionnaire (nb_5xx, total, ratio, alerte) |
| d6_purger_rapports(dossier, retention_jours) | une liste des noms de fichiers supprimés, ceux dont l'âge dépasse limite_jours (retention_jours * 30) |
| analyser(entrees, config) | un dictionnaire avec les clés D1 à D5 (le corps du rapport, sans D6) |
| ecrire_rapport(rapport, dossier) | le chemin du fichier JSON créé dans dossier, contenant tout le dictionnaire rapport |
| main(argv=None) | un code de sortie : 1 si entrees est vide, 0 sinon une fois le rapport construit et écrit |

## Les détections annoncées par le README (question 7)

| détection | fonction | ce que le README demande |
|---|---|---|
| D1 | d1_requetes_par_ip | toutes les requêtes de chaque IP, quel que soit le code de réponse ; affiche les top_ips plus actives ; somme = total_lines |
| D2 | d2_brute_force | signalée dès que le nombre d'échecs (POST url_login, 401/403) atteint seuil_brute_force |
| D3 | d3_scan | signalée à partir de seuil_scan URL distinctes typiques d'un scanner |
| D4 | d4_pic_trafic | fenêtres de fenetre_minutes minutes ; pic si une fenêtre dépasse seuil_pic requêtes |
| D5 | d5_erreurs_5xx | part de réponses 5xx ; alerte au-delà de seuil_5xx |
| D6 | d6_purger_rapports | tout rapport plus vieux que retention_jours **jours** est supprimé |

## Points opaques (question 8)
- ligne 42 (dans DEFAUTS) : que vaut seuil_5xx par défaut dans le code, et que dit le README pour cette même clé ?
- ligne 120 (dans d1_requetes_par_ip) : que compte la boucle exactement — le README dit "quel que soit le code de réponse", que fait le `if` juste avant `compteur[e["ip"]] += 1` ?
- ligne 136 (dans d2_brute_force) : le README dit "dès qu'elle atteint seuil_brute_force" — que vaut la comparaison utilisée (`>` ou `>=`) quand n est exactement égal au seuil ?
- ligne 188 (dans d6_purger_rapports) : retention_jours est en jours selon le README — quelle valeur limite_jours prend-elle dans le code, et le commentaire juste à côté dit quoi ?
- ligne 164 (dans d4_pic_trafic) : le README parle de fenêtres de fenetre_minutes qui ne se chevauchent pas — sur quoi le code regroupe-t-il réellement les entrées (par_minute), et charge est calculée comment (mean de quoi) ?