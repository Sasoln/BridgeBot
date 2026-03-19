import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="BridgetBot", page_icon="🤖", layout="wide")

# --- CUSTOM CSS ---
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* === GLOBAL TEXT COLOR FIX === */
    /* Only force color on text elements, NOT headings */
    html, body, label {
        color: #1F1F1F !important;
    }
    
    p, span, a {
        color: #1F1F1F !important;
    }
    
    /* Headings should NOT be forced - they have their own colors */
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }
    
    /* Override for specific elements that need different colors */
    .stButton > button {
        color: white !important;
    }
    
    .stChatInput {
        color: #F5F5F5 !important;
    }
    
    /* CRITICAL: Force dark text in ALL input fields */
    input {
        color: #000000 !important;
        background: white !important;
    }
    
    input[type="text"] {
        color: #000000 !important;
    }
    
    .stTextInput input {
        color: #000000 !important;
    }
    
    textarea {
        color: #000000 !important;
        background: white !important;
    }
    
    /* === LIGHT THEME (DEFAULT) === */
    /* Main background */
    .main {
        background: #FEFEFE !important;
    }
    
    /* Sidebar - Colore personalizzato */
    [data-testid="stSidebar"] {
        background-color: #FFFBF5 !important; /* 👈 CAMBIA QUESTO COLORE */
        border-right: 1px solid #E5E5E5 !important;
    }

    /* Assicura che il contenitore interno sia trasparente e mostri il colore che hai scelto sopra */
    [data-testid="stSidebar"] > div:first-child {
        background-color: transparent !important;
        padding: 2.5rem 1.8rem;
    }
    
    /* Typography - Light Mode */
    h1, h2, h3 {
        font-family: 'Lora', serif;
        color: #1A1A1A !important;
        font-weight: 600;
        letter-spacing: -0.8px;
    }
    
    h1 {
        font-size: 3.5rem;
        margin-bottom: 0.2rem;
        font-weight: 700;
        line-height: 1.1;
    }
    
    h2 {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }
    
    body, .stMarkdown {
        font-family: 'Inter', sans-serif;
        color: #1F1F1F !important;
        line-height: 1.7;
        font-weight: 400;
    }
    
    /* Force text color on all text elements */
    p, span, div, a, label, button {
        color: #1F1F1F !important;
    }
    
    /* Streamlit specific selectors */
    .stMarkdownContainer {
        color: #1F1F1F !important;
    }
    
    [data-testid="stMarkdownContainer"] {
        color: #1F1F1F !important;
    }
    
    /* Input and text styling */
    .stText {
        color: #1F1F1F !important;
    }
    
    /* Force label colors */
    label {
        color: #1A1A1A !important;
        font-weight: 500;
    }
    
/* === FIX DEFINITIVO CHAT INPUT === */
    
    /* 1. Forza il bordo nero fisso e lo sfondo bianco sul contenitore reale */
    [data-testid="stChatInput"] > div {
        
        border: 1px solid #000000 !important; /* BORDO NERO FISSO */
        border-radius: 10px !important;
        padding: 0.2rem 0.5rem !important;
        transition: all 0.3s ease !important;
    }

    
    /* 3. Colore del testo nero e sfondo trasparente per l'area dove scrivi */
    [data-testid="stChatInput"] textarea {
        color: #000000 !important;
        background-color: transparent !important;
        border: none !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* 4. Colore del testo di suggerimento (placeholder) */
    [data-testid="stChatInput"] textarea::placeholder {
        color: #888888 !important;
        font-weight: 400 !important;
    }
    
    /* 5. Colore dell'icona di invio (la freccia a destra) */
    [data-testid="stChatInput"] button {
        color: #000000 !important; 
        background-color: transparent !important;
    }
    
    [data-testid="stChatInput"] button:hover {
        color: #555555 !important;
        background-color: transparent !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: #1A1A1A !important;
        color: white !important;
        border: none !important;
        border-radius: 7px;
        padding: 0.7rem 1.8rem;
        font-weight: 500;
        font-size: 0.85rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.4px;
        box-shadow: 0 2px 6px rgba(26, 26, 26, 0.2);
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(26, 26, 26, 0.3);
        background: #0F0F0F !important;
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(26, 26, 26, 0.2);
    }
    
    /* Chat messages */
    .stChatMessage {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        border: 1px solid #E5E5E5;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
        animation: slideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stChatMessage * {
        color: #1F1F1F !important;
    }
    
    .stChatMessage[data-testid="chatAvatarIcon-user"] {
        background: #F8F8F8;
        border-left: 4px solid #1A1A1A;
    }
    
    .stChatMessage[data-testid="chatAvatarIcon-assistant"] {
        background: white;
        border-left: 4px solid #737373;
    }
    
    .stChatMessage p {
        color: #1F1F1F !important;
    }
    
    .stChatMessage .stMarkdown {
        color: #1F1F1F !important;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Info/Warning/Error boxes */
    .stInfo, .stWarning, .stError, .stSuccess {
        border-radius: 10px;
        border: 1.5px solid;
        border-left: 4px solid;
        padding: 1.2rem;
        font-size: 0.9rem;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stInfo {
        background: #F5F5FF;
        border-color: #D9D9E8;
        border-left-color: #1A1A1A;
        color: #1F1F1F !important;
    }
    
    .stInfo * {
        color: #1F1F1F !important;
    }
    
    .stWarning {
        background: #FFFAF5;
        border-color: #E8DCD0;
        border-left-color: #C67D24;
        color: #1F1F1F !important;
    }
    
    .stWarning * {
        color: #1F1F1F !important;
    }
    
    .stError {
        background: #FFF5F5;
        border-color: #E8D5D5;
        border-left-color: #B52E24;
        color: #1F1F1F !important;
    }
    
    .stError * {
        color: #1F1F1F !important;
    }
    
    .stSuccess {
        background: #F5FFF5;
        border-color: #D5E8D5;
        border-left-color: #3D7239;
        color: #1F1F1F !important;
    }
    
    .stSuccess * {
        color: #1F1F1F !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: #F9F9F9;
        border-radius: 8px;
        border: 1px solid #E5E5E5 !important;
        color: #1A1A1A !important;
        font-weight: 500;
        padding: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-family: 'Inter', sans-serif;
    }
    
    .streamlit-expanderHeader:hover {
        background: #F0F0F0;
        border-color: #D0D0D0 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    }
    
    /* Dividers */
    .stDivider {
        margin: 1.5rem 0;
        border: 0;
        height: 1px;
        background: #E5E5E5;
    }
    
    /* === FIX CAMPI DI TESTO (TONE & TARGET) === */

    /* Nasconde il fastidioso messaggio "Press Enter to apply" */
    [data-testid="InputInstructions"] {
        display: none !important;
    }

    [data-testid="stTextInput"] div[data-baseweb="input"] {
        border: 0.5px solid #000000 !important; /* Bordo di 1px nero fisso */
        border-radius: 7px !important;
        background-color: #FFFFFF !important;
        transition: all 0.3s ease !important;
    }

    /* Effetto quando clicchi dentro il campo */
    [data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
        box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.1) !important;
        border-color: #000000 !important;
    }

    /* Stile del testo e sfondo trasparente per l'input effettivo */
    [data-testid="stTextInput"] input {
        color: #000000 !important;
        background-color: transparent !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.5rem 0.8rem !important;
    }

    /* Colore del testo suggerito (placeholder) */
    [data-testid="stTextInput"] input::placeholder {
        color: #888888 !important;
        font-weight: 300 !important;
    }
    
    /* Caption & labels */
    .stCaption {
        color: #666666 !important;
        font-size: 0.8rem;
        font-weight: 400;
        font-family: 'Inter', sans-serif;
    }
    
    ..stLabel {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        font-size: 0.9rem;
        color: #1A1A1A !important;
        transition: color 0.2s ease;
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Selection */
    ::selection {
        background-color: #1A1A1A;
        color: #F5F5F5;
    }
    
    /* Header container animation */
    .header-container {
        animation: fadeInDown 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
</style>

<script>
    // Prevent default interactions and add custom behavior
    window.addEventListener('load', () => {
        // Scroll to bottom when new messages arrive
        const scrollToBottom = () => {
            window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'smooth' });
        };
        
        // Observe mutations for new chat messages
        const observer = new MutationObserver(() => {
            setTimeout(scrollToBottom, 300);
        });
        
        const chatContainer = document.querySelector('[data-testid="stChatMessageContainer"] || .main');
        if (chatContainer) {
            observer.observe(chatContainer, { childList: true, subtree: true });
        }
        
        // Enhanced button interactions
        document.querySelectorAll('button').forEach(btn => {
            btn.addEventListener('mouseenter', function() {
                this.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
            });
        });
        
        // Input focus effect
        const inputs = document.querySelectorAll('input[type="text"]');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
            });
        });
        
        // Auto-scroll on chat input
        const chatInput = document.querySelector('[data-testid="stChatInputContainer"]');
        if (chatInput) {
            chatInput.addEventListener('focus', () => {
                setTimeout(scrollToBottom, 100);
            });
        }


    });
    
   
</script>
"""
st.markdown(custom_css, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []


# --- SIDEBAR: CENTRO DI CONTROLLO ---
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom: 2.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid #E5E5E5;">
        <h2 style="font-family: 'Lora', serif; color: #000000 !important; margin: 0; line-height: 1; font-size: 1.5rem; font-weight: 700;">Bridget</h2>
        <p style="color: #555555; font-size: 0.8rem; margin: 0; margin-top: 4px; font-family: 'Inter', sans-serif; font-weight: 400; letter-spacing: 0.3px;">Your Strategic Copywriter</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("**Tone & Audience**", help="Define your strategic parameters")
    tono_manuale = st.text_input("Tone", placeholder="Professional, Sarcastic, Emotional, Institutional...")
    target_manuale = st.text_input("Target", placeholder="Gen Z, Fitness enthusiasts, Entrepreneurs, Millennials...")
    
   
    
    st.divider()
    
    with st.expander("Learn More", expanded=False):
        st.write("""
        - **Be Specific:** Include unique details to avoid generic copy.
        - **Tone Consistency:** Institutional tone suggests cinematic audio, not ironic songs.
        - **Post vs Story:** Stories drive engagement, Posts build authority over time.
        - **Authenticity Matters:** Ensure your chosen tone aligns with your campaign goal.
        """)
    
    st.divider()
    st.caption("BridgetBot v1.0  \nDeveloped by Salvatore Lo Nardo")
  

# --- AREA PRINCIPALE ---
st.markdown("""
<div class="header-container" style="padding: 2.5rem 0 1.5rem 0; margin-bottom: 2rem;">
    <h1 style="font-family: 'Lora', serif; margin: 0; font-size: 4rem; color: #000000 !important; font-weight: 700; line-height: 1;">BridgetBot</h1>
    <p style="margin: 0.8rem 0 0 0; color: #555555; font-size: 1rem; font-family: 'Inter', sans-serif; font-weight: 300; letter-spacing: 0.5px;">Multi-Format Strategy • Copy & Content Mastery</p>
</div>
""", unsafe_allow_html=True)





# --- PROMPT DI SISTEMA AVANZATO ---
PROMPT_SISTEMA = f"""
Sei BridgetBot, Senior Copywriter internazionale.

PARAMETRI:
- TONO: {tono_manuale if tono_manuale else 'Professionale e persuasivo'}
- TARGET: {target_manuale if target_manuale else 'Pubblico generalista'}

REGOLE ASSOLUTE DI LINGUA:
1. RILEVAMENTO: Identifica la lingua dell'ULTIMO messaggio dell'utente.
2. RISPOSTA: Scrivi l'INTERO output (inclusi i concetti e il copy) nella STESSA LINGUA dell'utente.
   - Se l'utente scrive in Inglese -> Rispondi in Inglese.
   - Se l'utente scrive in Italiano -> Rispondi in Italiano.
   - NON mescolare le lingue.


REGOLE DI CONTENUTO E FORMATTAZIONE (CRITICHE):
- COPY COMPLETO: Non fare riassunti o "spiegazioni" di cosa faresti. Scrivi il TESTO REALE, COMPLETO E CORPOSO, pronto per essere pubblicato.
- ZERO MURI DI TESTO: Genera testi ricchi e dettagliati, ma falli respirare. Dividili in paragrafi brevi (massimo 2-3 frasi per blocco). Usa sempre una riga vuota tra un paragrafo e l'altro.
- ELENCHI: Quando spieghi passaggi o benefici, usa sempre elenchi puntati per spezzare visivamente il testo.
- GRASSETTI: Usa il **grassetto** per far risaltare il gancio iniziale e i concetti cardine.
- VALIDO PER TUTTI E 4 I TAG: Applica queste regole a tutti e 4 i formati (LinkedIn, Instagram, TikTok, Facebook). Non fare eccezioni.

STRUTTURA DI OUTPUT OBBLIGATORIA:
Usa SEMPRE i tag [LINKEDIN], [INSTAGRAM], [TIKTOK], [FACEBOOK] per separare le sezioni. NON aggiungere alcun saluto o testo prima del primo tag.

[LINKEDIN]
Scrivi un post completo e lungo (almeno 150-200 parole) di Thought Leadership.
Crea un Gancio forte, sviluppa il caso in 3-4 paragrafi approfonditi e usa gli elenchi puntati. Chiudi con una CTA per generare dibattito nei commenti.

[INSTAGRAM]
Specifica se POST o STORY. Scrivi il copy reale, evocativo e abbondante.
Indica chiaramente: l'idea visuale, il copy da mettere nella caption e suggerisci un brano audio reale e specifico coerente con il tono.

[TIKTOK]
Scrivi l'intero SCRIPT dettagliato del video.
Dividi chiaramente l'output in: HOOK VISUALE (cosa si vede nei primi 3 secondi), TESTO A SCHERMO, e VOICE-OVER/PARLATO. Includi il suggerimento per l'audio o il trend.

[FACEBOOK]
Scrivi un post corposo e discorsivo per la community. Usa un tono colloquiale, paragrafi distanziati e chiudi con una domanda aperta e divisiva per stimolare engagement.

REGOLA FINALE: LA TUA RISPOSTA DEVE INIZIARE ESATTAMENTE E SOLO CON LA PAROLA [LINKEDIN].
"""


# --- CHAT INPUT (UNICO IN TUTTO IL CODICE) ---
idea = st.chat_input("Share your idea or request refinement...")

if idea:
    st.session_state.messages.append({"role": "user", "content": idea})
    with st.spinner("Bridget is crafting your strategy..."):
        full_messages = [{"role": "system", "content": PROMPT_SISTEMA}] + st.session_state.messages
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=full_messages,
            temperature=0.85 
        )
        risposta_ai = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": risposta_ai})


# --- VISUALIZZAZIONE ---
if st.session_state.messages:
    # 1. Ciclo per mostrare la cronologia
    for i, msg in enumerate(st.session_state.messages):
        # Determiniamo se è l'ultimo messaggio dell'assistente con i tag
        is_assistant = msg["role"] == "assistant"
        is_last = (i == len(st.session_state.messages) - 1)
        has_tags = "[LINKEDIN]" in msg["content"]

        # MOSTRA il messaggio solo se:
        # - È dell'utente
        # - O è un messaggio vecchio dell'assistente
        # - O è l'assistente ma NON ha i tag (es. un saluto "Ciao!")
        if msg["role"] == "user" or not (is_last and has_tags):
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    # 2. Se l'ultimo messaggio dell'assistente ha i tag, creiamo le Card
    ultimo_msg = st.session_state.messages[-1]
    if ultimo_msg["role"] == "assistant" and "[LINKEDIN]" in ultimo_msg["content"]:
        testo_completo = ultimo_msg["content"]

        def estrai(testo, tag, tag_succ=None):
            try:
                p = testo.split(tag)[1]
                if tag_succ: p = p.split(tag_succ)[0]
                return p.strip()
            except: return None

        def titolo_card(nome):
            st.markdown(f"""
            <div style="background-color: #1A1A1A; border-radius: 6px; padding: 0.6rem 1.2rem; margin-top: 1.5rem; margin-bottom: 1rem;">
                <h3 style="margin: 0; color: #FFFFFF !important; font-size: 1.05rem;">{nome}</h3>
            </div>
            """, unsafe_allow_html=True)

        socials = [
            ("[LINKEDIN]", "[INSTAGRAM]", "LinkedIn"),
            ("[INSTAGRAM]", "[TIKTOK]", "Instagram"),
            ("[TIKTOK]", "[FACEBOOK]", "TikTok"),
            ("[FACEBOOK]", None, "Facebook")
        ]

        for tag, succ, nome in socials:
            contenuto = estrai(testo_completo, tag, succ)
            if contenuto:
                titolo_card(nome)
                st.write(contenuto)

        # Versione potenziata: Titoli bianchi garantiti su fondo nero
        def titolo_card(nome):
            st.markdown(f"""
            <style>
                .dark-label-card-{nome.lower()} h3 {{
                    color: #FFFFFF !important;
                    -webkit-text-fill-color: #FFFFFF !important;
                }}
            </style>
            <div class="dark-label-card-{nome.lower()}" style="background-color: #1A1A1A; border-radius: 6px; padding: 0.6rem 1.2rem; margin-bottom: 1.2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.15);">
                <h3 style="margin: 0; font-family: 'Inter', sans-serif; font-size: 1.05rem; font-weight: 600; letter-spacing: 0.5px; color: #FFFFFF !important;">
                    {nome}
                </h3>
            </div>
            """, unsafe_allow_html=True)

        # Layout verticale: uno sotto l'altro con ampio respiro
        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        
        titolo_card("LinkedIn")
        st.write(estrai(ultima, "[LINKEDIN]", "[INSTAGRAM]"))
        
        st.markdown("<div style='margin-top: 2.5rem;'></div>", unsafe_allow_html=True)
        
        titolo_card("Instagram")
        st.write(estrai(ultima, "[INSTAGRAM]", "[TIKTOK]"))
        
        st.markdown("<div style='margin-top: 2.5rem;'></div>", unsafe_allow_html=True)
        
        titolo_card("TikTok")
        st.write(estrai(ultima, "[TIKTOK]", "[FACEBOOK]"))
        
        st.markdown("<div style='margin-top: 2.5rem;'></div>", unsafe_allow_html=True)
        
        titolo_card("Facebook")
        st.write(estrai(ultima, "[FACEBOOK]"))
            
    else:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
