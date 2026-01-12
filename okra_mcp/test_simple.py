import json
import subprocess
import os

def test_tool_call():
    # Construct a valid JSON-RPC request for tools/call
    req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "resolve_selector",
            "arguments": {
                "element_name": "link",
                "target_text": "Active Patient Check"
            }
        }
    }
    
    # Run server.py as a subprocess
    path = os.path.join(os.path.dirname(__file__), "server.py")
    process = subprocess.Popen(
        ["python3", path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print(f"Sending: {json.dumps(req)}")
    stdout, stderr = process.communicate(input=json.dumps(req) + "\n")
    
    print("--- Server Output ---")
    print(stdout)
    
    if stderr:
        print("--- Server Stderr ---")
        print(stderr)
        
    try:
        resp = json.loads(stdout)
        print("\n--- Parsed Result ---")
        content = resp["result"]["content"][0]["text"]
        print(content)
        if "Active Patient Check" in content:
            print("\nSUCCESS: Server resolved the selector correctly.")
        else:
            print("\nFAILURE: Response did not contain expected text.")
    except Exception as e:
        print(f"\nFAILURE: Could not parse response: {e}")

if __name__ == "__main__":
    test_tool_call()
