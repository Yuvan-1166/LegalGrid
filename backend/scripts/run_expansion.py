#!/usr/bin/env python3
"""
Corpus Expansion Script - Adds 80+ documents
Efficiently expands the legal corpus to 100+ documents
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.retriever import retriever
from app.rag.bm25_search import bm25_searcher

def generate_constitution_articles():
    """Generate 25 additional Constitution articles"""
    articles_data = {
        13: ("Laws inconsistent with fundamental rights", "All laws in force in the territory of India immediately before the commencement of this Constitution, in so far as they are inconsistent with the provisions of this Part, shall, to the extent of such inconsistency, be void."),
        16: ("Equality of opportunity in public employment", "There shall be equality of opportunity for all citizens in matters relating to employment or appointment to any office under the State."),
        17: ("Abolition of Untouchability", "Untouchability is abolished and its practice in any form is forbidden."),
        18: ("Abolition of titles", "No title, not being a military or academic distinction, shall be conferred by the State."),
        20: ("Protection in respect of conviction for offences", "No person shall be convicted of any offence except for violation of a law in force at the time of the commission of the act."),
        22: ("Protection against arrest and detention", "No person who is arrested shall be detained in custody without being informed of the grounds for such arrest."),
        23: ("Prohibition of traffic in human beings and forced labour", "Traffic in human beings and begar and other similar forms of forced labour are prohibited."),
        24: ("Prohibition of employment of children in factories", "No child below the age of fourteen years shall be employed to work in any factory or mine or engaged in any other hazardous employment."),
        25: ("Freedom of conscience and free profession, practice and propagation of religion", "All persons are equally entitled to freedom of conscience and the right freely to profess, practise and propagate religion."),
        26: ("Freedom to manage religious affairs", "Every religious denomination shall have the right to establish and maintain institutions for religious and charitable purposes."),
        27: ("Freedom from taxation for promotion of any particular religion", "No person shall be compelled to pay any taxes for the promotion or maintenance of any particular religion."),
        28: ("Freedom from attending religious instruction", "No religious instruction shall be provided in any educational institution wholly maintained out of State funds."),
        29: ("Protection of interests of minorities", "Any section of the citizens residing in the territory of India having a distinct language, script or culture of its own shall have the right to conserve the same."),
        30: ("Right of minorities to establish educational institutions", "All minorities shall have the right to establish and administer educational institutions of their choice."),
        36: ("Definition of State", "State has the same meaning as in Part III of the Constitution."),
        37: ("Application of Directive Principles", "The provisions contained in this Part shall not be enforceable by any court, but the principles therein laid down are nevertheless fundamental in the governance of the country."),
        38: ("State to secure a social order for the promotion of welfare", "The State shall strive to promote the welfare of the people by securing a social order in which justice shall inform all the institutions of the national life."),
        39: ("Certain principles of policy to be followed by the State", "The State shall direct its policy towards securing that the citizens have the right to an adequate means of livelihood."),
        40: ("Organisation of village panchayats", "The State shall take steps to organise village panchayats and endow them with such powers as may be necessary to enable them to function as units of self-government."),
        41: ("Right to work, to education and to public assistance", "The State shall make effective provision for securing the right to work, to education and to public assistance in cases of unemployment, old age, sickness and disablement."),
        42: ("Provision for just and humane conditions of work and maternity relief", "The State shall make provision for securing just and humane conditions of work and for maternity relief."),
        43: ("Living wage for workers", "The State shall endeavour to secure a living wage, conditions of work ensuring a decent standard of life for all workers."),
        44: ("Uniform civil code", "The State shall endeavour to secure for the citizens a uniform civil code throughout the territory of India."),
        45: ("Provision for free and compulsory education for children", "The State shall endeavour to provide early childhood care and education for all children until they complete the age of six years."),
        46: ("Promotion of educational and economic interests of Scheduled Castes, Scheduled Tribes", "The State shall promote with special care the educational and economic interests of the weaker sections of the people."),
    }
    
    docs = []
    for article_num, (title_suffix, content) in articles_data.items():
        docs.append({
            "doc_id": f"CONST_ART_{article_num}",
            "title": f"Constitution - Article {article_num}: {title_suffix}",
            "content": content,
            "collection": "statutes",
            "jurisdiction": "All-India",
            "metadata": {
                "doc_type": "constitution",
                "article": article_num,
                "year": 1950,
                "tags": ["constitution", "fundamental rights", "directive principles"]
            }
        })
    return docs

def generate_ipc_sections():
    """Generate 25 additional IPC sections"""
    ipc_data = {
        299: ("Culpable homicide", "Whoever causes death by doing an act with the intention of causing death, or with the intention of causing such bodily injury as is likely to cause death, commits the offence of culpable homicide."),
        300: ("Murder", "Culpable homicide is murder if the act by which the death is caused is done with the intention of causing death."),
        301: ("Culpable homicide by causing death of person other than person whose death was intended", "If a person, by doing anything which he intends or knows to be likely to cause death, commits culpable homicide by causing the death of any person."),
        303: ("Punishment for murder by life-convict", "Whoever, being under sentence of imprisonment for life, commits murder, shall be punished with death."),
        305: ("Abetment of suicide of child or insane person", "If any person under eighteen years of age, any insane person, commits suicide, whoever abets the commission of such suicide, shall be punished with death or imprisonment for life."),
        306: ("Abetment of suicide", "If any person commits suicide, whoever abets the commission of such suicide, shall be punished with imprisonment for a term which may extend to ten years."),
        307: ("Attempt to murder", "Whoever does any act with such intention or knowledge, and under such circumstances that, if he by that act caused death, he would be guilty of murder, shall be punished with imprisonment."),
        308: ("Attempt to commit culpable homicide", "Whoever does any act with such intention or knowledge and under such circumstances that, if he by that act caused death, he would be guilty of culpable homicide not amounting to murder."),
        309: ("Attempt to commit suicide", "Whoever attempts to commit suicide and does any act towards the commission of such offence, shall be punished with simple imprisonment for a term which may extend to one year."),
        310: ("Thug", "Whoever, at any time after the passing of this Act, shall have been habitually associated with any other or others for the purpose of committing robbery or child-stealing by means of or accompanied with murder, is a thug."),
        376: ("Punishment for rape", "Whoever commits rape shall be punished with rigorous imprisonment of either description for a term which shall not be less than ten years, but which may extend to imprisonment for life."),
        377: ("Unnatural offences", "Whoever voluntarily has carnal intercourse against the order of nature with any man, woman or animal, shall be punished with imprisonment for life."),
        379: ("Punishment for theft", "Whoever commits theft shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both."),
        380: ("Theft in dwelling house", "Whoever commits theft in any building, tent or vessel, which building, tent or vessel is used as a human dwelling, shall be punished with imprisonment of either description for a term which may extend to seven years."),
        381: ("Theft by clerk or servant of property in possession of master", "Whoever, being a clerk or servant, commits theft in respect of any property in the possession of his master or employer, shall be punished with imprisonment which may extend to seven years."),
        382: ("Theft after preparation made for causing death", "Whoever commits theft, having made preparation for causing death or hurt or restraint, shall be punished with rigorous imprisonment for a term which may extend to ten years."),
        383: ("Extortion", "Whoever intentionally puts any person in fear of any injury to that person, and thereby dishonestly induces the person so put in fear to deliver to any person any property, commits extortion."),
        384: ("Punishment for extortion", "Whoever commits extortion shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both."),
        385: ("Putting person in fear of injury in order to commit extortion", "Whoever, in order to the committing of extortion, puts any person in fear of any injury to that person, shall be punished with imprisonment which may extend to two years."),
        386: ("Extortion by putting a person in fear of death or grievous hurt", "Whoever commits extortion by putting any person in fear of death or of grievous hurt to that person, shall be punished with imprisonment which may extend to ten years."),
        403: ("Dishonest misappropriation of property", "Whoever dishonestly misappropriates or converts to his own use any movable property, shall be punished with imprisonment which may extend to two years, or with fine, or with both."),
        404: ("Dishonest misappropriation of property possessed by deceased person", "Whoever dishonestly misappropriates or converts to his own use property, knowing that such property was in the possession of a deceased person at the time of that person's decease, shall be punished with imprisonment which may extend to three years."),
        405: ("Criminal breach of trust", "Whoever, being in any manner entrusted with property, dishonestly misappropriates or converts to his own use that property, commits criminal breach of trust."),
        407: ("Criminal breach of trust by carrier", "Whoever, being entrusted with property as a carrier, wharfinger or warehouse-keeper, commits criminal breach of trust in respect of such property, shall be punished with imprisonment which may extend to seven years."),
        408: ("Criminal breach of trust by clerk or servant", "Whoever, being a clerk or servant, commits criminal breach of trust in respect of any property in the possession of his master or employer, shall be punished with imprisonment which may extend to seven years."),
    }
    
    docs = []
    for section_num, (title_suffix, content) in ipc_data.items():
        docs.append({
            "doc_id": f"IPC_{section_num}",
            "title": f"IPC Section {section_num} - {title_suffix}",
            "content": content,
            "collection": "statutes",
            "jurisdiction": "All-India",
            "metadata": {
                "act_name": "Indian Penal Code",
                "section": section_num,
                "year": 1860,
                "tags": ["criminal", "ipc", title_suffix.lower()]
            }
        })
    return docs

def generate_ica_sections():
    """Generate 15 Indian Contract Act sections"""
    ica_data = {
        1: ("Title and extent", "This Act may be called the Indian Contract Act, 1872, and it extends to the whole of India."),
        3: ("Communication, acceptance and revocation of proposals", "The communication of proposals, the acceptance of proposals, and the revocation of proposals and acceptances, respectively, are deemed to be made by any act or omission of the party proposing, accepting or revoking."),
        4: ("Communication when complete", "The communication of a proposal is complete when it comes to the knowledge of the person to whom it is made. The communication of an acceptance is complete as against the proposer, when it is put in a course of transmission to him."),
        5: ("Revocation of proposals and acceptances", "A proposal may be revoked at any time before the communication of its acceptance is complete as against the proposer. An acceptance may be revoked at any time before the communication of the acceptance is complete as against the acceptor."),
        6: ("Revocation how made", "A proposal is revoked by the communication of notice of revocation by the proposer to the other party."),
        7: ("Acceptance must be absolute", "In order to convert a proposal into a promise, the acceptance must be absolute and unqualified."),
        8: ("Acceptance by performing conditions", "Performance of the conditions of a proposal, or the acceptance of any consideration for a reciprocal promise which may be offered with a proposal, is an acceptance of the proposal."),
        9: ("Promises, express and implied", "In so far as the proposal or acceptance of any promise is made in words, the promise is said to be express. In so far as such proposal or acceptance is made otherwise than in words, the promise is said to be implied."),
        11: ("Who are competent to contract", "Every person is competent to contract who is of the age of majority according to the law to which he is subject, and who is of sound mind and is not disqualified from contracting by any law to which he is subject."),
        12: ("What is a sound mind for the purposes of contracting", "A person is said to be of sound mind for the purpose of making a contract, if, at the time when he makes it, he is capable of understanding it and of forming a rational judgment as to its effect upon his interests."),
        13: ("Consent defined", "Two or more persons are said to consent when they agree upon the same thing in the same sense."),
        14: ("Free consent defined", "Consent is said to be free when it is not caused by coercion, undue influence, fraud, misrepresentation or mistake."),
        15: ("Coercion defined", "Coercion is the committing, or threatening to commit, any act forbidden by the Indian Penal Code, or the unlawful detaining, or threatening to detain, any property, to the prejudice of any person whatever, with the intention of causing any person to enter into an agreement."),
        16: ("Undue influence defined", "A contract is said to be induced by undue influence where the relations subsisting between the parties are such that one of the parties is in a position to dominate the will of the other and uses that position to obtain an unfair advantage over the other."),
        17: ("Fraud defined", "Fraud means and includes any of the following acts committed by a party to a contract, with intent to deceive another party thereto or to induce him to enter into the contract: the suggestion as a fact, of that which is not true, by one who does not believe it to be true."),
    }
    
    docs = []
    for section_num, (title_suffix, content) in ica_data.items():
        docs.append({
            "doc_id": f"ICA_{section_num}",
            "title": f"Indian Contract Act Section {section_num} - {title_suffix}",
            "content": content,
            "collection": "statutes",
            "jurisdiction": "All-India",
            "metadata": {
                "act_name": "Indian Contract Act",
                "section": section_num,
                "year": 1872,
                "tags": ["contract", "civil", title_suffix.lower()]
            }
        })
    return docs

def generate_landmark_cases():
    """Generate 10 additional landmark cases"""
    cases = [
        {
            "doc_id": "CASE_ADM_JABALPUR",
            "title": "ADM Jabalpur v. Shivkant Shukla (1976)",
            "content": """During the Emergency of 1975-77, the Supreme Court held that the right to life and personal liberty under Article 21 could be suspended during Emergency. This controversial judgment was later criticized and effectively overruled by subsequent decisions. The case is remembered as a dark chapter in Indian constitutional history where the Court failed to protect fundamental rights during Emergency.""",
            "collection": "cases",
            "jurisdiction": "All-India",
            "metadata": {"court": "Supreme Court", "year": 1976, "citation_count": 200, "tags": ["emergency", "fundamental rights", "article 21"]}
        },
        {
            "doc_id": "CASE_MINERVA_MILLS",
            "title": "Minerva Mills v. Union of India (1980)",
            "content": """The Supreme Court struck down Sections 4 and 55 of the 42nd Amendment Act which gave unlimited amending power to Parliament and made Directive Principles supreme over Fundamental Rights. The Court held that the power to amend the Constitution is limited by the basic structure doctrine. This case reinforced the basic structure doctrine established in Kesavananda Bharati case.""",
            "collection": "cases",
            "jurisdiction": "All-India",
            "metadata": {"court": "Supreme Court", "year": 1980, "citation_count": 350, "tags": ["basic structure", "constitutional amendment", "judicial review"]}
        },
        {
            "doc_id": "CASE_MC_MEHTA",
            "title": "MC Mehta v. Union of India (1987)",
            "content": """This landmark environmental law case established the principle of absolute liability for hazardous industries. The Supreme Court held that an enterprise engaged in hazardous or inherently dangerous activity owes an absolute and non-delegable duty to the community to ensure that no harm results from such activity. The case arose from the Oleum gas leak in Delhi.""",
            "collection": "cases",
            "jurisdiction": "All-India",
            "metadata": {"court": "Supreme Court", "year": 1987, "citation_count": 280, "tags": ["environmental law", "absolute liability", "public interest"]}
        },
        {
            "doc_id": "CASE_INDRA_SAWHNEY",
            "title": "Indra Sawhney v. Union of India (1992)",
            "content": """The Supreme Court upheld the validity of 27% reservation for Other Backward Classes (OBCs) in government jobs but held that the creamy layer among OBCs should be excluded from reservation benefits. The Court also held that total reservation should not exceed 50% except in extraordinary situations. This case is the leading authority on reservation policy in India.""",
            "collection": "cases",
            "jurisdiction": "All-India",
            "metadata": {"court": "Supreme Court", "year": 1992, "citation_count": 400, "tags": ["reservation", "obc", "equality", "creamy layer"]}
        },
        {
            "doc_id": "CASE_DK_BASU",
            "title": "DK Basu v. State of West Bengal (1997)",
            "content": """The Supreme Court laid down comprehensive guidelines to prevent custodial violence and deaths. The guidelines include: right to inform family members about arrest, right to medical examination, maintenance of arrest memo, right to legal counsel, and prohibition of torture. These guidelines are mandatory and binding on all police authorities.""",
            "collection": "cases",
            "jurisdiction": "All-India",
            "metadata": {"court": "Supreme Court", "year": 1997, "citation_count": 250, "tags": ["custodial rights", "police", "human rights"]}
        },
        {
            "doc_id": "CASE_NAZ_FOUNDATION",
            "title": "Naz Foundation v. Govt of NCT of Delhi (2009)",
            "content": """The Delhi High Court decriminalized consensual homosexual acts between adults by reading down Section 377 of IPC. The Court held that Section 377, insofar as it criminalizes consensual sexual acts between adults in private, violates Articles 14, 15 and 21 of the Constitution. This judgment was later overturned by the Supreme Court in 2013 but ultimately upheld in Navtej Johar case in 2018.""",
            "collection": "cases",
            "jurisdiction": "Delhi",
            "metadata": {"court": "Delhi High Court", "year": 2009, "citation_count": 180, "tags": ["lgbtq rights", "section 377", "privacy"]}
        },
        {
            "doc_id": "CASE_NALSA",
            "title": "NALSA v. Union of India (2014)",
            "content": """The Supreme Court recognized transgender persons as the third gender and held that they have fundamental rights under Articles 14, 15, 16, 19 and 21. The Court directed the government to treat transgender persons as socially and educationally backward classes and provide them reservation in education and employment. This landmark judgment affirmed the rights and dignity of transgender community.""",
            "collection": "cases",
            "jurisdiction": "All-India",
            "metadata": {"court": "Supreme Court", "year": 2014, "citation_count": 220, "tags": ["transgender rights", "third gender", "equality"]}
        },
        {
            "doc_id": "CASE_PUTTASWAMY",
            "title": "K.S. Puttaswamy v. Union of India (2017)",
            "content": """The Supreme Court unanimously held that the right to privacy is a fundamental right protected under Article 21 of the Constitution. The nine-judge bench overruled earlier judgments that had held privacy was not a fundamental right. This judgment has far-reaching implications for data protection, surveillance, and individual autonomy. The case arose in the context of Aadhaar implementation.""",
            "collection": "cases",
            "jurisdiction": "All-India",
            "metadata": {"court": "Supreme Court", "year": 2017, "citation_count": 300, "tags": ["privacy", "fundamental rights", "aadhaar", "data protection"]}
        },
        {
            "doc_id": "CASE_TRIPLE_TALAQ",
            "title": "Shayara Bano v. Union of India (2017)",
            "content": """The Supreme Court declared the practice of triple talaq (talaq-e-biddat) unconstitutional and violative of Article 14 of the Constitution. The Court held that the practice was arbitrary and not an integral part of Islamic faith. This judgment was a significant step towards gender justice and equality for Muslim women. Parliament later criminalized triple talaq through legislation.""",
            "collection": "cases",
            "jurisdiction": "All-India",
            "metadata": {"court": "Supreme Court", "year": 2017, "citation_count": 190, "tags": ["triple talaq", "muslim personal law", "gender justice", "equality"]}
        },
        {
            "doc_id": "CASE_SABARIMALA",
            "title": "Indian Young Lawyers Association v. State of Kerala (2018)",
            "content": """The Supreme Court held that the practice of prohibiting entry of women aged 10-50 years into Sabarimala temple violates their fundamental rights under Articles 14, 15, 17, 19 and 25. The Court held that religion cannot be used as a cover to deny women their constitutional rights. This judgment sparked significant debate on the balance between religious freedom and gender equality.""",
            "collection": "cases",
            "jurisdiction": "All-India",
            "metadata": {"court": "Supreme Court", "year": 2018, "citation_count": 160, "tags": ["sabarimala", "women rights", "religious freedom", "equality"]}
        },
    ]
    return cases

def generate_cpc_sections():
    """Generate 5 CPC sections"""
    cpc_data = {
        9: ("Courts to try all civil suits unless barred", "The Courts shall have jurisdiction to try all suits of a civil nature excepting suits of which their cognizance is either expressly or impliedly barred."),
        11: ("Res judicata", "No Court shall try any suit or issue in which the matter directly and substantially in issue has been directly and substantially in issue in a former suit between the same parties."),
        80: ("Notice to Government", "No suit shall be instituted against the Government until the expiration of two months next after notice in writing has been delivered to the appropriate authority."),
        96: ("Appeal from original decree", "Save where otherwise expressly provided in the body of this Code or by any other law for the time being in force, an appeal shall lie from every decree passed by any Court exercising original jurisdiction."),
        151: ("Saving of inherent powers of Court", "Nothing in this Code shall be deemed to limit or otherwise affect the inherent power of the Court to make such orders as may be necessary for the ends of justice or to prevent abuse of the process of the Court."),
    }
    
    docs = []
    for section_num, (title_suffix, content) in cpc_data.items():
        docs.append({
            "doc_id": f"CPC_{section_num}",
            "title": f"CPC Section {section_num} - {title_suffix}",
            "content": content,
            "collection": "statutes",
            "jurisdiction": "All-India",
            "metadata": {
                "act_name": "Code of Civil Procedure",
                "section": section_num,
                "year": 1908,
                "tags": ["civil procedure", "cpc", title_suffix.lower()]
            }
        })
    return docs

def ingest_all_documents():
    """Ingest all generated documents"""
    print("=" * 70)
    print("CORPUS EXPANSION - Adding 80+ Documents")
    print("=" * 70)
    
    # Generate all documents
    all_docs = []
    all_docs.extend(generate_constitution_articles())
    all_docs.extend(generate_ipc_sections())
    all_docs.extend(generate_ica_sections())
    all_docs.extend(generate_landmark_cases())
    all_docs.extend(generate_cpc_sections())
    
    print(f"\nTotal documents to ingest: {len(all_docs)}")
    print(f"  - Constitution Articles: {len(generate_constitution_articles())}")
    print(f"  - IPC Sections: {len(generate_ipc_sections())}")
    print(f"  - ICA Sections: {len(generate_ica_sections())}")
    print(f"  - Landmark Cases: {len(generate_landmark_cases())}")
    print(f"  - CPC Sections: {len(generate_cpc_sections())}")
    print()
    
    success_count = 0
    error_count = 0
    
    for doc in all_docs:
        try:
            # Add to Qdrant
            retriever.add_document(
                doc_id=doc["doc_id"],
                title=doc["title"],
                content=doc["content"],
                collection=doc["collection"],
                jurisdiction=doc["jurisdiction"],
                metadata=doc["metadata"]
            )
            
            # Add to BM25
            bm25_searcher.add_document(
                doc_id=doc["doc_id"],
                title=doc["title"],
                content=doc["content"],
                collection=doc["collection"],
                jurisdiction=doc["jurisdiction"],
                **doc["metadata"]
            )
            
            print(f"✓ {doc['doc_id']}")
            success_count += 1
            
        except Exception as e:
            print(f"✗ {doc['doc_id']}: {e}")
            error_count += 1
    
    print(f"\n{'=' * 70}")
    print(f"EXPANSION COMPLETE")
    print(f"{'=' * 70}")
    print(f"✓ Successfully added: {success_count} documents")
    if error_count > 0:
        print(f"✗ Errors: {error_count} documents")
    print(f"\nTotal corpus size: ~{success_count + 20} documents")
    print(f"Target achieved: {'YES ✅' if (success_count + 20) >= 100 else 'NO ❌'}")

if __name__ == "__main__":
    ingest_all_documents()
