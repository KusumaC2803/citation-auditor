from backend.answer_generator import generate_answer


question = "What is the objective of the sleep disorder prediction project?"

result = generate_answer(question)

print("\nQUESTION:")
print(result["question"])

print("\nANSWER:")
print(result["answer"])

print("\nSOURCES:")

for source in result["sources"]:
    print("\n----------------------------")
    print("Citation:", f'[{source["chunk_id"]}, Page {source["page"]}]')
    print("Evidence:", source["text"])