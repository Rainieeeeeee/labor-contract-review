from scripts.retriever import retrieve
from scripts.analyzer import analyze
from scripts.parse_laws import parse_law

def run_analysis(file_path):
    clauses = parse_law(file_path)
    results = []
    for clause in clauses:
        res = retrieve(clause["content"], n_results=3)
        law_articles = [
            {"article_number":m["article_number"], "content":d}
            for d, m in zip(res["documents"][0],res["metadatas"][0])
        ]
        result = analyze(clause, law_articles)
        results.append(result)
    return results