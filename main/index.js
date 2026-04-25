import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';

// Schema
import typeDefs from './src/schema/typeDefs.js';

// Resolvers
import resolvers from './src/resolvers/index.js';

// Services
import AnalyzeService from './src/services/analyzeService.js';

// Datasources
import FastApiClient from './src/datasources/fastApiClient.js';

// 🔥 Inicialización (DI manual)
const fastApiClient = new FastApiClient("http://localhost:8000");
const analyzeService = new AnalyzeService(fastApiClient);

// Server
const server = new ApolloServer({
  typeDefs,
  resolvers,
});

// Run
const { url } = await startStandaloneServer(server, {
  listen: { port: 4000 },

  context: async () => ({
    services: {
      analyzeService,
    },
  }),
});

console.log(`🚀 Server ready at ${url}`);