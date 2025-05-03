import Navbar from '../components/Navbar';
import ProductCard from '../components/ProductCard';

export default function HomePage() {
  return (
    <>
      <Navbar />
      <main className="p-8">
        <h1 className="text-2xl font-bold mb-4">Welcome to MyQuotes</h1>
        <ProductCard />
      </main>
    </>
  );
}