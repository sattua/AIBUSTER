export default class AnalyzeService {
  constructor(fastApiClient) {
    this.fastApiClient = fastApiClient;
  }

  async analyze(content) {
    if (!content || content.length === 0) {
      throw new Error("Content is required");
    }

    return await this.fastApiClient.analyzeDocument(content);
  }

  async getSearches() {
    return this.fastApiClient.getSearches();
  }

  async getDocuments() {
    return this.fastApiClient.getDocuments();
  }
}