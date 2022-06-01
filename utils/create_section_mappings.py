import mwparserfromhell
import json
import pandas as pd
import stanza
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
            
            
def parse_section(section_doc):
    parsed = mwparserfromhell.parse(section_doc)
    subsections = parsed.get_sections(flat=True, include_lead=True)
    return subsections

def create_passages_for_subsection(subsection_doc):
    passages = []
    tmp = []
    subsection_label = None
    subsubsection_label = None
    for s in subsection_doc.split("\n"):
        if s.startswith("=== "):
            subsection_label = s.replace("===", "").strip()
            continue
        if s.startswith("==== "):
            subsubsection_label = s.replace("====", "").strip()
            continue       
        
        if s:
            tmp.append(s)
    
    for s in tmp:
        split = s.split()
        if len(split) < 6:
            continue
        
        if len(split) > 256:
            stanza_doc = nlp(s)
            sentences = stanza_doc.sents
            passage = ""
            for sentence in sentences:
                passage = passage + " " + sentence.text 
                if len(passage.split()) > 256:
                    passages.append(passage.strip())
                    passage = ""
            if passage.strip():
                passages.append(passage.strip())
        else:
            passages.append(s)       
    return passages, subsection_label, subsubsection_label

def map_passages_for_section(article_name, section_name, section_doc):
    subsections = parse_section(section_doc)
    for s in subsections:
        mapping_string = article_name + " " + section_name
        passages = create_passages_for_subsection(s)
        subsection = 
        
    