# autotopic-data


1. DBPedia Category Dumps (December 2021)

https://databus.dbpedia.org/dbpedia/generic/categories/2021.12.01/categories_lang=en_labels.ttl.bz2

https://databus.dbpedia.org/dbpedia/generic/categories/2021.12.01/categories_lang=en_articles.ttl.bz2

https://databus.dbpedia.org/dbpedia/generic/categories/2021.12.01/categories_lang=en_skos.ttl.bz2


2. Wikipedia Article Dump

https://dumps.wikimedia.org/enwiki/20211201/enwiki-20211201-pages-articles-multistream.xml.bz2

3. Process Wikipedia Article Dump using gensim

`python -m gensim.scripts.segment_wiki -i -m 500 -f enwiki-20211201-pages-articles-multistream.xml.bz2 -o enwiki-dec2021.json.gz `

4. Create Pairs

