# Registre des défauts LogWatch - 2 défaut(s) ouvert(s) au 2026-09-XX

| n° | date | symptôme observé | fonction suspectée | état |
|----|------------|---------------------------------------------------------|--------------------|--------|
| B1 | 2026-09-XX | test_d1_somme_egale_total_lines rouge : attendu 6, reçu 3 | d1_requetes_par_ip | ouvert |
| B2 | 2026-09-XX | test_d3_ignore_url_legitime rouge : attendu [], reçu une liste d'une alerte | d3_scan | ouvert |

## B1 - D1 ne compte pas toutes les requêtes
Test en échec : test_d1_somme_egale_total_lines
Attendu / reçu : 6 / 3
Fonction visée : d1_requetes_par_ip, ligne 120
Cause racine : Le if ne compte que les requêtes avec statut < 400, le README indique de toutes les compter, peu importe le code de réponse.
Correction prévue : Corriger le if de la ligne 120 

## B2 - D3 signale des pages légitimes
Test en échec : test_d3_ignore_url_legitime
Attendu / reçu : [] / liste d'une alerte
Fonction visée : d3_scan, ligne 147
Cause racine : ""admin" in "administration"" renvoie True, le test construit 6 URL qui contiennent toutes "admin".
Correction prévue : Trouver un nom moins générique que "admin"

Ligne 121 et ligne 301 → sorties par le premier return None (la regex ne matche pas du tout : structure incomplète pour l’une, pas une ligne de log pour l’autre)
Ligne  521 → 11:2x:15: sortie par le deuxième return None (la regex matche, mais la date est illisible pour strptime)