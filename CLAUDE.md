# AI Labor Contract Review — Claude 工作手册

## 项目简介
RAG-based 中文劳动合同风险分析系统。用户上传合同 PDF，系统逐条款提取、检索相关劳动法条、分析风险、输出结构化报告。

**核心亮点：** 用 RAG grounding 防止 LLM 法律幻觉，每条风险结论都有真实法条引用支撑。

## 技术栈
- Backend: Python, FastAPI
- AI: OpenAI (embedding: text-embedding-3-small, LLM: gpt-4o-mini)
- Vector DB: Chroma (MVP) → pgvector (V1)
- Frontend: React + Next.js + Tailwind
- Infra: Docker

## 环境
```bash
cd /Users/ruirui/Desktop/labor-contract-review
source venv/bin/activate   # 每次开新终端都要激活虚拟环境
```

## 文件说明（快速上手）
```
scripts/parse_laws.py   — 解析法条/合同，按"第X条"切分
scripts/build_index.py  — embed法条 + 存入Chroma向量库
scripts/retriever.py    — 接收文字 → embed → Chroma搜索 → 返回3条法条
scripts/analyzer.py     — 接收条款+法条 → LLM分析 → 返回JSON
scripts/run_analysis.py — 串联以上四个，分析整份合同
app/api/routes.py       — FastAPI路由，POST /analyze接口
main.py                 — 启动服务器入口
```

## 指导原则
- **不直接给代码**，引导 Rainie 自己写，在她能理解的范围内让她动手
- 遇到不懂的概念要解释清楚，可以用 Java 类比
- 每完成一个模块，输出面试材料：填空模板 + 高频词表 + 背诵句子（格式参考截图）
- 遇到问题记录到 `/Users/ruirui/Desktop/job-search/progress/python-questions.md`
- 面试材料记录到 `/Users/ruirui/Desktop/job-search/progress/ai-contract-interview-prep.md`
- 每次 session 结束更新本文件进度
- Rainie 问过的所有问题都要记录，方便复习

---

## 当前进度

### ✅ Phase 0 — 知识库 & 项目结构

- [x] 建项目目录结构
- [x] requirements.txt + venv 虚拟环境
- [x] .env（OPENAI_API_KEY）+ .gitignore
- [x] 法条原文：`data/laws/中华人民共和国劳动合同法_20121228.txt`
- [x] `scripts/parse_laws.py` — 解析法条，按"第X条"切分，返回 chunk list
- [x] `scripts/build_index.py` — embed 每条法条 + 存入 Chroma（98条）
- [x] 验证检索质量：查询"试用期工资"返回第二十条、第八十三条，语义搜索正确

### ✅ Phase 1 — 核心 Pipeline
- [x] 条款提取：`parse_law` 复用，提取合同9条条款
- [x] RAG 检索模块：`scripts/retriever.py` — 条款 embed → Chroma 搜索 → 返回3条法条
- [x] 风险分析：`scripts/analyzer.py` — LLM 对照法条分析，输出结构化 JSON
- [x] 端到端验证：`scripts/run_analysis.py` — 9条全部分析完成，风险识别准确
- [ ] 待优化：第二条试用期风险漏检，检索法条不够准确

### ✅ Phase 2 — FastAPI 封装
- [x] POST /analyze 接口 — 上传合同文件，返回9条风险分析 JSON
- [x] 文件上传处理（UploadFile + 临时文件）
- [x] Swagger UI 自动生成，可直接测试
- [ ] GET /result/{job_id} 接口（异步任务，暂缓）

### ✅ Phase 3 — 前端
- [x] React 上传页面（文件选择 + 提交按钮）
- [x] 风险报告展示页（高/中/低风险颜色区分）
- [x] 前后端联调成功（CORS 配置）

---

## Chunk Schema
```python
{
    "law_name":       "劳动合同法",
    "article_number": "第十七条",
    "content":        "劳动合同应当具备以下条款...",
    "effective_date": "2012-12-28",
}
```

## 文件结构
```
labor-contract-review/
├── app/
│   ├── api/        # FastAPI 路由（Phase 2）
│   ├── core/       # 配置、依赖注入
│   ├── models/     # Pydantic 数据模型
│   └── services/   # 业务逻辑（RAG、分析）
├── data/
│   └── laws/       # 法条原文 txt 文件
├── scripts/
│   ├── parse_laws.py    # ✅ 解析法条 → chunk list
│   └── build_index.py   # 下一步：embed + 存 Chroma
├── tests/
├── .env            # OPENAI_API_KEY（不上传 git）
├── .gitignore
└── requirements.txt
```
