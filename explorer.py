from logwatch import lire_log
fichier_log = "dix-echecs.log"

entrees, lignes_ignorees = lire_log(fichier_log)
print(len(entrees), lignes_ignorees)

familles = {}

for e in entrees:
    famille = f"{e['statut'] // 100}xx"
    familles[famille] = familles.get(famille, 0) + 1

print(familles)
print(sum(familles.values()))

par_ip = {}

for e in entrees:
    ip = e["ip"]
    par_ip[ip] = par_ip.get(ip, 0) + 1

print(par_ip)
print(sum(par_ip.values()))

echecs_par_ip = {}

for e in entrees:
    if e["methode"] == "POST" and e["url"] == "/login" and e["statut"] in (401, 403):
        ip = e["ip"]
        echecs_par_ip[ip] = echecs_par_ip.get(ip, 0) + 1

print(echecs_par_ip)

par_minute = {}
for e in entrees:
    minute = e["horodatage"].strftime("%Y-%m-%d %H:%M")
    par_minute[minute] = par_minute.get(minute, 0) + 1

print(par_minute)
charge_recalculee = sum(par_minute.values()) / len(par_minute)
print("Charge recalculée :", round(charge_recalculee, 1))

par_fenetre = {}

for minute, compte in par_minute.items():
    numero_minute = int(minute[-2:])
    debut = numero_minute - numero_minute % 5
    fenetre = minute[:-2] + f"{debut:02d}"
    par_fenetre[fenetre] = par_fenetre.get(fenetre, 0) + compte

print("Total des fenêtres :", sum(par_fenetre.values()))

fenetre_pic = None

for fenetre, compte in par_fenetre.items():
    if fenetre_pic is None or compte > par_fenetre[fenetre_pic]:
        fenetre_pic = fenetre

print("Fenêtre la plus chargée :", fenetre_pic, par_fenetre[fenetre_pic])

nb_5xx = 0

for e in entrees:
    if 500 <= e["statut"] <= 599:
        nb_5xx += 1

part_5xx = nb_5xx / len(entrees)
print("Nombre de 5xx :", nb_5xx)
print(f"Part de 5xx : {part_5xx:.1%}")