# TP Neo4j

### Lundi

## Activity #1: Create your graph data model and generate the Cypher and image of your model

See the graph data model

Cypher script for creating the data model:

```cypher
CREATE (:Person {Name: "Sylvain", Age: 25})<-[:KNOWS]-(n0:Person {Name: "Thomas", Age: 22})-[:OWNS]->(:Animal {Type: "Cat"}),
(:Person {Name: "Charley", Age: 29})<-[:KNOWS]-(n0)-[:KNOWS]->(:Person {Name: "Martin", Age: 22})
```

![graph1](./assets/graph1.png)

## Activity #2: Run these queries of your graph model in Neo4j

Run the following Cypher queries:

```cypher
MATCH (n:Person)
RETURN n

```

```bash
╒═════════════════════════════════════════════════════════════╕
│n                                                            │
╞═════════════════════════════════════════════════════════════╡
│(:Person {Name: "Sylvain", Age: 25})                          │
│(:Person {Name: "Thomas", Age: 22})                           │
│(:Person {Name: "Charley", Age: 29})                          │
│(:Person {Name: "Martin", Age: 22})                           │
└─────────────────────────────────────────────────────────────┘
```

```cypher
MATCH (a:Person)-[r:OWNS]->(b:Animal)
RETURN a, r, b

```

```bash
╒═════════════════════════════════════════════════════════════╤══════════════════════════╤══════════════════════════════════════════════════════╕
│a                                                            │r                         │b                                                     │
╞═════════════════════════════════════════════════════════════╪══════════════════════════╪══════════════════════════════════════════════════════╡
│(:Person {Name: "Thomas", Age: 22})                          │[:OWNS]                   │(:Animal {Type: "Cat"})                               │
└─────────────────────────────────────────────────────────────┴──────────────────────────┴──────────────────────────────────────────────────────┘
```

```cypher

MATCH (a:Person)-[r:KNOWS]->(b:Person)
RETURN a.Name AS person_a_name, a.Age AS person_a_age, b.Name AS person_b_name, b.Age AS person_b_age

```

```bash
╒══════════════════════════════════════════════╤══════════════════════════════════════════════════════╤══════════════════════════════════════════════════════╕
│person_a_name                                 │person_a_age                                         │person_b_name                                          │
╞══════════════════════════════════════════════╪══════════════════════════════════════════════════════╪══════════════════════════════════════════════════════╡
│"Thomas"                                      │22                                                    │"Sylvain"                                              │
│"Thomas"                                      │22                                                    │"Charley"                                              │
│"Charley"                                     │29                                                    │"Martin"                                               │
└──────────────────────────────────────────────┴──────────────────────────────────────────────────────┴──────────────────────────────────────────────────────┘
```


#### Activité 3

![first_import](./assets/first_import.png)

WITH "file:///nvdcve-1.1-2021.json" as url 
CALL apoc.load.json(url) YIELD value 
UNWIND keys(value) AS key
RETURN key, apoc.meta.cypher.type(value[key]);

CALL apoc.periodic.iterate("CALL apoc.load.json('file:///nvdcve-1.1-2021.json') YIELD value",
"UNWIND  value.CVE_Items AS data  \r\n"+
"UNWIND data.cve.references.reference_data AS references \r\n"+
"MERGE (cveItem:CVE {uid: apoc.create.uuid()}) \r\n"+
"ON CREATE SET cveItem.cveid = data.cve.CVE_data_meta.ID, cveItem.references = references.url",
 {batchSize:2000, iterateList:true});

![cve_call](./assets/cve_call.png)



#### Activité 4



CALL apoc.load.json('file:///data.json') YIELD value
UNWIND value.items as item

MERGE (question:Question {
    id: item.question_id,
    title: item.title,
    score: item.score,
    view_count: item.view_count,
    creation_date: datetime({epochSeconds: item.creation_date})
})

WITH item, question
UNWIND item.tags as tagName
MERGE (tag:Tag {name: tagName})
CREATE (question)-[:TAGGED]->(tag)

WITH item, question
MERGE (author:User {
    id: item.owner.user_id,
    display_name: item.owner.display_name,
    reputation: item.owner.reputation
})
CREATE (author)-[:ASKED]->(question)

WITH item, question
UNWIND item.answers as answerData
MERGE (answer:Answer {
    id: answerData.answer_id,
    score: answerData.score,
    is_accepted: answerData.is_accepted,
    creation_date: datetime({epochSeconds: answerData.creation_date})
})
CREATE (answer)-[:ANSWERS]->(question)

MERGE (answerer:User {
    id: answerData.owner.user_id,
    display_name: answerData.owner.display_name,
    reputation: answerData.owner.reputation
})
CREATE (answerer)-[:PROVIDED]->(answer);

![4](./assets/4.png)

### Mardi
