"""Exam-aligned training blueprint.
FINRA scored SIE weighting: Capital Markets 12/75; Products & Risks 33/75;
Trading/Accounts/Prohibited Activities 23/75; Regulatory Framework 7/75.
Training blocks should not manufacture 50 superficially different items when the underlying
concept inventory is smaller. Quality and blueprint coverage take priority over raw count.
"""
SECTION_WEIGHTS={"Capital Markets":12,"Products & Risks":33,"Trading, Accounts & Prohibited Activities":23,"Regulatory Framework":7}

# Hard-mode item-writing rules used as acceptance criteria for future banks.
ITEM_RULES=[
"Test a decision, consequence, comparison, exception, sequence, calculation, or rule application whenever the source supports it.",
"All four options must be plausible in the same conceptual neighborhood; avoid joke answers and category mismatches.",
"At least two distractors should represent realistic mistakes a prepared candidate could make.",
"Do not create multiple scored items by merely adding a prefix or paraphrasing the same fact pattern.",
"Use BEST/MOST/EXCEPT/NOT only when the distinction is supported by the curriculum and does not create ambiguity.",
"Mix short direct items with multi-step scenarios; difficulty should come from distinctions and reasoning, not needless verbosity.",
"Math items should require identifying the correct inputs/formula before arithmetic, not simply plugging numbers into a named formula.",
"Explanations must state why the correct option wins and, for close distractors, why they fail.",
]

# Block exams are capped until enough genuinely distinct source-grounded items exist.
# A smaller high-quality exam is preferable to forced repetition.
BLOCK_TARGETS={1:35,2:40,3:40,4:35}
MIN_UNIQUE_CONCEPTS_PER_BLOCK={1:25,2:30,3:30,4:25}
