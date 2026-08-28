"""Product-quality roadmap for turning the study prototype into a sellable SIE prep product.
Research basis: official FINRA blueprint for scope/weighting; learning-science evidence for retrieval,
spacing and interleaving; competitor research for expected product features. Competitor marketing
claims are not treated as evidence of pass rates or instructional superiority.
"""
PRODUCT_GATES=[
("Content integrity","Every tested objective maps to the current FINRA outline and an internal source record; no copied proprietary questions."),
("Question quality","Large bank of genuinely unique, expert-reviewed items with plausible same-domain distractors and explanations for every option."),
("Learning science","Retrieval practice, spaced review, interleaving, confidence calibration and targeted remediation are core behavior, not add-ons."),
("Readiness validity","Readiness score uses recent unseen weighted performance, confidence and objective coverage; never market an unsupported pass probability."),
("Mobile UX","Responsive one-question-at-a-time test mode, resume state, fast navigation, accessibility, low-friction onboarding and offline-capable architecture before app-store launch."),
("Commercial readiness","Accounts, cloud persistence, subscriptions/entitlements, privacy policy, terms, support workflow, analytics/telemetry, crash reporting and content-version controls."),
]

NEXT_FEATURES=[
{"feature":"Objective-level mastery graph","priority":"P0","why":"Chapter scores are too coarse. Track each FINRA objective/concept separately and weight by blueprint importance."},
{"feature":"Spaced review queue","priority":"P0","why":"Schedule weak/uncertain concepts for later retrieval instead of immediately repeating them."},
{"feature":"Interleaved mixed drills","priority":"P0","why":"Mix similar concepts so the learner must discriminate between them rather than rely on chapter context."},
{"feature":"Option-by-option explanations","priority":"P0","why":"A premium bank should explain why the right answer wins and why each distractor fails."},
{"feature":"Question provenance/versioning","priority":"P0","why":"Each item needs objective ID, source basis, author/reviewer status, difficulty, last review date and version."},
{"feature":"Timed exam simulation","priority":"P0","why":"Replicate official exam pacing and remove immediate feedback during simulation mode."},
{"feature":"Diagnostic onboarding exam","priority":"P1","why":"Start users at an appropriate depth and create a personalized study plan."},
{"feature":"Daily study prescription","priority":"P1","why":"Turn mastery data into a concrete 15/30/60-minute daily queue."},
{"feature":"Offline/mobile persistence","priority":"P1","why":"Commercial competitors support convenient mobile study; users should not lose progress between sessions."},
{"feature":"Content QA dashboard","priority":"P1","why":"Flag ambiguous items, over-easy distractors, abnormal miss rates, duplicates and stale regulatory content."},
{"feature":"Audio/micro-lessons","priority":"P2","why":"Useful alternate study mode after core content/question quality is commercially defensible."},
]

READINESS_MODEL={
"weighted_recent_exam":0.45,
"objective_mastery":0.30,
"confidence_calibration":0.15,
"coverage":0.10,
"rule":"Only count unseen or sufficiently spaced questions toward readiness. Guessed-correct answers do not count as full mastery."
}
