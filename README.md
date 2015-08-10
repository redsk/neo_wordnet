Neo_Wordnet
-----------

This software imports [WordNet RDF (version tested: 3.1)](http://wordnet-rdf.princeton.edu/) into neo4j 2.2.2. 
This is a sister project of [Neo_Concept](https://github.com/redsk/neo_concept) which imports ConceptNet into neo4j.

Pre-Requisites
--------------

- neo4j version 2.2.2 (needed for the [new import tool](http://neo4j.com/docs/2.2.2/import-tool.html))
- [WordNet 3.1 RDF](http://wordnet-rdf.princeton.edu/wn31.nt.gz) provides a list of assertions
- regular Python, no dependencies

Tested with neo4j-community-2.2.2.

- NEW!: Check out [Neo_Merger](https://github.com/redsk/neo_merger) to import Conceptnet and Wordnet into the same neo4j graph!

How-To 
-------------------

    mkdir neo4j-kbs
    cd neo4j-kbs
    git clone https://github.com/redsk/neo_wordnet.git

    # get latest wordnet rdf from http://wordnet-rdf.princeton.edu/wn31.nt.gz
    mkdir wordnet
    cd wordnet
    wget http://wordnet-rdf.princeton.edu/wn31.nt.gz
    gunzip http://wordnet-rdf.princeton.edu/wn31.nt.gz
    cd ..

    # Usage:
    # python convertwn.py <input file>
    python neo_wordnet/convertwn.py wordnet/nt31.nt

    # I've filtered some relations and made some replacements to WordNet namespace (to shorten names)
    # Have a look at the log file
    less wordnet/WNimporter.log

    # get latest neo4j (tested with neo4j-community-2.2.2)
    curl -O -J -L http://neo4j.com/artifact.php?name=neo4j-community-2.2.2-unix.tar.gz
    tar zxf neo4j-community-2.2.2-unix.tar.gz

    # import WNnodes.csv and WNedges.csv using the new import tool
    neo4j-community-2.2.2/bin/neo4j-import --into neo4j-community-2.2.2/data/graph.db --nodes wordnet/WNnodes.csv --relationships wordnet/WNedges.csv --delimiter "TAB"

    # start neo4j
    neo4j-community-2.2.2/bin/neo4j start


Go to localhost:7474 to see the graph. Create indexes on labels for performance reasons:

    CREATE INDEX ON :`lemon#LexicalEntry`(id)
    CREATE INDEX ON :`lemon#LexicalSense`(id)
    CREATE INDEX ON :`wdo#Synset`(id)

You can now query the database. Example:

    MATCH (c0:`lemon#LexicalEntry` { id:"wn/bus+driver-n" }), (c1:`lemon#LexicalEntry` { id:"wn/drive-v" }), path=allShortestPaths((c0)-[*..10]-(c1))
    RETURN c0,c1,path
