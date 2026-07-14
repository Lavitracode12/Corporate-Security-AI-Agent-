import os
import requests
import base64
from dotenv import load_dotenv

# Load .env configuration parameters
load_dotenv()

from Graph.workflow import app_graph

def export_pipeline_graph():
    output_path = "architecture_flowchart.png"
    
    try:
        # 1. Fetch the raw syntax block from the workflow engine
        raw_mermaid = app_graph.get_graph().draw_mermaid()
        
        # 🌟 CLEAN TOOL SUBGRAPH LAYOUT DEFINITION
        db_subgraph = (
            "\n    subgraph SQLite_Data_Vault [Corporate Data Fabrics]\n"
            "        DB_HR[(HR Performance Matrix Ledger)]\n"
            "        DB_Policy[(Compliance Policy Table)]\n"
            "    end\n"
            "    DB_HR --> general_chat\n"
            "    DB_Policy --> general_chat\n"
        )
        
        # We target the specific node instantiation sequence to avoid duplicating text blocks
        if "general_chat(general_chat)" in raw_mermaid:
            enhanced_mermaid = raw_mermaid.replace("general_chat(general_chat)", f"general_chat(general_chat){db_subgraph}")
        elif "general_chat" in raw_mermaid:
            # Safe second check configuration if parentheses aren't present
            enhanced_mermaid = raw_mermaid.replace("general_chat\n", f"general_chat\n{db_subgraph}", 1)
        else:
            enhanced_mermaid = raw_mermaid

        # 2. Transmit syntax string safely to compilation engine
        print("🌐 Connecting to Mermaid engine to compile hybrid data fabrics image...")
        
        graphbytes = enhanced_mermaid.encode("utf-8")
        base64_bytes = base64.b64encode(graphbytes)
        base64_string = base64_bytes.decode("utf-8")
        
        url = f"https://mermaid.ink/img/{base64_string}"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"🎯 Success! Upgraded architecture graph successfully exported to: {os.path.abspath(output_path)}")
        else:
            raise Exception(f"Mermaid renderer returned status code: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Image generation pipeline bypassed: {e}")
        print("💡 Falling back to displaying the raw Upgraded Mermaid Syntax instead:\n")
        print("```mermaid")
        print(enhanced_mermaid)
        print("```")

if __name__ == "__main__":
    export_pipeline_graph()