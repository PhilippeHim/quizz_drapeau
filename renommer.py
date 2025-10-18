# rename_flags_to_french.py
import os
import re
import unicodedata
from pathlib import Path

FOLDER = Path("drapeaux")  # ton dossier
VALID_EXTS = {".svg", ".png", ".jpg", ".jpeg", ".webp"}


def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def norm_key(name: str) -> str:
    """
    Normalisation pour trouver la clé de mapping :
    - enlève extension, parenthèses/annotations
    - remplace tirets/underscores par espaces
    - passe en minuscules
    - enlève accents
    - compresse les espaces
    """
    base = re.sub(r"\.[A-Za-z0-9]+$", "", name)  # enlève extension
    base = re.sub(r"\(.*?\)", " ", base)        # enlève (annotations)
    base = base.replace("_", " ").replace("-", " ")
    base = re.sub(r"\s+", " ", base).strip()
    base = strip_accents(base).lower()
    return base


def fr_filename(country_fr: str, ext: str) -> str:
    """
    Formate le nom final :
    - espaces simples
    - garde les tirets si présents dans l’endonyme français fourni
    - corrige double espaces
    """
    country_fr = re.sub(r"\s+", " ", country_fr).strip()
    return f"{country_fr}{ext}"


# --- TABLE DE CORRESPONDANCE EN → FR ---
# Les clés sont en "norm_key" (donc sans accents, minuscules, espaces simples)
MAP_EN_TO_FR = {
    # Exemples déjà français mais on sécurise la casse/accents
    "cote d ivoire": "Côte d’Ivoire",
    "republique democratique du congo": "République démocratique du Congo",
    "republique du congo": "République du Congo",
    "emirats arabes unis": "Émirats arabes unis",
    "pays bas": "Pays-Bas",
    "iles cook": "Îles Cook",
    "iles marshall": "Îles Marshall",
    "iles salomon": "Îles Salomon",
    "timor oriental": "Timor oriental",
    "micronesie": "Micronésie",
    "tchequie": "Tchéquie",
    "etat s unis": "États-Unis",
    "etats unis": "États-Unis",
    "royaume uni": "Royaume-Uni",
    "sao tome et principe": "São Tomé-et-Principe",
    "coree du sud": "Corée du Sud",
    "coree du nord": "Corée du Nord",

    # Anglais → Français
    "nigeria": "Nigéria",
    "australie": "Australie",
    "switzerland": "Suisse",
    "panama": "Panama",
    "oman": "Oman",
    "malaysia": "Malaisie",
    "montenegro": "Monténégro",
    "madagascar": "Madagascar",
    "grenada": "Grenade",
    "tonga": "Tonga",
    "libya": "Libye",
    "ecuador": "Équateur",
    "gabon": "Gabon",
    "cyprus": "Chypre",
    "andorra": "Andorre",
    "greece": "Grèce",
    "benin": "Bénin",
    "brazil": "Brésil",
    "mozambique": "Mozambique",
    "belgium": "Belgique",
    "moldova": "Moldavie",
    "seychelles": "Seychelles",
    "burundi": "Burundi",
    "sweden": "Suède",
    "nepal": "Népal",
    "monaco": "Monaco",
    "turkey": "Turquie",
    "cameroon": "Cameroun",
    "niue": "Niue",
    "kiribati": "Kiribati",
    "armenia": "Arménie",
    "honduras": "Honduras",
    "algeria": "Algérie",
    "china": "Chine",
    "sierra leone": "Sierra Leone",
    "cuba": "Cuba",
    "tajikistan": "Tadjikistan",
    "kyrgyzstan": "Kirghizistan",
    "laos": "Laos",
    "syria": "Syrie",
    "estonia": "Estonie",
    "guinea": "Guinée",
    "tunisia": "Tunisie",
    "ukraine": "Ukraine",
    "angola": "Angola",
    "djibouti": "Djibouti",
    "cambodia": "Cambodge",
    "lesotho": "Lesotho",
    "zambia": "Zambie",
    "jamaica": "Jamaïque",
    "tanzania": "Tanzanie",
    "iran": "Iran",
    "namibia": "Namibie",
    "venezuela": "Venezuela",
    "colombia": "Colombie",
    "liberia": "Libéria",
    "iceland": "Islande",
    "hungary": "Hongrie",
    "kazakhstan": "Kazakhstan",
    "argentina": "Argentine",
    "poland": "Pologne",
    "bolivia": "Bolivie",
    "russia": "Russie",
    "guatemala": "Guatemala",
    "ghana": "Ghana",
    "kenya": "Kenya",
    "afghanistan": "Afghanistan",
    "samoa": "Samoa",
    "norway": "Norvège",
    "mexico": "Mexique",
    "belize": "Belize",
    "botswana": "Botswana",
    "morocco": "Maroc",
    "romania": "Roumanie",
    "chile": "Chili",
    "indonesia": "Indonésie",
    "slovenia": "Slovénie",
    "slovakia": "Slovaquie",
    "nauru": "Nauru",
    "lithuania": "Lituanie",
    "ireland": "Irlande",
    "finland": "Finlande",
    "uzbekistan": "Ouzbékistan",
    "japan": "Japon",
    "vietnam": "Viêt Nam",
    "uruguay": "Uruguay",
    "malta": "Malte",
    "egypt": "Égypte",
    "niger": "Niger",
    "malawi": "Malawi",
    "croatia": "Croatie",
    "fiji": "Fidji",
    "jordan": "Jordanie",
    "vanuatu": "Vanuatu",
    "the bahamas": "Bahamas",
    "bahamas": "Bahamas",
    "palestine": "Palestine",
    "iraq": "Irak",
    "vatican": "Vatican",
    "ethiopia": "Éthiopie",
    "georgia": "Géorgie",
    "lebanon": "Liban",
    "singapore": "Singapour",
    "peru": "Pérou",
    "canada": "Canada",
    "india": "Inde",
    "philippines": "Philippines",
    "barbados": "Barbade",
    "cape verde": "Cap-Vert",
    "albania": "Albanie",
    "denmark": "Danemark",
    "trinidad and tobago": "Trinité-et-Tobago",
    "palau": "Palaos",
    "belarus": "Biélorussie",   # ou "Bélarus" selon préférence
    "eritrea": "Érythrée",
    "chad": "Tchad",
    "brunei": "Brunéi",
    "liechtenstein": "Liechtenstein",
    "italy": "Italie",
    "zimbabwe": "Zimbabwe",
    "france": "France",
    "south africa": "Afrique du Sud",
    "dominica": "Dominique",
    "kuwait": "Koweït",
    "thailand": "Thaïlande",
    "burkina faso": "Burkina Faso",
    "bangladesh": "Bangladesh",
    "serbia": "Serbie",
    "mali": "Mali",
    "suriname": "Suriname",
    "mongolia": "Mongolie",
    "bahrain": "Bahreïn",
    "san marino": "Saint-Marin",
    "luxembourg": "Luxembourg",
    "paraguay": "Paraguay",
    "eswatini": "Eswatini",
    "portugal": "Portugal",
    "mauritius": "Maurice",
    "spain": "Espagne",
    "tuvalu": "Tuvalu",
    "gambia": "Gambie",
    "myanmar": "Myanmar",  # ou "Birmanie"
    "turkmenistan": "Turkménistan",
    "nicaragua": "Nicaragua",
    "haiti": "Haïti",
    "costa rica": "Costa Rica",
    "guinea bissau": "Guinée-Bissau",
    "uganda": "Ouganda",
    "austria": "Autriche",
    "israel": "Israël",
    "latvia": "Lettonie",
    "sudan": "Soudan",
    "maldives": "Maldives",
    "somalia": "Somalie",
    "germany": "Allemagne",
    "saudi arabia": "Arabie saoudite",
    "bhutan": "Bhoutan",
    "qatar": "Qatar",
    "azerbaijan": "Azerbaïdjan",
    "pakistan": "Pakistan",
    "mauritania": "Mauritanie",
    "bulgaria": "Bulgarie",
    "sri lanka": "Sri Lanka",
    "togo": "Togo",
    "yemen": "Yémen",
    "united kingdom": "Royaume-Uni",
    "the united kingdom": "Royaume-Uni",
    "guyana": "Guyana",
    "south korea": "Corée du Sud",
    "el salvador": "Salvador",
    # variantes qu’on voit parfois dans les noms de fichiers
    "republique centrafricaine": "République centrafricaine",
    "republique dominicaine": "République dominicaine",
    "bosnie herzegovine": "Bosnie-Herzégovine",
    "macedoine du nord": "Macédoine du Nord",
    "soudan du sud": "Soudan du Sud",
}


# corrections orthographiques/casse François → François (ex. 'South africa.svg' déjà fr-anglicisé)
FIX_FR_CLEANUP = {
    "south africa": "Afrique du Sud",
    "the united kingdom": "Royaume-Uni",
    "the bahamas": "Bahamas",
    "sao tome et  principe": "São Tomé-et-Principe",  # 2 espaces dans ton liste
    "emirats arabes unis": "Émirats arabes unis",
    "cote d ivoire": "Côte d’Ivoire",
    "micronesie": "Micronésie",
}


def main():
    renamed, skipped, unresolved = [], [], []

    if not FOLDER.exists():
        print(f"❌ Dossier introuvable: {FOLDER}")
        return

    for path in sorted(FOLDER.iterdir()):
        if not path.is_file():
            continue
        ext = path.suffix.lower()
        if ext not in VALID_EXTS:
            continue

        original = path.name
        key = norm_key(original)  # clé normalisée

        # 1) enlever les mentions comme '(pantone)', '(3-5)', '(2025-)' de la cible finale
        key_clean = re.sub(r"\b(pantone|flag|ensign)\b", "", key)
        key_clean = re.sub(r"\d{2,4}\s*-\s*\d{0,4}", "", key_clean)  # ex: '3-5', '2025-'
        key_clean = re.sub(r"\s+", " ", key_clean).strip()

        # 2) mapping principal
        fr = MAP_EN_TO_FR.get(key_clean)

        # 3) fallback : corrections FR (cas mixtes/bad case)
        if not fr:
            fr = FIX_FR_CLEANUP.get(key_clean)

        # 4) si toujours pas, tenter heuristique : mettre majuscules françaises “simples”
        if not fr:
            # Remet un peu de casse correcte sans diacritiques
            approx = " ".join(w.capitalize() for w in key_clean.split())
            fr = approx

        # Compose le nom final
        new_name = fr_filename(fr, ext)

        # Ne renomme pas si identique
        if new_name == original:
            skipped.append(original)
            continue

        # Si le chemin cible existe déjà, ajoute un suffixe (2), (3)…
        target = FOLDER / new_name
        if target.exists():
            stem, e = os.path.splitext(new_name)
            i = 2
            while (FOLDER / f"{stem} ({i}){e}").exists():
                i += 1
            target = FOLDER / f"{stem} ({i}){e}"

        try:
            path.rename(target)
            renamed.append((original, target.name))
            # print(f"✅ {original} -> {target.name}")
        except Exception as e:
            unresolved.append((original, str(e)))

    print("\n=== RAPPORT ===")
    print(f"✅ Renommés : {len(renamed)}")
    print(f"⏭️  Inchangés : {len(skipped)}")
    print(f"⚠️ Non résolus/erreurs : {len(unresolved)}")

    if renamed:
        print("\nRenommages réalisés (extraits) :")
        for a, b in renamed[:20]:
            print(f"- {a}  →  {b}")
        if len(renamed) > 20:
            print("…")

    if unresolved:
        print("\nProblèmes rencontrés :")
        for a, err in unresolved[:20]:
            print(f"- {a} : {err}")
        if len(unresolved) > 20:
            print("…")


if __name__ == "__main__":
    main()
