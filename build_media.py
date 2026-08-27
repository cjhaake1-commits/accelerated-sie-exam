import asyncio
from pathlib import Path
import edge_tts
from question_bank import QUESTION_FAMILIES, FLASHCARDS, CLIFF_NOTES

OUT = Path('assets')
OUT.mkdir(exist_ok=True)


def build_script():
    parts = []
    parts.append("Welcome to the Accelerated SIE day-off review. This is designed for passive reinforcement after you have already done active study. Listen while walking, driving, exercising, or doing chores. The goal is recognition: hear a key phrase and connect it immediately to the rule, product, risk, or prohibited practice. We will move through the exam in the same four-part structure used by the SIE outline: capital markets, products and risks, trading and customer accounts, and the regulatory framework. Products and risks plus trading, accounts and prohibited activities make up most of the scored exam, so those areas receive the most repetition. Do not try to memorize every sentence. Listen for the trigger words and relationships.")
    for domain in ["Capital Markets", "Products & Risks", "Trading, Accounts & Prohibited Activities", "Regulatory Framework"]:
        parts.append(f"Now, {domain}.")
        for note in CLIFF_NOTES[domain]:
            parts.append(note)
            parts.append("Remember that relationship. Pause mentally and say it back in your own words.")
    parts.append("Now we move into rapid buzzword recall. I will say a term, then the rule. Try to answer before I finish.")
    for term, definition in FLASHCARDS:
        parts.append(f"Quick check. {term}. What does it mean? {definition} Say it once more: {term}. {definition}")
    parts.append("Now we reinforce the exam through question-family explanations. Do not focus on the exact wording of a question. Focus on the concept that makes the answer correct.")
    for i, q in enumerate(QUESTION_FAMILIES, 1):
        parts.append(f"Concept {i}. {q['q1']} The correct answer is {q['a']}. {q['e']}")
        parts.append(f"Same concept, different wording. {q['q2']} Again, the answer is {q['a']}. {q['e']}")
        if i % 10 == 0:
            parts.append("Checkpoint. If any of the last concepts felt unfamiliar, mark that topic for a rapid drill later. Keep moving.")
    parts.append("Final high-yield lightning round. Nineteen thirty-three means new issues, primary market, prospectus and full disclosure. Nineteen thirty-four means secondary trading, the SEC, antifraud and margin regulation. Broker means agent and commission. Dealer means principal and markup or markdown. Bid is the dealer buy price. Ask is the dealer sell price. Stock means ownership. Bond means creditor. Rates up, bond prices down. Rates down, bond prices up. General obligation municipal bond means taxes. Revenue bond means project revenues. Call means right to buy. Put means right to sell. Option buyer has a right and pays the premium. Option writer has an obligation and receives the premium. Market order prioritizes execution. Limit order prioritizes price. A stop becomes a market order when triggered. Most equities settle T plus one. Systematic risk cannot be diversified away. Nonsystematic risk can be reduced by diversification. Regulation Best Interest means the retail customer's best interest. C I P verifies identity. C T R generally means cash over ten thousand dollars. S A R means suspicious activity reporting. Churning is excessive trading. Front running is trading ahead. Insider trading involves material nonpublic information. S I P C protects customer assets if a member broker-dealer fails, not market losses. Form U four is registration and disclosure. Form U five is termination. M S R B writes municipal securities rules. FINRA is the primary broker-dealer self-regulatory organization. The SEC is the federal securities regulator.")
    parts.append("Test-day technique. Read every word. Watch for not, except, best, primary, required, prohibited, most likely, and least likely. Eliminate wrong choices before you debate the final two. If two choices look correct, ask which one is more directly tied to the rule being tested. Do not let one difficult question steal time from the rest of the exam. Your job is not to know everything. Your job is to recognize enough correct concepts consistently to clear the passing score with margin.")
    parts.append("That completes the Accelerated SIE day-off review. Your next move should be active recall: ten to twenty flashcards, a targeted rapid drill on your weakest domain, and then a fresh full-length exam. Aim to make eighty-five percent or better repeatable before test day. Good luck.")
    return "\n\n".join(parts)


async def main():
    script = build_script()
    (OUT / 'SIE_40_Minute_Day_Off_Review_Transcript.txt').write_text(script, encoding='utf-8')
    voice = 'en-US-GuyNeural'
    communicate = edge_tts.Communicate(script, voice=voice, rate='-18%', pitch='+0Hz')
    await communicate.save(str(OUT / 'SIE_40_Minute_Day_Off_Review.mp3'))

if __name__ == '__main__':
    asyncio.run(main())
