CREATE (:Person {Name: "Sylvain", Age: 25})<-[:KNOWS]-(n0:Person {Name: "Thomas", Age: 22})-[:OWNS]->(:Animal {Type: "Cat"}),
(:Person {Name: "Charley", Age: 29})<-[:KNOWS]-(n0)-[:KNOWS]->(:Person {Name: "Martin", Age: 22})



