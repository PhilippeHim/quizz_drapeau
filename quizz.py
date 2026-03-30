import streamlit as st
import streamlit.components.v1 as components
import base64
import html
import os
import random
import sys
from streamlit.runtime.scriptrunner_utils.script_run_context import get_script_run_ctx


DOSSIER_CIBLE = "drapeaux"
MIME_TYPES_IMAGES = {
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
}


def execution_via_streamlit():
    """Retourne True si le script est lance via `streamlit run`."""
    return get_script_run_ctx(suppress_warning=True) is not None

def charger_drapeaux_et_initialiser_session():
    
    if 'drapeaux_restants' not in st.session_state:
        drapeaux_data = []
        for nom_fichier in os.listdir(DOSSIER_CIBLE):
            if nom_fichier.lower().endswith(('.svg', '.png', '.jpg', '.jpeg')):
                chemin_complet = os.path.join(DOSSIER_CIBLE, nom_fichier)
                nom_pays = os.path.splitext(nom_fichier)[0]
                drapeaux_data.append({'chemin': chemin_complet, 'nom_pays': nom_pays})
        
        random.shuffle(drapeaux_data)
        
        st.session_state['drapeaux_originaux'] = drapeaux_data
        st.session_state['drapeaux_restants'] = list(drapeaux_data)
        st.session_state['index_courant'] = 0
        st.session_state['montrer_reponse'] = False
        st.session_state['quiz_termine'] = False
        
    if not st.session_state['drapeaux_originaux']:
        st.error(f"Aucun fichier de drapeau trouvé dans le dossier '{DOSSIER_CIBLE}'.")
        st.stop()


def passer_au_suivant():
    """Logique pour passer au drapeau suivant."""
    
    if st.session_state['montrer_reponse']:
        st.session_state['index_courant'] += 1
        st.session_state['montrer_reponse'] = False
        
        if st.session_state['index_courant'] >= len(st.session_state['drapeaux_originaux']):
            st.session_state['quiz_termine'] = True
    else:

        st.session_state['montrer_reponse'] = True


def activer_raccourci_entree(libelle_bouton):
    """Associe la touche Entree au bouton principal affiche."""
    components.html(
        f"""
        <script>
            const doc = window.parent.document;
            const targetLabel = {libelle_bouton!r};

            const normalize = (value) => value.replace(/\\s+/g, " ").trim();
            const previousHandler = doc.defaultView.__quizEnterHandler;

            if (previousHandler) {{
                doc.removeEventListener("keydown", previousHandler, true);
            }}

            const handler = (event) => {{
                if (event.key !== "Enter" && event.key !== "NumpadEnter") {{
                    return;
                }}

                const tagName = event.target?.tagName;
                if (
                    ["INPUT", "TEXTAREA", "SELECT", "BUTTON"].includes(tagName) ||
                    event.target?.isContentEditable
                ) {{
                    return;
                }}

                const bouton = Array.from(doc.querySelectorAll("button")).find(
                    (element) => normalize(element.innerText) === normalize(targetLabel)
                );

                if (!bouton) {{
                    return;
                }}

                event.preventDefault();
                event.stopPropagation();
                bouton.click();
            }};

            doc.defaultView.__quizEnterHandler = handler;
            doc.addEventListener("keydown", handler, true);
        </script>
        """,
        height=0,
    )


def construire_data_uri_image(chemin_image):
    """Construit une data URI pour afficher proprement l'image en HTML."""
    extension = os.path.splitext(chemin_image)[1].lower()
    mime_type = MIME_TYPES_IMAGES.get(extension, "application/octet-stream")

    with open(chemin_image, "rb") as fichier_image:
        contenu_encode = base64.b64encode(fichier_image.read()).decode("utf-8")

    return f"data:{mime_type};base64,{contenu_encode}"


def afficher_drapeau(chemin_image, legende):
    """Affiche le drapeau sans depasser de la fenetre."""
    data_uri = construire_data_uri_image(chemin_image)
    legende_html = html.escape(legende)

    st.markdown(
        f"""
        <div style="
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            height: min(65vh, 700px);
            padding: 1rem 0;
            overflow: hidden;
        ">
            <img
                src="{data_uri}"
                alt="{legende_html}"
                style="
                    max-width: 100%;
                    max-height: 100%;
                    width: auto;
                    height: auto;
                    object-fit: contain;
                "
            />
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(legende)


def application_quiz():
    st.set_page_config(layout="wide")
    st.title("🌍 Quiz des Drapeaux du Monde")
    
    charger_drapeaux_et_initialiser_session()
    
    if st.session_state['quiz_termine']:
        st.balloons()
        st.success("🎉 Félicitations ! Vous avez parcouru tous les drapeaux.")
        if st.button("Recommencer le Quiz"):

            del st.session_state['drapeaux_restants']
            st.rerun()
        return

    drapeaux = st.session_state['drapeaux_originaux']
    index = st.session_state['index_courant']
    drapeau_actuel = drapeaux[index]
    

    st.markdown(f"**Drapeau n° {index + 1}** sur **{len(drapeaux)}**")
    

    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col2:
        afficher_drapeau(drapeau_actuel['chemin'], "Quel est ce pays ?")

    if st.session_state['montrer_reponse']:
        st.markdown(f"<h1 style='text-align: center; color: green;'>{drapeau_actuel['nom_pays']}</h1>", unsafe_allow_html=True)

        libelle_bouton = "Drapeau Suivant (⏎)"
        st.button(libelle_bouton, on_click=passer_au_suivant, width="stretch")
    else:

        libelle_bouton = "Révéler la Réponse (⏎)"
        st.button(libelle_bouton, on_click=passer_au_suivant, type="primary", width="stretch")

    activer_raccourci_entree(libelle_bouton)


if __name__ == "__main__":
    if execution_via_streamlit():
        application_quiz()
    else:
        print("Cette application doit etre lancee avec Streamlit.")
        print(f"Commande : {sys.executable} -m streamlit run quizz.py")
