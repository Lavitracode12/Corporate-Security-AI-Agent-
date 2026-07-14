import os
import json
from google import genai

class ThreatScorer:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY", "")
        self.client = genai.Client(api_key=api_key) if api_key else None

    def calculate_score(self, timeline, demo_mode: bool = False):
        """
        RAG Steps 2 & 3: Single-Prompt Cross-Document Reasoning Matrix.
        Evaluates risk parameters dynamically using LLM context or high-fidelity local rules.
        """
        if not timeline:
            return 15.0, "LOW", "Log analysis complete. No anomalous operational footprints isolated within corporate security data blocks."

        # AUGMENTATION 
        # Build out a clean chronological context window stream
        context_stream = ""
        for idx, log in enumerate(timeline, 1):
            doc_source = log.get("source_document", log.get("source", "LOG")).upper()
            details = str(log.get("details", log.get("action", str(log))))
            timestamp = log.get("timestamp", "UNKNOWN")
            context_stream += f"Record #{idx} | Source: [{doc_source}] | Time: {timestamp} | Event: {details}\n"

        # GENERATION
        if self.client and not demo_mode:
            try:
                prompt = (
                    "You are a Senior Corporate Risk AI Auditor.\n"
                    "Analyze these retrieved audit logs across multiple business channels:\n\n"
                    f"{context_stream}\n\n"
                    "Output a valid JSON object matching this structure exactly:\n"
                    "{\n  \"score\": <integer 0-100>,\n  \"verdict\": \"<3-sentence executive forensic brief detailing risk anomalies>\"\n}"
                )
                
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
                clean_json = response.text.replace("```json", "").replace("```", "").strip()
                result = json.loads(clean_json)
                
                score = float(result.get("score", 15.0))
                verdict = result.get("verdict", "")
                level = "CRITICAL" if score >= 75 else "HIGH" if score >= 50 else "MEDIUM" if score >= 30 else "LOW"
                return score, level, verdict
                
            except Exception as e:
                print(f"⚠️ API Exception encountered ({e}). Transitioning instantly to Local Heuristic Scorer...")


        # This executes if Gemini hits a 429 quota exception or demo_mode is triggered.
        base_score = 15.0
        risk_indicators = []
        full_text = context_stream.lower()

        # Context-Aware Parameter Traversal Rules
        if "falcon" in full_text or "confidential" in full_text:
            base_score += 35.0
            risk_indicators.append("Confidential Project Falcon files referenced")
            
        if "download" in full_text or "copied" in full_text or "exfiltration" in full_text:
            base_score += 25.0
            risk_indicators.append("Mass download or data copy action detected")
            
        if "usb" in full_text or "mass storage" in full_text or "removable" in full_text:
            base_score += 15.0
            risk_indicators.append("External hardware mass storage mounting signature")
            
        if "resigned" in full_text or "resignation" in full_text or "terminated" in full_text:
            base_score += 10.0
            risk_indicators.append("Active HR resignation window profile discrepancy")

        # Cap the output score safely at standard boundaries
        score = min(base_score, 100.0)
        level = "CRITICAL" if score >= 75 else "HIGH" if score >= 50 else "MEDIUM" if score >= 30 else "LOW"

        # Generate dynamic text brief completely locally
        if score > 45.0:
            verdict = (
                f"LOCAL AUDIT WARNING ({level}): High-risk correlation isolated across tracking channels. "
                f"Target identity logs show clear risk vector signatures: {', '.join(risk_indicators)}. "
                f"Incident timeline indicates active data staging behaviors."
            )
        else:
            verdict = (
                f"LOCAL AUDIT STATUS ({level}): Checked logs match typical corporate operational behaviors. "
                f"No unified malicious signatures or high-priority data staging flags have been isolated."
            )

        return score, level, verdict