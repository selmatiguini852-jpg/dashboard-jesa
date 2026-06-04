import streamlit as st
import pandas as pd

def show_fiabilite():
    st.markdown("<h2 style='color: #1E3A8A;'>⚙️ Audit de Fiabilité (Analyse par Phases)</h2>", unsafe_allow_html=True)
    st.write("Cet outil permet de diagnostiquer un équipement et de discuter les solutions étape par étape.")

    # --- PHASE 1 : SAISIE ---
    st.markdown("### 🟦 PHASE 1 : Saisie des données terrain")
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            equipement = st.selectbox("Équipement à auditer", ["A11ST229", "A11HX230", "A11ST215", "A11TK200"])
            tps_ouverture = st.number_input("Temps d'ouverture (h)", value=720)
        with col2:
            nb_pannes = st.number_input("Nombre de pannes", min_value=1, value=1)
            tps_arret = st.number_input("Temps total d'arrêt (h)", value=0.0)
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            # On utilise une variable pour déclencher l'affichage de la phase 2
            analyser = st.button("🔍 Lancer le Diagnostic", use_container_width=True)

    # --- LOGIQUE DE CALCUL ---
    # Initialisation pour éviter les bugs d'affichage
    mtbf, mttr, dispo = 0, 0, 0
    tbf = tps_ouverture - tps_arret
    if nb_pannes > 0:
        mtbf = tbf / nb_pannes
        mttr = tps_arret / nb_pannes
        if (mtbf + mttr) > 0:
            dispo = (mtbf / (mtbf + mttr)) * 100

    # --- PHASE 2 : RÉSULTATS ---
    st.markdown("### 🟨 PHASE 2 : Interprétation & Résultats")
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        c1.metric("Fiabilité (MTBF)", f"{mtbf:.1f} h")
        c2.metric("Maintenabilité (MTTR)", f"{mttr:.1f} h")
        c3.metric("Disponibilité", f"{dispo:.2f} %")

        if analyser:
            st.markdown("---")
            st.info("**Analyse du système :**")
            if mttr > 4:
                st.warning(f"👉 Le temps de réparation ({mttr:.1f}h) est élevé. Vérifiez le stock PDR ou l'outillage.")
            if mtbf < 100:
                st.error(f"👉 Les pannes sont trop fréquentes. La fiabilité de {equipement} est critique.")

    # --- PHASE 3 : DÉCISION ---
    st.markdown("### 🟥 PHASE 3 : Plan d'Action & Décision")
    with st.container(border=True):
        causes = st.multiselect("Quelles sont les causes probables identification ?", 
                               ["Usure normale", "Mauvaise conduite", "Défaut de lubrification", "Pièce non conforme", "Conditions climatiques"])
        
        notes = st.text_area("Observations de l'expert :", placeholder="Écrivez vos conclusions ici...")
        
        decision = st.radio("Décision finale :", 
                           ["Maintenir le plan actuel", "Augmenter le préventif", "Rénovation (Overhaul)", "Remplacement de l'équipement"],
                           horizontal=True)
        
        if st.button("💾 Enregistrer l'Audit final", use_container_width=True):
            st.success(f"L'audit pour {equipement} a été sauvegardé avec la décision : {decision}")