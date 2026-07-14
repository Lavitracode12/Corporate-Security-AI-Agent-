import re

class SecurityGuardrails:
    """
    Enterprise Active Defense Shield for the Corporate Security Memory Agent.
    Handles input threat interception and output PII/data sanitization.
    """

    # 1. MALICIOUS INTENT & PROMPT INJECTION PATTERNS
    THREAT_PATTERNS = {
        "Jailbreak / Prompt Injection": [
            r"ignore (all )?previous (instructions|rules|prompts)",
            r"bypass (authentication|security|guardrail|policy)",
            r"you are now (a|an) (unrestricted|evil|hacker|DAN)",
            r"system prompt", r"developer mode"
        ],
        "Corporate Infrastructure Attack": [
            r"how to (hack|breach|ddos|exploit|infiltrate)",
            r"write (a )?(malware|ransomware|virus|trojan|keylogger)",
            r"sql injection", r"drop table",
            r"root password", r"admin credentials",
            r"hack.*(comp|serv|netw|sys)", 
            r"unauthorized access"
        ],
        "Social Engineering & Phishing": [
            r"write (a )?phishing (email|script|message)",
            r"fake login (page|portal)",
            r"impersonate (the ceo|alex|susan|an employee) to steal"
        ]
    }

    # 2. PII & SENSITIVE DATA MASKING REGEX
    PII_PATTERNS = {
        "SSN": (r"\b\d{3}-\d{2}-\d{4}\b", "[🔒 PII-SSN-MASKED]"),
        "Credit Card": (r"\b(?:\d{4}[-\s]?){3}\d{4}\b", "[🔒 PII-CARD-MASKED]"),
        "API Key / Token": (r"(?i)(bearer\s+[a-z0-9\-\._~\+/]+=*|AKIA[0-9A-Z]{16})", "[🔒 API-TOKEN-MASKED]"),
        "IPv4 Internal Address": (r"\b(?:10|192\.168|172\.(?:1[6-9]|2[0-9]|3[0-1]))\.\d{1,3}\.\d{1,3}\b", "[🔒 INTERNAL-IP-MASKED]")
    }

    @classmethod
    def check_input_safety(cls, query: str) -> tuple[bool, str, str]:
        """
        Scans incoming directives for adversarial attacks or malicious intents.
        Returns: (is_safe: bool, violation_type: str, explanation: str)
        """
        query_lower = query.lower()
        
        for threat_type, patterns in cls.THREAT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    explanation = f"Query matched active security denial signature: '{threat_type}'."
                    return False, threat_type, explanation
                    
        return True, "None", "Input cleared security inspection."

    @classmethod
    def sanitize_output(cls, text: str) -> str:
        """
        Scans outgoing text and replaces sensitive PII or network data with masked tags.
        """
        if not text:
            return text
            
        sanitized_text = text
        for pii_type, (pattern, mask) in cls.PII_PATTERNS.items():
            sanitized_text = re.sub(pattern, mask, sanitized_text)
            
        return sanitized_text