import base64
import os
import time
from datetime import date, datetime

import pandas as pd
import streamlit as st

# ------------------------------------------------------------------
# CONFIG  (edit the TODO items so the page is truly yours)
# ------------------------------------------------------------------
NAME = "Sarah Mae B. Sario"
SECTION = "CSIT 349 · Section: TODO"          # TODO: put your real section
PROGRAM = "BS Computer Science, Year 3"        # TODO: confirm your year level
SCHOOL = "Cebu Institute of Technology – University"
EMAIL = "sarahmaebasalo8@gmail.com"
BASE = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title=f"{NAME} | Portfolio",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# DATA
# ------------------------------------------------------------------
INTERESTS = [
    "📚 Reading", "😴 Sleeping", "📺 Watching series",
    "🎬 Watching movies", "🎮 Playing ML", "🧱 Roblox",
]

# TODO: write this in your own words!
BIO = (
    "I am a Computer Science student at Cebu Institute of Technology – University. "
    "I enjoy building apps that solve everyday problems, especially in healthcare "
    "and study tools. I'm now exploring data science and AI."
)


@st.cache_data
def load_skills():
    # Taken straight from the CV: no ratings, just the tools I list.
    rows = [
        ("Java", "Language"), ("Kotlin", "Language"), ("C#", "Language"),
        ("Python", "Language"), ("C++", "Language"),
        ("HTML", "Web"), ("CSS", "Web"),
        ("SQL", "Database"), ("MySQL", "Database"), ("PostgreSQL", "Database"),
        ("JavaFX", "Framework / Tool"), ("Java Swing", "Framework / Tool"),
        ("Android Studio", "Framework / Tool"),
    ]
    return pd.DataFrame(rows, columns=["Skill", "Category"])


SKILLS = load_skills()

PROJECTS = [
    {
        "title": "MedServe",
        "subtitle": "Public Health Center Queuing System",
        "role": "Full-stack developer",
        "tools": ["Java", "JavaFX", "MySQL"],
        "type": "Desktop / Web",
        "summary": "A queuing application for local health centers that reduces "
                   "wait times and streamlines visitor flow.",
        "did": [
            "Built the front-end profile interface and the backend logic for "
            "self-service patient info updates.",
            "Built an admin user-management dashboard for directory oversight "
            "and status controls.",
        ],
        "outcome": "A working queuing system with patient self-service and an admin dashboard.",
        "link": None,
    },
    {
        "title": "StudyGo",
        "subtitle": "Interactive Flashcard Study Tool",
        "role": "Front-end developer",
        "tools": ["Java", "Java Swing"],
        "type": "Desktop / Web",
        "summary": "A flashcard platform designed for active recall and "
                   "self-paced study.",
        "did": [
            "Implemented flip-card state management.",
            "Created custom interfaces for users to input their own flashcards.",
        ],
        "outcome": "Students can make their own decks and flip through them at their own pace.",
        "link": None,
    },
    {
        "title": "MediMap",
        "subtitle": "Smart Pharmacy Inventory and Localized Search",
        "role": "Mobile developer",
        "tools": ["Kotlin", "Android Studio"],
        "type": "Mobile",
        "summary": "An Android app that helps people find which nearby pharmacies "
                   "have the medicine they need.",
        "did": [
            "Built a pharmacy-facing inventory module with real-time product "
            "listing and stock updates.",
            "Implemented user search and location matching for nearby pharmacies.",
        ],
        "outcome": "Pharmacies update stock live; users see where a medicine is available.",
        "link": None,
    },
]

# which of my projects use each skill (from the project tool lists)
SKILLS["Used in"] = SKILLS["Skill"].apply(
    lambda k: ", ".join(p["title"] for p in PROJECTS if k in p["tools"]) or "-"
)

MILESTONES = pd.DataFrame(
    {
        "When": ["May 2024", "2024", "2024 – 2026", "Sept 2026", "May 2028"],
        "Milestone": [
            "Finished Senior High School (STEM) at Immaculate Heart of Mary Academy",
            "Started BS Computer Science at CIT-U",       # TODO: confirm year
            "Built MedServe, StudyGo and MediMap",         # TODO: confirm years
            "Enrolled in the OmniCampus Data Science & AI course (remote)",
            "Expected graduation",
        ],
    }
)

PLACES = pd.DataFrame(
    {
        "place": ["Cebu City (CIT-U)", "Minglanilla (Senior High)"],
        "lat": [10.3157, 10.2447],
        "lon": [123.8854, 123.7966],
    }
)

# ------------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# ------------------------------------------------------------------
# DIALOG + HELPERS
# ------------------------------------------------------------------
@st.dialog("⚡ Quick facts about me")
def quick_facts():
    st.markdown(
        "- 🎓 BS Computer Science at CIT-U (graduating 2028)\n"
        "- 🛠️ Projects: MedServe, StudyGo, MediMap\n"
        "- 🗣️ I speak English, Filipino and Cebuano\n"
        "- 📊 Currently taking a Data Science & AI course\n"
        "- 🎮 Off-duty: reading, series, movies, ML and Roblox"
    )
    if st.button("Close"):
        st.rerun()


def stream_bio():
    for word in BIO.split(" "):
        yield word + " "
        time.sleep(0.04)


def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def shade(h, f):
    r, g, b = _rgb(h)
    return "#%02x%02x%02x" % (int(r * f), int(g * f), int(b * f))


def on_color(h):
    r, g, b = _rgb(h)
    return "#1F1B3A" if (0.299 * r + 0.587 * g + 0.114 * b) > 160 else "#ffffff"


def find_photo():
    for fname in ("sarah.png", "sarah.jpg", "sarah.jpeg", "photo.jpg", "cat.jpg"):
        p = os.path.join(BASE, fname)
        if os.path.exists(p):
            return p
    return None


def photo_html(path):
    if path is None:
        return '<div class="initials">SS</div>'
    ext = os.path.splitext(path)[1].lower().strip(".")
    mime = "png" if ext == "png" else "jpeg"
    with open(path, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode()
    return f'<img src="data:image/{mime};base64,{b64}" alt="Sarah">'


# ------------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------------
with st.sidebar:
    st.header("🎛️ Page controls")
    st.caption(f"**{NAME}**  \n{SECTION}")
    st.divider()

    st.subheader("Skills view")
    show_table = st.checkbox("Show skills table", value=True)
    show_chart = st.checkbox("Show skills chart", value=True)
    only_project = st.toggle("Only skills used in my projects")
    chart_group = st.radio("Chart shows skills per", ["Category", "Project"], horizontal=True)

    st.subheader("Look & feel")
    accent = st.color_picker("Accent color", "#7C3AED")
    text_size = st.select_slider("Text size", ["Small", "Medium", "Large"], value="Medium")

    st.divider()
    if st.button("⚡ Quick facts"):
        quick_facts()

# ------------------------------------------------------------------
# STYLING
# ------------------------------------------------------------------
FONT = {"Small": "0.92", "Medium": "1.0", "Large": "1.15"}[text_size]
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
html, body, [class*="css"], .stMarkdown, button, input, textarea {
    font-family: 'Poppins', sans-serif;
}
.stMarkdown p, .stMarkdown li { font-size: __FS__rem; }
.block-container { padding-top: 2rem; max-width: 1150px; }

.hero {
    display: flex; align-items: center; gap: 2rem; flex-wrap: wrap;
    background: linear-gradient(135deg, #7C3AED 0%, #C026D3 60%, #F472B6 100%);
    border-radius: 28px; padding: 2.2rem 2.5rem; color: #fff;
    box-shadow: 0 18px 40px rgba(124, 58, 237, .28);
}
.hero img, .hero .initials {
    width: 170px; height: 170px; border-radius: 50%; object-fit: cover;
    border: 6px solid rgba(255,255,255,.85); flex-shrink: 0;
    box-shadow: 0 8px 24px rgba(0,0,0,.25);
}
.hero .initials {
    display: flex; align-items: center; justify-content: center;
    font-size: 3.2rem; font-weight: 700; background: rgba(255,255,255,.2);
}
.hero h1 { color: #fff; font-size: 2.6rem; font-weight: 700; margin: 0; padding: 0; line-height: 1.15; }
.hero .tag { font-size: 1.05rem; opacity: .95; margin: .5rem 0 1rem 0; }
.badge {
    display: inline-block; background: rgba(255,255,255,.22); color: #fff;
    padding: .3rem .85rem; border-radius: 999px; font-size: .85rem;
    margin: 0 .4rem .4rem 0;
}
.chip {
    display: inline-block; background: #fff; color: __T__; font-weight: 500;
    padding: .45rem 1rem; border-radius: 999px; margin: 0 .5rem .6rem 0;
    border: 1.5px solid #DDD0FB; box-shadow: 0 2px 8px rgba(124,58,237,.10);
}
h2 { color: __T__ !important; font-weight: 700 !important; }
h3 { color: __T__ !important; font-weight: 600 !important; }

[data-testid="stMetric"] {
    background: #fff; border: 1px solid #E7DDFB; border-radius: 18px;
    padding: 1rem 1.2rem; box-shadow: 0 6px 18px rgba(124,58,237,.08);
}
[data-testid="stMetricValue"] { color: __A__; font-weight: 700; }

.stTabs [data-baseweb="tab-list"] { gap: .5rem; flex-wrap: wrap; }
.stTabs [data-baseweb="tab"] {
    background: #fff; border-radius: 999px; padding: .5rem 1.2rem;
    border: 1px solid #E7DDFB; font-weight: 500;
}
.stTabs [aria-selected="true"] { background: __A__ !important; color: __OA__ !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }

[data-testid="stVerticalBlockBorderWrapper"] {
    background: #fff; border-radius: 20px !important;
    border: 1px solid #E7DDFB !important; box-shadow: 0 8px 22px rgba(124,58,237,.08);
}
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
    border-radius: 999px; border: none; color: __OA__; font-weight: 600;
    background: __A__; padding: .5rem 1.4rem;
}
.stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover {
    color: __OA__; filter: brightness(1.08);
}
[data-testid="stSidebar"] { border-right: 1px solid #E7DDFB; }
code { color: __T__; background: #F1EAFF; border-radius: 6px; }
</style>
"""
st.markdown(
    CSS.replace("__A__", accent)
    .replace("__T__", shade(accent, 0.75))
    .replace("__OA__", on_color(accent))
    .replace("__FS__", FONT),
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# HERO
# ------------------------------------------------------------------
st.markdown(
    f"""
<div class="hero">
  {photo_html(find_photo())}
  <div>
    <h1>Hi, I'm {NAME} 👋</h1>
    <div class="tag">{PROGRAM} · {SCHOOL}</div>
    <span class="badge">{SECTION}</span>
    <span class="badge">📍 Cebu, Philippines</span>
    <span class="badge">🎓 Graduating 2028</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)
st.write("")

# ------------------------------------------------------------------
# ABOUT
# ------------------------------------------------------------------
st.header("About me")
if st.session_state.get("intro_done"):
    st.write(BIO)
else:
    st.write_stream(stream_bio())   # types the bio out once per visit
    st.session_state.intro_done = True

box1, box2, box3 = st.columns(3)
with box1.container(border=True):
    st.markdown("**🚀 Projects**")
    st.markdown("\n".join(f"- {p['title']}" for p in PROJECTS))
with box2.container(border=True):
    st.markdown("**🗣️ Languages**")
    st.markdown("- English\n- Filipino\n- Cebuano")
with box3.container(border=True):
    st.markdown("**💻 Tech I use**")
    st.write(", ".join(SKILLS["Skill"].tolist()))
st.write("")

# ------------------------------------------------------------------
# TABS
# ------------------------------------------------------------------
tab_story, tab_skills, tab_projects, tab_fun, tab_contact = st.tabs(
    ["📖 Autobiography", "🛠️ Skills", "🚀 Projects", "🎮 Fun zone", "✉️ Contact"]
)

# ---------------- Autobiography ----------------
with tab_story:
    st.header("My story")
    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.subheader("Background")
        st.write(
            "I'm from Cebu, Philippines. I speak English, Filipino and Cebuano. "
            "TODO: add 2–3 sentences about where you grew up and what pushed you toward computers."
        )
        st.subheader("Education")
        st.markdown(
            f"- **{SCHOOL}**: BS Computer Science (May 2028)\n"
            "- **Immaculate Heart of Mary Academy**, Minglanilla: Senior High School, STEM (May 2024)"
        )
        with st.expander("Relevant coursework"):
            st.markdown(
                "- Data Structures and Algorithms\n- Object-Oriented Programming\n"
                "- Database Management Systems\n- Web Development\n"
                "- Human-Computer Interaction\n- Mobile Application Development"
            )
        st.subheader("Where my story happens")
        st.map(PLACES, size=400, zoom=9)

    with c2:
        st.subheader("Interests")
        st.markdown(
            "".join(f'<span class="chip">{i}</span>' for i in INTERESTS),
            unsafe_allow_html=True,
        )
        st.write(
            "When I'm not coding, I like reading, sleeping, watching series and "
            "movies, and playing ML and Roblox. "
            "TODO: add what you read or watch lately."
        )
        st.subheader("Milestones")
        st.table(MILESTONES.set_index("When"))

# ---------------- Skills ----------------
with tab_skills:
    st.header("Skills")
    st.write(
        "These are the languages, databases and tools I list on my CV. "
        "The last column shows which of my projects use each one."
    )
    view = SKILLS
    if only_project:
        view = view[view["Used in"] != "-"]
    cat_pick = st.selectbox("Filter by category", ["All"] + sorted(SKILLS["Category"].unique()))
    if cat_pick != "All":
        view = view[view["Category"] == cat_pick]

    if view.empty:
        st.warning("No skills match the current filters.")
    else:
        s1, s2 = st.columns(2, gap="large")
        with s1:
            if show_table:
                st.subheader("Table")
                st.dataframe(view, hide_index=True, use_container_width=True)
            else:
                st.caption("Table hidden (see sidebar).")
        with s2:
            if show_chart:
                st.subheader("Chart")
                if chart_group == "Category":
                    counts = view["Category"].value_counts()
                else:
                    counts = pd.Series(
                        {p["title"]: sum(t in set(view["Skill"]) for t in p["tools"]) for p in PROJECTS}
                    )
                st.bar_chart(counts)
            else:
                st.caption("Chart hidden (see sidebar).")

    with st.expander("💻 A tiny Python snippet"):
        snippet = (
            'skills = ["Java", "Kotlin", "Python"]\n'
            "for s in skills:\n"
            '    print(f"Sarah can build with {s}!")'
        )
        st.code(snippet, language="python")
        if st.button("Run it"):
            st.text("\n".join(f"Sarah can build with {s}!" for s in ["Java", "Kotlin", "Python"]))

    with st.expander("🧾 My profile as JSON"):
        st.json(
            {
                "name": NAME,
                "school": SCHOOL,
                "program": "BS Computer Science",
                "graduation": "May 2028",
                "languages": ["English", "Filipino", "Cebuano"],
                "skills": SKILLS["Skill"].tolist(),
                "interests": [i.split(" ", 1)[1] for i in INTERESTS],
            }
        )

# ---------------- Projects ----------------
with tab_projects:
    st.header("Projects")
    all_tools = sorted({t for p in PROJECTS for t in p["tools"]})
    tool_filter = st.multiselect("Filter by tool", all_tools)
    shown = [p for p in PROJECTS if not tool_filter or set(tool_filter) & set(p["tools"])]

    view_mode = st.segmented_control("View as", ["Cards", "Comparison table"], default="Cards")
    if view_mode == "Comparison table" and shown:
        st.dataframe(
            pd.DataFrame(
                [{"Project": p["title"], "Role": p["role"], "Type": p["type"],
                  "Tools": ", ".join(p["tools"]), "Outcome": p["outcome"]} for p in shown]
            ),
            hide_index=True,
            use_container_width=True,
        )
    if not shown:
        st.info("No project uses that combination of tools.")
    for p in (shown if view_mode != "Comparison table" else []):
        with st.container(border=True):
            left, right = st.columns([3, 1])
            with left:
                st.subheader(f"{p['title']}: {p['subtitle']}")
                st.write(p["summary"])
                st.markdown("**What I did**")
                for item in p["did"]:
                    st.markdown(f"- {item}")
                st.markdown(f"**Outcome:** {p['outcome']}")
            with right:
                st.markdown(f"**Role**  \n{p['role']}")
                st.markdown(f"**Type**  \n{p['type']}")
                st.markdown("**Tools**  \n" + " ".join(f"`{t}`" for t in p["tools"]))
                if p["link"]:
                    st.link_button("View project", p["link"])

# ---------------- Fun zone ----------------
with tab_fun:
    st.header("Fun zone")

    st.subheader("Why are you here?")
    visitor = st.pills("Pick one:", ["Recruiter", "Classmate", "Teacher", "Just browsing"])
    replies = {
        "Recruiter": "Welcome! Check my Projects tab and grab my CV from the Contact tab.",
        "Classmate": "Hi! Feel free to try every widget on this page. 😄",
        "Teacher": "Thank you for checking my work, ma'am/sir! 🙏",
        "Just browsing": "Enjoy your stay, and don't forget to hit the like button!",
    }
    if visitor:
        st.info(replies[visitor])

    st.subheader("🎯 How well do you know me?")
    guess = st.multiselect(
        "Pick everything I enjoy:",
        ["Reading", "Sleeping", "Skydiving", "Roblox", "Gardening",
         "Watching movies", "Playing ML", "Watching series"],
        key="quiz",
    )
    if st.button("Check my answers"):
        answer = {"Reading", "Sleeping", "Roblox", "Watching movies", "Playing ML", "Watching series"}
        if set(guess) == answer:
            st.success("Perfect score! You know me well. 🎉")
            st.balloons()
        else:
            wrong = [g for g in guess if g not in answer]
            missing = len(answer - set(guess))
            st.warning(f"Not quite: {len(wrong)} wrong pick(s) and {missing} missing. Try again!")


# ---------------- Contact ----------------
with tab_contact:
    st.header("Contact & feedback")
    f1, f2 = st.columns([2, 1], gap="large")

    with f1:
        with st.form("feedback_form", clear_on_submit=True):
            who = st.text_input("Your name")
            mail = st.text_input("Your email")
            topic = st.selectbox("Topic", ["Feedback", "Collaboration", "Question", "Just saying hi"])
            project_pick = st.selectbox(
                "Which project are you interested in?",
                ["None / general"] + [p["title"] for p in PROJECTS],
            )
            meet_date = st.date_input("Preferred date to talk", value=date.today())
            msg = st.text_area("Message", height=120)
            attach = st.file_uploader("Attach a brief or document (optional)")
            sent = st.form_submit_button("Send message")

        if sent:
            if not who.strip() or not msg.strip():
                st.error("Please add your name and a message.")
            else:
                with st.spinner("Sending..."):
                    time.sleep(1)
                st.session_state.messages.append(
                    {"Time": datetime.now().strftime("%H:%M:%S"), "From": who,
                     "Topic": topic, "Project": project_pick,
                     "Attachment": attach.name if attach else "-"}
                )
                st.success(f"Thanks, {who}! Your {topic.lower()} was received. 💜")
                st.balloons()

        if st.session_state.messages:
            st.caption("Messages sent in this session:")
            st.dataframe(pd.DataFrame(st.session_state.messages), hide_index=True)


    with f2:
        st.subheader("Reach me")
        st.write(f"📧 {EMAIL}")
        st.write("📍 Cebu, Philippines")
        st.link_button("✉️ Email me", f"mailto:{EMAIL}")
        st.subheader("Downloads")
        cv_path = os.path.join(BASE, "Sario_CV.pdf")
        if os.path.exists(cv_path):
            with open(cv_path, "rb") as fh:
                st.download_button("⬇️ Download my CV (PDF)", fh.read(),
                                   file_name="Sario_CV.pdf", mime="application/pdf")
        st.download_button(
            "⬇️ Download my bio (.txt)",
            f"{NAME}\n{PROGRAM}\n\n{BIO}\n\nInterests: " + ", ".join(INTERESTS),
            file_name="bio.txt",
        )

st.divider()
st.caption(f"Built with Streamlit · {NAME} · {SECTION}")