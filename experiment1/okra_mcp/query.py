import sys
import json
import subprocess
import os

def call_mcp(tool_name, args):
    # Prepare the JSON-RPC request
    req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": args
        }
    }
    
    # Run the server as a subprocess
    server_path = os.path.join(os.path.dirname(__file__), "server.py")
    
    process = subprocess.Popen(
        ["python3", server_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Send request and get response
    stdout, stderr = process.communicate(input=json.dumps(req) + "\n")
    
    if stderr:
        # Filter out random logs if any, but show errors
        pass

    try:
        resp = json.loads(stdout)
        if "result" in resp and "content" in resp["result"]:
            print(resp["result"]["content"][0]["text"])
        else:
            print("Error parsing MCP response:", stdout)
    except Exception as e:
        print(f"Failed to communicate with server: {e}\nRaw Output: {stdout}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 query.py <command> [args...]")
        return

    command = sys.argv[1]
    
    if command == "resolve":
        # usage: resolve link "Active Patient Check"
        if len(sys.argv) < 4:
            print("Usage: resolve <element_name> <target_text>")
            return
        call_mcp("resolve_selector", {"element_name": sys.argv[2], "target_text": sys.argv[3]})
        
    elif command == "explain":
        # usage: explain "Click the 'Foo' link"
        if len(sys.argv) < 3:
            print("Usage: explain <full_okra_line>")
            return
        line = " ".join(sys.argv[2:]) # Rejoin just in case
        call_mcp("explain_okra_line", {"line": line})
        
    elif command == "def":
        # usage: def link
        if len(sys.argv) < 3:
            print("Usage: def <element_name>")
            return
        call_mcp("get_element_definition", {"element_name": sys.argv[2]})

    elif command == "convert":
        # usage: convert 'Click the "Active Patient Check" link'
        if len(sys.argv) < 3:
            print("Usage: convert <full_okra_line>")
            return
        
        line = " ".join(sys.argv[2:])
        # Simple regex to extract parts for the demo
        import re
        m = re.search(r'(Click|Verify exists|Enter)\s+(?:the\s+)?(?:"([^"]+)"\s+)?(\w+)', line, re.IGNORECASE)
        if m:
            action, text, element = m.groups()
            print(f"# Converting: {line}")
            
            # 1. Resolve selector via MCP
            sel_args = {"element_name": element, "target_text": text if text else ""}
            
            # We need to capture the output, so we'll duplicate call_mcp logic slightly or refactor. 
            # For brevity, let's just run the subprocess again for the resolve call.
            
            req = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "resolve_selector", "arguments": sel_args}}
            server_path = os.path.join(os.path.dirname(__file__), "server.py")
            process = subprocess.Popen(["python3", server_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
            out, _ = process.communicate(input=json.dumps(req) + "\n")
            
            try:
                res = json.loads(out)
                xpath_raw = res["result"]["content"][0]["text"]
                # Extract just the first line of the xpath for the code snippet
                xpath = xpath_raw.splitlines()[1].strip() if "Resolved Selectors" in xpath_raw else xpath_raw
                
                # 2. Generate Playwright Code
                if action.lower() == "click":
                    print(f"page.locator('{xpath}').click()")
                elif "verify" in action.lower():
                    print(f"expect(page.locator('{xpath}')).to_be_visible()")
                
            except Exception as e:
                print(f"Error fetching selector: {e}")
        else:
             print("Could not parse line locally. Try: convert 'Click the \"Save\" button'")
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
