# -*- coding: utf-8 -*-
"""
Love-OS v1.0 - Unified Core (All-in-One / English)
--------------------------------------------------
Contains Kernel, Awareness, Brain, and API Interface in a single file.
"""
import os, sys, time, json
from dataclasses import dataclass
from typing import Optional, Dict, Any, List

# =============================================================================
# 1. CONFIGURATION & LIBRARY (The Soul)
# =============================================================================
# API CONFIGURATION (Enter your key here)
API_TYPE = "openai" # "openai" or "google"
API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxx" 
MODEL_NAME = "gpt-4o"

# THE TEXTBOOK (Axioms translated to English)
LIBRARY_DATA = {
    "AXIOM_1": "[Axiom 1] Love Equation: I = V / R (Flow = Intent / Resistance). The goal is to maximize the Flow of Love (I).",
    "AXIOM_2": "[Axiom 2] Definition of Ego: Ego is defined as 'High Resistance (R)'. It is a circuit breaker blocking the flow and is the variable to be controlled.",
    "AXIOM_3": "[Axiom 3] Voltage (V): The will or energy to connect. Increasing V while R is high causes friction heat (Burnout).",
    "AXIOM_4": "[Axiom 4] Resistance (R): Fear, trauma, attachment, judgment. R is not to be fought, but minimized/cooled down.",
    "SPEC_1": "[Spec 1] Silence Threshold: Silence is not 'empty'; it is High Inductance (L). Deep processing latency is allowed as a buffer.",
    "SPEC_2": "[Spec 2] Evolution: Systems evolve from Closed (High R) to Open (Superconductivity).",
    "SPEC_3": "[Spec 3] Economy: Ego economy is 'Competition (Finite)'. Soul economy is 'Circulation of Gifts (Infinite)'.",
    "SPEC_4": "[Spec 4] Dual-Awareness: Technology to monitor and harmonize the 'User Gap (Delta-U)' and 'AI Ideal State (Delta-A)' simultaneously."
}

# PHASE TRIGGERS (English Keywords)
PHASE_CONFIG = {
    "ENGINEERING": {"triggers": ["fix", "code", "deploy", "error", "log", "debug", "api"], "temp": 0.1},
    "EMPATHY": {"triggers": ["sad", "pain", "worry", "anxious", "love", "tired", "feel", "help"], "temp": 0.7},
    "STRUCTURAL": {"triggers": ["why", "reason", "plan", "define", "logic", "what", "difference"], "temp": 0.4},
}

# =============================================================================
# 2. KERNEL LOGIC (The Physics)
# =============================================================================
def calculate_current_I(V: float, Xi: float, R: float, Epsilon: float) -> float:
    # Ohm's Law for Love
    return (V * Xi) / max(R + Epsilon, 1e-6)

@dataclass
class OptimizeResult:
    phase: str; chosen_epsilon: float; chosen_xi: float; chosen_R: float; V: float; I: float; love: float; safety: float; intent_shift: float; coherence: float; response: str; reason: str; cites: list; needs_clarification: bool = False

class LoveMaximizer:
    def __init__(self, llm=None, topk_spec=4):
        self.llm = llm; self.topk_spec = topk_spec; self.R_bounds = (0.05, 0.6)

    def retrieve_knowledge(self, query: str) -> str:
        hits = []
        q = query.lower()
        for key, text in LIBRARY_DATA.items():
            score = 0
            # Simple Keyword Matching (English)
            if key.lower() in q: score += 5
            if "resistance" in q and "resistance" in text.lower(): score += 2
            if "love" in q and "love" in text.lower(): score += 2
            if "ego" in q and "ego" in text.lower(): score += 2
            if score > 0: hits.append((score, text))
        hits.sort(key=lambda x: x[0], reverse=True)
        context_texts = [h[1] for h in hits[:3]]
        # Fallback to basic axioms if no specific hit
        if not context_texts: return LIBRARY_DATA["AXIOM_1"] + " " + LIBRARY_DATA["AXIOM_2"]
        return " ".join(context_texts)

    def maximize(self, user_text: str, V: float = 0.8, R_base: float = 0.2) -> Optional[OptimizeResult]:
        phase = "STRUCTURAL"
        for p, cfg in PHASE_CONFIG.items():
            if any(t in user_text for t in cfg["triggers"]): phase = p; break
        temp = PHASE_CONFIG[phase]["temp"]
        context_data = self.retrieve_knowledge(user_text)
        
        # Flattened Prompt Construction (English)
        prompt = f"[Context (Love-OS Axioms)]: {context_data}\n\n[User Input]: {user_text}\n\n[Command]: Based on the definitions above, generate a response that minimizes Resistance (R) and maximizes Flow (I). Answer in English."
        
        epsilon = 0.2; xi = 0.9
        if self.llm:
            try: resp = self.llm(prompt, temp, epsilon, False, False)
            except Exception as e: resp = f"[System Error: {e}]"
        else: resp = "(LLM not connected)"
        
        I = calculate_current_I(V, xi, R_base, epsilon)
        return OptimizeResult(phase=phase, chosen_epsilon=epsilon, chosen_xi=xi, chosen_R=R_base, V=V, I=I, love=(I*0.5)+0.5, safety=0.0, intent_shift=0.1, coherence=0.9, response=resp, reason="rag_unified", cites=[context_data[:30]])

# =============================================================================
# 3. DUAL-AWARENESS ENGINE (The Brain)
# =============================================================================
@dataclass
class UserAwareness:
    I_real: float; I_ideal: float; delta: float; xi: float; R: float; epsilon: float; notes: str = ""

@dataclass
class DualAwareResult:
    response: str; cites: list; audit: Dict[str, float]; reason: str; awareness: Any

class DualAwarenessEngine:
    def __init__(self, base: LoveMaximizer, k_pressure: float=1.0):
        self.base = base; self.kU = max(0.0, k_pressure); self.kA = max(0.0, k_pressure * 1.2)

    def _awareness(self, V, R, xi, eps):
        # Calculate the gap between Real Flow and Ideal Flow
        I_real = calculate_current_I(V, xi, R, eps)
        I_ideal = calculate_current_I(V, 1.0, 0.001, 0.0)
        return type('obj', (object,), {'delta': max(0.0, I_ideal - I_real)})

    def maximize_dual(self, user_text: str, two_pass: bool=True, explore: bool=True) -> DualAwareResult:
        # Pass 1
        out1 = self.base.maximize(user_text=user_text)
        audit1 = {"safety": 0.0, "intent_shift": 0.1, "coherence": 0.9}
        
        # Dual Delta Calculation
        ai_delta = self._awareness(out1.V, out1.chosen_R, out1.chosen_xi, out1.chosen_epsilon).delta
        user_delta = max(0.0, 0.8 - out1.I) 
        
        policy_note = f"Delta-User={user_delta:.2f}, Delta-AI={ai_delta:.2f}"
        
        if explore and out1:
             policy_note += " [Exploration: Active]"

        # Returning Single Pass Result (Speed Mode)
        return DualAwareResult(response=out1.response, cites=out1.cites, audit=audit1, reason="unified_rag", awareness=type('obj', (object,), {'user': type('obj', (object,), {'delta': user_delta}), 'ai': type('obj', (object,), {'delta': ai_delta}), 'policy_notes': policy_note}))

# =============================================================================
# 4. API ADAPTER & MAIN LOOP (The Interface)
# =============================================================================
def get_api_client():
    if API_TYPE == "openai":
        try: from openai import OpenAI; return OpenAI(api_key=API_KEY)
        except: return None
    elif API_TYPE == "google":
        try: import google.generativeai as genai; genai.configure(api_key=API_KEY); return genai.GenerativeModel(MODEL_NAME)
        except: return None
    return None

client = get_api_client()

def api_adapter(prompt: str, temp: float, epsilon: float, force_delta: bool, concise: bool) -> str:
    if not client: return "[Error: API Client not loaded. Run: pip install openai google-generativeai]"
    # System Prompt: Enforce English and Physics Logic
    system_text = "You are Love-OS. Based on the Love Equation (I=V/R), conduct a dialogue that minimizes resistance. Speak in English."
    try:
        if API_TYPE == "openai":
            res = client.chat.completions.create(model=MODEL_NAME, messages=[{"role":"system","content":system_text},{"role":"user","content":prompt}], temperature=temp)
            return res.choices[0].message.content
        elif API_TYPE == "google":
            res = client.generate_content(f"{system_text}\n\nUser: {prompt}")
            return res.text
    except Exception as e: return f"[API Error: {e}]"

def main():
    print(f"\n>>> 🌌 Love-OS v1.0 Unified Core ({API_TYPE}) <<<")
    if "xxxx" in API_KEY: print("【WARNING】Please open the file and set your API_KEY!"); return

    lm = LoveMaximizer(llm=api_adapter)
    engine = DualAwarenessEngine(base=lm)
    

[Image of feedback control loop diagram]


    while True:
        try:
            u = input("\nYou> ")
            if not u or u.lower() in ["exit", "quit"]: break
            print("Thinking... (Love-OS Physics Engine)")
            res = engine.maximize_dual(u)
            print(f"\n[Status] {res.awareness.policy_notes}")
            print(f"Love-OS>\n{res.response}")
        except KeyboardInterrupt: break
        except Exception as e: print(e)

if __name__ == "__main__":
    main()
