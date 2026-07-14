from datetime import datetime
class ForensicCorrelator:
    @staticmethod
    def construct_timeline(findings: list[dict]) -> list[dict]:
        events = []
        for finding in findings:
            payload = finding.get("data", {})
            source = finding.get("source", "UNKNOWN")
            
            # Unpack potential nested payloads from stringified storage blocks
            if isinstance(payload, str):
                try: import json; payload = json.loads(payload)
                except: payload = {"description": payload}

            timestamp = payload.get("timestamp") or payload.get("start_date")
            
            if not timestamp:
                continue
                
            events.append({
                "timestamp": timestamp,
                "source": source.upper(),
                "details": payload
            })
            
        # Clear sort step to ensure temporal correctness across distributed data points
        def parse_date(x):
            try: return datetime.fromisoformat(x["timestamp"].replace("Z", ""))
            except: return datetime.min

        events.sort(key=parse_date)
        return events