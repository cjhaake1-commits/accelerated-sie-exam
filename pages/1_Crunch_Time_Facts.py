import streamlit as st

st.set_page_config(page_title="SIE Crunch Time Facts", page_icon="⚡", layout="wide")

st.markdown(
    """
    <style>
    .block-container{max-width:1200px;padding-top:1.2rem}
    .hero{padding:1.35rem;border-radius:18px;background:linear-gradient(135deg,#101827,#1e3a5f);color:white;margin-bottom:1rem}
    .big{font-size:2rem;font-weight:800}
    .muted{opacity:.82}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero"><div class="big">⚡ Crunch Time Facts</div>'
    '<div class="muted">Fast final-review tab built from the SIE Crunch Time Facts / Key Formulas packet you supplied.</div></div>',
    unsafe_allow_html=True,
)

st.info(
    "This is a condensed study companion rather than a page-for-page reproduction. Use it for rapid review, then return to the app quizzes and full simulations to test retention."
)

CHAPTERS = {
    1: ("Overview of Market Participants and Market Structure", [
        "Investment banking helps issuers raise capital; research analyzes issuers and markets; trading executes customer and firm transactions; compliance oversees information barriers.",
        "Information barriers separate investment banking, research, and trading when needed, but compliance must be able to interact across departments.",
        "Transfer agents maintain shareholder records and process transfers; registrars help prevent an issuer from exceeding authorized shares.",
        "Arbitrage is simultaneous purchase and sale of the same security in different markets to exploit a price difference.",
        "A dealer sells to customers at the ask and buys from customers at the bid; the spread is the difference.",
        "Market makers provide liquidity by standing ready to buy and sell at quoted prices.",
        "DTC supports book-entry securities settlement; OCC issues and guarantees exchange-listed options.",
    ]),
    2: ("Overview of Regulation", [
        "The Uniform Securities Act is the model state securities law commonly associated with Blue Sky regulation.",
        "FINRA member firms are members; individual representatives are associated persons rather than FINRA members themselves.",
        "SIPC protects customers when a broker-dealer fails, subject to coverage rules; it does not protect against market losses.",
        "SIPC can cover securities and qualifying cash at a failed broker-dealer, while FDIC protection applies to qualifying bank deposits.",
        "The Federal Reserve buys and sells securities in open-market operations but does not issue securities as part of that function.",
        "Regulatory hearings can impose industry sanctions; imprisonment requires court action.",
    ]),
    3: ("Equity Securities", [
        "Preferred stock generally has a fixed dividend preference but no voting rights; common stock generally has voting rights and greater price volatility.",
        "At liquidation, creditors are paid before stockholders, and preferred shareholders rank ahead of common shareholders.",
        "Restricted stock is unregistered stock commonly acquired in a private placement and is subject to resale restrictions such as Rule 144.",
        "Cumulative preferred stock must receive dividends in arrears before common dividends can be paid.",
        "ADRs represent foreign-company shares and therefore introduce currency and political risk in addition to ordinary equity risk.",
        "Rights and warrants are issuer-created instruments allowing purchase of common stock at a stated price; rights are generally shortest-lived, warrants longest-lived.",
        "Preemptive rights help existing common shareholders preserve proportional ownership.",
    ]),
    4: ("Introduction to Debt Instruments", [
        "Bond prices and market interest rates generally move in opposite directions.",
        "Longer maturities and low/no coupons create greater interest-rate sensitivity; a long-term zero-coupon bond is especially rate-sensitive.",
        "A bond trading below par has a yield above its coupon rate; a bond above par has a yield below its coupon rate.",
        "Callable bonds are most likely to be called when rates fall, which is favorable to the issuer and creates reinvestment risk for investors.",
        "Call protection is most valuable when rates fall and bond prices rise.",
        "Convertible bonds combine debt characteristics with potential equity appreciation through conversion into common shares.",
    ]),
    5: ("Types of Debt Instruments", [
        "General obligation municipal bonds are backed primarily by taxing power; revenue bonds depend primarily on revenues from a specified project or facility.",
        "Municipal bond interest may be tax-advantaged, while capital gains remain taxable.",
        "T-bills are short-term Treasury obligations issued at a discount; Treasury notes and bonds pay stated interest and can trade above or below par.",
        "Treasury interest is federally taxable but generally exempt from state and local income tax.",
        "U.S. Treasury securities carry interest-rate and inflation risk but are generally treated as free of default risk.",
        "Money-market instruments mature in one year or less; commercial paper has a maximum maturity of 270 days.",
        "Bankers' acceptances are commonly used to finance international trade.",
        "Asset-backed securities may be backed by receivables such as auto, credit-card, or home-equity debt and can carry prepayment risk.",
        "Debentures are unsecured corporate bonds.",
    ]),
    6: ("Investment Returns", [
        "Dividend yield equals annual dividend divided by current market price.",
        "Reinvested mutual-fund distributions increase an investor's tax cost basis.",
        "A buyer must own stock before the ex-dividend date to receive the upcoming dividend; the stock price is adjusted for the dividend on the ex-date.",
        "A stock dividend increases shares while proportionally reducing price so the position's total market value is unchanged immediately after the distribution.",
        "For bonds: premium price → yield below coupon; par price → yield equals coupon; discount price → yield above coupon.",
        "Yield to worst is the lower of yield to maturity and yield to call when both are relevant.",
    ]),
    7: ("Packaged Products", [
        "A mutual fund's custodian holds fund assets; the investment adviser manages the portfolio.",
        "A contingent deferred sales charge declines with holding period; no-load funds avoid specified sales loads and are limited in 12b-1 charges.",
        "Breakpoints reduce front-end mutual-fund sales charges as qualifying investment amounts rise; letters of intent can help qualify for discounts.",
        "Open-end funds continuously issue and redeem shares at NAV-based prices and remain in the primary market.",
        "Closed-end funds issue a fixed number of shares and then trade in the secondary market at prices set by supply and demand.",
        "UITs are investment companies with a generally fixed portfolio; REITs are not investment companies under the Investment Company Act.",
    ]),
    8: ("Variable Contracts and Municipal Fund Securities", [
        "Variable annuities and variable life insurance use separate-account investments and are securities as well as insurance products.",
        "Variable contracts offer tax-deferred growth but can include mortality, administrative, and surrender charges.",
        "A 1035 exchange can permit tax-deferred replacement of qualifying insurance/annuity contracts when requirements are met.",
        "The insurer guarantees the contractual settlement obligation, not the market performance of variable subaccounts.",
        "529 plans are municipal fund securities used for education savings and generally use after-tax contributions with potentially tax-free qualified withdrawals.",
        "A 529 plan owner generally controls the account and can change the beneficiary to another qualifying family member.",
        "ABLE plans provide tax-advantaged savings for qualifying individuals with disabilities, subject to statutory rules.",
    ]),
    9: ("Alternative Investments", [
        "Listed REITs are exchange-traded and liquid; non-traded REITs are much less liquid.",
        "REITs can avoid entity-level taxation on distributed income when statutory distribution requirements are satisfied.",
        "ETFs are pooled equity securities; ETNs are unsecured issuer debt linked to an index or benchmark.",
        "ETFs and ETNs both have market risk, but ETNs also expose investors directly to issuer credit risk.",
        "DPPs are pass-through structures that can pass income and losses to investors; limited-partnership interests are typically illiquid and long-term.",
        "Hedge funds are generally private, illiquid, high-minimum vehicles that may use leverage and performance fees.",
    ]),
    10: ("Options", [
        "Bullish investors can buy calls; bearish investors can buy puts.",
        "Option buyers have limited loss equal to the premium paid; uncovered call writers can face theoretically unlimited loss.",
        "Intrinsic value exists only when an option is in the money; otherwise the premium is entirely time value.",
        "Long call breakeven = strike + premium; long put breakeven = strike - premium.",
        "A protective put hedges a long stock position; a long call can hedge a short stock position.",
        "A covered call generates premium income against long stock but caps upside above the strike.",
        "American-style options may be exercised before expiration; European-style options are exercisable only at expiration, though they can trade before then.",
        "Index options settle in cash rather than by delivery of individual index-component shares.",
    ]),
    11: ("Offerings", [
        "A prospectus is the principal disclosure document for a registered public offering.",
        "A primary offering sells newly issued securities for the issuer; a secondary offering sells existing shareholder securities.",
        "During the cooling-off period, a preliminary prospectus may be distributed, but orders cannot be accepted before effectiveness.",
        "The SEC effectiveness process does not mean the SEC guarantees the accuracy or merits of the offering.",
        "Municipal new issues use an official statement; EMMA is a key source for municipal disclosure and trade information.",
        "Regulation D offerings rely on private-offering exemptions and commonly use an offering memorandum.",
        "Rule 144 governs resale of certain restricted/control securities; Rule 144A facilitates institutional resale to QIBs.",
    ]),
    12: ("Orders and Strategies", [
        "Agency trades generally involve commissions; principal trades generally involve markups or markdowns.",
        "Short sales must be executed in a margin account.",
        "A market order prioritizes execution, not price; a limit order prioritizes price and may not execute.",
        "Customers buy at the ask and sell at the bid when transacting at current dealer quotes.",
        "A sell stop can protect a long position; a buy stop can protect a short position.",
        "Protective options can also hedge stock: long put for long stock, long call for short stock.",
    ]),
    13: ("Settlement and Corporate Actions", [
        "Stock splits change share count and price per share proportionally while leaving total position value unchanged at the instant of the split.",
        "Forward split: shares increase and price falls; reverse split: shares decrease and price rises.",
        "Tender offers invite shareholders to sell under specified terms and may include minimum/maximum conditions.",
        "Standard settlement for corporate, municipal, and Treasury securities is generally T+1.",
        "Federal holidays can alter the business-day settlement calendar.",
        "For jointly registered certificates, required owners must properly endorse documents for good delivery.",
    ]),
    14: ("Customer Accounts", [
        "A hypothecation agreement allows a broker-dealer to pledge margin-account securities as collateral for a bank loan.",
        "Certain securities are not margin-eligible at purchase, including open-end mutual funds and many new issues.",
        "Options customers must receive the Options Disclosure Document before options trading is permitted.",
        "A joint account with rights of survivorship transfers the deceased owner's interest to the surviving owner.",
        "A spouse has no automatic authority over the other spouse's individual account without authorization.",
        "Custodial accounts are controlled by an adult custodian for a minor; tax identification generally belongs to the minor.",
        "Traditional IRAs provide tax-deferred growth; Roth IRA qualified distributions can be tax-free subject to the rules.",
        "Representatives cannot take discretionary action without proper authority and may never sign a customer's name.",
    ]),
    15: ("Compliance Considerations", [
        "Regulation S-P governs privacy of customer information and requires privacy notices and safeguards for nonpublic personal information.",
        "Retail communications about a broker-dealer's securities business are subject to supervisory approval rules; purely non-business communications are treated differently.",
        "Cold calls generally must occur between 8:00 a.m. and 9:00 p.m. in the recipient's local time unless an exception applies.",
        "Telemarketing firms must maintain firm-specific do-not-call procedures and required caller identification.",
        "Customer complaint records and account records have specific FINRA retention periods.",
        "Suitability applies when a recommendation is made; unsolicited customer orders are treated differently.",
        "AML programs must include policies, procedures, an AML officer, training, and independent testing, with reporting obligations such as SARs and currency transaction reports when thresholds and facts require them.",
        "OFAC sanctions screening includes checking prohibited persons such as names on the SDN list.",
    ]),
    16: ("Prohibited Activities", [
        "Front-running is trading ahead of a known customer block order; trading ahead of research is trading before a research report release.",
        "Pump-and-dump schemes manipulate price upward so insiders can sell at inflated levels.",
        "Freeriding occurs when a customer buys securities and improperly uses later sale proceeds to pay for the original purchase.",
        "Trading while aware of material nonpublic information can violate insider-trading laws, and both tipper and tippee can face liability depending on the facts.",
        "IPO allocation rules restrict purchases by many broker-dealer personnel and specified immediate-family members.",
        "Borrowing from or lending to customers is heavily restricted and may require firm approval depending on the relationship.",
    ]),
    17: ("SRO Requirements for Associated Persons", [
        "Certain broker-dealer employees with access to records, trade processing, or customer funds must be fingerprinted.",
        "A terminated representative may receive contractual trailing commissions on previously written business if the arrangement complied with registration rules.",
        "Registered persons must complete required annual compliance and continuing-education obligations.",
        "Passing the SIE alone does not make a person registered; an SIE-only individual remains unregistered and cannot perform functions requiring registration.",
        "Statutory disqualification can arise from specified criminal or regulatory events.",
    ]),
    18: ("Employee Conduct and Reportable Events", [
        "Form U4 requires disclosure of specified events, including recent bankruptcies and reportable criminal matters.",
        "Outside business activities generally require written notice to the employing broker-dealer.",
        "A person who leaves the industry for too long can lose registration status unless an available qualification-maintenance program applies.",
        "BrokerCheck provides public registration and disciplinary information but does not publish prior failed-exam scores.",
        "FINRA/MSRB gift limits restrict gifts to employees of other member firms; ordinary business entertainment can be treated differently when the giver attends.",
        "Non-cash compensation tied to securities sales is restricted, particularly sponsor-paid contests and trips.",
        "Municipal finance professionals are subject to political-contribution rules that can trigger a two-year underwriting ban.",
        "Selling away means participating in private securities transactions outside the firm without required written notice/approval.",
    ]),
    19: ("Economic Factors", [
        "Business-cycle sequence: expansion → peak → contraction → trough.",
        "Cyclical companies tend to rise and fall with the business cycle.",
        "Fiscal policy uses government spending and taxation; monetary policy is conducted by the Federal Reserve.",
        "Easy-money policy generally increases money supply and tends to lower interest rates; tightening policy does the opposite.",
        "The discount rate is directly set by the Federal Reserve; open-market operations influence market rates through securities purchases and sales.",
        "GDP measures the value of final goods and services produced; net exports are part of the calculation.",
        "Fundamental analysis studies company financials, industry conditions, and economic factors.",
        "Balance sheet equation: assets = liabilities + shareholders' equity.",
    ]),
    20: ("Investment Risks", [
        "Systematic risk affects the broad market and cannot be diversified away; nonsystematic risk is issuer/industry-specific and can be reduced through diversification.",
        "Long-term bonds have more interest-rate risk than short-term bonds.",
        "Liquidity risk is the risk that an asset cannot be sold quickly at a fair price.",
        "Mortgage-backed securities can face prepayment and reinvestment risk.",
        "Common stock can serve as a long-term inflation hedge but carries substantial market and capital risk.",
        "Short-term U.S. government securities are often used when capital preservation is the priority.",
        "Foreign securities can add currency and political risk beyond ordinary domestic investment risks.",
        "Beta measures a security's volatility relative to a market benchmark.",
    ]),
}

FORMULAS = [
    ("Outstanding stock", "Issued shares - treasury shares"),
    ("Market capitalization", "Market price per share × shares outstanding"),
    ("Preferred conversion ratio", "$100 par value ÷ conversion price"),
    ("Bond annual interest", "$1,000 par × coupon rate"),
    ("Bond points", "1 point = 1% of par = $10 on a $1,000 bond"),
    ("Treasury quote", "Treasury notes/bonds are quoted in 32nds"),
    ("Bond conversion ratio", "$1,000 par value ÷ conversion price"),
    ("Adjusted stock price ex-dividend", "Old stock price - cash dividend"),
    ("Stock-dividend shares", "Shares owned × stock-dividend percentage"),
    ("Current yield - stock", "Annual dividend ÷ current market price"),
    ("Current yield - bond", "Annual interest ÷ current market price"),
    ("Total return", "[(Ending value - beginning value) + investment income] ÷ beginning value"),
    ("Real return", "Actual return - inflation rate"),
    ("Mutual-fund POP", "NAV ÷ (1 - sales-charge percentage)"),
    ("Mutual-fund sales charge %", "(POP - NAV) ÷ POP"),
    ("Option premium", "Intrinsic value + time value"),
    ("Time value", "Option premium - intrinsic value"),
    ("Call breakeven", "Strike price + premium"),
    ("Put breakeven", "Strike price - premium"),
    ("Covered-call breakeven", "Original stock cost - premium received"),
    ("Protective-put breakeven", "Original stock cost + premium paid"),
    ("Rule 144 volume limit", "Greater of 1% of shares outstanding or average weekly trading volume for the prior 4 weeks"),
    ("Forward split new shares", "Old shares × split ratio"),
    ("Forward split new price", "Old price × inverse split ratio"),
    ("Reg T initial margin", "Security purchase or short-sale amount × 50%"),
    ("Balance sheet", "Total assets = total liabilities + shareholders' equity"),
]

EDUCATION = [
    ("529 plan", "Education-focused; owner controls account; no federal deduction; qualified education withdrawals can be tax-free; contribution/gift-tax treatment depends on current law and state rules."),
    ("Coverdell ESA", "Education-focused; annual contribution limit and contributor income restrictions apply; qualified education withdrawals can be tax-free."),
    ("UGMA/UTMA", "General-purpose custodial savings for a minor; irrevocable gift to the child; earnings are taxable under applicable rules; not limited to education expenses."),
]

query = st.text_input("Search this review", placeholder="e.g., SIPC, Rule 144, options, 529, margin")

left, right = st.columns([2, 1])
with left:
    chapter_choice = st.selectbox(
        "Jump to chapter",
        list(CHAPTERS.keys()),
        format_func=lambda n: f"Chapter {n}: {CHAPTERS[n][0]}",
    )
with right:
    st.metric("Coverage", "20 chapters")

if query.strip():
    q = query.strip().lower()
    matches = []
    for n, (title, facts) in CHAPTERS.items():
        for fact in facts:
            if q in title.lower() or q in fact.lower():
                matches.append((n, title, fact))
    for name, formula in FORMULAS:
        if q in name.lower() or q in formula.lower():
            matches.append(("Formula", name, formula))
    if not matches:
        st.warning("No condensed-review match found. Try a broader term.")
    else:
        st.subheader(f"Search results ({len(matches)})")
        for ch, title, fact in matches:
            st.markdown(f"**{ch} — {title}**  \n{fact}")
            st.divider()
else:
    title, facts = CHAPTERS[chapter_choice]
    st.subheader(f"Chapter {chapter_choice}: {title}")
    for fact in facts:
        st.markdown(f"- {fact}")

st.divider()
with st.expander("🧮 Key Formulas — open for rapid math review", expanded=True):
    for name, formula in FORMULAS:
        st.markdown(f"**{name}:** {formula}")

with st.expander("🎓 Education Savings Comparison"):
    for name, summary in EDUCATION:
        st.markdown(f"**{name}** — {summary}")

st.warning(
    "Exam rules, tax figures, contribution limits, and regulatory thresholds can change. Treat the supplied packet as the source for this tab and verify time-sensitive figures against current FINRA/IRS materials before relying on them outside exam prep."
)
