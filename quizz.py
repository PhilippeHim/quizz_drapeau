import streamlit as st
import os
import random
from PIL import Image


DOSSIER_CIBLE = "drapeaux"

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

        st.image(drapeau_actuel['chemin'], use_container_width=True, caption="Quel est ce pays ?")

    if st.session_state['montrer_reponse']:
        st.markdown(f"<h1 style='text-align: center; color: green;'>{drapeau_actuel['nom_pays']}</h1>", unsafe_allow_html=True)

        st.button("Drapeau Suivant (⏎)", on_click=passer_au_suivant, use_container_width=True)
    else:

        st.button("Révéler la Réponse (⏎)", on_click=passer_au_suivant, type="primary", use_container_width=True)


if __name__ == "__main__":
    application_quiz()