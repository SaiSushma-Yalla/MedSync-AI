from agents.extract_node import extract_report_node


state = {
    "pdf": "test.pdf"
}


result = extract_report_node(state)


print("\n========== FINAL STATE ==========\n")

print(result)