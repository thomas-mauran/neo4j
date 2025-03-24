// Create nodes with Person label instead of Actor
MERGE (m:Movie {title: "Oussama Ammar"})
ON CREATE SET m.released = 2025, m.tagline = "The incredible life of Oussama Ammar!"
MERGE (g:Genre {name: "Sci-Fi"})
MERGE (a:Person {name: "Thomas Mauran"})
MERGE (you:Person {name: "Thomas Mauran", born: 1990})  // Changing Actor to Person
MERGE (you)-[:ACTED_IN]->(m)
MERGE (m)-[:IN_GENRE]->(g)
RETURN m, g, a, you;



// See the movies I acted in

MATCH (p:Person {name: "Thomas Mauran"})-[:ACTED_IN]->(m:Movie)
RETURN p.name AS Actor, m.title AS Movie, m.released AS Released, m.tagline AS Tagline;
