import streamlit as st
import random
import time

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Aurelflex - Coach", page_icon="💪", layout="centered")

# --- 0. INITIALISATION MÉMOIRE (Tout en haut pour éviter les erreurs) ---
if 'seance' not in st.session_state:
    st.session_state.seance = None
if 'mode_entrainement' not in st.session_state:
    st.session_state.mode_entrainement = False

# --- FONCTION DE RESET (La solution à ton problème) ---
def reset_app():
    """Cette fonction se lance quand on change de mode (Muscu/Cardio)"""
    st.session_state.mode_entrainement = False
    st.session_state.seance = None

# --- 1. L'INTERFACE (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2548/2548532.png", width=100)
    st.header("Objectif du jour")
    
    # AJOUT DU on_change=reset_app ICI 👇
    choix_type = st.radio(
        "Type d'entraînement :", 
        ["Musculation 🏋️‍♂️", "Cardio 🏃💨"],
        on_change=reset_app # C'est ça qui force le retour à l'accueil !
    )
    
    st.divider()
    st.info("💡 **Conseil :** Bois de l'eau !!! Arrête le coca")

# --- 2. COULEURS DYNAMIQUES ---
if "Cardio" in choix_type:
    color = "#007BFF" # Bleu
    nom_mode = "CARDIO"
    icone = "🏃💨"
else:
    color = "#8A2BE2" # Violet
    nom_mode = "MUSCU"
    icone = "🏋️‍♂️"

# CSS
st.markdown(f"""
    <style>
    .titre {{ color: {color}; text-align: center; font-size: 40px; font-weight: bold; }}
    .stButton>button {{ background-color: {color}; color: white; border-radius: 10px; height: 50px; width: 100%; border: none; font-size: 18px; }}
    .stButton>button:hover {{ opacity: 0.8; color: white; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE ---
seances_cardio = [
    {"titre": "HIIT Express", "duree": "20", "exos": ["30s Jumping Jacks", "15s Repos", "30s Montées genoux", "15s Repos", "30s Burpees", "🔁 4 Tours"]},
    {"titre": "Cardio Boxe", "duree": "25", "exos": ["1 min Sautillements", "1 min Directs", "30s Esquives", "15s Repos", "🔁 5 Tours"]},
    {
        "titre": "HIIT Brûle-Graisse Express",
        "duree": "20",
        "exos": ["45s Jumping Jacks", "15s Repos", "45s Montées de genoux", "15s Repos", "45s Burpees (sans pompe)", "15s Repos", "45s Mountain Climbers", "15s Repos", "🔁 Répéter 4 fois"]
    },
    {
        "titre": "Cardio Boxe (Shadow)",
        "duree": "25",
        "exos": ["1 min Sautillements sur place", "15s Repos", "1 min Directs (Gauche/Droite)", "15s Repos", "1 min Uppercuts rapides", "15s Repos", "1 min Esquives (Squats rotatifs)", "🔁 Répéter 5 fois"]
    },
    {
        "titre": "Le Tueur de Calories (Jambes)",
        "duree": "18",
        "exos": ["30s Squats sautés", "15s Repos", "30s Fentes sautées (alternées)", "15s Repos", "30s Patineur (Sauts latéraux)", "15s Repos", "30s Chaise murale (Isométrie)", "15s Repos", "🔁 Répéter 4 fois"]
    },
    {
        "titre": "Agilité & Cardio",
        "duree": "22",
        "exos": ["40s Pas chassés latéraux", "15s Repos", "40s Talons-fesses", "15s Repos", "40s Sauts en étoile", "15s Repos", "40s Course sur place rapide", "15s Repos", "🔁 Répéter 4 fois"]
    },
    {
        "titre": "Tabata Infernal",
        "duree": "16",
        "exos": ["20s Sprint sur place", "10s Repos", "20s Burpees", "10s Repos", "20s Jumping Jacks", "10s Repos", "20s Mountain Climbers", "10s Repos", "🔁 Répéter 8 fois (Courage !)"]
    }
]
seances_muscu = [
    {"titre": "Full Body", "duree": "28", "exos": ["12 Squats", "10 Pompes", "30s Planche", "15 Ponts fessiers", "🔁 4 Tours"]},
    {"titre": "Spécial Abdos", "duree": "15", "exos": ["30s Crunchs", "30s Toucher chevilles", "30s Planche côté G", "30s Planche côté D", "🔁 3 Tours"]},
    {
        "titre": "Pectoraux & Bras (Poids du corps)",
        "duree": "25",
        "exos": ["12 Pompes classiques", "15s Repos", "15 Dips (sur chaise ou canapé)", "15s Repos", "10 Pompes diamant (mains serrées)", "15s Repos", "20 Cercles de bras (épaules)", "15s Repos", "🔁 Répéter 4 tours"]
    },
    {
        "titre": "Abdos en Béton",
        "duree": "20",
        "exos": ["40s Planche statique", "15s Repos", "20 Crunchs", "15s Repos", "20 Touchers de chevilles", "15s Repos", "40s Russian Twist (rotation)", "15s Repos", "🔁 Répéter 3 tours"]
    },
    {
        "titre": "Jambes Puissantes",
        "duree": "28",
        "exos": ["15 Squats profonds", "15s Repos", "12 Fentes arrières (par jambe)", "15s Repos", "20 Ponts fessiers (Hip thrust sol)", "15s Repos", "15 Mollets (montée pointe de pieds)", "15s Repos", "🔁 Répéter 4 tours"]
    },
    {
        "titre": "Dos & Posture (Sans matériel)",
        "duree": "22",
        "exos": ["15 Supermans (allongé ventre)", "15s Repos", "15 Nageurs (bras/jambes opposés)", "15s Repos", "30s Planche bras tendus", "15s Repos", "12 Pompes scapulaires (juste les omoplates)", "15s Repos", "🔁 Répéter 4 tours"]
    },
    {
        "titre": "Full Body Contrôlé (Lent)",
        "duree": "30",
        "exos": ["10 Squats tempo lent (3s descente)", "15s Repos", "8 Pompes tempo lent", "15s Repos", "12 Fentes latérales", "15s Repos", "45s La Chaise (Dos au mur)", "15s Repos", "🔁 Répéter 4 tours"]
    }
]

# --- 4. PAGE PRINCIPALE ---
st.markdown(f"<h1 class='titre'>{icone} {nom_mode}</h1>", unsafe_allow_html=True)

# Placeholder : C'est une boîte vide qu'on va remplir ou vider
conteneur_principal = st.empty()

# --- CAS 1 : MODE SÉLECTION (Accueil) ---
if not st.session_state.mode_entrainement:
    
    with conteneur_principal.container():
        st.write("Génère ta séance du jour 👇")
        
        if st.button(f"🎲 GÉNÉRER SÉANCE {nom_mode}"):
            # Choix aléatoire
            if "Cardio" in choix_type:
                st.session_state.seance = random.choice(seances_cardio)
            else:
                st.session_state.seance = random.choice(seances_muscu)
        

        # Affichage de la prévisualisation
        if st.session_state.seance:
            s = st.session_state.seance
            st.divider()
            st.subheader(f"🎯 {s['titre']} ({s['duree']} min)")
             # BOUTON POUR PASSER EN MODE "LIVE"
            def lancer_mode_live():
                st.session_state.mode_entrainement = True

            st.button("⏱️ ALLER AU CHRONO", on_click=lancer_mode_live)
            for exo in s['exos']:
                if "🔁" in exo: st.warning(exo)
                elif "Repos" in exo: st.info(exo)
                else: st.success(exo)
            
            st.divider()
            
           
# --- CAS 2 : MODE ENTRAÎNEMENT (Chrono actif) ---
else:
    # Ici, le conteneur_principal du haut est vide
    
    s = st.session_state.seance
    
    # 1. Bouton retour
    def retour():
        st.session_state.mode_entrainement = False
    st.button("⬅️ Retour au menu", on_click=retour)

    st.markdown(f"<h2 style='text-align:center; color:{color}'>🔥 {s['titre']} 🔥</h2>", unsafe_allow_html=True)

    # 2. Le TIMER JAVASCRIPT
    duree_sec = int(s['duree']) * 60
    
    timer_html = f"""
    <div style="text-align: center; background-color: #f0f2f6; padding: 20px; border-radius: 15px; border: 2px solid {color}; margin-bottom: 20px;">
        <div id="timer" style="font-size: 80px; font-weight: bold; color: {color}; font-family: monospace;">
            {s['duree']}:00
        </div>
        <button onclick="startTimer()" style="background-color: {color}; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-size: 20px; cursor: pointer;">▶️ Start</button>
        <button onclick="pauseTimer()" style="background-color: #orange; color: black; border: 1px solid #ccc; padding: 10px 20px; border-radius: 5px; font-size: 20px; cursor: pointer;">⏸️ Pause</button>
        <button onclick="resetTimer()" style="background-color: #red; color: black; border: 1px solid #ccc; padding: 10px 20px; border-radius: 5px; font-size: 20px; cursor: pointer;">🔄 Reset</button>
    </div>

    <script>
    var timeLeft = {duree_sec};
    var timerId;
    var isRunning = false;

    function updateDisplay() {{
        var m = Math.floor(timeLeft / 60);
        var s = timeLeft % 60;
        m = m < 10 ? '0' + m : m;
        s = s < 10 ? '0' + s : s;
        document.getElementById('timer').innerHTML = m + ':' + s;
    }}

    function startTimer() {{
        if (!isRunning) {{
            isRunning = true;
            timerId = setInterval(function() {{
                if (timeLeft <= 0) {{
                    clearInterval(timerId);
                    document.getElementById('timer').innerHTML = "FINI !";
                    isRunning = false;
                }} else {{
                    timeLeft--;
                    updateDisplay();
                }}
            }}, 1000);
        }}
    }}

    function pauseTimer() {{
        clearInterval(timerId);
        isRunning = false;
    }}

    function resetTimer() {{
        pauseTimer();
        timeLeft = {duree_sec};
        updateDisplay();
    }}
    </script>
    """
    
    st.components.v1.html(timer_html, height=250)

    # 3. La liste des exos en dessous
    with st.expander("📝 Voir les exercices", expanded=True):
        for i, exo in enumerate(s['exos']):
            if "🔁" in exo:
                st.warning(f"{exo}", icon="⚠️")
            elif "Repos" in exo:
                st.info(f"{exo}", icon="💤")
            else:
                st.success(f"**{i+1}.** {exo}", icon="🔥")