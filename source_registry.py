"""Public-source provenance registry for the commercial SIE build.
Production content should map to these source classes rather than proprietary prep-provider material.
URLs are intentionally centralized so source/version review can be automated later.
"""
from datetime import date

SOURCE_REGISTRY={
 "FINRA_SIE_OVERVIEW":{
  "publisher":"FINRA","kind":"official_public","url":"https://www.finra.org/registration-exams-ce/qualification-exams/securities-industry-essentials-exam","use":"exam structure, eligibility, timing, passing-score and public exam information","reviewed":str(date.today())},
 "FINRA_SIE_OUTLINE":{
  "publisher":"FINRA","kind":"official_public","url":"https://www.finra.org/sites/default/files/SIE_Content_Outline.pdf","use":"controlling exam functions, objectives and blueprint scope","reviewed":str(date.today())},
 "FINRA_SIE_PRACTICE":{
  "publisher":"FINRA","kind":"official_public","url":"https://www.finra.org/registration-exams-ce/qualification-exams/securities-industry-essentials-exam/practice-test","use":"format/style calibration only; never copy or lightly rewrite items","reviewed":str(date.today())},
 "FINRA_RULES":{
  "publisher":"FINRA","kind":"official_public","url":"https://www.finra.org/rules-guidance/rulebooks/finra-rules","use":"current FINRA rule facts and conduct requirements","reviewed":str(date.today())},
 "SEC_INVESTOR":{
  "publisher":"U.S. SEC","kind":"official_public","url":"https://www.investor.gov/","use":"securities/product/risk and market education","reviewed":str(date.today())},
 "SEC_LAWS_RULES":{
  "publisher":"U.S. SEC","kind":"official_public","url":"https://www.sec.gov/about/laws-and-regulations","use":"federal securities-law and regulatory facts","reviewed":str(date.today())},
 "MSRB":{
  "publisher":"MSRB","kind":"official_public","url":"https://www.msrb.org/","use":"municipal-securities regulatory and market concepts","reviewed":str(date.today())},
 "SIPC":{
  "publisher":"SIPC","kind":"official_public","url":"https://www.sipc.org/","use":"customer-protection facts and limits","reviewed":str(date.today())},
 "FEDERAL_RESERVE":{
  "publisher":"Federal Reserve","kind":"official_public","url":"https://www.federalreserve.gov/","use":"monetary policy, rates, economics and market concepts","reviewed":str(date.today())},
 "TREASURY":{
  "publisher":"U.S. Treasury","kind":"official_public","url":"https://www.treasurydirect.gov/","use":"Treasury-security characteristics","reviewed":str(date.today())},
}

PROHIBITED_COMMERCIAL_SOURCE_CLASSES={
 "paid_vendor_manual","paid_vendor_question_bank","vendor_private_course","vendor_recorded_class","vendor_proprietary_flashcards"
}

def approved(source_key):
    return source_key in SOURCE_REGISTRY and SOURCE_REGISTRY[source_key]["kind"]=="official_public"

def production_source_keys():
    return tuple(SOURCE_REGISTRY)
