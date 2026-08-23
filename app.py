import random
import streamlit as st

st.set_page_config(page_title="Accelerated SIE Exam", page_icon="🎯", layout="wide")

QUESTIONS = [
{"q":"Which organization is primarily responsible for enforcing federal securities laws?","c":["FINRA","SEC","SIPC","FDIC"],"a":"SEC","d":"Regulatory Framework","e":"The SEC is the federal agency that administers and enforces federal securities laws. FINRA is an SRO."},
{"q":"An investor purchases common stock. What is the maximum potential loss on a long stock position?","c":["Unlimited","The amount invested","50% of the investment","Par value"],"a":"The amount invested","d":"Products & Risks","e":"A long stockholder can lose the entire investment if the stock becomes worthless, but no more than the amount invested."},
{"q":"If prevailing interest rates rise, the market price of an existing fixed-rate bond will generally:","c":["Rise","Fall","Remain unchanged","Automatically increase its coupon"],"a":"Fall","d":"Products & Risks","e":"Bond prices and market interest rates generally move inversely."},
{"q":"Which security represents an ownership interest in a corporation?","c":["Corporate bond","Treasury note","Common stock","Certificate of deposit"],"a":"Common stock","d":"Products & Risks","e":"Common stock represents equity ownership. Bonds represent debt."},
{"q":"Interest on most municipal bonds is generally:","c":["Exempt from federal income tax","Exempt from every tax in all circumstances","Taxed federally as ordinary income","Subject only to payroll tax"],"a":"Exempt from federal income tax","d":"Products & Risks","e":"Interest on most municipal securities is exempt from federal income tax; state/local treatment varies."},
{"q":"An investor expects ABC stock to rise substantially. Which position most directly benefits from that increase?","c":["Buy a put","Sell stock short","Buy a call","Write a call"],"a":"Buy a call","d":"Products & Risks","e":"A call buyer has the right to buy at the strike price and generally benefits as the underlying stock rises."},
{"q":"Which investment company continuously issues and redeems shares based on NAV?","c":["Closed-end fund","Open-end mutual fund","REIT","Hedge fund"],"a":"Open-end mutual fund","d":"Products & Risks","e":"Open-end investment companies issue redeemable shares; transactions are based on NAV (with applicable sales charges for purchases)."},
{"q":"SIPC protection is primarily relevant when:","c":["A security declines in value","Inflation rises","A SIPC-member broker-dealer fails and customer assets are missing","A bond issuer defaults"],"a":"A SIPC-member broker-dealer fails and customer assets are missing","d":"Regulatory Framework","e":"SIPC does not protect against market losses; it helps restore missing customer cash/securities when a member brokerage fails."},
{"q":"Bondholders are generally what to the issuing corporation?","c":["Owners","Creditors","Employees","General partners"],"a":"Creditors","d":"Products & Risks","e":"A bond is a debt obligation, making its holder a creditor of the issuer."},
{"q":"Which Treasury security normally has the shortest original maturity?","c":["Treasury bill","Treasury note","Treasury bond","TIPS bond"],"a":"Treasury bill","d":"Products & Risks","e":"Treasury bills are short-term Treasury obligations with maturities of one year or less."},
{"q":"Diversification primarily helps reduce which risk?","c":["Systematic market risk","Nonsystematic company-specific risk","Inflation risk completely","All investment risk"],"a":"Nonsystematic company-specific risk","d":"Products & Risks","e":"Diversification can reduce issuer/company-specific risk but cannot eliminate broad market risk."},
{"q":"Money needed for a house down payment in three months makes which factor especially important?","c":["Voting rights","Liquidity","Long-term appreciation only","Maximum leverage"],"a":"Liquidity","d":"Trading, Accounts & Prohibited Activities","e":"A short time horizon and imminent cash need make liquidity and preservation particularly important."},
{"q":"A market order instructs a broker to:","c":["Execute only at a specified price","Execute at the best available price","Guarantee a particular price","Wait for the closing price"],"a":"Execute at the best available price","d":"Trading, Accounts & Prohibited Activities","e":"A market order prioritizes execution, not a guaranteed execution price."},
{"q":"Which best describes illegal insider trading?","c":["Trading from public financial statements","Trading while possessing material nonpublic information in violation of applicable duties/law","Any officer buying company stock","Buying securities on an exchange"],"a":"Trading while possessing material nonpublic information in violation of applicable duties/law","d":"Trading, Accounts & Prohibited Activities","e":"Material nonpublic information and an applicable breach/duty are central concepts in insider-trading violations."},
{"q":"In a variable annuity separate account, who bears the investment risk?","c":["Insurance company","FINRA","Contract owner","SIPC"],"a":"Contract owner","d":"Products & Risks","e":"The contract owner bears investment risk for variable separate-account performance."},
{"q":"FINRA is best described as:","c":["A federal cabinet department","A self-regulatory organization overseeing member broker-dealers","A deposit insurer","A securities issuer"],"a":"A self-regulatory organization overseeing member broker-dealers","d":"Regulatory Framework","e":"FINRA is an SRO, not a federal agency."},
{"q":"A classic purpose of money laundering is to:","c":["Invest legitimate wages","Make illegally obtained funds appear legitimate","Realize a capital loss","Transfer an IRA"],"a":"Make illegally obtained funds appear legitimate","d":"Trading, Accounts & Prohibited Activities","e":"Money laundering seeks to disguise the illicit origin or ownership of funds."},
{"q":"Which position generally benefits from a decline in the underlying stock?","c":["Long stock","Long call","Long put","Long convertible bond"],"a":"Long put","d":"Products & Risks","e":"A put gives its buyer the right to sell at the strike price and generally increases in value as the stock falls."},
{"q":"A sell limit order at $50 may generally execute:","c":["Only below $50","At $50 or higher","At any price","Only at exactly $50"],"a":"At $50 or higher","d":"Trading, Accounts & Prohibited Activities","e":"A sell limit establishes a minimum acceptable execution price."},
{"q":"A traditional IRA generally permits:","c":["Tax-deferred growth of earnings","All withdrawals to be tax-free","Every contribution to be deductible","Only insurance products"],"a":"Tax-deferred growth of earnings","d":"Products & Risks","e":"Traditional IRA earnings generally grow tax-deferred; contribution deductibility and distribution taxation depend on circumstances."},
{"q":"A representative guarantees that a common stock cannot lose money. This is:","c":["Acceptable for blue chips","Acceptable with strong research","Improper","Required with recommendations"],"a":"Improper","d":"Trading, Accounts & Prohibited Activities","e":"Representatives may not guarantee customers against securities investment losses."},
{"q":"The primary market is where:","c":["Previously issued securities trade","Issuers sell newly issued securities","Only municipal bonds trade","Broker-dealers settle trades"],"a":"Issuers sell newly issued securities","d":"Capital Markets","e":"New securities are distributed in the primary market; outstanding securities trade in the secondary market."},
{"q":"Which regulator has primary responsibility for the municipal securities industry's rulemaking organization?","c":["MSRB","FDIC","Federal Reserve only","SIPC"],"a":"MSRB","d":"Regulatory Framework","e":"The MSRB writes rules governing municipal securities dealers and municipal advisors, subject to SEC oversight."},
{"q":"An issuer's prospectus is principally intended to provide:","c":["A guaranteed return","Material information about an offering and its risks","A promise of liquidity","FDIC insurance"],"a":"Material information about an offering and its risks","d":"Capital Markets","e":"A prospectus provides material disclosure about the issuer/offering, including risks; it does not guarantee results."},
{"q":"Which is generally considered a systematic risk?","c":["A factory fire at one company","A CEO resignation","Broad recession","A product recall"],"a":"Broad recession","d":"Products & Risks","e":"Systematic risks affect broad markets and generally cannot be diversified away."},
{"q":"A stop order becomes what once its stop price is reached?","c":["A market order","A limit order automatically","A cancelled order","A guaranteed-price order"],"a":"A market order","d":"Trading, Accounts & Prohibited Activities","e":"A traditional stop order is triggered at the stop price and then becomes a market order."},
{"q":"Which statement about preferred stock is generally true?","c":["It has priority over common stock for dividends","It always has voting control","It is a debt security","Its dividend is legally guaranteed"],"a":"It has priority over common stock for dividends","d":"Products & Risks","e":"Preferred shareholders generally have dividend and liquidation preference over common shareholders."},
{"q":"Which security is backed by the full faith and credit of the U.S. government?","c":["Corporate debenture","Treasury bond","Municipal revenue bond","Preferred stock"],"a":"Treasury bond","d":"Products & Risks","e":"U.S. Treasury securities are direct obligations backed by the full faith and credit of the U.S. government."},
{"q":"A customer seeking current income would generally be most interested in which feature?","c":["Dividend or interest payments","Voting control only","Stock splits","High turnover"],"a":"Dividend or interest payments","d":"Products & Risks","e":"Income-oriented investors generally focus on cash distributions such as interest and dividends."},
{"q":"Which account feature allows borrowed broker-dealer funds to purchase securities?","c":["Cash account","Margin account","Custodial account only","Transfer agent account"],"a":"Margin account","d":"Trading, Accounts & Prohibited Activities","e":"Margin accounts permit customers to borrow from the broker-dealer, subject to applicable requirements."},
{"q":"A customer buys 100 shares at $40 and sells them at $55. Ignoring costs, the result is:","c":["$1,500 capital gain","$5,500 capital gain","$4,000 loss","$15 interest income"],"a":"$1,500 capital gain","d":"Products & Risks","e":"The gain is $15 per share × 100 shares = $1,500."},
{"q":"Which generally has the greatest interest-rate sensitivity, all else equal?","c":["A long-term bond","A very short-term bond","A money market instrument","Cash"],"a":"A long-term bond","d":"Products & Risks","e":"Longer-maturity fixed-income securities generally have greater interest-rate risk."},
{"q":"An ETF differs from a traditional open-end mutual fund because ETF shares generally:","c":["Trade intraday on an exchange","Can never track an index","Have no market risk","Are FDIC insured"],"a":"Trade intraday on an exchange","d":"Products & Risks","e":"ETF shares trade intraday at market prices, unlike traditional mutual-fund shares priced after NAV calculation."},
{"q":"Which customer information is central to understanding an investment profile?","c":["Time horizon and risk tolerance","Favorite television program","Political preference","Unrelated hobbies"],"a":"Time horizon and risk tolerance","d":"Trading, Accounts & Prohibited Activities","e":"Investment objectives, risk tolerance, time horizon, liquidity needs and financial circumstances are core profile factors."},
{"q":"Which activity is prohibited market manipulation?","c":["Trading based on research","Creating artificial trading activity to mislead investors","Buying an index fund","Rebalancing a portfolio"],"a":"Creating artificial trading activity to mislead investors","d":"Trading, Accounts & Prohibited Activities","e":"Transactions intended to create false or misleading market activity can constitute manipulation."},
{"q":"A corporate debenture is primarily backed by:","c":["Specific real estate collateral","The issuer's general creditworthiness","FDIC insurance","Municipal taxing power"],"a":"The issuer's general creditworthiness","d":"Products & Risks","e":"A debenture is an unsecured corporate bond backed by the issuer's general credit."},
{"q":"Which entity insures qualifying bank deposits rather than brokerage securities?","c":["SIPC","FDIC","FINRA","MSRB"],"a":"FDIC","d":"Regulatory Framework","e":"FDIC protects qualifying deposits at insured banks; SIPC protection concerns customer assets at failed member brokerages."},
{"q":"An investor who sells stock short is generally:","c":["Bullish","Bearish","Guaranteed a profit","Receiving a bond coupon"],"a":"Bearish","d":"Products & Risks","e":"A short seller generally expects the stock price to decline so shares can be repurchased at a lower price."},
{"q":"A callable bond presents which additional risk to its holder?","c":["Reinvestment risk","Voting dilution only","No interest-rate exposure","Unlimited loss"],"a":"Reinvestment risk","d":"Products & Risks","e":"An issuer may call debt when rates fall, forcing the investor to reinvest returned principal at potentially lower yields."},
{"q":"Which is a characteristic of common stock?","c":["Fixed maturity date","Potential voting rights","Guaranteed dividend","Creditor status"],"a":"Potential voting rights","d":"Products & Risks","e":"Common shareholders may have voting rights and residual ownership; dividends are not guaranteed."},
{"q":"The secondary market primarily facilitates:","c":["Trading of outstanding securities among investors","Initial issuance only","Federal tax collection","Bank deposit insurance"],"a":"Trading of outstanding securities among investors","d":"Capital Markets","e":"Secondary markets provide liquidity for already-issued securities."},
{"q":"A limit order primarily gives a customer control over:","c":["Execution price","Whether execution is guaranteed","Issuer dividends","Settlement regulation"],"a":"Execution price","d":"Trading, Accounts & Prohibited Activities","e":"Limit orders establish a price boundary but may never execute."},
{"q":"Which statement best describes inflation risk?","c":["Purchasing power may decline","Issuer must default","Stock must fall","Interest rates cannot change"],"a":"Purchasing power may decline","d":"Products & Risks","e":"Inflation erodes the purchasing power of investment returns and principal."},
{"q":"A 529 plan is primarily designed to help save for:","c":["Qualified education expenses","Corporate acquisitions","Day trading","Margin interest"],"a":"Qualified education expenses","d":"Products & Risks","e":"529 plans are tax-advantaged programs designed for qualified education expenses, subject to applicable rules."},
{"q":"Which organization writes rules for FINRA-member broker-dealers and associated persons?","c":["FINRA","FDIC","IRS only","Treasury Department only"],"a":"FINRA","d":"Regulatory Framework","e":"FINRA regulates member broker-dealers and their associated persons under SEC oversight."},
{"q":"An investor's call option is in the money when the stock market price is:","c":["Above the call strike price","Below the call strike price","Always equal to zero","Below zero"],"a":"Above the call strike price","d":"Products & Risks","e":"A call has intrinsic value when the market price exceeds the strike price."},
{"q":"An investor's put option is in the money when the stock market price is:","c":["Below the put strike price","Above the put strike price","Always equal to the premium","Above the call strike"],"a":"Below the put strike price","d":"Products & Risks","e":"A put has intrinsic value when the market price is below its strike price."},
{"q":"Which best describes credit risk?","c":["Risk an issuer cannot meet debt obligations","Risk of voting dilution only","Risk a stock splits","Risk an order executes"],"a":"Risk an issuer cannot meet debt obligations","d":"Products & Risks","e":"Credit/default risk concerns the issuer's ability and willingness to make required principal and interest payments."},
{"q":"Before recommending a security, understanding a customer's liquidity needs helps determine:","c":["Whether the investment's access to funds fits the customer","The issuer's board composition","The exchange's opening bell","The security's CUSIP only"],"a":"Whether the investment's access to funds fits the customer","d":"Trading, Accounts & Prohibited Activities","e":"Liquidity needs are an important component of the customer's investment profile."},
{"q":"A registered representative sharing in a customer's account profits and losses without satisfying applicable requirements is generally:","c":["Automatically permitted","Potentially prohibited","Required","FDIC insured"],"a":"Potentially prohibited","d":"Trading, Accounts & Prohibited Activities","e":"Sharing in customer accounts is restricted and subject to specific FINRA requirements."},
]

FLASHCARDS = [
("SEC", "Federal agency administering/enforcing federal securities laws."),
("FINRA", "SRO regulating member broker-dealers and associated persons under SEC oversight."),
("SIPC", "Helps protect customer cash/securities if a SIPC-member brokerage fails; not market-loss insurance."),
("MSRB", "Writes rules for municipal securities dealers and municipal advisors, subject to SEC oversight."),
("Common stock", "Equity ownership; potential voting rights and dividends; dividends are not guaranteed."),
("Bond", "Debt security. Holder is a creditor of the issuer."),
("Interest rates ↑", "Existing fixed-rate bond prices generally ↓."),
("Diversification", "Primarily reduces nonsystematic/company-specific risk, not broad market risk."),
("Call", "Right to BUY the underlying at the strike price."),
("Put", "Right to SELL the underlying at the strike price."),
("Market order", "Prioritizes execution at the best available price; price is not guaranteed."),
("Limit order", "Sets an execution-price boundary; execution is not guaranteed."),
("Primary market", "Newly issued securities are sold by issuers."),
("Secondary market", "Outstanding securities trade among investors."),
("AML", "Framework intended to detect/prevent laundering of illicit funds and related financial crime."),
("Liquidity", "Ability to convert an asset to cash quickly without substantial loss of value."),
]

def new_test(n=50):
    pool = QUESTIONS.copy()
    random.shuffle(pool)
    chosen = pool[:min(n, len(pool))]
    out=[]
    for x in chosen:
        y=x.copy(); y["c"]=x["c"].copy(); random.shuffle(y["c"]); out.append(y)
    return out

def init():
    for k,v in {"test":None,"i":0,"answers":{},"done":False,"history":[],"card":0}.items():
        if k not in st.session_state: st.session_state[k]=v
init()

st.title("🎯 Accelerated SIE Exam")
st.caption("MISSION: PASS THE SIE • Performance-based accelerated preparation")
page=st.sidebar.radio("Training Center",["Mission Control","Cold Diagnostic","Knowledge Center","Flashcards","Practice Lab","Full SIE Simulator","Readiness"])
st.sidebar.info("Blueprint focus: Capital Markets 16% • Products & Risks 44% • Trading/Accounts/Prohibited 31% • Regulatory Framework 9%")

if page=="Mission Control":
    st.header("MISSION: PASS THE SIE")
    st.write("Start cold. Measure what you already know. Then concentrate study time on weaknesses rather than rereading material you have already mastered.")
    st.subheader("Accelerated loop")
    st.write("Cold Diagnostic → Learn → Watch/Listen → Flashcards → Targeted Practice → Full Simulation → Remediate → Prove Readiness")
    if st.button("START COLD SIE DIAGNOSTIC",type="primary",use_container_width=True):
        st.session_state.test=new_test(50); st.session_state.i=0; st.session_state.answers={}; st.session_state.done=False; st.rerun()
    st.info("Practice content is original and aligned to publicly available SIE concepts. It is not copied from or represented as actual FINRA examination questions.")

elif page=="Cold Diagnostic":
    st.header("Cold SIE Diagnostic")
    if st.session_state.test is None:
        st.warning("Do not study first. This establishes your baseline.")
        if st.button("Begin 50-question diagnostic",type="primary"):
            st.session_state.test=new_test(50); st.session_state.i=0; st.session_state.answers={}; st.session_state.done=False; st.rerun()
    elif not st.session_state.done:
        t=st.session_state.test; i=st.session_state.i; q=t[i]
        st.progress((i+1)/len(t)); st.write(f"Question {i+1} of {len(t)}")
        choice=st.radio(q["q"],q["c"],key=f"diag_{i}")
        if st.button("Lock answer",type="primary"):
            st.session_state.answers[i]=choice
            if i+1==len(t): st.session_state.done=True
            else: st.session_state.i+=1
            st.rerun()
    else:
        t=st.session_state.test; correct=sum(st.session_state.answers.get(i)==q["a"] for i,q in enumerate(t)); score=100*correct/len(t)
        st.metric("Cold diagnostic",f"{score:.0f}%",f"{correct}/{len(t)}")
        domains={}
        for i,q in enumerate(t):
            a,b=domains.get(q["d"],[0,0]); domains[q["d"]]=[a+(st.session_state.answers.get(i)==q["a"]),b+1]
        for d,(a,b) in domains.items(): st.write(f"**{d}: {100*a/b:.0f}%** ({a}/{b})")
        if st.button("Generate a fresh diagnostic (30%+ fresh/reshuffled)"):
            st.session_state.test=new_test(50); st.session_state.i=0; st.session_state.answers={}; st.session_state.done=False; st.rerun()

elif page=="Knowledge Center":
    st.header("Knowledge Center")
    st.write("Use short lessons, authoritative resources, audio-style review scripts and retrieval practice. Prioritize weak diagnostic domains.")
    topics={
    "Capital Markets":"Primary vs. secondary markets, offerings, issuers, economic factors and market participants.",
    "Products & Risks":"Equities, debt, municipals, funds, ETFs, options basics, variable products, retirement accounts and major investment risks.",
    "Trading & Customer Accounts":"Orders, liquidity, customer profiles, accounts, recommendations, AML and prohibited practices.",
    "Regulatory Framework":"SEC, FINRA, MSRB, SIPC, registration concepts, reportable/prohibited conduct and regulatory responsibilities."}
    for title,text in topics.items():
        with st.expander(title): st.write(text); st.write("**Teach-back:** Explain this topic aloud without notes, then test yourself in Practice Lab.")
    st.subheader("Authoritative learning resources")
    st.markdown("- [FINRA SIE exam page](https://www.finra.org/registration-exams-ce/qualification-exams/securities-industry-essentials-exam-sie)\n- [FINRA SIE practice test](https://www.finra.org/registration-exams-ce/qualification-exams/securities-industry-essentials-exam/practice-test)\n- [SEC Investor.gov](https://www.investor.gov/)\n- [Investor.gov videos](https://www.investor.gov/additional-resources/spotlight/videos)\n- [SIPC investor education](https://www.sipc.org/for-investors/)\n- [MSRB education](https://www.msrb.org/) ")
    st.subheader("🎧 Audio Review Mode")
    st.write("Use your device's text-to-speech/read-aloud feature on these compact review sections. Dedicated narrated files can be added later without changing your progress data.")
    st.text_area("Rapid review script","Stocks represent ownership. Bonds represent debt. Bond prices generally move inversely to interest rates. Diversification primarily reduces nonsystematic risk. A call gives the buyer the right to buy; a put gives the buyer the right to sell. Market orders prioritize execution; limit orders prioritize price. The SEC is the federal securities regulator; FINRA is an SRO; SIPC is not market-loss insurance; the MSRB writes municipal securities rules.",height=180)

elif page=="Flashcards":
    st.header("Flashcard Speed Round")
    i=st.session_state.card%len(FLASHCARDS); front,back=FLASHCARDS[i]
    st.subheader(front)
    if st.toggle("Reveal answer",key=f"reveal{i}"): st.success(back)
    c1,c2,c3=st.columns(3)
    for col,label in [(c1,"Don't Know"),(c2,"Unsure"),(c3,"Know It")]:
        if col.button(label,use_container_width=True):
            st.session_state.card=(i+1)%len(FLASHCARDS); st.rerun()
    st.caption(f"Card {i+1} of {len(FLASHCARDS)} • Responses are designed for later spaced-repetition weighting.")

elif page=="Practice Lab":
    st.header("Targeted Practice Lab")
    domain=st.selectbox("Focus",["All"]+sorted(set(q["d"] for q in QUESTIONS)))
    pool=QUESTIONS if domain=="All" else [q for q in QUESTIONS if q["d"]==domain]
    q=random.choice(pool); opts=q["c"].copy(); random.shuffle(opts)
    choice=st.radio(q["q"],opts,key="practice_choice")
    if st.button("Submit answer",type="primary"):
        if choice==q["a"]: st.success("Correct")
        else: st.error(f"Incorrect. Correct answer: {q['a']}")
        st.info(q["e"])
        st.caption(f"FINRA domain: {q['d']}")

elif page=="Full SIE Simulator":
    st.header("Full SIE Simulator")
    st.write("Target format: 85 questions / 105 minutes / 75 scored concepts + 10 simulated pretest-style items. This starter build expands the question bank over time; use the official FINRA practice exam as an external checkpoint.")
    st.warning("Do not interpret a practice percentage as a guaranteed FINRA score. FINRA equates live exam forms statistically.")
    st.markdown("[Open FINRA's official SIE practice test](https://www.finra.org/registration-exams-ce/qualification-exams/securities-industry-essentials-exam/practice-test)")

elif page=="Readiness":
    st.header("Readiness Dashboard")
    st.write("**Target:** repeated ≥85% performance on fresh material, not merely crossing the published minimum once.")
    st.write("🔴 <70% — Not Ready\n\n🟠 70–76% — Borderline\n\n🟡 77–81% — Probably Ready\n\n🟢 82–84% — Strong\n\n🟢 85%+ repeatedly — Exam Ready")
    st.info("Readiness labels are study targets, not FINRA guarantees.")
