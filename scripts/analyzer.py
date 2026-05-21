from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze(clause, law_articles):
    law_text = "\n".join([
        f"{a['article_number']}: {a['content']}"
        for a in law_articles

    ])

    prompt = f"""你是一位中国劳动法专家。请分析以下合同条款是否存在法律风险。

【合同条款】
{clause['article_number']}: {clause['content']}

【相关法条】
{law_text}

请用JSON格式输出分析结果，包含以下字段：
- risk_level: 风险等级（高/中/低/无）
- risk_description: 风险描述
- violated_articles: 违反的法条列表
- suggestion: 建议

如果合同条款中的数字明确超出法条规定的上限，risk_level 必须为"高"，不得为"低"或"无"。
请逐条对照相关法条，明确计算合同条款中的数字是否超出法条规定的上限。例如：合同期限一年，对应试用期上限为两个月，若合同约定超过两个月则为高风险。



只输出JSON，不要其他文字。"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content
    content = content.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(content)

