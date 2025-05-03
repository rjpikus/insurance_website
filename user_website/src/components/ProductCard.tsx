import Link from 'next/link';
import React from 'react';

export default function ProductCard() {
  return (
    <div className="border rounded-lg p-4 shadow hover:shadow-lg transition">
      <h2 className="text-xl font-semibold">Insurance Quote</h2>
      <p className="text-gray-600">Click below to get a quote for our services.</p>
      <Link href="/product/[id]" as="/product/1">
        <button className="mt-4 px-4 py-2 bg-blue-600 text-white rounded">Get a Quote</button>
      </Link>
    </div>
  );
}