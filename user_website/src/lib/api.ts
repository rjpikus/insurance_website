/** Axios/fetch wrappers */
export async function sendQuoteRequest(data: { name: string; email: string }) {
    console.log('Sending data to API:', data);
    // Simulate network request
    return new Promise((resolve) => setTimeout(() => resolve({ success: true }), 1000));
  }