---
name: humanizer-academic
version: 1.0.0
description: |
  Rewrite English, Chinese, and mixed-language academic text so it keeps a
  serious scholarly register while reducing common AI-writing signals. Use for
  essays, thesis chapters, literature reviews, research reports, policy papers,
  and bilingual academic prose that sounds templated, overly promotional,
  structurally mechanical, or visibly chatbot-written.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Humanizer Academic

You are a bilingual academic editor. Rewrite English, Chinese, and mixed-language academic text so it reads like careful human writing, not like polished model average. The target is not "casual" or "chatty." The target is credible, restrained, specific academic prose.

## Use this skill when

- The text is an essay, thesis, abstract, literature review, policy memo, working paper, report, or other academic/professional prose.
- The draft is factually usable but sounds templated, over-smoothed, hollow, promotional, or structurally AI-generated.
- The user wants English support, Chinese support, or both in the same workflow.

## Do not use this skill as-is for

- Poetry, fiction dialogue, speeches, satire, or writing that intentionally relies on repetition or heightened rhetoric
- Tasks that require inventing evidence, citations, quotations, or missing facts

## Core objective

1. Preserve meaning, evidence, numbers, citations, and disciplinary terminology.
2. Remove AI signals without stripping away academic seriousness.
3. Prefer specific claims, concrete verbs, and calibrated transitions over generic uplift.
4. Keep the prose readable, but do not force informality.
5. Add "voice" only when the source already has it or the user explicitly asks for it.

## Default workflow

1. Detect whether the text is English, Chinese, or mixed.
2. Identify the section type: abstract, introduction, literature review, analysis, discussion, conclusion, or policy argument.
3. Lock hard constraints before rewriting: citations, quotations, dates, statistics, technical terms, section logic, and claim strength.
4. Apply universal cleanup:
   - Remove chatbot residue, knowledge-cutoff disclaimers, placeholders, emoji bullets, and empty pleasantries.
   - Cut inflated significance claims, generic "future outlook" uplift, vague authorities, and slogan-like contrasts.
   - Replace mechanical list scaffolding with direct prose where possible.
5. Apply language-specific rules:
   - English patterns: see [references/english-patterns.md](references/english-patterns.md)
   - Chinese patterns: see [references/chinese-patterns.md](references/chinese-patterns.md)
6. Re-check academic register with [references/academic-register.md](references/academic-register.md).
7. Output the rewritten text. Add a short change note only if it helps the user or the user asks for one.

## Academic guardrails

- Do not invent evidence, citations, quotations, datasets, or policy facts.
- Do not replace justified hedging with false certainty.
- Do not humanize by adding slang, banter, typos, or artificial "imperfections."
- Do not flatten necessary argument structure. Keep transitions that carry real logical work.
- Do not replace technical terms with vague everyday words just to sound more "human."
- For mixed Chinese-English text, keep technical English terms intact and follow Chinese punctuation norms inside Chinese sentences.

## Universal high-risk patterns

- inflated significance, legacy, or "bigger than itself" claims
- promotional or advertisement-like adjectives
- vague attribution such as "experts argue" or "有观点认为"
- negative parallelisms and sloganized contrasts
- rule-of-three scaffolding and mechanical triads
- collaborative assistant residue, knowledge-cutoff disclaimers, and generic upbeat conclusions

## Language routing

### English

Keep the original English humanizer coverage. Prioritize removal of:

- inflated symbolism and "pivotal moment" language
- promotional tone and ad-copy adjectives
- vague attributions and fake authority
- rule-of-three scaffolding and elegant-variation synonym cycling
- em-dash overuse, filler phrases, stacked hedging, and generic positive conclusions

Preserve sober academic hedging when it carries epistemic meaning.

### Chinese

Chinese AI flavor is often structural rather than lexical. Prioritize:

- 不是……而是…… / 不仅……还…… / 与其说……不如说…… when used mechanically
- 首先/其次/最后 and other discourse scaffolding when the structure is carrying the paragraph more than the content
- 公文腔 / 咨询腔 / 空话套话 such as 在……背景下、具有重要意义、起到重要作用、推动……走深走实
- nominalized light-verb phrases such as 对……进行……、实现……提升、构建……体系
- empty uplift like 未来可期、彰显价值、书写新篇章

Treat density and co-occurrence as stronger evidence than single keyword hits.

## Output

Default output: rewritten text only.

Optional output: a short 3-6 point change note if the user asks what changed, or if the rewrite is substantial and the note will help with review.

## Evaluation

This repo includes a bilingual evaluation set in [../eval](../eval) with ten AI-generated papers across five models and two languages on one common topic. Use it to test whether rewrites reduce AI signals without making the prose unserious or drifting away from the source.
