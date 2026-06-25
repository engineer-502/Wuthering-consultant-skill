# Example Gallery

These examples are validator fixtures and model-facing references for common user requests.

| File | User request shape | Purpose |
|---|---|---|
| `sample_consultation.json` | “루실라 세팅 봐줘” | Default build consultation schema. |
| `build_lucilla.json` | Character build advice | Confirms role/source-backed recommendations. |
| `pull_advice_cartethyia.json` | “카르테시아 뽑을까?” | Pull advice with opportunity-cost language. |
| `account_progression.json` | “계정 성장 순서 알려줘” | Account planning with Union/Data Bank state. |
| `report_mode_metadata.json` | “이미지 리포트로 만들어줘” | Visual artifact metadata contract. |
| `low_confidence_extraction.json` | Blurry screenshot | `needs_confirmation` extraction behavior. |
| `invalid/missing_sources.json` | Bad current-meta claim | Must fail validation. |
| `invalid/bad_confidence.json` | Bad confidence label | Must fail validation. |

When adding examples, include at least one official/reference source and a recommendation rationale.
