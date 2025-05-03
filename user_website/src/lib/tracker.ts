/** Event tracking logic */
export function trackEvent(eventName: string, metadata: Record<string, any> = {}) {
    console.log(`Tracked event: ${eventName}`, metadata);
    // Future: send this to a backend or logging service
  }