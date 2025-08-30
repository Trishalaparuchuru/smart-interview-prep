import streamlit as st
import re
import json
import os
from datetime import datetime, timedelta
import hashlib

# =========================
# PERSISTENT STORAGE SYSTEM
# =========================

def load_users_from_file():
    """Load users from JSON file"""
    try:
        if os.path.exists("users_data.json"):
            with open("users_data.json", "r") as f:
                return json.load(f)
    except:
        pass
    return {}

def save_users_to_file(users_db):
    """Save users to JSON file"""
    try:
        with open("users_data.json", "w") as f:
            json.dump(users_db, f, indent=2)
    except Exception as e:
        st.error(f"Failed to save user data: {e}")

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def init_session_state():
    """Initialize session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'user_scores' not in st.session_state:
        st.session_state.user_scores = {}
    if 'current_score' not in st.session_state:
        st.session_state.current_score = 0
    if 'questions_attempted' not in st.session_state:
        st.session_state.questions_attempted = {}
    
    # Load persistent user data
    if 'users_db' not in st.session_state:
        st.session_state.users_db = load_users_from_file()

def save_user_data(username, password, email=""):
    """Save user data - now with persistent storage"""
    if 'users_db' not in st.session_state:
        st.session_state.users_db = load_users_from_file()
    
    st.session_state.users_db[username] = {
        'password': hash_password(password),
        'email': email,
        'created_at': datetime.now().isoformat(),
        'scores': {},
        'total_questions': 0,
        'correct_answers': 0
    }
    
    # Save to file immediately
    save_users_to_file(st.session_state.users_db)

def verify_user(username, password):
    """Verify user credentials - now with persistent storage"""
    if 'users_db' not in st.session_state:
        st.session_state.users_db = load_users_from_file()
    
    if username in st.session_state.users_db:
        stored_hash = st.session_state.users_db[username]['password']
        return stored_hash == hash_password(password)
    return False

def login_signup_page():
    """Login and Signup page"""
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; margin-bottom: 2rem;'>
        <h1 style='color: white; font-size: 3rem; margin-bottom: 0.5rem;'>🧠</h1>
        <h2 style='color: white; margin: 0;'>Smart Interview Prep Assistant</h2>
        <p style='color: #e0e6ff; margin-top: 0.5rem;'>Master Your Tech Interviews</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Welcome Back!")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Login", use_container_width=True)
            
            if login_btn:
                if verify_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    
    with tab2:
        st.subheader("Create Your Account")
        with st.form("signup_form"):
            new_username = st.text_input("Choose Username")
            new_email = st.text_input("Email (Optional)")
            new_password = st.text_input("Create Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            signup_btn = st.form_submit_button("Sign Up", use_container_width=True)
            
            if signup_btn:
                if not new_username or not new_password:
                    st.error("Username and password are required")
                elif new_password != confirm_password:
                    st.error("Passwords don't match")
                elif 'users_db' in st.session_state and new_username in st.session_state.users_db:
                    st.error("Username already exists")
                else:
                    save_user_data(new_username, new_password, new_email)
                    st.success("Account created successfully! Please login.")

def login_signup_page():
    """Login and Signup page"""
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 15px; margin-bottom: 2rem;'>
        <h1 style='color: white; font-size: 3rem; margin-bottom: 0.5rem;'>🧠</h1>
        <h2 style='color: white; margin: 0;'>Smart Interview Prep Assistant</h2>
        <p style='color: #e0e6ff; margin-top: 0.5rem;'>Master Your Tech Interviews</p>
    </div>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("""
Created by **Trishala** 🌟 – CSE Final Year 💻, VRSEC 🎓  
Hey there! 👋 Hope you're doing well 😊  
Keep going, you can do it! 💪✨  
Have a productive day! ☀️📚
""")

    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Welcome Back!")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Login", use_container_width=True)
            
            if login_btn:
                if verify_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    
    with tab2:
        st.subheader("Create Your Account")
        with st.form("signup_form"):
            new_username = st.text_input("Choose Username")
            new_email = st.text_input("Email (Optional)")
            new_password = st.text_input("Create Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            signup_btn = st.form_submit_button("Sign Up", use_container_width=True)
            
            if signup_btn:
                if not new_username or not new_password:
                    st.error("Username and password are required")
                elif new_password != confirm_password:
                    st.error("Passwords don't match")
                elif 'users_db' in st.session_state and new_username in st.session_state.users_db:
                    st.error("Username already exists")
                else:
                    save_user_data(new_username, new_password, new_email)
                    st.success("Account created successfully! Please login.")

# =========================
# SCORING SYSTEM
# =========================

def calculate_score(user_answer, model_answer, keywords):
    """Calculate score based on keyword matching and answer quality"""
    user_words = set(re.findall(r'\b\w+\b', user_answer.lower()))
    model_words = set(re.findall(r'\b\w+\b', model_answer.lower()))
    
    # Keyword matching (40% of score)
    keyword_matches = sum(1 for k in keywords if k in user_answer.lower())
    keyword_score = (keyword_matches / len(keywords)) * 40 if keywords else 0
    
    # Length appropriateness (20% of score)
    length_ratio = min(len(user_answer) / max(len(model_answer), 1), 1.0)
    length_score = length_ratio * 20
    
    # Word overlap with model answer (40% of score)
    common_words = user_words.intersection(model_words)
    overlap_score = (len(common_words) / len(model_words)) * 40 if model_words else 0
    
    total_score = keyword_score + length_score + overlap_score
    return min(total_score, 100)  # Cap at 100

def update_user_score(username, role, question, score):
    """Update user's score - now with persistent storage"""
    if 'users_db' not in st.session_state:
        st.session_state.users_db = load_users_from_file()
    
    if username not in st.session_state.users_db:
        return
    
    user_data = st.session_state.users_db[username]
    
    # Initialize scores for role if not exists
    if role not in user_data['scores']:
        user_data['scores'][role] = []
    
    # Add new score
    user_data['scores'][role].append({
        'question': question,
        'score': score,
        'timestamp': datetime.now().isoformat()
    })
    
    # Update totals
    user_data['total_questions'] += 1
    if score >= 70:  # Consider 70+ as correct
        user_data['correct_answers'] += 1
    
    # Save to file immediately
    save_users_to_file(st.session_state.users_db)

def get_user_stats(username):
    """Get user statistics - now with persistent storage"""
    if 'users_db' not in st.session_state:
        st.session_state.users_db = load_users_from_file()
        
    if username not in st.session_state.users_db:
        return None
    
    user_data = st.session_state.users_db[username]
    
    total_questions = user_data.get('total_questions', 0)
    correct_answers = user_data.get('correct_answers', 0)
    accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    # Calculate average score per role
    role_averages = {}
    for role, scores in user_data.get('scores', {}).items():
        if scores:
            avg_score = sum(item['score'] for item in scores) / len(scores)
            role_averages[role] = avg_score
    
    return {
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'accuracy': accuracy,
        'role_averages': role_averages,
        'recent_scores': user_data.get('scores', {})
    }
# =========================
# ENHANCED UI COMPONENTS
# =========================

def render_user_dashboard():
    """Render user dashboard with statistics"""
    st.markdown(f"""
    <div style='background: linear-gradient(90deg, #4CAF50, #45a049); padding: 1rem; 
                border-radius: 10px; margin-bottom: 1rem;'>
        <h3 style='color: white; margin: 0;'>Welcome back, {st.session_state.username}!</h3>
    </div>
    """, unsafe_allow_html=True)
    
    stats = get_user_stats(st.session_state.username)
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Questions Attempted",
                value=stats['total_questions']
            )
        
        with col2:
            st.metric(
                label="Correct Answers",
                value=stats['correct_answers']
            )
        
        with col3:
            st.metric(
                label="Accuracy",
                value=f"{stats['accuracy']:.1f}%"
            )
        
        with col4:
            avg_score = sum(stats['role_averages'].values()) / len(stats['role_averages']) if stats['role_averages'] else 0
            st.metric(
                label="Avg Score",
                value=f"{avg_score:.1f}"
            )

def render_score_feedback(score, keywords_matched, total_keywords):
    """Render enhanced score feedback"""
    if score >= 90:
        color = "#4CAF50"
        message = "Excellent answer!"
    elif score >= 80:
        color = "#8BC34A"
        message = "Great job!"
    elif score >= 70:
        color = "#FFC107"
        message = "Good answer!"
    elif score >= 60:
        color = "#FF9800"
        message = "Needs improvement"
    else:
        color = "#F44336"
        message = "Keep practicing!"
    
    st.markdown(f"""
    <div style='background: {color}; padding: 1rem; border-radius: 10px; text-align: center; margin: 1rem 0;'>
        <h2 style='color: white; margin: 0;'>Score: {score:.1f}/100</h2>
        <p style='color: white; margin: 0.5rem 0 0 0;'>{message}</p>
        <p style='color: white; margin: 0;'>Keywords: {keywords_matched}/{total_keywords}</p>
    </div>
    """, unsafe_allow_html=True)

def render_progress_chart():
    """Render user progress chart"""
    stats = get_user_stats(st.session_state.username)
    if not stats or not stats['recent_scores']:
        return
    
    st.subheader("Your Progress")
    
    # Prepare data for chart
    all_scores = []
    for role, scores in stats['recent_scores'].items():
        for item in scores[-10:]:  # Last 10 attempts per role
            all_scores.append({
                'Date': datetime.fromisoformat(item['timestamp']).strftime('%m/%d'),
                'Score': item['score'],
                'Role': role
            })
    
    if all_scores:
        try:
            import pandas as pd
            df = pd.DataFrame(all_scores)
            st.bar_chart(df.set_index('Date')['Score'])

        except:
            st.info("Install pandas to see progress charts: pip install pandas")

def enhanced_answer_section(selected_role, qa_list):
    """Enhanced answer submission with scoring"""
    st.subheader("Try Answering a Question")
    
    if not qa_list:
        st.warning("No questions available for this role yet.")
        return
    
    question_choices = [q for q, _ in qa_list]
    selected_question = st.selectbox("Choose a question to answer:", question_choices)
    
    # Get the model answer
    model_answer = next(a for (q, a) in qa_list if q == selected_question)
    auto_keywords = extract_keywords(model_answer, max_terms=8)
    
    # Show hint button
    if st.button("Show Hint"):
        st.info(f"Key topics to cover: {', '.join(auto_keywords[:4])}")
    
    with st.form("answer_form"):
        user_answer = st.text_area(
            "Your Answer", 
            height=150,
            placeholder="Type your detailed answer here..."
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            submitted = st.form_submit_button("Submit Answer", use_container_width=True)
        with col2:
            show_model_answer = st.form_submit_button("Show Model Answer", use_container_width=True)
        
        if submitted and user_answer.strip():
            # Calculate score
            score = calculate_score(user_answer, model_answer, auto_keywords)
            keywords_matched = sum(1 for k in auto_keywords if k in user_answer.lower())
            
            # Update user score
            update_user_score(st.session_state.username, selected_role, selected_question, score)
            
            # Show feedback
            render_score_feedback(score, keywords_matched, len(auto_keywords))
            
            # Show improvement suggestions
            missed_keywords = [k for k in auto_keywords if k not in user_answer.lower()]
            if missed_keywords:
                st.warning(f"Consider mentioning: {', '.join(missed_keywords[:3])}")
        
        elif submitted:
            st.warning("Please type your answer before submitting.")
        
        if show_model_answer:
            st.markdown("### Model Answer:")
            st.success(model_answer)

def enhanced_sidebar():
    """Enhanced sidebar with user options"""
    st.sidebar.title("Smart Interview Prep")
    st.sidebar.write(f"Welcome, **{st.session_state.username}**!")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Progress section
    stats = get_user_stats(st.session_state.username)
    if stats:
        st.sidebar.subheader("Quick Stats")
        st.sidebar.metric("Total Questions", stats['total_questions'])
        st.sidebar.metric("Accuracy", f"{stats['accuracy']:.1f}%")
        
        if stats['role_averages']:
            st.sidebar.subheader("Role Averages")
            for role, avg in stats['role_averages'].items():
                role_name = role.split(' – ')[-1] if ' – ' in role else role
                st.sidebar.write(f"**{role_name}**: {avg:.1f}")
    
    st.sidebar.markdown("---")
    st.sidebar.write("Created by **Trishala** – CSE Final Year, VRSEC")

def apply_custom_css():
    """Apply custom CSS styling with black text everywhere"""
    import streamlit as st

    st.markdown("""
    <style>
    /* App background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Force all text to black */
    .stMarkdown, .stMarkdown p, .stMarkdown div, 
    .markdown-text-container, label, span, p, li, strong {
        color: #000000 !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }

    /* Text inputs (username, password, etc.) */
    input[type="text"], input[type="password"], textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #e0e6ff !important;
        border-radius: 10px !important;
        padding: 0.5rem !important;
    }

    /* Buttons (Login, Signup) */
    .stButton > button {
        border-radius: 10px !important;
        border: none !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.2rem !important;
        transition: 0.3s ease-in-out;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%) !important;
        transform: scale(1.02);
    }

    /* Expander styling */
    .stExpander, .stExpander summary {
        background: white !important;
        border-radius: 10px !important;
        border: 1px solid #ddd !important;
        color: #000000 !important;
    }

    /* Metrics */
    .stMetric {
        background: white !important;
        padding: 1rem !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    .stMetric label, .stMetric div, .stMetric span {
        color: #000000 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f0f2f6 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)



# Initialize at the very start
init_session_state()
apply_custom_css()

# =========================
# Small helpers
# =========================
STOPWORDS = {
    "the","a","an","and","or","but","if","then","else","for","while","to","from","of","in","on",
    "with","by","as","is","are","was","were","be","been","being","at","it","its","this","that",
    "those","these","he","she","they","we","you","your","yours","our","ours","their","theirs",
    "do","does","did","done","doing","i","me","my","mine","into","about","via","over","under"
}

def extract_keywords(answer_text, max_terms=8):
    words = re.findall(r"[A-Za-z0-9\-\+\.#]+", answer_text.lower())
    terms = [w for w in words if w not in STOPWORDS and len(w) > 2]
    # prioritize unique order-preserving
    seen = set()
    uniq = []
    for t in terms:
        if t not in seen:
            seen.add(t)
            uniq.append(t)
    return uniq[:max_terms]

# =========================
# Role descriptions
# =========================
role_descriptions = {
    "Software Developer/Engineer": """Build applications, websites, and software solutions.
Work with languages like Java, Python, C++, JavaScript. Collaborate to design features, fix bugs, and ship reliable software.""",

    "Web Developer – Frontend": """Create responsive, accessible user interfaces using HTML, CSS, and JavaScript frameworks (React, Angular, Vue).
Optimize performance, cross-browser behavior, and UX.""",

    "Web Developer – Backend": """Implement server-side logic, APIs, and integrations using Node.js, Python, Java, or PHP.
Manage auth, data access, performance, security, and reliability.""",

    "Web Developer – Full-Stack": """Work across frontend and backend. Design APIs, build UI, manage data models, and deploy apps.
Own end-to-end features and developer experience.""",

    "Data Analyst / Data Scientist": """Extract insights from data using Python/R/SQL. Build dashboards and visualizations (Excel/Tableau/Power BI).
For DS: apply statistics and ML to model, predict, and experiment.""",

    "Quality Assurance (QA) Engineer": """Test apps to find bugs early. Design test plans/cases, automate with tools like Selenium, Playwright, JUnit, PyTest.
Champion quality gates and CI test health.""",

    "Database Administrator (DBA)": """Install, configure, and maintain databases (e.g., MySQL, PostgreSQL, Oracle).
Optimize performance, ensure backups, replication, high availability, and security.""",

    "System Administrator": """Manage servers, operating systems, user accounts, and networks.
Automate provisioning, patching, monitoring, and incident response.""",

    "Cybersecurity Analyst": """Protect systems and data from threats. Monitor logs, investigate alerts, harden configurations,
run vulnerability scans, and support incident response and compliance.""",

    "DevOps Engineer": """Bridge dev and ops. Automate CI/CD, infra as code, observability, and cloud operations (AWS/Azure/GCP).
Drive reliability, scalability, and fast, safe delivery."""
}

# =========================
# Questions & Answers - COMPLETE DATA
# =========================
QA = {}

QA["Software Developer/Engineer"] = [
    ("Difference between procedural and OOP?",
     "Procedural organizes code as procedures and data; OOP organizes as classes/objects with encapsulation, inheritance, polymorphism, abstraction."),
    ("Explain SOLID principles.",
     "SRP, OCP, LSP, ISP, DIP — design for modularity, substitutability, small interfaces, and dependency on abstractions."),
    ("Stack vs Heap?",
     "Stack: automatic storage for frames; fast, limited. Heap: dynamic allocation; larger, needs GC/free."),
    ("Types of testing?",
     "Unit, Integration, System, Acceptance, Regression, Smoke, Performance."),
    ("Git workflow you follow?",
     "Feature branches + PRs; commit small; rebase/merge; code reviews; CI checks."),
    ("Abstract class vs Interface?",
     "Abstract class can have state and default methods; interface defines contracts; languages vary on multiple inheritance."),
    ("Common design patterns?",
     "Singleton, Factory, Strategy, Observer, Adapter, Decorator, Repository, MVC/MVVM."),
    ("Big-O examples?",
     "O(1) hash get, O(log n) binary search, O(n) scan, O(n log n) sort, O(n²) bubble."),
    ("What is polymorphism?",
     "Same interface, different implementations; compile-time overloading, run-time overriding."),
    ("Process vs Thread?",
     "Process: isolated address space. Thread: shares process memory; lower overhead.")
]

QA["Web Developer – Frontend"] = [
    ("Critical rendering path?",
     "Steps from HTML/CSS/JS to pixels: parse HTML→DOM, CSS→CSSOM, render tree, layout, paint, composite."),
    ("Reflow vs repaint?",
     "Reflow (layout) recalculates geometry; repaint updates visuals without layout."),
    ("CSS specificity order?",
     "Inline > ID > class/attr/pseudo-class > element/pseudo-element; later wins on tie; !important overrides in scope."),
    ("Flexbox vs Grid?",
     "Flexbox for 1D alignment; Grid for 2D layouts and precise placement."),
    ("React reconciliation?",
     "Diff virtual DOM trees, minimal real DOM updates via keys and heuristics."),
    ("Controlled vs uncontrolled components?",
     "Controlled: state via React; Uncontrolled: DOM holds state via refs."),
    ("Hooks rules?",
     "Call at top level and only in React functions; consistent order."),
    ("useMemo vs useCallback?",
     "useMemo memoizes values; useCallback memoizes function references."),
    ("Key prop purpose?",
     "Stable identity for list items to optimize diffing and avoid state bugs."),
    ("SSR vs CSR vs SSG?",
     "SSR: HTML on server; CSR: browser renders; SSG: prebuilt. Trade SEO, TTFB, interactivity.")
]

QA["Web Developer – Backend"] = [
    ("REST vs RPC vs GraphQL?",
     "REST resource-based; RPC procedure calls; GraphQL client-driven queries and types."),
    ("Statelessness importance?",
     "Simplifies scaling, caching, retries; store session in tokens or shared store."),
    ("Authentication vs Authorization?",
     "AuthN verifies identity; AuthZ checks permissions; implement least privilege."),
    ("JWT pros/cons?",
     "Self-contained claims enable stateless auth; watch size, revocation, expiry, signing."),
    ("Database transactions & ACID?",
     "Atomicity, Consistency, Isolation, Durability; ensure correctness under concurrency."),
    ("Indexes and trade-offs?",
     "Speed reads, slow writes; extra storage; choose selective columns."),
    ("N+1 query problem?",
     "Many small queries due to per-row fetch; fix with joins, batching, eager loading."),
    ("Rate limiting strategies?",
     "Token bucket, leaky bucket, fixed/sliding windows; store counters in Redis."),
    ("Idempotency keys?",
     "Deduplicate retries for POST-like operations; store request ID and result."),
    ("Message queues usage?",
     "Decouple services, buffer spikes, async processing; e.g., RabbitMQ, Kafka, SQS.")
]

QA["Web Developer – Full-Stack"] = [
    ("Design a full-stack feature end-to-end.",
     "Define API schema, DB model, validations, auth, UI states, loading/errors; ship with tests and telemetry."),
    ("Choosing tech stack?",
     "Based on team expertise, requirements, scale, ecosystem, hiring pool, and ops maturity."),
    ("Monolith vs microservices?",
     "Start monolith for speed; split by bounded contexts when needed; consider operational cost."),
    ("SPA + API security?",
     "Short-lived tokens, refresh flow, HTTPS, SameSite cookies, CSRF protection if cookies."),
    ("Data fetching patterns?",
     "SWR/React Query for server state; cache, revalidate, optimistic updates."),
    ("Form validation full-stack?",
     "Shared schema (e.g., JSON Schema/Zod) for client+server parity; sanitize on server."),
    ("Upload UX considerations?",
     "Progress UI, chunking, retries, drag-drop, validations, accessibility."),
    ("Error handling UX?",
     "Inline errors, retry buttons, fallback UI, logging with user/session context."),
    ("Internationalization (i18n)?",
     "Message catalogs, locale formatting, RTL support, date/number rules."),
    ("Feature flags?",
     "Progressive rollout, A/B tests, kill switches; guard risky changes.")
]

QA["Data Analyst / Data Scientist"] = [
    ("Population vs sample?",
     "Population: entire set; sample: subset; use sampling to estimate population metrics."),
    ("Bias vs variance trade-off?",
     "Low bias models fit complex patterns but risk high variance; balance via regularization/validation."),
    ("p-value meaning?",
     "Probability of observing data as extreme assuming null hypothesis is true."),
    ("Confidence interval?",
     "Range likely to contain true parameter at given confidence (e.g., 95%)."),
    ("Feature scaling?",
     "Standardization/normalization to help gradient methods and distance-based models."),
    ("Train/validation/test split?",
     "Hold out test; use CV for model selection to avoid overfitting."),
    ("Cross-validation types?",
     "k-fold, stratified, time-series CV with rolling windows."),
    ("Overfitting detection?",
     "High train, low validation performance; use regularization, more data, simpler model."),
    ("Regularization L1 vs L2?",
     "L1 induces sparsity; L2 shrinks weights; elastic net combines."),
    ("Precision vs recall vs F1?",
     "Precision: correctness of positives; Recall: coverage; F1 balances.")
]

QA["Quality Assurance (QA) Engineer"] = [
    ("Difference: QA vs QC vs Testing?",
     "QA: process-oriented; QC: product checks; Testing: executes tests to find defects."),
    ("Test pyramid?",
     "Many unit, fewer integration, few e2e; optimize speed and coverage."),
    ("Test case vs test scenario?",
     "Scenario: high-level behavior; Case: detailed steps, data, expected results."),
    ("Bug lifecycle?",
     "New → Assigned → In-progress → Fixed → Retest → Verified → Closed (or Reopen)."),
    ("Severity vs priority?",
     "Severity: impact; Priority: fix order/urgency."),
    ("Smoke vs sanity testing?",
     "Smoke: basic build checks; Sanity: focused verification after small changes."),
    ("Black-box vs white-box?",
     "Black-box ignores internals; white-box uses code knowledge; grey-box mixes."),
    ("Boundary value analysis?",
     "Test edges and just-inside/outside values to catch off-by-ones."),
    ("Equivalence partitioning?",
     "Group inputs into valid/invalid classes to reduce cases."),
    ("Exploratory testing?",
     "Charter-driven, simultaneous learning, design, execution; record notes.")
]

QA["Database Administrator (DBA)"] = [
    ("Normalization forms?",
     "1NF remove repeating groups; 2NF remove partial dependencies; 3NF remove transitive; BCNF stricter."),
    ("Index types?",
     "B-tree, hash, bitmap, GiST/Gin; clustered vs non-clustered."),
    ("When to use composite indexes?",
     "Frequent multi-column filters; order matches query predicates."),
    ("Query plan analysis?",
     "EXPLAIN/EXPLAIN ANALYZE to inspect scans, joins, costs, cardinality."),
    ("Isolation levels?",
     "Read uncommitted, committed, repeatable read, serializable; anomalies prevented vary."),
    ("Replication options?",
     "Synchronous vs async, logical vs physical; primary-replica setups."),
    ("Backups: full vs incremental?",
     "Full captures all; incremental/differential only changes; test restores regularly."),
    ("Point-in-time recovery?",
     "Use WAL/binlogs + base backups to restore to specific timestamp."),
    ("Sharding vs partitioning?",
     "Sharding splits across nodes; partitioning splits within a node/table by key."),
    ("Hot vs cold standby?",
     "Hot can serve reads; cold requires promote/restore on failover.")
]

QA["System Administrator"] = [
    ("What is DNS and its record types?",
     "A system to resolve names→IPs; A/AAAA, CNAME, MX, TXT, NS, SRV."),
    ("DHCP role?",
     "Automatically assigns IPs, gateways, DNS to clients."),
    ("Linux boot process?",
     "Firmware→bootloader→kernel→init/systemd→services."),
    ("Runlevels/systemd targets?",
     "Legacy runlevels map to systemd targets like multi-user, graphical."),
    ("SSH hardening?",
     "Disable root login/passwords, use keys, change port, fail2ban, MFA."),
    ("Firewall basics?",
     "Default-deny inbound; open minimal ports; stateful rules; log drops."),
    ("Monitoring stack?",
     "Metrics, logs, traces; Prometheus/Grafana/ELK/CloudWatch."),
    ("Backup strategy 3-2-1?",
     "3 copies, 2 media, 1 off-site; test restores."),
    ("RAID levels?",
     "RAID0 stripe, 1 mirror, 5 parity, 10 mirror+stripe; trade speed/fault tolerance."),
    ("Filesystem choices?",
     "ext4, XFS, ZFS (snapshots, checksums); choose per workload.")
]

QA["Cybersecurity Analyst"] = [
    ("CIA triad?",
     "Confidentiality, Integrity, Availability."),
    ("Threat vs vulnerability vs risk?",
     "Threat: potential harm; Vulnerability: weakness; Risk: likelihood×impact."),
    ("Zero trust?",
     "Never trust, always verify; continuous authZ, micro-segmentation, least privilege."),
    ("Common attack vectors?",
     "Phishing, credential stuffing, XSS, SQLi, RCE, ransomware, supply chain."),
    ("Defense in depth?",
     "Multiple controls: network, endpoint, identity, app, data, physical."),
    ("SIEM purpose?",
     "Aggregate logs, correlate alerts, support detection and investigation."),
    ("IDS/IPS?",
     "Detects intrusions; IPS can block in-line; signature + anomaly detection."),
    ("Vulnerability scanning vs pentest?",
     "Automated breadth vs manual depth/exploitation."),
    ("SOC tiers?",
     "Tier 1 triage, Tier 2 investigation, Tier 3 threat hunting/IR."),
    ("MITRE ATT&CK?",
     "Knowledge base of adversary tactics/techniques to map detections.")
]

QA["DevOps Engineer"] = [
    ("CI vs CD?",
     "CI builds/tests frequently; CD automates delivery/deployments."),
    ("Blue-green vs canary?",
     "Blue-green swaps environments; canary gradually shifts traffic to new version."),
    ("Infrastructure as Code?",
     "Declarative reproducible infra (Terraform/CloudFormation); reviewable and versioned."),
    ("Containers vs VMs?",
     "Containers share kernel, lighter; VMs isolate OS, heavier."),
    ("Kubernetes primitives?",
     "Pod, Deployment, Service, Ingress, ConfigMap/Secret, StatefulSet, Job/CronJob."),
    ("Service mesh purpose?",
     "mTLS, traffic policies, retries, observability between services (e.g., Istio/Linkerd)."),
    ("GitOps?",
     "Desired state in Git; reconciler applies changes; auditable rollbacks."),
    ("Observability stack?",
     "Metrics, logs, traces; SLOs, error budgets; alert on symptoms."),
    ("Autoscaling types?",
     "Horizontal/vertical; based on CPU, custom metrics, queue depth."),
    ("Secrets in CI/CD?",
     "Store in vaults; short-lived tokens; masked logs; scoped permissions.")
]

# Build structure
questions_answers = {role: QA.get(role, []) for role in role_descriptions.keys()}

# =========================
# MAIN APP LOGIC
# =========================

# Check if user is logged in
if not st.session_state.logged_in:
    login_signup_page()
else:
    # Render dashboard
    render_user_dashboard()
    
    # Original app title and role selection
    st.title("Smart Interview Prep Assistant")
    selected_role = st.selectbox("Choose a job role:", list(role_descriptions.keys()))
    
    # Show role description
    st.markdown(f"**Role Description:**\n{role_descriptions[selected_role]}")
    
    # Show questions and answers
    st.subheader("Interview Questions with Answers")
    qa_list = questions_answers[selected_role]
    
    if qa_list:  # Check if questions exist for this role
        for i, (q, a) in enumerate(qa_list, 1):
            with st.expander(f"{i}. {q}"):
                st.markdown(f"**Answer:** {a}")
        
        # Enhanced answer section
        enhanced_answer_section(selected_role, qa_list)
        
        # Progress chart
        render_progress_chart()
    else:
        st.warning("Questions for this role are being prepared. Please check back soon!")
    
# =========================
# SIDEBAR ENHANCEMENTS (Add to your sidebar)
# =========================
def enhanced_sidebar():
    """Enhanced sidebar with user options"""
    st.sidebar.title("Smart Interview Prep")
    st.sidebar.write(f"Welcome, **{st.session_state.username}**!")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Progress section
    stats = get_user_stats(st.session_state.username)
    if stats:
        st.sidebar.subheader("Quick Stats")
        st.sidebar.metric("Total Questions", stats['total_questions'])
        st.sidebar.metric("Accuracy", f"{stats['accuracy']:.1f}%")
        
        if stats['role_averages']:
            st.sidebar.subheader("Role Averages")
            for role, avg in stats['role_averages'].items():
                role_name = role.split(' – ')[-1] if ' – ' in role else role
                st.sidebar.write(f"**{role_name}**: {avg:.1f}")
    
    st.sidebar.markdown("---")
    st.sidebar.write("Created by **Trishala** – CSE Final Year, VRSEC")
