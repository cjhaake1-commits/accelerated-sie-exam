"""Expanded mastery notes for Block 1 (Chapters 1-5), grounded in the app curriculum/manual.
Designed as CliffNotes-plus: concise enough to review, deep enough to reason through scenarios.
"""
BLOCK1_MASTERY={
1:{"major":[
("Follow the money and the capacity","Primary market = issuer receives proceeds from a new issue. Secondary = investor-to-investor resale. Broker = agent for customer. Dealer = principal for own account. A broker-dealer can change capacity trade by trade."),
("Know the trading venues","Third market means exchange-listed securities trading away from the listing exchange. Fourth market is direct institution-to-institution trading. Dark pools reduce displayed information/market impact for large trades."),
("Understand the post-trade chain","Execution is not settlement. Clearing compares/processes obligations; settlement completes payment and delivery. DTCC is the umbrella infrastructure; NSCC is associated with many equity transactions, FICC with fixed income, OCC with listed options."),
("Firm roles matter","An introducing firm may face the customer but use a carrying/clearing firm for custody, clearing and back-office functions. A market maker is a dealer willing to buy/sell and quotes bid/ask."),
("Bid/ask reasoning","Bid is what the dealer will pay to buy; ask is what the dealer will accept to sell. Therefore a customer selling to a dealer generally receives the bid, while a customer buying from a dealer generally pays the ask.")],
"reason":"FINRA-style stems often describe behavior without naming the role. Ignore the company label and ask: whose account is being used, who gets the proceeds, and where in the transaction lifecycle are we?",
"math":["Spread = ask - bid. Example: 24.10 bid / 24.25 ask gives a $0.15 spread."],
"distinguish":["broker vs dealer","primary vs secondary","third vs fourth market","clearing vs settlement","introducing vs carrying/clearing firm","bid vs ask"]},
2:{"major":[
("Build a regulator map","SEC = federal regulator. FINRA = SRO for broker-dealers/associated persons. MSRB writes municipal securities rules. NASAA is associated with state securities administrators/Blue-Sky regulation."),
("Build a statute map by PURPOSE","1933 Act: new issues/registration/prospectus disclosure. 1934 Act: SEC, secondary trading and broker-dealer market framework. Investment Company Act: investment companies. Investment Advisers Act: advisers."),
("Registration is disclosure, not approval","A registration statement becoming effective does not mean the SEC recommends, guarantees or approves the investment's merits."),
("SIPC is narrow protection","SIPC addresses qualifying customer cash/securities when a member broker-dealer fails. It does not reimburse ordinary market losses. Keep it separate from FDIC bank-deposit insurance."),
("Supervision and disputes","WSPs assign firm supervisory responsibilities. FINRA arbitration handles monetary disputes; the Code of Procedure is associated with disciplinary proceedings."),
("State/federal can coexist","Federal securities regulation does not make state Blue-Sky regulation disappear. A question may be testing which level has jurisdiction rather than whether regulation exists at all.")],
"reason":"When several choices are true statements, choose the one governing the ACTIVITY in the stem. New issue? 1933. Secondary market? 1934. Broker-dealer conduct? FINRA. Municipal rulemaking? MSRB. State registration? state administrator/NASAA context.",
"math":["SIPC figures in the curriculum: generally $500,000 per separate customer, including a $250,000 cash sublimit. Treat these as limits to recognize, not a calculation of market-loss reimbursement."],
"distinguish":["SEC vs FINRA","FINRA vs MSRB","1933 vs 1934 Acts","Investment Company vs Investment Advisers Acts","SIPC vs market loss/FDIC","arbitration vs disciplinary procedure"]},
3:{"major":[
("Common stock is residual ownership","Common owners generally vote and participate in growth, but creditors and preferred shareholders stand ahead of them for their respective claims. Limited liability generally caps shareholder loss at the investment."),
("Preferred stock trades upside/control for priority","Preferred generally has dividend and liquidation preference over common. Cumulative preferred carries missed dividends forward; convertible preferred can be exchanged into common under stated terms."),
("Understand the share-count equation","Authorized is the charter ceiling. Issued is what the corporation has distributed. Treasury stock is issued stock repurchased by the company. Outstanding = issued - treasury."),
("Treasury stock is not outstanding","While held in treasury, shares generally do not vote or receive dividends. Repurchasing stock reduces outstanding shares without changing how many shares were historically issued."),
("Preemptive rights protect percentage ownership","If additional common shares are issued, a preemptive right may let an existing holder buy enough to avoid dilution of ownership percentage."),
("Foreign equity wrapper","ADR gives U.S. investors a receipt representing foreign shares; it can simplify access but does not erase foreign-company/country/currency risks."),
("Warrants are issuer-created equity-linked rights","A warrant is generally longer-term and permits purchase of stock at a stated price; exercise can result in new shares and dilution.")],
"reason":"Equity questions become easier if you identify the investor's objective: voting/control, growth, dividend priority, liquidation priority, maintaining ownership percentage, or foreign exposure.",
"math":["Outstanding shares = issued shares - treasury shares. Example: 12M issued - 2M treasury = 10M outstanding.","Market value of position = shares x market price. This becomes important for splits and later market-cap questions."],
"distinguish":["authorized vs issued vs outstanding vs treasury","common vs preferred","cumulative vs convertible preferred","preemptive right vs warrant","ADR vs direct domestic common stock"]},
4:{"major":[
("A bond is a cash-flow contract","The investor lends money; issuer promises interest and principal. Par is commonly $1,000 for corporate bonds. Coupon dollars are based on par, not today's market price."),
("Why price and yield move opposite","If new comparable bonds offer higher rates, an old fixed coupon is less attractive, so its market price must fall to compete. If new rates fall, the old coupon becomes more attractive and price tends to rise."),
("Premium/discount tells a story","Above par = premium; below par = discount. A discount adds a gain toward par if held to maturity; a premium embeds a loss toward par. That is why yield measures rank differently."),
("Interest-rate risk is not equal across bonds","Longer maturities generally react more to rate changes because fixed cash flows are locked in longer. Chapter 20 later formalizes sensitivity with duration."),
("Call favors issuer flexibility","When rates fall, issuer may refinance and call debt, returning principal early. Investor then faces reinvestment risk. Call protection delays that possibility."),
("Put favors investor flexibility","A put provision lets the holder sell the bond back under stated terms, which can be valuable when rates rise or credit concerns increase."),
("Convertible debt mixes bond and equity characteristics","Conversion ratio tells how many shares the bond can become. Conversion value depends on the stock price; conversion is a holder feature, not ordinary maturity repayment."),
("Credit risk remains separate from rate risk","A bond can lose value because market rates rise, because the issuer becomes less creditworthy, or both. Read the cause of the loss.")],
"reason":"For every debt question identify par, coupon dollars, market price, maturity/call feature and credit quality. Then ask what changed. Do not assume a price change changes the coupon.",
"math":["Annual interest = coupon rate x par. 6% x $1,000 = $60.","Current yield = annual interest / market price. $60 / $900 = 6.67%.","Conversion ratio = par / conversion price. $1,000 / $40 = 25 shares.","1 basis point = 0.01%; 100 bp = 1%.","Yield ordering: discount bond coupon < current yield < YTM; premium bond coupon > current yield > YTM; at par they are approximately equal (assuming standard conditions)."],
"distinguish":["coupon rate vs current yield vs YTM","premium vs discount","interest-rate vs credit risk","call vs put","call risk vs reinvestment risk","conversion price vs conversion ratio"]},
5:{"major":[
("Classify debt by repayment source","The strongest shortcut is not the issuer name but WHAT pays investors: federal government, taxes, project revenue, collateral, general corporate credit, mortgage cash flows or trade/bank obligations."),
("Treasury maturity families","T-bills are short-term discount obligations (one year or less in the curriculum). Notes are intermediate Treasury debt; bonds are long-term. TIPS adjust principal for inflation protection."),
("Agency/GSE distinction matters","GNMA mortgage-backed securities have explicit U.S. government backing in the curriculum. FNMA/FHLMC are GSEs and are not the same as direct Treasury obligations."),
("Mortgage-backed cash flows can arrive too soon","When rates fall, homeowners refinance. Principal returns faster, and the investor may have to reinvest at lower rates: prepayment/reinvestment risk."),
("Municipal repayment source is the key","GO = taxing power. Revenue = project/facility revenue. Do not select GO merely because a city issued the security."),
("Corporate priority/structure","Secured bonds have pledged collateral; debentures are unsecured and rely on general credit. Commercial paper is short-term unsecured corporate debt."),
("Money-market instruments have different users","Banker's acceptances are associated with financing international trade; negotiable CDs are large bank time deposits that may trade; commercial paper is corporate borrowing."),
("Tax treatment can affect investor value","Municipal interest may receive favorable federal tax treatment, so comparing a tax-exempt yield with a taxable bond can require a tax-equivalent-yield concept even when the question is primarily about suitability.")],
"reason":"Underline the repayment source and maturity before reading the answer choices. A city can issue either GO or revenue debt; a corporate issuer can issue secured or unsecured debt. The description determines the answer.",
"math":["Tax-equivalent yield concept: tax-exempt yield / (1 - marginal tax rate). Example: 3.5% municipal yield at a 30% marginal rate = 3.5% / .70 = 5.0% taxable-equivalent yield. Use only when the question supplies/asks for the comparison.","Discount-instrument intuition: a T-bill is bought below face value and the difference at maturity is the investor's return; do not treat it like a coupon-paying Treasury note/bond."],
"distinguish":["T-bill vs note vs bond vs TIPS","GNMA vs FNMA/FHLMC","GO vs revenue bond","secured bond vs debenture","commercial paper vs negotiable CD vs banker's acceptance","prepayment vs ordinary interest-rate risk"]}
}
