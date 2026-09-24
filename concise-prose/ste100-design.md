# STE100 writing sub-skill

## Scope and behavior

The sub-skill guides a model to write good STE100-style prose before `prose-check` runs. It applies when a user requests STE100 writing or review. It preserves technical meaning, requirements, conditions, obligations, and established terminology. If a writing change would alter these, the model reports the conflict.

The skill is self-contained. It does not direct routine work to a source document and does not reproduce a reference manual. It covers general writing, procedures, descriptions, safety instructions, and review. `prose-check` remains the deterministic authority for vocabulary and mechanically checkable rules.

## Approach and acceptance

Update `concise-prose/ste100/SKILL.md` with sections for meaning, general rules, procedures, descriptions, safety, and checking. Keep the parent skill's route to it. Add no code or dependencies.

Confirm that each requested behavior appears in the skill, no source or rule citations remain, the skill validates, and Vale reports no findings. The checker may flag vocabulary in the skill instructions themselves; that is not a test of the generated guidance.
