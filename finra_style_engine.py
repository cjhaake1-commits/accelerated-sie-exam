"""Hard-mode SIE question engine.
Application scenarios are the primary source. Definition/recognition items remain a minority.
All questions are original and grounded in the user's study curriculum.
"""
import random
import re
from curriculum import CHAPTERS
from scenario_engine import expanded_scenarios
from question_metadata import enrich

CLUSTERS = {
1:[["Broker","Dealer","Market Maker","Introducing Firm"],["Primary Market","Secondary Market","Third Market","Fourth Market"],["DTCC","NSCC vs FICC","OCC","Introducing Firm"]],
2:[["SEC","FINRA","MSRB","NASAA"],["Securities Act of 1933","Securities Exchange Act of 1934","Investment Advisers Act of 1940","Investment Company Act of 1940"],["SIPA / SIPC","SIPC Limits","USA PATRIOT Act","TCPA"]],
3:[["Common Stock","Preferred Stock","Treasury Stock","ADR"],["Authorized Shares","Issued Shares","Outstanding Shares","Treasury Stock"],["Cumulative Preferred","Convertible Preferred","Preferred Stock","Common Stock"]],
4:[["Par Value","Coupon Rate","Current Yield","Yield to Maturity"],["Premium Bond","Discount Bond","Price-Yield Relationship","Interest-Rate Risk"],["Call Provision","Call Protection","Put Provision","Conversion Ratio"]],
5:[["Treasury Bill","Treasury Note","Treasury Bond","TIPS"],["GNMA","FNMA / FHLMC","Prepayment Risk","TIPS"],["GO Municipal Bond","Revenue Bond","Municipal Note","Debenture"]],
6:[["Nominal Yield","Current Yield Formula","Premium Yield Relationship","Discount Yield Relationship"],["Capital Gain","Capital Loss","Total Return","Basis Point"]],
7:[["Open-End Fund","Closed-End Fund","UIT","NAV"],["Class A Shares","Class C Shares","Breakpoint","Letter of Intent"],["Breakpoint","Letter of Intent","Rights of Accumulation","Breakpoint Sale"]],
8:[["Fixed Annuity","Variable Annuity","General Account","Separate Account"],["Accumulation Phase","Annuity Phase","Annuitant","Contract Owner"],["Qualified Annuity","Nonqualified Annuity","1035 Exchange","Variable Annuity"]],
9:[["ETF","Leveraged ETF","Inverse ETF","ETN"],["Hedge Fund","REIT","DPP","Limited Partnership"],["General Partner","Limited Partner","Limited Partnership","Flow-Through Taxation"]],
10:[["Call Buyer","Put Buyer","Option Writer","Covered Call"],["Call In the Money","Put In the Money","Intrinsic Value","Time Value"],["Long Call Breakeven","Long Put Breakeven","Option Buyer Max Loss","Uncovered Call"]],
11:[["IPO","Follow-On Offering","Firm Commitment","Best Efforts"],["Registration Statement","Cooling-Off Period","Red Herring","Statutory Prospectus"],["Regulation D","Rule 144A","EMMA","Red Herring"]],
12:[["Market Order","Buy Limit","Sell Limit","Stop Order"],["Buy Stop","Sell Stop","Stop Order","Stop-Limit Order"],["Agent Capacity","Principal Capacity","5% Policy","Long Sale"]],
13:[["Regular-Way Equity Settlement","Cash Settlement","Settlement Date","Good Delivery"],["Forward Split","Reverse Split","Tender Offer","Corporate Action"],["Record Date","Ex-Date","Due Bill","Proxy"]],
14:[["Cash Account","Margin Account","Options Account","Discretionary Account"],["Joint Tenants with Rights of Survivorship","Tenants in Common","UGMA/UTMA","Individual Account"],["Traditional IRA","Roth IRA","RMD","ERISA"]],
15:[["KYC","Regulation Best Interest","Customer Identification Program","Trusted Contact"],["Placement","Layering","Integration","CTR"],["CTR","SAR","FinCEN","Customer Identification Program"],["Correspondence","Retail Communication","Institutional Communication","BCP"]],
16:[["Churning","Reverse Churning","Front-Running","Trading Ahead of Research"],["Marking the Close","Interpositioning","Insider Trading","Front-Running"],["Freeriding","Best Execution","Interpositioning","Churning"]],
17:[["Associated Person","Representative","Principal","Unregistered Personnel"],["Form U4","CRD","Statutory Disqualification","Fingerprinting"],["Regulatory Element","Firm Element","MQP","Exam Confidentiality"]],
18:[["Form U5","Form U6","BrokerCheck","U4 Update"],["Outside Business Activity","Private Securities Transaction","Selling Away","Gift Limit"],["Customer Complaint","Complaint Records","Statutory Disclosures","U4 Update"]],
19:[["GDP","GNP","Inflation","Deflation"],["Expansion","Peak","Contraction / Recession","Trough"],["Normal Yield Curve","Inverted Yield Curve","Open Market Operations","Discount Rate"],["Balance Sheet","Income Statement","GDP","GNP"]],
20:[["Systematic Risk","Unsystematic Risk","Market Risk","Business Risk"],["Interest-Rate Risk","Inflation Risk","Credit Risk","Prepayment Risk"],["Beta","Alpha","Duration","Systematic Risk"],["Strategic Asset Allocation","Tactical Asset Allocation","Passive Strategies","Sector Rotation"]],
}

def _cards(ch): return {t:d for t,d in CHAPTERS[ch]["cards"]}
def _cluster_for(ch,term):
    for cluster in CLUSTERS.get(ch,[]):
        if term in cluster:return cluster
    terms=list(_cards(ch)); others=[t for t in terms if t!=term]
    return [term]+random.sample(others,min(3,len(others)))
def _term_choices(ch,term):
    cluster=list(dict.fromkeys(_cluster_for(ch,term)))
    if term not in cluster:cluster.insert(0,term)
    for t in _cards(ch):
        if len(cluster)>=4:break
        if t not in cluster:cluster.append(t)
    choices=[term]+random.sample([t for t in cluster if t!=term],3);random.shuffle(choices);return choices

def generate_recall(ch,card,variant=0):
    term,definition=card;definition=re.sub(r"\s+"," ",definition).strip();choices=_term_choices(ch,term)
    stems=[f"Which term is BEST described by the following: {definition}",f"Which concept MOST directly matches this characteristic: {definition}",f"Which term is MOST closely associated with this rule or characteristic: {definition}"]
    return enrich({"q":stems[variant%len(stems)],"c":choices,"a":term,"why":f"{term}: {definition}","chapter":ch,"term":term,"style":"recall"})

def build_pool(chapters,variants=12):
    """Build a bank dominated by application/scenario questions.
    Every item receives commercial metadata, provenance, difficulty and per-option rationales.
    """
    pool=[]
    for ch in chapters:
        pool.extend(enrich(q) for q in expanded_scenarios(ch,max(5,variants//2)))
        cards=CHAPTERS[ch]["cards"]
        recall_variants=max(1,variants//6)
        for i,card in enumerate(cards):
            for v in range(recall_variants): pool.append(generate_recall(ch,card,v+i))
    random.shuffle(pool)
    return pool
