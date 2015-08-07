Neo_Wordnet
-----------

This software imports [WordNet RDF (version tested: 3.1)](http://wordnet-rdf.princeton.edu/) into neo4j 2.3. 
This is a sister project of [Neo_Concept](https://github.com/redsk/neo_concept) which imports ConceptNet into neo4j.

Pre-Requisites
--------------

- neo4j version 2.2.2 (needed for the [new import tool](http://neo4j.com/docs/2.2.2/import-tool.html))
- [WordNet 3.1 RDF](http://wordnet-rdf.princeton.edu/wn31.nt.gz) provides a list of assertions
- regular Python, no dependencies

Tested with neo4j-community-2.2.2.

How-To 
-------------------

    mkdir neo-kbs
    cd neo-kbs
    git clone https://github.com/redsk/neo_concept.git

    # get latest conceptnet from http://conceptnet5.media.mit.edu/downloads/
    wget http://conceptnet5.media.mit.edu/downloads/current/conceptnet5_flat_csv_5.3.tar.bz2
    tar jxvf conceptnet5_flat_csv_5.3.tar.bz2
    ln -s csv_<version> csv_current

    # Usage:
    # python convertcn.py <input directory> [ALL_LANGUAGES]
    # If the flag ALL_LANGUAGES is not set, only English concepts will be converted
    # this will take a while
    python neo_concept/convertcn.py csv_current/assertions/

    # optionally, you can get the POS tags. This assumes that stanford nlp is installed in
    # stanfordNLPdir = "../../stanford-corenlp-python/stanford-corenlp-full-2015-01-30"
    # neoConceptRootForSNLP = '../../neo4j-conceptnet5/converter/'
    # modify the two variables above in POScn.py to fit your stanford nlp installation
    # the following commands will take a while and were tested with a java memory of 2GB
    python neo_concept/POScn.py surface edges.csv
    python neo_concept/POScn.py genpos edges.csv 50000
    python neo_concept/POScn.py poscount edges.csv

    # get latest neo4j (tested with neo4j-community-2.2.2)
    curl -O -J -L http://neo4j.com/artifact.php?name=neo4j-community-2.2.2-unix.tar.gz
    tar zxf neo4j-community-2.2.2-unix.tar.gz

    # do only one of the two import commands below. If you calculated the POS tags, edges.csv is no longer needed

    # import nodes.csv and edges.csv using the new import tool (WITHOUT POS TAGS!) -- this will take a while too
    neo4j-community-2.2.2/bin/neo4j-import --into neo4j-community-2.2.2/data/graph.db --nodes nodes.csv --relationships edges.csv --delimiter "TAB"

    # import nodes.csv and edges.csv using the new import tool (WITH POS TAGS!) -- this will take a while too
    neo4j-community-2.2.2/bin/neo4j-import --into neo4j-community-2.2.2/data/graph.db --nodes nodes.csv --relationships edgesPOS.csv --delimiter "TAB"

    # start neo4j
    neo4j-community-2.2.2/bin/neo4j start


Goto localhost:7474 to see the graph. Create and index on Concepts for performance reasons:

    CREATE INDEX ON :Concept(id)

You can now query the database. Example:

    MATCH (sushi {id:"/c/en/sushi"}), sushi-[r]->other_concepts
    RETURN sushi.id, other_concepts.id, type(r), r.context, r.weight, r.surface
