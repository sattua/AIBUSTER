export default `#graphql
  type User {
    id: ID!
    name: String!
  }

  type Document {
    id: ID!
    content: String!
    createdAt: String!
  }

  type Finding {
    type: String
    sentence: String
    match: String
    start: Int
    end: Int
  }

  type AnalysisResult {
    riskScore: Float
    findings: [Finding!]!
  }

  type Search {
    id: ID!
    query: String!
    result: AnalysisResult!
    createdAt: String!
  }

  type Query {
    hello: String
    users: [User!]!
    documents: [Document!]!
    searches: [Search!]!
  }

  type Mutation {
    analyzeDocument(content: String!): Search!
  }
`;