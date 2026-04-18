from app.tools.tools import web_search_tool
import sys

print("Testing web_search_tool...")
try:
    result = web_search_tool.invoke({"query": "Claude code new achievements 2026"})
    print("Result obtained!")
    print("Length:", len(str(result)))
    print(str(result)[:500])
except Exception as e:
    print("Error:", e)

sys.exit(0)
