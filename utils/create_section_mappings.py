import mwparserfromhell
import json
import pandas as pd
import stanza
from ftfy import fix_text
import re
# stanza.download('en')

nlp = stanza.Pipeline(lang='en', processors='tokenize')

data = []

with open(path+'enwiki-latest.json', encoding='utf-8') as f:
    for i, line in enumerate(f):
        doc = json.loads(line)
        lst = [doc['title'], doc['section_titles'], doc['section_texts'], doc['interlinks']]
        data.append(lst)
        
        if not i % 500:
            break
            
        if not i % 500000:
            print(i)
            
def parse_section(doc):
    parsed = mwparserfromhell.parse(doc)
    subsections = parsed.get_sections(flat=True, include_lead=True)
    return subsections

def create_passages_for_subsection(subsection_doc):
    passages = []
    tmp = []
    subsection_label = ""
    subsubsection_label = ""
    for s in subsection_doc.split("\n"):
        if s.startswith("=== "):
            subsection_label = s.replace("===", "").strip()
            continue
        if s.startswith("==== "):
            subsubsection_label = s.replace("====", "").strip()
            continue              
        if s:
            tmp.append(s.strip())
    
    for s in tmp:
        split = s.split()
        if len(re.findall(r"[A-Za-z]+", str(split))) < 3:
            continue
        
        if len(split) > 256:
            stanza_doc = nlp(s)
            sentences = stanza_doc.sents
            passage = ""
            for sentence in sentences:
                passage = passage + " " + sentence.text 
                if len(passage.split()) > 256:
                    passage = fix_text(passage)
                    passages.append(passage.strip())
                    passage = ""
            if passage.strip():
                passage = fix_text(passage)
                passages.append(passage.strip())
        else:
            passages.append(fix_text(s))  
#     print(passages)
    return passages, subsection_label, subsubsection_label

def map_passages_for_section(article_name, section_name, section_doc):
    subsections = parse_section(section_doc)
    pairs = []
    prev_subsection = ""
    prev_subsubsection = ""
    for i, s in enumerate(subsections):
#         print(i)
        tmp0 = []
        tmp1 = []

        mapping_string = article_name + " " + section_name
        passages, subsection, subsubsection = create_passages_for_subsection(s)
        
        if i > 0:

            if subsection and subsubsection:
                mapping_string = article_name + " " + section_name + " " + subsection + " " + subsubsection

            if subsection and not subsubsection:
                mapping_string = article_name + " " + section_name + " " + subsection + " " + subsubsection

            if not subsection and subsubsection:
                mapping_string = article_name + " " + section_name + " " + prev_subsection + " " + subsubsection

            if not subsection and not subsubsection:
                mapping_string = article_name + " " + section_name + " " + prev_subsection + " " + prev_subsubsection
                
        else:
            tmp0 = list(zip(passages, [mapping_string.strip()]*len(passages)))
#             print(tmp0)


        prev_subsection = subsection
        prev_subsubsection = subsubsection
        
        tmp1 = list(zip(passages, [mapping_string.strip()]*len(passages)))
#         print(tmp)
        pairs.extend(tmp0)
        pairs.extend(tmp1)
        
    return pairs

not_allowed = ['Introduction', 'See also', 'Notes', \
               'References', 'Further reading', 'External links', \
               'Sources', 'Overview']

name = 'Hinduism' #article name
pairs = pd.DataFrame()

#Islam
# m = 4
# print(df.loc[n].page)
# print(df.loc[n].sections)
# df.loc[n].sections[m]

for text, section in zip(df.loc[name].text, df.loc[name].sections):
    if section in not_allowed:
        section = ""
    tmp = pd.DataFrame(map_passages_for_section(name, section, text), columns=["text", "category"])
    pairs = pd.concat([pairs, tmp], ignore_index=True)
    
pairs['length'] = pairs.text.apply(lambda x: len(x.split()))
# pairs
pairs.drop_duplicates()