# Wuthering Consultant Skill

Codex skill for Korean Wuthering Waves / 명조 account consulting. It helps with resonator builds, weapons, echoes, sonata sets, team composition, rotation coaching, pull advice, and optional local visual cards using bundled assets.

## Install

Clone this repository into your Codex skills directory:

### Windows PowerShell

```powershell
git clone https://github.com/engineer-502/Wuthering-consultant-skill.git "$env:USERPROFILE\.codex\skills\wuthering-consultant"
```

### macOS / Linux

```bash
git clone https://github.com/engineer-502/Wuthering-consultant-skill.git ~/.codex/skills/wuthering-consultant
```

Restart Codex after installing if the skill list was already loaded.

## Use

Mention the skill in a prompt:

```text
$wuthering-consultant 양양 추천 파티랑 무기, 에코 알려줘
```

You can also attach screenshots of resonators, weapons, echoes, roster, inventory, or endgame progress. The skill is written to answer in Korean by default.

## Included

- `SKILL.md`: main skill instructions
- `agents/`: helper agent prompts
- `references/`: consulting references and extraction schemas
- `scripts/`: cache lookup, card rendering, validation, and smoke tests
- `data/` and `assets/`: local Wuthering Waves asset metadata and PNG images
- `examples/`: sample requests and outputs

## Verify

From the skill directory:

```powershell
python scripts\validate_seed.py data\seed\wuwa_official_3_4_seed.json
python scripts\run_smoke_tests.py
```

On macOS / Linux:

```bash
python scripts/validate_seed.py data/seed/wuwa_official_3_4_seed.json
python scripts/run_smoke_tests.py
```

## Privacy Notes

This repository is intended for public installation. It should not contain personal account screenshots, local user paths, API keys, tokens, or Codex private runtime folders.
