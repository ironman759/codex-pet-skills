---
name: jarvis-pet-studio
description: Design a private personalized Codex pet through grounded character understanding, approved main art, action and look previews, a production idle prototype, and gated handoff to hatch-pet. Use when the user asks to make, design, personalize, or turn a character, animal, person, or original concept into a Codex pet or intelligent companion. Do not use for general animal chat, ordinary image generation, or pet-photo analysis.
---

# Jarvis Pet Studio

Design the pet with the user before invoking the full production pipeline. Visual approval is a real contract, not inspiration that later generation may ignore.

## Scope

This is a private-first workflow. It structurally accepts animals, recognizable characters, public or private people, and original characters. Treat a category as validated only after a real pilot has passed main-art approval, action preview, idle prototype, full v2 QA, installation, and live Codex use.

Use `$hatch-pet` for atlas production, deterministic processing, visual QA, repair, and packaging. Do not duplicate its scripts or animation contract here.

## Source Priority

Use this order:

1. Current user references and corrections
2. The current approved character understanding
3. Source-checked authoritative material
4. Model knowledge
5. Historical preferences

For named IP, public people, brands, or factual characters, use `$image-prompt-copilot` and complete its lightweight grounding plus bilingual prompt confirmation before generation. For a private person, do not search for them; obtain one explicit authorization per pet project before using their photos for image generation, and do not store the photos or identity in long-term memory or Jarvis Hub.

## Required Gates

Do not skip a gate for a new character.

1. **Character understanding and prompt**
   - State source interpretation, ambiguity, design axes, identity cues, simplifications, avoidances, ratio, resolution, and English plus Chinese prompt.
   - Generate nothing until the user confirms the prompt.
2. **Main art and naming**
   - Generate one recommended main design by default. Offer two only for genuine ambiguity or an explicit request.
   - Confirm display name, technical id, variant, and the identity hard lock.
3. **Action and look preview**
   - Produce one six-pose action personality board, one four-cardinal look-mechanics board, and a written action contract.
   - Add labels deterministically, never ask image generation to draw text or grids.
   - Confirm the action-semantic and look-mechanics locks.
4. **Production idle prototype**
   - Produce the final six-frame idle row, processed at real `192x208` cell size, plus a GIF.
   - Approved idle frames become part of the final atlas; do not regenerate them.
5. **Full hatch and live acceptance**
   - Hand the approved base and studio brief to `$hatch-pet`.
   - Install only after full deterministic and visual QA. Never auto-select the pet.
   - A new category is complete only after live Codex checks of idle, cardinal look, working, waiting, review, and at least one movement state.

## Studio Brief

Write one `studio-brief.json` as the design source of truth. Include:

- `source_character`
- `source_interpretation`
- `design_axes`
- `identity_lock.must_preserve`
- `identity_lock.must_not_add`
- `action_contract` keyed by Codex state
- `look_mechanics`
- `animation_energy`
- `naming` with display name, technical id, and variant
- `approvals`

Pass it with the approved main image:

```text
prepare_pet_run.py --approved-base /absolute/approved.png --studio-brief /absolute/studio-brief.json ...
```

## Autonomy And Convergence

- Main identity is hard-locked; action preview is semantic-locked; look preview is mechanics-locked. Animation interpolation may vary without changing those locks.
- Permit at most one targeted visual repair per animation row when it preserves all approved locks.
- If the same root problem fails twice, stop random retries and change strategy with the user.
- Pause for any identity, action-semantic, look-mechanics, or structural redesign.
- Keep drafts outside `~/.codex/pets`. Install only a fully approved, validated version. Back up before updating an installed version; use a new id for major redesigns.

## Retention

Preserve original Codex generations and run the user's configured generated-image archive command after each completed generation. The project keeps approved assets, representative failure evidence, decisions, final output, and QA. Do not delete original generated images even if a downstream production skill normally optimizes storage by doing so.
