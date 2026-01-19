import re

SKILL_ALIASES = {
    "Python": ["python"],
    "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript", "ts"],
    "Java": ["java"],
    "C": ["c"],
    "C++": ["c++", "cpp"],
    "C#": ["c#", "c sharp"],
    "Go": ["go", "golang"],
    "R": ["r"],
    "Ruby": ["ruby"],
    "PHP": ["php"],
    "Swift": ["swift"],
    "Kotlin": ["kotlin"],
    "Rust": ["rust"],
    "SQL": ["sql"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MySQL": ["mysql"],
    "SQLite": ["sqlite"],
    "MongoDB": ["mongodb", "mongo"],
    "Redis": ["redis"],
    "Elasticsearch": ["elasticsearch", "elastic search"],
    "DynamoDB": ["dynamodb"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure"],
    "GCP": ["gcp", "google cloud"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Linux": ["linux"],
    "Git": ["git"],
    "REST": ["rest", "restful"],
    "GraphQL": ["graphql"],
    "React": ["react", "react.js", "reactjs"],
    "Vue": ["vue", "vue.js", "vuejs"],
    "Angular": ["angular", "angularjs"],
    "Node.js": ["node.js", "nodejs"],
    "Django": ["django"],
    "Flask": ["flask"],
    "FastAPI": ["fastapi"],
    "Spring": ["spring", "spring boot", "springboot"],
    "Express": ["express", "express.js", "expressjs"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "CI/CD": ["ci/cd", "ci cd", "cicd"],
    "Jenkins": ["jenkins"],
    "Terraform": ["terraform"],
    "Ansible": ["ansible"],
    "Kafka": ["kafka"],
    "RabbitMQ": ["rabbitmq"],
    "Spark": ["spark", "apache spark"],
    "Hadoop": ["hadoop"],
    "Airflow": ["airflow", "apache airflow"],
    "ETL": ["etl"],
    "Tableau": ["tableau"],
    "Power BI": ["power bi", "powerbi"],
    "Excel": ["excel"],
    "Selenium": ["selenium"],
}

SENIORITY_KEYWORDS = [
    "senior",
    "staff",
    "principal",
    "lead",
    "manager",
    "director",
    "head of",
    "architect",
]

ENTRY_KEYWORDS = [
    "entry level",
    "entry-level",
    "junior",
    "jr",
    "jr.",
    "graduate",
    "new grad",
    "intern",
    "apprentice",
    "trainee",
]

YEAR_RANGE_RE = re.compile(r"(\d+)\s*-\s*(\d+)\s*years", re.IGNORECASE)
YEAR_PLUS_RE = re.compile(r"(\d+)\s*\+\s*years", re.IGNORECASE)
YEAR_PLAIN_RE = re.compile(r"(\d+)\s*years", re.IGNORECASE)


def _build_pattern(alias):
    alias_lower = alias.lower()
    if alias_lower == "c":
        return re.compile(r"(?<!\w)c(?![\w#\+])", re.IGNORECASE)
    if alias_lower == "r":
        return re.compile(r"(?<!\w)r(?!\w)", re.IGNORECASE)
    escaped = re.escape(alias)
    return re.compile(r"(?<!\w)" + escaped + r"(?!\w)", re.IGNORECASE)


_SKILL_PATTERNS = {
    canonical: [_build_pattern(alias) for alias in aliases]
    for canonical, aliases in SKILL_ALIASES.items()
}


def extract_skills(text):
    if not text:
        return []
    matches = set()
    for canonical, patterns in _SKILL_PATTERNS.items():
        for pattern in patterns:
            if pattern.search(text):
                matches.add(canonical)
                break
    return sorted(matches)


def _keyword_matches(text, keywords):
    matches = []
    seen = set()
    for keyword in keywords:
        pattern = re.compile(
            r"(?<!\w)" + re.escape(keyword) + r"(?!\w)", re.IGNORECASE
        )
        for match in pattern.finditer(text):
            value = match.group(0)
            if value.lower() not in seen:
                matches.append(value)
                seen.add(value.lower())
    return matches


def _overlaps(span, spans):
    start, end = span
    for other_start, other_end in spans:
        if start < other_end and end > other_start:
            return True
    return False


def extract_signals(text):
    if not text:
        return {
            "min_years": None,
            "max_years": None,
            "year_matches": [],
            "senior_signals": [],
            "entry_signals": [],
        }

    min_years = None
    max_years = None
    year_matches = []
    used_spans = []

    for match in YEAR_RANGE_RE.finditer(text):
        low = int(match.group(1))
        high = int(match.group(2))
        min_years = low if min_years is None else min(min_years, low)
        max_years = high if max_years is None else max(max_years, high)
        year_matches.append(match.group(0))
        used_spans.append(match.span())

    for match in YEAR_PLUS_RE.finditer(text):
        value = int(match.group(1))
        min_years = value if min_years is None else min(min_years, value)
        year_matches.append(match.group(0))
        used_spans.append(match.span())

    for match in YEAR_PLAIN_RE.finditer(text):
        if _overlaps(match.span(), used_spans):
            continue
        value = int(match.group(1))
        min_years = value if min_years is None else min(min_years, value)
        max_years = value if max_years is None else max(max_years, value)
        year_matches.append(match.group(0))
        used_spans.append(match.span())

    senior_signals = _keyword_matches(text, SENIORITY_KEYWORDS)
    entry_signals = _keyword_matches(text, ENTRY_KEYWORDS)

    return {
        "min_years": min_years,
        "max_years": max_years,
        "year_matches": year_matches,
        "senior_signals": senior_signals,
        "entry_signals": entry_signals,
    }
