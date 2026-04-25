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
  }

  type AnalysisResult {
    risk_score: Float
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