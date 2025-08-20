from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import os, sys, re
import random

app = FastAPI(
    title="AI/DS Matchmaker API",
    description="AI-powered collaboration platform for AI/DS practitioners",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "AI/DS Matchmaker API",
        "version": "1.0.0",
        "status": "running",
        "build_id": os.getenv("RAILWAY_BUILD_ID", "local"),
        "demo": "Enhanced with rich mock data for portfolio showcase",
        "endpoints": {
            "analyze": "/analyze - Extract skills from conversation",
            "match": "/match - Find collaboration partners",
            "demo_users": "/demo/users - Sample user profiles",
            "demo_conversation": "/demo/conversation - Example conversation analysis"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "AI/DS Matchmaker API"}

# Enhanced Models
class AnalyzeRequest(BaseModel):
    text: str

class SkillExtraction(BaseModel):
    skill: str
    confidence: float
    evidence: List[str]

class ConversationAnalysis(BaseModel):
    extracted_skills: List[SkillExtraction]
    experience_level: str
    learning_goals: List[str]
    collaboration_style: str
    problem_solving_approach: str
    portfolio_readiness: float

class UserProfile(BaseModel):
    id: str
    name: str
    title: str
    location: str
    skills: Dict[str, int]
    learning_goals: List[str]
    collaboration_preferences: List[str]
    current_projects: List[str]
    bio: str
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None

class MatchResult(BaseModel):
    user: UserProfile
    compatibility_score: float
    skill_complementarity: float
    learning_synergy: float
    collaboration_fit: float
    reasoning: List[str]
    suggested_projects: List[str]
    mutual_benefits: Dict[str, List[str]]

# Enhanced Skill Detection
SKILL_KEYWORDS = {
    "Python": ["python", "py", "django", "flask", "fastapi", "pandas", "numpy"],
    "Machine Learning": ["ml", "machine learning", "scikit-learn", "sklearn", "model", "algorithm"],
    "Deep Learning": ["deep learning", "neural network", "tensorflow", "pytorch", "keras"],
    "NLP": ["nlp", "natural language", "text processing", "spacy", "nltk", "transformers"],
    "Data Science": ["data science", "data analysis", "statistics", "visualization"],
    "SQL": ["sql", "database", "postgresql", "mysql", "query"],
    "JavaScript": ["javascript", "js", "react", "node", "express", "next"],
    "Frontend": ["frontend", "ui", "css", "html", "react", "vue", "angular"],
    "Backend": ["backend", "api", "server", "fastapi", "django", "flask"],
    "DevOps": ["docker", "kubernetes", "aws", "deployment", "ci/cd"],
    "Git": ["git", "github", "version control", "collaboration"],
    "Cloud": ["aws", "azure", "gcp", "cloud", "deployment"]
}

EXPERIENCE_INDICATORS = {
    "expert": ["expert", "senior", "lead", "architect", "years", "production", "scale"],
    "advanced": ["advanced", "complex", "optimization", "architecture", "design"],
    "intermediate": ["intermediate", "working with", "experience", "familiar"],
    "beginner": ["learning", "new to", "getting started", "beginner", "tutorial"]
}

def extract_skills_enhanced(text: str) -> List[SkillExtraction]:
    """Enhanced skill extraction with confidence scoring"""
    text_lower = text.lower()
    extracted = []
    
    for skill, keywords in SKILL_KEYWORDS.items():
        matches = [kw for kw in keywords if kw in text_lower]
        if matches:
            confidence = min(len(matches) / len(keywords) * 2, 1.0)
            extracted.append(SkillExtraction(
                skill=skill,
                confidence=round(confidence, 2),
                evidence=matches[:3]
            ))
    
    return sorted(extracted, key=lambda x: x.confidence, reverse=True)

def assess_experience_level(text: str) -> str:
    """Assess experience level from conversation"""
    text_lower = text.lower()
    
    for level, indicators in EXPERIENCE_INDICATORS.items():
        if any(indicator in text_lower for indicator in indicators):
            return level
    
    return "intermediate"

def extract_learning_goals(text: str) -> List[str]:
    """Extract learning goals from conversation"""
    goals = []
    text_lower = text.lower()
    
    learning_phrases = ["want to learn", "need to learn", "interested in", "learning"]
    for skill in SKILL_KEYWORDS.keys():
        if any(phrase in text_lower for phrase in learning_phrases):
            if skill.lower() in text_lower and skill not in [s.skill for s in extract_skills_enhanced(text)]:
                goals.append(skill)
    
    return goals[:3]

@app.post("/analyze")
async def analyze_conversation(request: AnalyzeRequest) -> ConversationAnalysis:
    """Enhanced conversation analysis with detailed insights"""
    text = request.text
    
    skills = extract_skills_enhanced(text)
    experience = assess_experience_level(text)
    learning_goals = extract_learning_goals(text)
    
    # Analyze collaboration style
    collab_indicators = {
        "Portfolio Builder": ["portfolio", "showcase", "project", "build"],
        "Learning Partner": ["learn", "study", "together", "mentor"],
        "Technical Leader": ["lead", "manage", "team", "architecture"],
        "Problem Solver": ["solve", "challenge", "problem", "optimize"]
    }
    
    collaboration_style = "Portfolio Builder"
    for style, indicators in collab_indicators.items():
        if any(indicator in text.lower() for indicator in indicators):
            collaboration_style = style
            break
    
    # Assess problem-solving approach
    approaches = {
        "Systematic": ["systematic", "process", "methodology", "framework"],
        "Creative": ["creative", "innovative", "unique", "original"],
        "Practical": ["practical", "real-world", "useful", "efficient"],
        "Research-Oriented": ["research", "academic", "theory", "analysis"]
    }
    
    problem_solving = "Practical"
    for approach, indicators in approaches.items():
        if any(indicator in text.lower() for indicator in indicators):
            problem_solving = approach
            break
    
    portfolio_readiness = min(len(skills) * 0.2 + (0.3 if experience in ["advanced", "expert"] else 0.1), 1.0)
    
    return ConversationAnalysis(
        extracted_skills=skills,
        experience_level=experience,
        learning_goals=learning_goals,
        collaboration_style=collaboration_style,
        problem_solving_approach=problem_solving,
        portfolio_readiness=round(portfolio_readiness, 2)
    )

# Demo User Profiles
DEMO_USERS = [
    UserProfile(
        id="user1",
        name="Sarah Chen",
        title="Full-Stack Developer & ML Enthusiast",
        location="San Francisco, CA",
        skills={"JavaScript": 5, "React": 5, "Python": 3, "Machine Learning": 2},
        learning_goals=["Machine Learning", "Deep Learning", "Data Science"],
        collaboration_preferences=["Portfolio Building", "Learning Partner"],
        current_projects=["E-commerce Platform", "Learning ML Fundamentals"],
        bio="Frontend expert transitioning to AI/ML. Love building user-friendly interfaces and want to add intelligence to my applications.",
        github_url="https://github.com/sarahchen",
        linkedin_url="https://linkedin.com/in/sarahchen"
    ),
    UserProfile(
        id="user2",
        name="Marcus Rodriguez",
        title="NLP Research Engineer",
        location="Austin, TX",
        skills={"Python": 5, "NLP": 5, "Deep Learning": 4, "Frontend": 2},
        learning_goals=["Frontend", "Product Management", "UI/UX"],
        collaboration_preferences=["Portfolio Building", "Technical Mentor"],
        current_projects=["Sentiment Analysis API", "Chatbot Framework"],
        bio="NLP specialist with 4+ years experience. Want to learn how to build better user interfaces for my AI models.",
        github_url="https://github.com/marcusrodriguez"
    ),
    UserProfile(
        id="user3",
        name="Priya Patel",
        title="Data Scientist → Product Manager",
        location="New York, NY",
        skills={"Data Science": 4, "SQL": 5, "Python": 4, "Product Management": 3},
        learning_goals=["Machine Learning", "Technical Leadership"],
        collaboration_preferences=["Co-founder", "Strategic Partner"],
        current_projects=["Analytics Dashboard", "ML Product Strategy"],
        bio="Bridging data science and product. Looking for technical co-founders to build AI-powered products.",
        linkedin_url="https://linkedin.com/in/priyapatel"
    ),
    UserProfile(
        id="user4",
        name="Alex Kim",
        title="DevOps Engineer Learning AI",
        location="Seattle, WA",
        skills={"DevOps": 5, "Cloud": 5, "Python": 3, "Machine Learning": 1},
        learning_goals=["Machine Learning", "AI/ML Operations"],
        collaboration_preferences=["Learning Partner", "Portfolio Building"],
        current_projects=["ML Pipeline Infrastructure", "Kubernetes for ML"],
        bio="Infrastructure expert wanting to specialize in MLOps. Can handle all deployment and scaling needs.",
        github_url="https://github.com/alexkim"
    )
]

@app.get("/demo/users")
async def get_demo_users() -> List[UserProfile]:
    """Get sample user profiles for demo"""
    return DEMO_USERS

@app.post("/match")
async def find_matches(request: Dict) -> Dict[str, List[MatchResult]]:
    """Enhanced matching with detailed compatibility analysis"""
    user_skills = request.get("skills", [])
    
    matches = []
    for user in DEMO_USERS:
        # Calculate compatibility scores
        skill_overlap = len(set(user_skills) & set(user.skills.keys())) / max(len(user_skills), 1)
        learning_synergy = len(set(user_skills) & set(user.learning_goals)) / max(len(user.learning_goals), 1)
        
        # Mock collaboration fit
        collab_fit = random.uniform(0.6, 0.9)
        
        overall_score = (skill_overlap * 0.4 + learning_synergy * 0.4 + collab_fit * 0.2)
        
        # Generate reasoning
        reasoning = []
        if skill_overlap > 0.3:
            reasoning.append("Strong skill complementarity for collaboration")
        if learning_synergy > 0.3:
            reasoning.append("Excellent learning exchange opportunities")
        if "Portfolio Building" in user.collaboration_preferences:
            reasoning.append("Both focused on portfolio development")
        
        # Suggest projects
        suggested_projects = [
            f"Full-stack AI application combining {user.title.split()[0]} and ML",
            f"Portfolio project showcasing {user.skills} integration",
            "Real-time data processing and visualization platform"
        ]
        
        # Mutual benefits
        mutual_benefits = {
            "you_gain": [f"Learn {skill}" for skill in user.skills.keys() if skill in user_skills][:2],
            "they_gain": [f"Learn {skill}" for skill in user_skills if skill not in user.skills][:2]
        }
        
        matches.append(MatchResult(
            user=user,
            compatibility_score=round(overall_score, 2),
            skill_complementarity=round(skill_overlap, 2),
            learning_synergy=round(learning_synergy, 2),
            collaboration_fit=round(collab_fit, 2),
            reasoning=reasoning,
            suggested_projects=suggested_projects[:2],
            mutual_benefits=mutual_benefits
        ))
    
    # Sort by compatibility and return top matches
    matches.sort(key=lambda x: x.compatibility_score, reverse=True)
    return {"matches": matches[:3]}

@app.get("/demo/conversation")
async def demo_conversation_analysis():
    """Example conversation analysis for demo purposes"""
    example_text = """I'm a mechanical engineer with 2 years of data science experience. 
    I'm working on a football momentum prediction project using machine learning with 
    walk-forward validation. I need to learn web development and NLP to build the 
    complete application with commentary features. Looking for portfolio building 
    collaboration partners."""
    
    analysis = await analyze_conversation(AnalyzeRequest(text=example_text))
    
    return {
        "example_input": example_text,
        "analysis_result": analysis,
        "demo_note": "This shows how the AI extracts skills, assesses experience, and identifies collaboration needs from natural conversation"
    }

@app.get("/stats")
async def get_demo_stats():
    """Demo statistics for impressive presentation"""
    return {
        "total_users": 1247,
        "successful_matches": 89,
        "active_collaborations": 34,
        "completed_projects": 23,
        "skills_analyzed": 15000,
        "avg_match_accuracy": 0.87,
        "countries_represented": 42,
        "top_skills": ["Python", "Machine Learning", "JavaScript", "Data Science", "React"],
        "success_stories": [
            "AI-powered e-commerce platform built by ML engineer + Full-stack developer",
            "NLP research project turned into startup by Data Scientist + Product Manager",
            "Open-source ML tools with 2K+ GitHub stars from international collaboration"
        ]
    }
