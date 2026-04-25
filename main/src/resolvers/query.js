export default {
  hello: () => "AIBuster backend ready 🚀",

  documents: async (_, __, { services }) => {
    return services.analyzeService.getDocuments();
  },

  searches: async (_, __, { services }) => {
    const result = await services.analyzeService.getSearches();
    console.log("DEBUG SEARCHES:", result); 
    return result?.searches || result?.data || result || [];
  },
};