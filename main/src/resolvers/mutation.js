export default {
  analyzeDocument: async (_, { content }, { services }) => {
    return services.analyzeService.analyze(content);
  },
};