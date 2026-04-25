export default class FastApiClient {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
  }

  async analyzeDocument(content) {
    const res = await fetch(`${this.baseUrl}/analyze/document`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ content }),
    });
    if (!res.ok) {
      throw new Error("FastAPI error");
    }

    return res.json();
  }

  async getSearches() {
    const res = await fetch(`${this.baseUrl}/searches`);
    return res.json();
  }

  async getDocuments() {
    console.log("getDocuments");
    const res = await fetch(`${this.baseUrl}/documents`);
    console.dir(res.json());
    return res.json();
  }
}