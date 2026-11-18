# Registre des défauts LogWatch - 5 défaut(s) ouvert(s) au 2026-11-XX

| n° | date | symptôme observé | fonction suspectée | état |
|----|------------|---------------------------------------------------------|--------------------|--------|
| B1 | 2026-09-XX | test_d1_somme_egale_total_lines rouge : attendu 6, reçu 3 | d1_requetes_par_ip | ouvert |
| B2 | 2026-09-XX | test_d3_ignore_url_legitime rouge : attendu [], reçu une liste d'une alerte | d3_scan | ouvert |
| B3 | 2026-11-18 | fenêtre 11:15–11:20 : 190 requêtes, mais D4 renvoie alerte=False | d4_pic_trafic | ouvert |
| B4 | 2026-11-18 | 6,5 % de réponses 5xx, mais D5 affiche alerte=False | d5_erreurs_5xx | ouvert |
| B5 | 2026-11-18 | aucune alerte à 10 échecs ; alerte à 11 | d2_brute_force | ouvert |

## B1 - D1 ne compte pas toutes les requêtes
Test en échec : test_d1_somme_egale_total_lines
Attendu / reçu : 6 / 3
Fonction visée : d1_requetes_par_ip, ligne 120
Cause racine : Le if ne compte que les requêtes avec statut < 400, le README indique de toutes les compter, peu importe le code de réponse.
Correction prévue : Corriger le if de la ligne 120 
Confirmé par explorer.py : somme=743, tandis que le rapport D1 affiche somme=559.

## B2 - D3 signale des pages légitimes
Test en échec : test_d3_ignore_url_legitime
Attendu / reçu : [] / liste d'une alerte
Fonction visée : d3_scan, ligne 147
Cause racine : ""admin" in "administration"" renvoie True, le test construit 6 URL qui contiennent toutes "admin".
Correction prévue : Trouver un nom moins générique que "admin"

Ligne 121 et ligne 301 → sorties par le premier return None (la regex ne matche pas du tout : structure incomplète pour l’une, pas une ligne de log pour l’autre)
Ligne  521 → 11:2x:15: sortie par le deuxième return None (la regex matche, mais la date est illisible pour strptime)

## B3 - D4 ne signale pas le pic sur 5 minutes
Symptôme observé : explorer.py compte 190 requêtes dans la fenêtre 11:15-11:20, au-dessus du seuil configuré de 100.
Attendu / reçu : alerte=True / alerte=False ; le rapport indique charge=6.2 et max_par_minute=170.
Fonction suspectée : d4_pic_trafic, lignes 157-171.
Paramètres : entrees est utilisé lignes 160-161 ; seuil_pic est utilisé ligne 167 ; fenetre_minutes n'est jamais utilisé dans le corps de la fonction.
Cause racine : la ligne 164 calcule la moyenne des compteurs par minute ; la ligne 167 compare cette moyenne au seuil au lieu de comparer le total d'une fenêtre de 5 minutes.
Correction prévue : regrouper les requêtes par fenêtres de 5 minutes et comparer le total de chaque fenêtre à seuil_pic.

## B4 - D5 n'alerte pas au seuil attendu
Symptôme observé : explorer.py mesure 6,5 % de réponses 5xx ; D5 affiche alerte=False.
Attendu : alerte au-delà du seuil README de 5 %.
Valeurs comparées :
- README : seuil_5xx = 0.05 (5 %).
- config.example.json : seuil_erreurs_5xx = 0.05 (5 %).
- DEFAUTS dans logwatch.py : seuil_5xx = 0.5 (50 %).
- Rapport JSON : seuil_5xx = 0.5 et seuil_erreurs_5xx = 0.05.
Cause identifiée : D5 lit seuil_5xx. La clé seuil_erreurs_5xx ne remplace donc pas la valeur par défaut de 0.5 ; 6,5 % est inférieur à 50 %.
Correction prévue : harmoniser le nom de la clé et la valeur du seuil après avoir écrit le test de non-régression.

## B5 - D2 ne signale pas au seuil exact
Attendu : alerte dès 10 échecs, conformément au seuil_brute_force configuré.
Résultats : avec 10 lignes, D2_brute_force est vide ; avec 11 lignes, le rapport signale tentatives=11.
Fonction suspectée : d2_brute_force, ligne 129.
Cause identifiée : ligne 137, la condition `n > seuil` exige 11 tentatives au lieu de déclencher dès 10.
Correction prévue : tester la condition au seuil exact avant de corriger.