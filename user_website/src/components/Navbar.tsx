import Link from 'next/link';
import React from 'react';

export default function Navbar() {
  return (
    <nav className="bg-blue-600 text-white p-4">
      <div className="container mx-auto flex justify-between">
        <Link href="/">
          <span className="font-bold text-lg cursor-pointer">MyQuotes</span>
        </Link>
        <Link href="/product/[id]" as="/product/1">
          <span className="hover:underline cursor-pointer">Get a Quote</span>
        </Link>
      </div>
    </nav>
  );
}