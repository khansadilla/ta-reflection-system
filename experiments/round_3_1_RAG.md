# Round 3.1 — Stage-Aware Lightweight RAG (TF-IDF)

## Objective
Improve reasoning depth via stage-aware knowledge retrieval.

## Implementation
- Replaced static knowledge injection with TF-IDF cosine similarity retrieval.
- Retrieval limited to stage-specific knowledge.
- Top-k = 2.

## Evaluation
Direct reasoning tests (n=5):

Non-generic reasoning questions: 5 / 5

Questions demonstrated:
- Factor differentiation
- Perspective framing
- Root-cause probing
- Conceptual categorization

## Conclusion
Stage-aware lightweight retrieval improves reasoning depth without increasing architectural complexity.

System frozen for Week 3 Round 1.