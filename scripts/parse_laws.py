import re
import json


def parse_law(file_path):
    chunks = []
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    matches = re.findall(r"(第[一二三四五六七八九十百]+条)[　\s]*(.*?)(?=第[一二三四五六七八九十百]+条|$)", text, re.DOTALL)

    for article_number,content in matches:
        chunk = {
            "law_name": "劳动合同法",
            "article_number": article_number,
            "content": content.strip(),
            "effective_date": "2012-12-28"
        }
        chunks.append(chunk)
    return chunks
    
