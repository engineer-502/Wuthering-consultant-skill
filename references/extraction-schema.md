# Extraction Schema — Wuthering Waves Screenshot Consulting

Use this schema as the working object. Keep unknown values explicit.

```json
{
  "game": "Wuthering Waves",
  "language": "ko",
  "consultation_type": "build|account|pull|rotation|report",
  "input_images": [
    {"display_role":"resonator-detail|weapon|echo|roster|inventory|tower|other", "display_path":"/abs/path", "status":"rendered|missing|unreadable"}
  ],
  "account": {
    "union_level": {"value": null, "confidence":"needs_confirmation"},
    "data_bank_level": {"value": null, "confidence":"needs_confirmation"},
    "astrite": null,
    "tides": {"radiant": null, "forging": null, "lustrous": null, "dreamcatcher": null, "shadowforge": null},
    "endgame_progress": {"tower": null, "endstate_matrix": null}
  },
  "resonators": [
    {
      "name": "Lucilla",
      "attribute": "Glacio",
      "weapon_type": "Rectifier",
      "level": null,
      "sequence": null,
      "skills": {"basic": null, "skill": null, "forte": null, "liberation": null, "intro": null},
      "stats": {"hp": null, "atk": null, "def": null, "crit_rate": null, "crit_dmg": null, "energy_regen": null, "attribute_bonus": null, "healing_bonus": null},
      "weapon": {"name": null, "level": null, "rank": null, "confidence":"needs_confirmation"},
      "echoes": [
        {"slot":1, "cost":4, "name": null, "sonata": null, "level": null, "main_stat": null, "substats": [], "tuned": null, "confidence":"needs_confirmation"}
      ],
      "notes": []
    }
  ],
  "sources": [],
  "visual_artifacts": []
}
```

Confidence labels must be exactly `confirmed`, `inferred`, or `needs_confirmation`.
