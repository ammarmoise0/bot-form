"""
Strategies de reponses pour le formulaire.

Chaque strategie definit des regles par question :
- choice : {"weights": {"Option A": 70, "Option B": 20, "Option C": 10}}
  -> probabilites ponderees
- rating : {"range": [3, 5], "center": 4}
  -> distribution gaussienne centree
- nps : {"range": [7, 10], "center": 9}
  -> distribution gaussienne centree
- text : {"pool": ["reponse 1", "reponse 2", ...]}
  -> pioche aleatoire dans le pool
- choice_multi : {"options_weights": {"Opt A": 80, "Opt B": 40}}
  -> chaque option a une probabilite independante d'etre choisie
"""

import random
import math

# IDs des questions par theme (pour lisibilite)
Q = {
    "situation": "r020f4f892fa14420a8c41b5b06f0fc43",
    "niveau_poste": "r63689e2a3bf8484abf8cffc5383c28e9",
    "secteur": "r16d390cf1b504ebb8d2f60d5c13388e5",
    "tests_avant": "r3e53b86f1d4b4a798f392f18c3161f7e",
    "tests_ici": "r9a7783c02a4b4369b5b878b9b9a36792",
    "types_test": "r85a7eaabbcda484698a30d5db65f58cb",
    "moment_process": "r879b4c0f290842dda1c133441a1adde5",
    "duree": "r444a32c5ea73499294e7422a4f7f0401",
    "administration": "ree912609a6b244479b1c281850f875a5",
    "modalite": "r7193c3cc6841463f903e688b9cdccd82",
    "instructions": "r8702ce4cb5004424a5abcc0f1f12d9f5",
    "environnement": "r3f7be34423eb4f48af43d0974d56c178",
    "stress": "r8d388a2dac404f518c2f577967d005d0",
    "equite": "rabd463f274c34fd08038efd9353321d6",
    "restitution_recu": "r4eb335901f914c3f8633892028ed93ad",
    "forme_restitution": "reada7faa68ea4927bac88d35881635e6",
    "qualite_restitution": "r2e4b366ea5744b1ca78dcc390acfdb24",
    "contribution_dev": "ra30c1de1b51d47c7ae2a7559dd10e477",
    "possibilite_refus": "r9d5e66a1882b488ba9fd1dd67ae423fe",
    "confidentialite": "rbd8e625e214b4b67b1cc3187a70942a1",
    "transparence": "r84cebdc50d9d41c283b86083cf4cffbf",
    "reduit_biais": "r2d485046e6254dfc95c2db4f30e0d93b",
    "fidelite": "r66e8f3dd01934a17a91eeb1821fb6f82",
    "anxiogene": "r5d8aa3e2ce2b49bdbe548b7ca62a9eee",
    "facile_comprendre": "rc6e3019b4b454a16a2037de82c2d26ee",
    "restitution_necessaire": "rec610b31c6b44512a615abd6ef82e455",
    "jamais_seul_critere": "r51ef2d1b49b84a19916b1cb97f7d57a7",
    "image_entreprise": "rfb6987ac6a534362b3d42a71a088c780",
    "utilite_recruteurs": "r57771f8fdcc2451cbe151ae77552810f",
    "atout": "rd238594fc2164511bc57184525995ea9",
    "risque_frein": "r0ecfd1408ced4bc687cde2a25a2d1eab",
    "influence_decision": "rfcf4d411f0ad41a9a05acfcbeaa00f7e",
    "nps_recommandation": "r2c0881af018a48ffab04c5c7e04c0718",
    "nps_influence_offre": "rcb0fdb082b1349d1b92bf866ae555f0e",
    "recommander_candidats": "r8b109331b45e4081b5df2c9c23e0f8e2",
    "nps_experience": "r4eb75bb6bfe24c37895ca0d227afc004",
    "ameliorations": "r00430e273398489a89de9c256551b202",
    "commentaire": "r0ed595b93c2348dba87fe89430b50c86",
}

SECTEURS = [
    "Banque / Assurance", "IT / Numerique", "Industrie", "Conseil",
    "Sante", "Grande distribution", "BTP", "Energie",
    "Transport / Logistique", "Telecommunications", "Agroalimentaire",
    "Automobile", "Pharmacie", "Services aux entreprises", "Finance",
]

ATOUTS_POSITIFS = [
    "Objectivite dans l'evaluation des competences",
    "Permet de mieux se connaitre en tant que candidat",
    "Reduit les biais lies au feeling en entretien",
    "Apporte une base concrete pour l'echange avec le recruteur",
    "Donne une image professionnelle de l'entreprise",
    "Permet de comparer les candidats sur des criteres mesurables",
    "Aide a identifier des competences pas visibles en entretien",
    "C'est un outil complementaire interessant",
    "La restitution m'a permis de mieux comprendre mes forces",
    "Cela structure le processus de recrutement",
    "Equite : tout le monde passe le meme test",
    "Meilleure adequation poste / candidat",
]

ATOUTS_MITIGES = [
    "Ca peut etre utile si bien utilise",
    "Interessant mais pas suffisant seul",
    "Le principe est bon mais l'execution variable",
    "Peut aider si accompagne d'un echange",
    "Ca depend beaucoup du test utilise",
    "Utile pour les postes techniques, moins pour le reste",
]

ATOUTS_NEGATIFS = [
    "Je ne vois pas vraiment d'atout",
    "Trop standardise pour capter la singularite d'un candidat",
    "Ca ne reflette pas les competences reelles",
    "L'entretien classique est plus pertinent",
]

AMELIORATIONS_POSITIVES = [
    "Peut-etre expliquer davantage l'objectif des tests en amont",
    "Proposer un temps d'echange apres les resultats",
    "Rien de particulier, l'experience etait bonne",
    "Envoyer les resultats par email en complement",
    "Donner des conseils personnalises suite aux tests",
]

AMELIORATIONS_MITIGEES = [
    "Mieux expliquer a quoi servent les tests avant de les faire passer",
    "Reduire la duree des tests, c'etait un peu long",
    "Donner les resultats meme quand on n'est pas retenu",
    "Proposer les tests en amont pour eviter le stress sur place",
    "Ameliorer l'ergonomie de la plateforme de test",
    "Etre plus transparent sur le poids des tests dans la decision",
]

AMELIORATIONS_NEGATIVES = [
    "Supprimer les tests ou les rendre facultatifs",
    "Ne pas en faire un element de decision",
    "Mieux former les recruteurs a interpreter les resultats",
    "Laisser le choix au candidat de passer ou non",
    "Revoir completement l'approche, trop impersonnelle",
]


# ============================================================
# STRATEGIE 1 : CANDIDAT SATISFAIT
# ============================================================
STRATEGIE_SATISFAIT = {
    "name": "Candidat Satisfait",
    "description": "Experience tres positive. Notes elevees, recommande les tests. Profil type : a eu une bonne restitution et trouve les tests justes.",
    "color": "#27ae60",
    "rules": {
        Q["situation"]: {"type": "choice", "weights": {"Candidat externe": 50, "Mobilite interne": 35, "Alternant": 15}},
        Q["niveau_poste"]: {"type": "choice", "weights": {"Employe / Technicien": 25, "Agent de maitrise": 35, "Cadre": 40}},
        Q["secteur"]: {"type": "text", "pool": SECTEURS},
        Q["tests_avant"]: {"type": "choice", "weights": {"Oui": 65, "Non": 35}},
        Q["tests_ici"]: {"type": "choice", "weights": {"Oui": 95, "Non": 5}},
        Q["types_test"]: {"type": "choice", "weights": {
            "Aptitudes (logiques, numerique, verbale)": 35,
            "Personnalite": 35,
            "Motivation / Interets / Valeurs": 20,
            "Mise en situation": 10,
        }},
        Q["moment_process"]: {"type": "choice", "weights": {
            "Avant le premier entretien": 30,
            "Apres le premier entretien": 45,
            "Avant la decision finale": 25,
        }},
        Q["duree"]: {"type": "choice", "weights": {"20 min": 30, "20 - 40 min": 50, "40 - 60 min": 20}},
        Q["administration"]: {"type": "choice_multi", "options_weights": {"Individuelle": 70, "Collective": 40}},
        Q["modalite"]: {"type": "choice_multi", "options_weights": {"Papier crayon": 20, "Digital": 90}},
        Q["instructions"]: {"type": "rating", "range": [3, 5], "center": 4.2},
        Q["environnement"]: {"type": "rating", "range": [3, 5], "center": 4.3},
        Q["stress"]: {"type": "rating", "range": [1, 3], "center": 2.0},
        Q["equite"]: {"type": "rating", "range": [3, 5], "center": 4.4},
        Q["restitution_recu"]: {"type": "choice", "weights": {"Oui": 70, "Non": 5, "Partiellement": 25}},
        Q["forme_restitution"]: {"type": "choice", "weights": {
            "Debrief oral": 40, "Rapport ecrit": 25,
            "Synthese par e-mail": 20, "Acces plate-forme": 10, "Autre": 5,
        }},
        Q["qualite_restitution"]: {"type": "rating", "range": [3, 5], "center": 4.3},
        Q["contribution_dev"]: {"type": "rating", "range": [3, 5], "center": 4.0},
        Q["possibilite_refus"]: {"type": "choice", "weights": {"Oui": 55, "Non": 20, "Je sais pas": 25}},
        Q["confidentialite"]: {"type": "rating", "range": [3, 5], "center": 4.2},
        Q["transparence"]: {"type": "rating", "range": [3, 5], "center": 4.1},
        Q["reduit_biais"]: {"type": "rating", "range": [3, 5], "center": 4.0},
        Q["fidelite"]: {"type": "rating", "range": [3, 5], "center": 3.8},
        Q["anxiogene"]: {"type": "rating", "range": [1, 4], "center": 2.5},
        Q["facile_comprendre"]: {"type": "rating", "range": [3, 5], "center": 4.2},
        Q["restitution_necessaire"]: {"type": "rating", "range": [4, 5], "center": 4.6},
        Q["jamais_seul_critere"]: {"type": "rating", "range": [3, 5], "center": 4.3},
        Q["image_entreprise"]: {"type": "rating", "range": [3, 5], "center": 4.1},
        Q["utilite_recruteurs"]: {"type": "choice", "weights": {
            "Aider a objectiver la decision": 55,
            "Structurer l'entretien": 35,
            "Autre": 10,
        }},
        Q["atout"]: {"type": "text", "pool": ATOUTS_POSITIFS},
        Q["risque_frein"]: {"type": "choice", "weights": {
            "E. Ethique": 20, "confidentialite": 40, "consentement": 40,
        }},
        Q["influence_decision"]: {"type": "choice", "weights": {
            "Faible": 15, "Modere": 50, "Decisif": 20, "Je ne sais pas": 15,
        }},
        Q["nps_recommandation"]: {"type": "nps", "range": [7, 10], "center": 8.5},
        Q["nps_influence_offre"]: {"type": "nps", "range": [5, 9], "center": 7.0},
        Q["recommander_candidats"]: {"type": "choice", "weights": {"Oui": 75, "Non": 5, "Ca depend": 20}},
        Q["nps_experience"]: {"type": "nps", "range": [7, 10], "center": 8.5},
        Q["ameliorations"]: {"type": "text", "pool": AMELIORATIONS_POSITIVES},
        Q["commentaire"]: {"type": "text", "pool": [
            "Bonne experience globale",
            "Tests bien organises et pertinents",
            "J'ai apprecie le debrief apres les tests",
            "Experience professionnelle",
            "RAS, tout etait bien",
            "",
        ]},
    },
}


# ============================================================
# STRATEGIE 2 : CANDIDAT MITIGE
# ============================================================
STRATEGIE_MITIGE = {
    "name": "Candidat Mitige",
    "description": "Experience correcte mais avec des reserves. Notes moyennes, feedback mixte. Trouve les tests utiles mais pas toujours bien mis en oeuvre.",
    "color": "#f39c12",
    "rules": {
        Q["situation"]: {"type": "choice", "weights": {"Candidat externe": 55, "Mobilite interne": 30, "Alternant": 15}},
        Q["niveau_poste"]: {"type": "choice", "weights": {"Employe / Technicien": 35, "Agent de maitrise": 40, "Cadre": 25}},
        Q["secteur"]: {"type": "text", "pool": SECTEURS},
        Q["tests_avant"]: {"type": "choice", "weights": {"Oui": 50, "Non": 50}},
        Q["tests_ici"]: {"type": "choice", "weights": {"Oui": 90, "Non": 10}},
        Q["types_test"]: {"type": "choice", "weights": {
            "Aptitudes (logiques, numerique, verbale)": 40,
            "Personnalite": 30,
            "Motivation / Interets / Valeurs": 15,
            "Mise en situation": 15,
        }},
        Q["moment_process"]: {"type": "choice", "weights": {
            "Avant le premier entretien": 40,
            "Apres le premier entretien": 35,
            "Avant la decision finale": 25,
        }},
        Q["duree"]: {"type": "choice", "weights": {"20 min": 20, "20 - 40 min": 45, "40 - 60 min": 35}},
        Q["administration"]: {"type": "choice_multi", "options_weights": {"Individuelle": 55, "Collective": 50}},
        Q["modalite"]: {"type": "choice_multi", "options_weights": {"Papier crayon": 35, "Digital": 75}},
        Q["instructions"]: {"type": "rating", "range": [2, 4], "center": 3.0},
        Q["environnement"]: {"type": "rating", "range": [2, 4], "center": 3.2},
        Q["stress"]: {"type": "rating", "range": [2, 4], "center": 3.2},
        Q["equite"]: {"type": "rating", "range": [2, 4], "center": 3.1},
        Q["restitution_recu"]: {"type": "choice", "weights": {"Oui": 30, "Non": 30, "Partiellement": 40}},
        Q["forme_restitution"]: {"type": "choice", "weights": {
            "Debrief oral": 30, "Rapport ecrit": 15,
            "Synthese par e-mail": 30, "Acces plate-forme": 15, "Autre": 10,
        }},
        Q["qualite_restitution"]: {"type": "rating", "range": [2, 4], "center": 3.0},
        Q["contribution_dev"]: {"type": "rating", "range": [2, 4], "center": 2.8},
        Q["possibilite_refus"]: {"type": "choice", "weights": {"Oui": 25, "Non": 35, "Je sais pas": 40}},
        Q["confidentialite"]: {"type": "rating", "range": [2, 4], "center": 3.0},
        Q["transparence"]: {"type": "rating", "range": [2, 4], "center": 2.9},
        Q["reduit_biais"]: {"type": "rating", "range": [2, 4], "center": 3.2},
        Q["fidelite"]: {"type": "rating", "range": [2, 4], "center": 2.8},
        Q["anxiogene"]: {"type": "rating", "range": [2, 5], "center": 3.5},
        Q["facile_comprendre"]: {"type": "rating", "range": [2, 4], "center": 3.1},
        Q["restitution_necessaire"]: {"type": "rating", "range": [3, 5], "center": 4.2},
        Q["jamais_seul_critere"]: {"type": "rating", "range": [3, 5], "center": 4.4},
        Q["image_entreprise"]: {"type": "rating", "range": [2, 4], "center": 3.0},
        Q["utilite_recruteurs"]: {"type": "choice", "weights": {
            "Aider a objectiver la decision": 45,
            "Structurer l'entretien": 30,
            "Autre": 25,
        }},
        Q["atout"]: {"type": "text", "pool": ATOUTS_MITIGES},
        Q["risque_frein"]: {"type": "choice", "weights": {
            "E. Ethique": 30, "confidentialite": 35, "consentement": 35,
        }},
        Q["influence_decision"]: {"type": "choice", "weights": {
            "Faible": 30, "Modere": 40, "Decisif": 10, "Je ne sais pas": 20,
        }},
        Q["nps_recommandation"]: {"type": "nps", "range": [4, 8], "center": 6.0},
        Q["nps_influence_offre"]: {"type": "nps", "range": [3, 7], "center": 5.0},
        Q["recommander_candidats"]: {"type": "choice", "weights": {"Oui": 30, "Non": 20, "Ca depend": 50}},
        Q["nps_experience"]: {"type": "nps", "range": [4, 7], "center": 5.5},
        Q["ameliorations"]: {"type": "text", "pool": AMELIORATIONS_MITIGEES},
        Q["commentaire"]: {"type": "text", "pool": [
            "Peut mieux faire sur la restitution",
            "Experience correcte sans plus",
            "Les tests sont un outil parmi d'autres",
            "Mitige sur la pertinence des resultats",
            "",
        ]},
    },
}


# ============================================================
# STRATEGIE 3 : CANDIDAT INSATISFAIT
# ============================================================
STRATEGIE_INSATISFAIT = {
    "name": "Candidat Insatisfait",
    "description": "Mauvaise experience. Notes basses, ne recommande pas, stresse par les tests. Trouve le processus injuste ou inutile.",
    "color": "#e74c3c",
    "rules": {
        Q["situation"]: {"type": "choice", "weights": {"Candidat externe": 60, "Mobilite interne": 25, "Alternant": 15}},
        Q["niveau_poste"]: {"type": "choice", "weights": {"Employe / Technicien": 45, "Agent de maitrise": 35, "Cadre": 20}},
        Q["secteur"]: {"type": "text", "pool": SECTEURS},
        Q["tests_avant"]: {"type": "choice", "weights": {"Oui": 40, "Non": 60}},
        Q["tests_ici"]: {"type": "choice", "weights": {"Oui": 90, "Non": 10}},
        Q["types_test"]: {"type": "choice", "weights": {
            "Aptitudes (logiques, numerique, verbale)": 45,
            "Personnalite": 25,
            "Motivation / Interets / Valeurs": 15,
            "Mise en situation": 15,
        }},
        Q["moment_process"]: {"type": "choice", "weights": {
            "Avant le premier entretien": 50,
            "Apres le premier entretien": 30,
            "Avant la decision finale": 20,
        }},
        Q["duree"]: {"type": "choice", "weights": {"20 min": 10, "20 - 40 min": 35, "40 - 60 min": 55}},
        Q["administration"]: {"type": "choice_multi", "options_weights": {"Individuelle": 45, "Collective": 60}},
        Q["modalite"]: {"type": "choice_multi", "options_weights": {"Papier crayon": 45, "Digital": 65}},
        Q["instructions"]: {"type": "rating", "range": [1, 3], "center": 1.8},
        Q["environnement"]: {"type": "rating", "range": [1, 3], "center": 2.0},
        Q["stress"]: {"type": "rating", "range": [3, 5], "center": 4.2},
        Q["equite"]: {"type": "rating", "range": [1, 3], "center": 2.0},
        Q["restitution_recu"]: {"type": "choice", "weights": {"Oui": 10, "Non": 65, "Partiellement": 25}},
        Q["forme_restitution"]: {"type": "choice", "weights": {
            "Debrief oral": 20, "Rapport ecrit": 10,
            "Synthese par e-mail": 35, "Acces plate-forme": 10, "Autre": 25,
        }},
        Q["qualite_restitution"]: {"type": "rating", "range": [1, 3], "center": 1.8},
        Q["contribution_dev"]: {"type": "rating", "range": [1, 2], "center": 1.4},
        Q["possibilite_refus"]: {"type": "choice", "weights": {"Oui": 10, "Non": 60, "Je sais pas": 30}},
        Q["confidentialite"]: {"type": "rating", "range": [1, 3], "center": 2.0},
        Q["transparence"]: {"type": "rating", "range": [1, 3], "center": 1.8},
        Q["reduit_biais"]: {"type": "rating", "range": [1, 3], "center": 2.0},
        Q["fidelite"]: {"type": "rating", "range": [1, 3], "center": 1.8},
        Q["anxiogene"]: {"type": "rating", "range": [4, 5], "center": 4.6},
        Q["facile_comprendre"]: {"type": "rating", "range": [1, 3], "center": 2.2},
        Q["restitution_necessaire"]: {"type": "rating", "range": [4, 5], "center": 4.8},
        Q["jamais_seul_critere"]: {"type": "rating", "range": [4, 5], "center": 4.8},
        Q["image_entreprise"]: {"type": "rating", "range": [1, 3], "center": 1.8},
        Q["utilite_recruteurs"]: {"type": "choice", "weights": {
            "Aider a objectiver la decision": 30,
            "Structurer l'entretien": 25,
            "Autre": 45,
        }},
        Q["atout"]: {"type": "text", "pool": ATOUTS_NEGATIFS},
        Q["risque_frein"]: {"type": "choice", "weights": {
            "E. Ethique": 35, "confidentialite": 30, "consentement": 35,
        }},
        Q["influence_decision"]: {"type": "choice", "weights": {
            "Faible": 40, "Modere": 25, "Decisif": 10, "Je ne sais pas": 25,
        }},
        Q["nps_recommandation"]: {"type": "nps", "range": [0, 5], "center": 3.0},
        Q["nps_influence_offre"]: {"type": "nps", "range": [0, 4], "center": 2.0},
        Q["recommander_candidats"]: {"type": "choice", "weights": {"Oui": 10, "Non": 55, "Ca depend": 35}},
        Q["nps_experience"]: {"type": "nps", "range": [0, 4], "center": 2.5},
        Q["ameliorations"]: {"type": "text", "pool": AMELIORATIONS_NEGATIVES},
        Q["commentaire"]: {"type": "text", "pool": [
            "Experience stressante et inutile",
            "Les tests ne refletent pas mes competences",
            "Aucune restitution, c'est irrespectueux",
            "Processus deshumanisant",
            "Je ne comprends pas l'interet de ces tests",
            "",
        ]},
    },
}


# ============================================================
# STRATEGIE 4 : CANDIDAT NEUTRE / PRAGMATIQUE
# ============================================================
STRATEGIE_NEUTRE = {
    "name": "Candidat Neutre",
    "description": "Ni pour ni contre, pragmatique. Repond de maniere factuelle, notes au milieu, pas d'avis tranche.",
    "color": "#3498db",
    "rules": {
        Q["situation"]: {"type": "choice", "weights": {"Candidat externe": 45, "Mobilite interne": 35, "Alternant": 20}},
        Q["niveau_poste"]: {"type": "choice", "weights": {"Employe / Technicien": 35, "Agent de maitrise": 35, "Cadre": 30}},
        Q["secteur"]: {"type": "text", "pool": SECTEURS},
        Q["tests_avant"]: {"type": "choice", "weights": {"Oui": 50, "Non": 50}},
        Q["tests_ici"]: {"type": "choice", "weights": {"Oui": 90, "Non": 10}},
        Q["types_test"]: {"type": "choice", "weights": {
            "Aptitudes (logiques, numerique, verbale)": 30,
            "Personnalite": 30,
            "Motivation / Interets / Valeurs": 20,
            "Mise en situation": 20,
        }},
        Q["moment_process"]: {"type": "choice", "weights": {
            "Avant le premier entretien": 35,
            "Apres le premier entretien": 35,
            "Avant la decision finale": 30,
        }},
        Q["duree"]: {"type": "choice", "weights": {"20 min": 30, "20 - 40 min": 45, "40 - 60 min": 25}},
        Q["administration"]: {"type": "choice_multi", "options_weights": {"Individuelle": 60, "Collective": 45}},
        Q["modalite"]: {"type": "choice_multi", "options_weights": {"Papier crayon": 30, "Digital": 80}},
        Q["instructions"]: {"type": "rating", "range": [2, 4], "center": 3.0},
        Q["environnement"]: {"type": "rating", "range": [2, 4], "center": 3.3},
        Q["stress"]: {"type": "rating", "range": [2, 4], "center": 3.0},
        Q["equite"]: {"type": "rating", "range": [2, 4], "center": 3.2},
        Q["restitution_recu"]: {"type": "choice", "weights": {"Oui": 35, "Non": 30, "Partiellement": 35}},
        Q["forme_restitution"]: {"type": "choice", "weights": {
            "Debrief oral": 25, "Rapport ecrit": 20,
            "Synthese par e-mail": 25, "Acces plate-forme": 20, "Autre": 10,
        }},
        Q["qualite_restitution"]: {"type": "rating", "range": [2, 4], "center": 3.0},
        Q["contribution_dev"]: {"type": "rating", "range": [2, 4], "center": 2.8},
        Q["possibilite_refus"]: {"type": "choice", "weights": {"Oui": 30, "Non": 30, "Je sais pas": 40}},
        Q["confidentialite"]: {"type": "rating", "range": [2, 4], "center": 3.2},
        Q["transparence"]: {"type": "rating", "range": [2, 4], "center": 3.0},
        Q["reduit_biais"]: {"type": "rating", "range": [2, 4], "center": 3.0},
        Q["fidelite"]: {"type": "rating", "range": [2, 4], "center": 3.0},
        Q["anxiogene"]: {"type": "rating", "range": [2, 4], "center": 3.0},
        Q["facile_comprendre"]: {"type": "rating", "range": [2, 4], "center": 3.2},
        Q["restitution_necessaire"]: {"type": "rating", "range": [3, 5], "center": 3.8},
        Q["jamais_seul_critere"]: {"type": "rating", "range": [3, 5], "center": 4.0},
        Q["image_entreprise"]: {"type": "rating", "range": [2, 4], "center": 3.0},
        Q["utilite_recruteurs"]: {"type": "choice", "weights": {
            "Aider a objectiver la decision": 40,
            "Structurer l'entretien": 35,
            "Autre": 25,
        }},
        Q["atout"]: {"type": "text", "pool": ATOUTS_MITIGES + ATOUTS_POSITIFS[:3]},
        Q["risque_frein"]: {"type": "choice", "weights": {
            "E. Ethique": 33, "confidentialite": 34, "consentement": 33,
        }},
        Q["influence_decision"]: {"type": "choice", "weights": {
            "Faible": 25, "Modere": 35, "Decisif": 10, "Je ne sais pas": 30,
        }},
        Q["nps_recommandation"]: {"type": "nps", "range": [4, 7], "center": 5.5},
        Q["nps_influence_offre"]: {"type": "nps", "range": [3, 6], "center": 4.5},
        Q["recommander_candidats"]: {"type": "choice", "weights": {"Oui": 25, "Non": 15, "Ca depend": 60}},
        Q["nps_experience"]: {"type": "nps", "range": [4, 7], "center": 5.5},
        Q["ameliorations"]: {"type": "text", "pool": AMELIORATIONS_MITIGEES},
        Q["commentaire"]: {"type": "text", "pool": [
            "Pas d'avis particulier",
            "C'etait correct",
            "Experience standard",
            "",
            "",
        ]},
    },
}


# ============================================================
# STRATEGIE 5 : MIX REALISTE (melange pondéré des 4 profils)
# ============================================================
STRATEGIE_MIX = {
    "name": "Mix Realiste",
    "description": "Melange automatique : 35% satisfaits, 30% mitiges, 15% insatisfaits, 20% neutres. Simule une population reelle de repondants.",
    "color": "#9b59b6",
    "mix": {
        "satisfait": 35,
        "mitige": 30,
        "insatisfait": 15,
        "neutre": 20,
    },
}


ALL_STRATEGIES = {
    "satisfait": STRATEGIE_SATISFAIT,
    "mitige": STRATEGIE_MITIGE,
    "insatisfait": STRATEGIE_INSATISFAIT,
    "neutre": STRATEGIE_NEUTRE,
    "mix": STRATEGIE_MIX,
}


# ============================================================
# MOTEUR DE RESOLUTION
# ============================================================

def weighted_choice(weights_dict):
    """Choisit une option selon des poids ponderes."""
    options = list(weights_dict.keys())
    weights = list(weights_dict.values())
    total = sum(weights)
    r = random.uniform(0, total)
    cumul = 0
    for opt, w in zip(options, weights):
        cumul += w
        if r <= cumul:
            return opt
    return options[-1]


def gaussian_int(center, low, high):
    """Genere un entier selon une distribution gaussienne bornee."""
    # Sigma calibre pour que ~95% des valeurs tombent dans [low, high]
    sigma = (high - low) / 3.5
    if sigma <= 0:
        return round(center)
    val = random.gauss(center, sigma)
    val = max(low, min(high, val))
    return round(val)


def resolve_rule(rule):
    """Resout une regle en une valeur concrete."""
    rtype = rule["type"]

    if rtype == "choice":
        return weighted_choice(rule["weights"])

    if rtype == "choice_multi":
        result = []
        for opt, prob in rule["options_weights"].items():
            if random.randint(1, 100) <= prob:
                result.append(opt)
        return result if result else [list(rule["options_weights"].keys())[0]]

    if rtype == "rating":
        return gaussian_int(rule["center"], rule["range"][0], rule["range"][1])

    if rtype == "nps":
        return gaussian_int(rule["center"], rule["range"][0], rule["range"][1])

    if rtype == "text":
        return random.choice(rule["pool"])

    return None


def resolve_strategy(strategy_key):
    """
    Resout une strategie complete en un dict {question_id: valeur}.
    Chaque appel produit des reponses differentes.
    """
    strategy = ALL_STRATEGIES.get(strategy_key)
    if not strategy:
        return {}

    # Si c'est un mix, choisir d'abord quel profil utiliser
    if "mix" in strategy:
        chosen = weighted_choice(strategy["mix"])
        strategy = ALL_STRATEGIES[chosen]

    answers = {}
    for qid, rule in strategy["rules"].items():
        val = resolve_rule(rule)
        if val is not None and val != "":
            answers[qid] = val
    return answers


def get_strategies_info():
    """Retourne les infos des strategies pour le frontend."""
    result = {}
    for key, strat in ALL_STRATEGIES.items():
        result[key] = {
            "name": strat["name"],
            "description": strat["description"],
            "color": strat["color"],
        }
        if "mix" in strat:
            result[key]["is_mix"] = True
            result[key]["mix"] = strat["mix"]
    return result
