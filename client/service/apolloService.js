// service/apolloService.js
import { ApolloClient, InMemoryCache, HttpLink } from "@apollo/client";

const apiUrl = __API_URL__;

const client = new ApolloClient({
  link: new HttpLink({
    uri: `${apiUrl}/graphql`,
  }),
  cache: new InMemoryCache(),
});

export default client;