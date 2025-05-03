import { useRouter } from 'next/router';
import { useState } from 'react';
import Navbar from '../../components/Navbar';
import { sendQuoteRequest } from '../../lib/api';
import { trackEvent } from '../../lib/tracker';

export default function QuotePage() {
  const router = useRouter();
  const { id } = router.query;

  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    trackEvent('quote_request_submitted', { name, email, productId: id });
    await sendQuoteRequest({ name, email });
    setSubmitted(true);
  };

  return (
    <>
      <Navbar />
      <main className="p-8 max-w-lg mx-auto">
        <h1 className="text-2xl font-bold mb-4">Get a Quote for Product {id}</h1>
        {submitted ? (
          <p className="text-green-600">Thank you! We'll be in touch soon.</p>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="text"
              placeholder="Your name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full border p-2 rounded"
              required
            />
            <input
              type="email"
              placeholder="Your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full border p-2 rounded"
              required
            />
            <button
              type="submit"
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
            >
              Submit
            </button>
          </form>
        )}
      </main>
    </>
  );
}
