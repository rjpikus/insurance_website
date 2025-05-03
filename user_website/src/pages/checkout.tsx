// src/pages/checkout.tsx
import Navbar from '../components/Navbar';
import { useEffect } from 'react';
import { trackEvent } from '../lib/tracker';

export default function CheckoutPage() {
  useEffect(() => {
    trackEvent('visited_checkout');
  }, []);

  return (
    <>
      <Navbar />
      <main className="p-8 max-w-xl mx-auto">
        <h1 className="text-2xl font-bold mb-4">Checkout</h1>
        <p className="mb-4">Thanks for submitting your quote request.</p>
        <p>We'll review your information and follow up shortly with more details.</p>
      </main>
    </>
  );
}
