"""
Configuration du formulaire Microsoft Forms.
Contient la structure complète des questions avec leurs IDs techniques.
"""

FORM_URL = "https://forms.office.com/Pages/ResponsePage.aspx?id=GMsoogB-dESACoiaRXvibekBIfR14vxHiGxcS3aAkzdUODRIVDQ4TThMN1BKUEtETjNCVktHRzdRSS4u"
FORM_ID = "GMsoogB-dESACoiaRXvibekBIfR14vxHiGxcS3aAkzdUODRIVDQ4TThMN1BKUEtETjNCVktHRzdRSS4u"
TENANT_ID = "a228cb18-7e00-4474-800a-889a457be26d"
USER_ID = "f42101e9-e275-47fc-886c-5c4b76809337"

API_BASE = f"https://forms.office.com/formapi/api/{TENANT_ID}/users/{USER_ID}"
SUBMIT_URL = f"{API_BASE}/forms('{FORM_ID}')/responses"

QUESTIONS = [
    # === Section A : Profil du repondant ===
    {
        "id": "r020f4f892fa14420a8c41b5b06f0fc43",
        "section": "A. Profil du repondant",
        "title": "Votre situation au moment du recrutement",
        "type": "choice",
        "required": True,
        "options": ["Candidat externe", "Mobilite interne", "Alternant"],
    },
    {
        "id": "r63689e2a3bf8484abf8cffc5383c28e9",
        "section": "A. Profil du repondant",
        "title": "Niveau de poste vise",
        "type": "choice",
        "required": True,
        "options": ["Employe / Technicien", "Agent de maitrise", "Cadre"],
    },
    {
        "id": "r16d390cf1b504ebb8d2f60d5c13388e5",
        "section": "A. Profil du repondant",
        "title": "Secteur d'activite de l'entreprise",
        "type": "text",
        "required": False,
        "multiline": True,
    },
    {
        "id": "r3e53b86f1d4b4a798f392f18c3161f7e",
        "section": "A. Profil du repondant",
        "title": "Aviez-vous deja passe des tests psychometriques avant ce recrutement ?",
        "type": "choice",
        "required": True,
        "options": ["Oui", "Non"],
    },
    {
        "id": "r9a7783c02a4b4369b5b878b9b9a36792",
        "section": "A. Profil du repondant",
        "title": "Dans ce recrutement, avez-vous passe des tests psychometriques ?",
        "type": "choice",
        "required": True,
        "options": ["Oui", "Non"],
    },

    # === Section B : Experience de passation ===
    {
        "id": "r85a7eaabbcda484698a30d5db65f58cb",
        "section": "B. Experience de passation",
        "title": "Quels types de test avez-vous passes ?",
        "type": "choice",
        "required": False,
        "options": [
            "Aptitudes (logiques, numerique, verbale)",
            "Personnalite",
            "Motivation / Interets / Valeurs",
            "Mise en situation",
        ],
    },
    {
        "id": "r879b4c0f290842dda1c133441a1adde5",
        "section": "B. Experience de passation",
        "title": "A quel moment du processus de recrutement ?",
        "type": "choice",
        "required": False,
        "options": [
            "Avant le premier entretien",
            "Apres le premier entretien",
            "Avant la decision finale",
        ],
    },
    {
        "id": "r444a32c5ea73499294e7422a4f7f0401",
        "section": "B. Experience de passation",
        "title": "Duree totale des tests",
        "type": "choice",
        "required": False,
        "options": ["20 min", "20 - 40 min", "40 - 60 min"],
    },
    {
        "id": "ree912609a6b244479b1c281850f875a5",
        "section": "B. Experience de passation",
        "title": "Administration des tests",
        "type": "choice_multi",
        "required": False,
        "options": ["Individuelle", "Collective"],
    },
    {
        "id": "r7193c3cc6841463f903e688b9cdccd82",
        "section": "B. Experience de passation",
        "title": "Modalite de passation du test",
        "type": "choice_multi",
        "required": False,
        "options": ["Papier crayon", "Digital"],
    },

    # === Section C : Conditions de passation ===
    {
        "id": "r8702ce4cb5004424a5abcc0f1f12d9f5",
        "section": "C. Conditions de passation",
        "title": "Instructions recues avant les tests",
        "type": "rating",
        "required": False,
        "min": 1,
        "max": 5,
    },
    {
        "id": "r3f7be34423eb4f48af43d0974d56c178",
        "section": "C. Conditions de passation",
        "title": "Environnement technique (facilite, stabilite, ergonomie)",
        "type": "rating",
        "required": False,
        "min": 1,
        "max": 5,
    },
    {
        "id": "r8d388a2dac404f518c2f577967d005d0",
        "section": "C. Conditions de passation",
        "title": "Stress ressenti durant les tests",
        "type": "rating",
        "required": False,
        "min": 1,
        "max": 5,
    },
    {
        "id": "rabd463f274c34fd08038efd9353321d6",
        "section": "C. Conditions de passation",
        "title": "Perception d'equite : les tests m'ont semble justes et non discriminants",
        "type": "rating",
        "required": False,
        "min": 1,
        "max": 5,
    },

    # === Section D : Restitution ===
    {
        "id": "r4eb335901f914c3f8633892028ed93ad",
        "section": "D. Restitution",
        "title": "Avez-vous recu une restitution de vos resultats ?",
        "type": "choice",
        "required": False,
        "options": ["Oui", "Non", "Partiellement"],
    },
    {
        "id": "reada7faa68ea4927bac88d35881635e6",
        "section": "D. Restitution",
        "title": "Si Oui/Partielle : Sous quelle forme ?",
        "type": "choice",
        "required": False,
        "options": [
            "Debrief oral",
            "Rapport ecrit",
            "Synthese par e-mail",
            "Acces plate-forme",
            "Autre",
        ],
    },
    {
        "id": "r2e4b366ea5744b1ca78dcc390acfdb24",
        "section": "D. Restitution",
        "title": "Qualite de la restitution : comprehensible",
        "type": "rating",
        "required": False,
        "min": 1,
        "max": 5,
    },
    {
        "id": "ra30c1de1b51d47c7ae2a7559dd10e477",
        "section": "D. Restitution",
        "title": "La restitution a-t-elle contribue a mon developpement ?",
        "type": "rating",
        "required": False,
        "min": 1,
        "max": 5,
    },

    # === Section E : Ethique et consentement ===
    {
        "id": "r9d5e66a1882b488ba9fd1dd67ae423fe",
        "section": "E. Ethique et consentement",
        "title": "J'ai eu la possibilite de refuser les tests sans penalite ?",
        "type": "choice",
        "required": False,
        "options": ["Oui", "Non", "Je sais pas"],
    },
    {
        "id": "rbd8e625e214b4b67b1cc3187a70942a1",
        "section": "E. Ethique et consentement",
        "title": "Je suis a l'aise avec le niveau de confidentialite des tests",
        "type": "rating",
        "required": False,
        "min": 1,
        "max": 5,
    },
    {
        "id": "r84cebdc50d9d41c283b86083cf4cffbf",
        "section": "E. Ethique et consentement",
        "title": "Les tests psychometriques apportent de la transparence au recrutement",
        "type": "rating",
        "required": False,
        "min": 1,
        "max": 5,
    },

    # === Section F : Perception generale ===
    {
        "id": "r2d485046e6254dfc95c2db4f30e0d93b",
        "section": "F. Perception generale",
        "title": "Les tests reduisent certains biais de jugement",
        "type": "rating",
        "required": False,
        "min": 1,
        "max": 5,
    },
    {
        "id": "r66e8f3dd01934a17a91eeb1821fb6f82",
        "section": "F. Perception generale",
        "title": "Les tests refletent fidelement la maniere de fonctionner",
        "type": "rating",
        "required": False,
        "min": 1,
        "max": 5,
    },
    {
        "id": "r5d8aa3e2ce2b49bdbe548b7ca62a9eee",
        "section": "F. Perception generale",
        "title": "Les tests peuvent etre anxiogenes pour certains candidats",
        "type": "rating",
        "required": False,
        "min": 1,
        "max": 5,
    },
    {
        "id": "rc6e3019b4b454a16a2037de82c2d26ee",
        "section": "F. Perception generale",
        "title": "Les tests sont faciles a comprendre pour un candidat",
        "type": "rating",
        "required": False,
        "min": 1,
        "max": 5,
    },
    {
        "id": "rec610b31c6b44512a615abd6ef82e455",
        "section": "F. Perception generale",
        "title": "Les tests devraient toujours etre accompagnes d'une restitution",
        "type": "rating",
        "required": False,
        "min": 1,
        "max": 5,
    },
    {
        "id": "r51ef2d1b49b84a19916b1cb97f7d57a7",
        "section": "F. Perception generale",
        "title": "Les tests ne devraient jamais etre la seule base d'une decision",
        "type": "rating",
        "required": False,
        "min": 1,
        "max": 5,
    },
    {
        "id": "rfb6987ac6a534362b3d42a71a088c780",
        "section": "F. Perception generale",
        "title": "Les tests ameliorent l'image de l'entreprise qui les utilise",
        "type": "rating",
        "required": False,
        "min": 1,
        "max": 5,
    },

    # === Section G : Utilite et recommandation ===
    {
        "id": "r57771f8fdcc2451cbe151ae77552810f",
        "section": "G. Utilite et recommandation",
        "title": "Utilite des tests pour les recruteurs",
        "type": "choice",
        "required": False,
        "options": [
            "Aider a objectiver la decision",
            "Structurer l'entretien",
            "Autre",
        ],
    },
    {
        "id": "rd238594fc2164511bc57184525995ea9",
        "section": "G. Utilite et recommandation",
        "title": "Quel principal atout voyez-vous dans ces tests ?",
        "type": "text",
        "required": False,
        "multiline": True,
    },
    {
        "id": "r0ecfd1408ced4bc687cde2a25a2d1eab",
        "section": "G. Utilite et recommandation",
        "title": "Quel principal risque ou frein voyez-vous ?",
        "type": "choice",
        "required": False,
        "options": ["E. Ethique", "confidentialite", "consentement"],
        "allow_other": True,
    },
    {
        "id": "rfcf4d411f0ad41a9a05acfcbeaa00f7e",
        "section": "G. Utilite et recommandation",
        "title": "Degre d'influence percu sur la decision finale",
        "type": "choice",
        "required": False,
        "options": ["Faible", "Modere", "Decisif", "Je ne sais pas"],
    },

    # === Section H : Evaluation globale ===
    {
        "id": "r2c0881af018a48ffab04c5c7e04c0718",
        "section": "H. Evaluation globale",
        "title": "Recommanderiez-vous notre service a un ami ou un collegue ? (NPS 0-10)",
        "type": "nps",
        "required": False,
        "min": 0,
        "max": 10,
    },
    {
        "id": "rcb0fdb082b1349d1b92bf866ae555f0e",
        "section": "H. Evaluation globale",
        "title": "Les tests ont influence ma decision d'accepter/refuser l'offre (1-10)",
        "type": "nps",
        "required": False,
        "min": 0,
        "max": 10,
    },
    {
        "id": "r8b109331b45e4081b5df2c9c23e0f8e2",
        "section": "H. Evaluation globale",
        "title": "Recommanderiez-vous ce type d'evaluation a d'autres candidats ?",
        "type": "choice",
        "required": False,
        "options": ["Oui", "Non", "Ca depend"],
    },
    {
        "id": "r4eb75bb6bfe24c37895ca0d227afc004",
        "section": "H. Evaluation globale",
        "title": "Globalement, comment evaluez-vous votre experience ? (NPS 0-10)",
        "type": "nps",
        "required": False,
        "min": 0,
        "max": 10,
    },
    {
        "id": "r00430e273398489a89de9c256551b202",
        "section": "H. Evaluation globale",
        "title": "Comment l'entreprise pourrait-elle ameliorer l'experience des tests ?",
        "type": "text",
        "required": False,
        "multiline": True,
    },
    {
        "id": "r0ed595b93c2348dba87fe89430b50c86",
        "section": "H. Evaluation globale",
        "title": "Commentaire final",
        "type": "text",
        "required": False,
        "multiline": False,
    },
]

def get_sections():
    """Retourne les questions groupees par section."""
    sections = {}
    for q in QUESTIONS:
        sec = q["section"]
        if sec not in sections:
            sections[sec] = []
        sections[sec].append(q)
    return sections
