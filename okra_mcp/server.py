import sys
import json
import os
import re
import traceback
from pod_loader import PodLoader

# Configuration
# Assuming server.py is in okra_mcp/ and okrapods/ is in parent
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PODS_DIR = os.path.join(WORKSPACE_ROOT, 'okrapods')
GENERATED_TESTS_DIR = os.path.join(WORKSPACE_ROOT, 'generated_tests')

# Initialize Logic
loader = PodLoader(PODS_DIR)

def get_element_definition(element_name: str) -> str:
    """
    Look up the exact definition of an Okra element (e.g. 'link', 'field', 'checkbox').
    Returns the XPath or CSS selectors defined in the .pod files.
    """
    defn = loader.get_element(element_name)
    if defn:
        return f"Definition for '{element_name}':\n{defn}"
    else:
        # Try fuzzy search
        matches = loader.search_elements(element_name)
        if matches:
            return f"Element '{element_name}' not found. Did you mean: {', '.join(matches[:5])}?"
        return f"Element '{element_name}' not found in loaded pods."

def resolve_selector(element_name: str, target_text: str) -> str:
    """
    Takes an element name (e.g. 'link') and the target text (e.g. 'Active Patient Check')
    and returns the resolved XPath/CSS with placeholders replaced.
    """
    defn = loader.get_element(element_name)
    if not defn:
        return f"Error: Element '{element_name}' not found."

    # Logic to replace {OKRA_TEXT} and {OKRA_TEXT_CLS}
    resolved = defn.replace("{OKRA_TEXT}", target_text)
    text_cls_xpath = f'[contains(normalize-space(.), "{target_text}")]'
    resolved = resolved.replace("{OKRA_TEXT_CLS}", text_cls_xpath)

    return f"Resolved Selectors for '{element_name}' with text '{target_text}':\n{resolved}"

def explain_okra_line(line: str) -> str:
    """
    Analyzes a line of Okra code and explains how it maps to underlying pods.
    Example input: 'Click the "Active Patient Check" link'
    """
    m = re.search(r'(Click|Verify|Enter)\s+(?:the\s+)?(?:"([^"]+)"\s+)?(\w+)$', line.strip(), re.IGNORECASE)
    
    if m:
        action = m.group(1)
        text = m.group(2)
        element = m.group(3)
        
        info = []
        info.append(f"Action: {action}")
        if text:
            info.append(f"Target Text: {text}")
        info.append(f"Element Type: {element}")
        
        defn = loader.get_element(element)
        if defn:
            info.append(f"\nUnderlying Definition for '{element}':\n{defn}")
        else:
            info.append(f"\nWarning: Element '{element}' not defined in pods.")
            
        return "\n".join(info)
    
    return "Could not parse line structure. Expected format: Action \"Text\" Element"

def save_generated_test(filename: str, content: str) -> str:
    """
    Saves generated test code to the generated_tests directory.
    """
    if not os.path.exists(GENERATED_TESTS_DIR):
        os.makedirs(GENERATED_TESTS_DIR)
        
    if not filename.endswith('.py'):
        filename += '.py'
        
    file_path = os.path.join(GENERATED_TESTS_DIR, filename)
    
    with open(file_path, "w") as f:
        f.write(content)
        
    return f"Successfully saved test to: {file_path}"

# --- Minimal Dependency-Free MCP Server ---

TOOLS = [
    {
        "name": "get_element_definition",
        "description": "Look up the exact definition of an Okra element. Returns the XPath.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "element_name": {"type": "string", "description": "The name of the element (e.g. 'link')"}
            },
            "required": ["element_name"]
        }
    },
    {
        "name": "resolve_selector",
        "description": "Get a ready-to-use XPath/Selector for a specific element and text.",
        "inputSchema": {
            "type": "object",
     ,
    {
        "name": "save_generated_test",
        "description": "Saves a generated Playwright test script to the dedicated 'generated_tests' folder.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "The filename (e.g. test_login.py)"},
                "content": {"type": "string", "description": "The full Python code content"}
            },
            "required": ["filename", "content"]
        }
    }       "properties": {
                "element_name": {"type": "string", "description": "element type (e.g. 'link')"},
                "target_text": {"type": "string", "description": "visible text (e.g. 'Save')"}
            },
            "required": ["element_name", "target_text"]
        }
    },
    {
        "name": "explain_okra_line",
        "description": "Analyzes a line of Okra code and explains variables and selectors.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "line": {"type": "string", "description": "The full line of code"}
            },
            "required": ["line"]
        }
    }
]

def handle_request(request):
    method = request.get("method")
    
    if method == "initialize":
        return {
            "protocolVersion": "2024-11-05", # Dummy version
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "okra_mcp",
                "version": "1.0.0"
            }
        }
    
    if method == "notifications/initialized":
        return None # No response needed
        
    if method == "tools/list":
        return {
            "tools": TOOLS
        }
        
    if method == "tools/call":
        params = request.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {})
        
        # Log if name == "save_generated_test":
                result_text = save_generated_test(args.get("filename"), args.get("content"))
            elfor debug
        with open("server.log", "a") as log:
            log.write(f"Calling {name} with {args}\n")

        result_text = ""
        try:
            if name == "get_element_definition":
                result_text = get_element_definition(args.get("element_name"))
            elif name == "resolve_selector":
                result_text = resolve_selector(args.get("element_name"), args.get("target_text"))
            elif name == "explain_okra_line":
                result_text = explain_okra_line(args.get("line"))
            else:
                raise ValueError(f"Unknown tool: {name}")
                
            return {
                "content": [
                    {
                        "type": "text",
                        "text": str(result_text)
                    }
                ]
            }
        except Exception as e:
            with open("server.log", "a") as log:
                log.write(f"Error: {e}\n")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error executing tool {name}: {str(e)}"
                    }
                ],
                "isError": True
            }

    return None

def main():
    # Use unbuffered stdin/stdout via sys
    stdin = sys.stdin
    stdout = sys.stdout
    
    # Simple logging
    with open("server.log", "w") as f:
        f.write(f"Server started. Loaded {len(loader.elements)} elements from {PODS_DIR}\n")

    while True:
        try:
            line = stdin.readline()
            if not line:
                break
            
            request = json.loads(line)
            response_data = handle_request(request)
            
            # Responses vary by request type
            # Initialize, tools/list, tools/call require responses with IDs
            if response_data is not None:
                response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": response_data
                }
                stdout.write(json.dumps(response) + "\n")
                stdout.flush()
                
        except Exception as e:
            # Don't crash the server, just log
            with open("server.log", "a") as f:
                f.write(f"Loop Exception: {e}\n")
            continue

if __name__ == "__main__":
    main()
