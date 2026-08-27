# Accelerated SIE Exam

URL-based Streamlit training application for accelerated Securities Industry Essentials (SIE) preparation.

## Training flow

**CliffNotes → Flashcards → Rapid Drill → Full Simulation → Remediation → Readiness**

## Full exam engine

- 75 scored-style questions per simulation
- FINRA/STC outline weighting: 12 Capital Markets, 33 Products & Risks, 23 Trading/Accounts/Prohibited Activities, 7 Regulatory Framework
- Every question family has alternate stems
- Consecutive full exams alternate the stem for every family, giving **100% different question wording from the immediately prior full exam**
- Answer choices are independently reshuffled
- Every answer includes an explanation during review
- Missed questions feed the remediation screen
- Score history and domain-level performance are tracked during the session

The questions are original training questions aligned to the concepts and weighting in the SIE study materials. They are not copied from, claimed to be, or reconstructed from live FINRA exam questions.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Go to Streamlit Community Cloud.
2. Create a new app from `cjhaake1-commits/accelerated-sie-exam`.
3. Branch: `main`.
4. Entry point: `app.py`.
5. Deploy.

## Study target

The actual SIE passing score is 70%. The app uses 85%+ repeated practice performance as a conservative readiness target, not a guarantee of passing.
