# STE100 writing sub-skill

## Scope and behavior

The sub-skill guides a model to write good STE100-style prose before `prose-check` runs. It is the language foundation for all model-authored prose and for the general `concise-prose` skill. It preserves technical meaning, requirements, conditions, obligations, and established terminology. If a writing change would alter these, the model reports the conflict.

The skill is self-contained. It does not direct routine work to a source document and does not reproduce a reference manual. It covers general writing, procedures, descriptions, and safety instructions. `concise-prose` owns the instruction to run `prose-check`; the checker remains the deterministic authority for vocabulary and mechanically checkable rules.

## Approach and acceptance

Keep `concise-prose/ste100/SKILL.md` focused on language guidance. Make its description show that other skills use it. Keep the general skill's unconditional route to it and its scope across documents, source documentation comments, and commit messages.

Confirm that each requested behavior appears in the skill, no source or rule citations remain, the skill validates, and Vale reports no findings. The checker may flag vocabulary in the skill instructions themselves; that is not a test of the generated guidance.
