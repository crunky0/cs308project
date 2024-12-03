import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../../components/customer/layout/Navbar';
import ProductCard from '../../components/products/ProductCard';
import './Products.css';

// Interface definitions
interface Product {
  productid: number;
  productname: string;
  price: number;
  discountPrice?: number;
  image: string;
  averageRating?: number; // Average rating for display
}

interface Category {
  id: number;
  name: string;
}

const categories: Category[] = [
  { id: 0, name: "All Products" },
  { id: 1, name: "Electronics" },
  { id: 2, name: "Books" },
  { id: 3, name: "Sports" },
  { id: 4, name: "Home Appliances" },
  { id: 5, name: "Toys" },
  { id: 6, name: "Beauty Products" },
  { id: 7, name: "Gaming" },
];

const Products = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [activeCategory, setActiveCategory] = useState<number>(0); // Default category is "All Products"
  const [filteredProducts, setFilteredProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchProductsByCategory = async (categoryId: number) => {
    setLoading(true);
    try {
      const endpoint = categoryId === 0
        ? 'http://localhost:8000/products/' // Fetch all products
        : `http://localhost:8000/products/category/${categoryId}/`;

      const response = await fetch(endpoint);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to fetch products');
      }

      const data = await response.json();

      // Fetch and add ratings to products
      const productsWithRatings = await Promise.all(
        data.map(async (product: Product) => {
          try {
            const ratingResponse = await fetch(
              `http://localhost:8000/products/${product.productid}/average-rating/`
            );
            const averageRating = ratingResponse.ok
              ? await ratingResponse.json()
              : null;

            return { ...product, averageRating };
          } catch (error) {
            console.error(`Error fetching rating for product ${product.productid}:`, error);
            return { ...product, averageRating: null };
          }
        })
      );

      setFilteredProducts(productsWithRatings);
    } catch (error) {
      console.error("Error fetching products:", error);
      setFilteredProducts([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Fetch products for the active category on mount or when the category changes
    fetchProductsByCategory(activeCategory);
  }, [activeCategory]);

  return (
    <div className="products-page">
      <Navbar onSearch={(query: string) => setSearchQuery(query)} />
      <main className="main-content">
        {/* Categories Section */}
        <div className="categories-section">
          <h2>Categories</h2>
          <div className="categories-container">
            {categories.map((category) => (
              <button
                key={category.id}
                className={`category-item ${activeCategory === category.id ? 'active' : ''}`}
                onClick={() => setActiveCategory(category.id)}
              >
                {category.name}
              </button>
            ))}
          </div>
        </div>

        {/* Products Grid */}
        <div className="products-grid">
          {loading ? (
            <div className="loading">Loading products...</div>
          ) : filteredProducts.length > 0 ? (
            filteredProducts.map((product) => (
              <ProductCard 
                key={product.productid} 
                {...product} 
                onClick={() => navigate(`/product/${product.productid}`)} // Navigate to details page
              />
            ))
          ) : (
            <div className="no-products">
              <p>No products found for this category.</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Products;