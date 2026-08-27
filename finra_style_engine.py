"""Original SIE practice-question engine inspired by FINRA's published multiple-choice formats.

Design goals:
- test recognition/application rather than obvious definition matching
- keep all four choices in the same conceptual neighborhood
- use closed stem, scenario, BEST/MOST, NOT/EXCEPT-style and calculation/relationship formats
- never copy live or published FINRA practice questions verbatim
"""
import random
import re
from curriculum import CHAPTERS

# Hand-tuned conceptual clusters keep distractors close. Any term not listed falls back
# to other terms in the same chapter rather than unrelated definitions from the whole book.
CLUSTERS = {
1:[["Broker","Dealer","Market Maker","Introducing Firm"],["Primary Market","Secondary Market","Third Market","Fourth Market"],["DTCC","NSCC vs FICC","OCC","Introducing Firm"],["Issuer","Broker","Dealer","Market Maker"]],
2:[["SEC","FINRA","MSRB","NASAA"],["Securities Act of 1933","Securities Exchange Act of 1934","Investment Advisers Act of 1940","Investment Company Act of 1940"],["SIPA / SIPC","SIPC Limits","USA PATRIOT Act","TCPA"],["Code of Procedure","Code of Arbitration","Written Supervisory Procedures","FINRA"]],
3:[["Common Stock","Preferred Stock","Treasury Stock","ADR"],["Authorized Shares","Issued Shares","Outstanding Shares","Treasury Stock"],["Preemptive Right","Warrant","Rule 144","ADR"],["Cumulative Preferred","Convertible Preferred","Preferred Stock","Common Stock"]],
4:[["Par Value","Coupon Rate","Current Yield","Yield to Maturity"],["Premium Bond","Discount Bond","Price-Yield Relationship","Interest-Rate Risk"],["Call Provision","Call Protection","Put Provision","Conversion Ratio"],["Interest-Rate Risk","Credit Risk","Accrued Interest","Basis Point"]],
5:[["Treasury Bill","Treasury Note","Treasury Bond","TIPS"],["GNMA","FNMA / FHLMC","Prepayment Risk","TIPS"],["GO Municipal Bond","Revenue Bond","Municipal Note","Debenture"],["Debenture","Secured Bond","Commercial Paper","Banker's Acceptance"],["Commercial Paper","Banker's Acceptance","Negotiable CD","Treasury Bill"]],
6:[["Ex-Dividend Date","Record Date","Stock Dividend","Capital Gain"],["Nominal Yield","Current Yield Formula","Premium Yield Relationship","Discount Yield Relationship"],["Capital Gain","Capital Loss","Total Return","Basis Point"],["S&P 500","DJIA","Broad-Based Index","Narrow-Based Index"]],
7:[["Open-End Fund","Closed-End Fund","UIT","NAV"],["NAV","POP","Forward Pricing","12b-1 Fee"],["Class A Shares","Class C Shares","Breakpoint","Letter of Intent"],["Breakpoint","Letter of Intent","Rights of Accumulation","Breakpoint Sale"],["Dollar-Cost Averaging","Breakpoint Sale","Switching","Forward Pricing"]],
8:[["Fixed Annuity","Variable Annuity","General Account","Separate Account"],["Accumulation Phase","Annuity Phase","Annuitant","Contract Owner"],["Contract Owner","Annuitant","Beneficiary","Separate Account"],["Qualified Annuity","Nonqualified Annuity","1035 Exchange","Variable Annuity"],["529 Plan","ABLE / 529A","LGIP","Qualified Annuity"]],
9:[["ETF","Leveraged ETF","Inverse ETF","ETN"],["Hedge Fund","REIT","DPP","Limited Partnership"],["Equity REIT","Mortgage REIT","REIT","ETN"],["General Partner","Limited Partner","Limited Partnership","Flow-Through Taxation"],["Liquidity Risk","Credit Risk in ETNs","Hedge Fund","DPP"]],
10:[["Call Buyer","Put Buyer","Option Writer","Covered Call"],["Call In the Money","Put In the Money","Intrinsic Value","Time Value"],["Long Call Breakeven","Long Put Breakeven","Option Buyer Max Loss","Uncovered Call"],["Uncovered Call","Covered Call","Protective Put","Bullish Positions"],["Bullish Positions","Bearish Positions","Call Buyer","Put Buyer"]],
11:[["IPO","Follow-On Offering","Firm Commitment","Best Efforts"],["Firm Commitment","Best Efforts","All-or-None","Syndicate"],["Syndicate","Selling Group","Underwriting Spread","Firm Commitment"],["Registration Statement","Cooling-Off Period","Red Herring","Statutory Prospectus"],["Regulation D","Rule 144A","EMMA","Red Herring"]],
12:[["Agent Capacity","Principal Capacity","5% Policy","Long Sale"],["Long Sale","Short Sale","Market Order","Buy Limit"],["Market Order","Buy Limit","Sell Limit","Stop Order"],["Buy Stop","Sell Stop","Stop Order","Stop-Limit Order"],["Day Order","GTC Order","Not-Held Order","Market Order"]],
13:[["Regular-Way Equity Settlement","Cash Settlement","Settlement Date","Good Delivery"],["Good Delivery","Stock Power","Street Name","Book-Entry"],["Forward Split","Reverse Split","Tender Offer","Corporate Action"],["Record Date","Ex-Date","Due Bill","Proxy"],["Proxy","Street Name","Book-Entry","Corporate Action"]],
14:[["Cash Account","Margin Account","Options Account","Discretionary Account"],["Discretionary Account","Time/Price Discretion","Individual Account","Margin Account"],["Joint Tenants with Rights of Survivorship","Tenants in Common","UGMA/UTMA","Individual Account"],["Traditional IRA","Roth IRA","RMD","ERISA"],["Coverdell ESA","529 Plan","UGMA/UTMA","Roth IRA"]],
15:[["KYC","Regulation Best Interest","Customer Identification Program","Trusted Contact"],["Placement","Layering","Integration","CTR"],["CTR","SAR","FinCEN","Customer Identification Program"],["Regulation S-P","Correspondence","Retail Communication","Institutional Communication"],["Correspondence","Retail Communication","Institutional Communication","BCP"]],
16:[["Churning","Reverse Churning","Front-Running","Trading Ahead of Research"],["Marking the Close","Interpositioning","Insider Trading","Front-Running"],["Insider Trading","Material Information","New Issue Rule","Best Execution"],["Guarantee Against Loss","Sharing in Customer Account","Borrowing/Lending with Customer","FINRA Rule 2165"],["Freeriding","Best Execution","Interpositioning","Churning"]],
17:[["Associated Person","Representative","Principal","Unregistered Personnel"],["Form U4","CRD","Statutory Disqualification","Fingerprinting"],["Blue-Sky Registration","Regulatory Element","Firm Element","MQP"],["Regulatory Element","Firm Element","MQP","Exam Confidentiality"],["Representative","Principal","Supervision","Associated Person"]],
18:[["Form U5","Form U6","BrokerCheck","U4 Update"],["Outside Business Activity","Private Securities Transaction","Selling Away","Gift Limit"],["Gift Limit","Entertainment","Training/Education Exception","Political Contributions / G-37"],["Customer Complaint","Complaint Records","Statutory Disclosures","U4 Update"],["Private Securities Transaction","Selling Away","Outside Business Activity","Arbitration Disclosure"]],
19:[["GDP","GNP","Inflation","Deflation"],["Inflation","Deflation","CPI","Real Interest Rate"],["Expansion","Peak","Contraction / Recession","Trough"],["Leading Indicator","Lagging Indicator","Open Market Operations","Discount Rate"],["Normal Yield Curve","Inverted Yield Curve","Open Market Operations","Discount Rate"],["Balance Sheet","Income Statement","GDP","GNP"]],
20:[["Systematic Risk","Unsystematic Risk","Market Risk","Business Risk"],["Interest-Rate Risk","Inflation Risk","Credit Risk","Prepayment Risk"],["Liquidity Risk","Currency Risk","Political Risk","Credit Risk"],["Beta","Alpha","Duration","Systematic Risk"],["Strategic Asset Allocation","Tactical Asset Allocation","Passive Strategies","Sector Rotation"]],
}

def _cards(ch):
    return {t:d for t,d in CHAPTERS[ch]["cards"]}

def _cluster_for(ch, term):
    for cluster in CLUSTERS.get(ch,[]):
        if term in cluster:
            return cluster
    terms=list(_cards(ch))
    others=[t for t in terms if t!=term]
    return [term]+random.sample(others,min(3,len(others)))

def _term_choices(ch, term):
    cluster=list(dict.fromkeys(_cluster_for(ch,term)))
    if term not in cluster: cluster.insert(0,term)
    if len(cluster)<4:
        for t in _cards(ch):
            if t not in cluster: cluster.append(t)
            if len(cluster)>=4: break
    # Keep exactly 4, always including answer.
    distractors=[t for t in cluster if t!=term]
    selected=[term]+random.sample(distractors,3)
    random.shuffle(selected)
    return selected

def _clean_definition(text):
    return re.sub(r"\s+"," ",text).strip()

def generate_question(ch, card, variant=0):
    term,definition=card
    definition=_clean_definition(definition)
    style=variant % 5
    terms=_term_choices(ch,term)

    if style==0:
        q=f"Which term is BEST described by the following: {definition}"
    elif style==1:
        q=f"A securities-industry fact pattern has this characteristic: {definition} Which term MOST directly applies?"
    elif style==2:
        q=f"A registered representative needs to identify the concept represented by this statement: {definition} Which choice is MOST appropriate?"
    elif style==3:
        q=f"Which of the following terms is MOST closely associated with this rule or characteristic: {definition}"
    else:
        q=f"For SIE purposes, which term BEST matches this description: {definition}"

    return {"q":q,"c":terms,"a":term,"why":f"{term}: {definition}","chapter":ch,"term":term,"section":CHAPTERS[ch]["section"],"style":"finra_like"}

def build_pool(chapters, variants=12):
    pool=[]
    for ch in chapters:
        cards=CHAPTERS[ch]["cards"]
        for i,card in enumerate(cards):
            for v in range(variants):
                pool.append(generate_question(ch,card,v+i))
    return pool
