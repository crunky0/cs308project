
import { useState, useRef, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../../components/customer/layout/Navbar';
import ProductCard from '../../components/products/ProductCard';
import { useAuth } from '../../context/AuthContext';
import './Products.css';

// Interface definitions
interface Product {
  productid: number;
  productname: string;
  price: number;
  discountprice?: number;
  image: string;
  averagerating: number; // Average rating for display
  stock: number;
}

interface Category {
  id: number;
  name: string;
  icon: string;
}

const categories: Category[] = [
  { id: 0, name: "All Products", icon: "local_offer" },
  { id: 1, name: "Electronics", icon: "devices" },
  { id: 2, name: "Books", icon: "library_books" },
  { id: 3, name: "Sports", icon: "fitness_center" },
  { id: 4, name: "Home Appliances", icon: "home" },
  { id: 5, name: "Toys", icon: "toys" },
  { id: 6, name: "Beauty Products", icon: "soap" },
  { id: 7, name: "Gaming", icon: "sports_esports" },
];

const Products = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [activeCategory, setActiveCategory] = useState<number>(0); // Default category is "All Products"
  const [filteredProducts, setFilteredProducts] = useState<Product[]>([]);
  const [showLeftScroll, setShowLeftScroll] = useState(false);
  const [showRightScroll, setShowRightScroll] = useState(true);
  const [loading, setLoading] = useState<boolean>(false);
  const [wishlist, setWishlist] = useState<number[]>([]);
  const [sortBy, setSortBy] = useState<string>('popular'); // Default sort
  const [filters, setFilters] = useState<{ [key: string]: string | number | boolean }>({});
  const [searchMode, setSearchMode] = useState<'name' | 'description'>('name');
  const { user } = useAuth(); // Dynamically retrieve user

  const fetchWishlist = useCallback(async () => {
    if (!user || !user.userid) {
      console.error("User ID is not available.");
      return;
    }
  
    try {
      const response = await fetch(`http://localhost:8000/wishlist/${user.userid}`);
      if (!response.ok) throw new Error('Failed to fetch wishlist');
      const wishlistData = await response.json();
      setWishlist(wishlistData.map((item: { productid: number }) => item.productid));
    } catch (error) {
      console.error('Error fetching wishlist:', error);
    }
  }, [user]);
  

  const toggleWishlist = async (productid: number) => {
    if (!user || !user.userid) {
      console.error("User not logged in. Cannot toggle wishlist.");
      return; // Exit if the user is not logged in
    }
  
    try {
      if (wishlist.includes(productid)) {
        // Remove from wishlist
        const response = await fetch('http://localhost:8000/wishlist/remove', {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ userid: user.userid, productid }),
        });
        if (!response.ok) throw new Error('Failed to remove from wishlist');
        setWishlist((prev) => prev.filter((id) => id !== productid));
      } else {
        // Add to wishlist
        const response = await fetch('http://localhost:8000/wishlist/add', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ userid: user.userid, productid }),
        });
        if (!response.ok) throw new Error('Failed to add to wishlist');
        setWishlist((prev) => [...prev, productid]);
      }
    } catch (error) {
      console.error('Error toggling wishlist:', error);
    }
  };
  
  
  const fetchProductsByCategory = async (categoryId: number) => {
    setLoading(true);
    try {
      let endpoint = 'http://localhost:8000/products/';
      if (searchQuery) {
        endpoint = `http://localhost:8000/products/search?query=${encodeURIComponent(searchQuery)}`;
      } else if (categoryId !== 0) {
        endpoint = `http://localhost:8000/products/category/${categoryId}/`;
      }
  
      const response = await fetch(endpoint);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to fetch products');
      }
  
      let data = await response.json();
  
      // Use averagerating from the API response directly
      setFilteredProducts(data);

      // Sort products
      if (sortBy === 'priceLowHigh') {
        data.sort((a: Product, b: Product) => a.price - b.price);
      } else if (sortBy === 'priceHighLow') {
        data.sort((a: Product, b: Product) => b.price - a.price);
      } else if (sortBy === 'ratingHighToLow') {
        data.sort((a: Product, b: Product) => (b.averagerating || 0) - (a.averagerating || 0));
      } else if (sortBy === 'ratingLowToHigh') {
        data.sort((a: Product, b: Product) => (a.averagerating || 0) - (b.averagerating || 0));
      }      
  
      setFilteredProducts(data);
    } catch (error) {
      console.error('Error fetching products:', error);
      setFilteredProducts([]);
    } finally {
      setLoading(false);
    }
  };
  
  
  const scroll = (direction: 'left' | 'right') => {
    if (categoriesRef.current) {
      const scrollAmount = 300;
      const container = categoriesRef.current;
      const newScrollLeft = container.scrollLeft + (direction === 'left' ? -scrollAmount : scrollAmount);
      
      container.scrollTo({
        left: newScrollLeft,
        behavior: 'smooth'
      });

      // Update scroll buttons visibility after scrolling
      setTimeout(checkScroll, 100);
    }
  };

  const fetchProductsBySearch = async (query: string) => {
    setLoading(true);
    try {
      const nameEndpoint = `http://localhost:8000/products/search/name/?productName=${encodeURIComponent(query)}`;
      const descriptionEndpoint = `http://localhost:8000/products/search/description/?description=${encodeURIComponent(query)}`;
  
      // İki endpoint'i paralel olarak çağır
      const [nameResponse, descriptionResponse] = await Promise.all([
        fetch(nameEndpoint),
        fetch(descriptionEndpoint),
      ]);
  
      if (!nameResponse.ok || !descriptionResponse.ok) {
        throw new Error('Failed to fetch search results');
      }
  
      const nameResults = await nameResponse.json();
      const descriptionResults = await descriptionResponse.json();
  
      // İsim ve açıklama sonuçlarını birleştir, tekrarlayanları kaldır
      const combinedResults = [
        ...new Map(
          [...nameResults, ...descriptionResults].map((item) => [item.productid, item])
        ).values(),
      ];
  
      // Sıralama uygula
      if (sortBy === 'priceLowHigh') {
        combinedResults.sort((a, b) => a.price - b.price);
      } else if (sortBy === 'priceHighLow') {
        combinedResults.sort((a, b) => b.price - a.price);
      } else if (sortBy === 'ratingHighToLow') {
        combinedResults.sort((a, b) => (b.averagerating || 0) - (a.averagerating || 0));
      } else if (sortBy === 'ratingLowToHigh') {
        combinedResults.sort((a, b) => (a.averagerating || 0) - (b.averagerating || 0));
      }
  
      setFilteredProducts(combinedResults);
    } catch (error) {
      console.error('Error fetching search results:', error);
      setFilteredProducts([]);
    } finally {
      setLoading(false);
    }
  };
  
  const categoriesRef = useRef<HTMLDivElement>(null);
  const checkScroll = useCallback(() => {
    if (categoriesRef.current) {
      const { scrollLeft, scrollWidth, clientWidth } = categoriesRef.current;
      setShowLeftScroll(scrollLeft > 0);
      setShowRightScroll(scrollLeft < scrollWidth - clientWidth - 10);
    }
  }, []);

  useEffect(() => {
    fetchWishlist();
  }, [fetchWishlist]);

  useEffect(() => {
    fetchProductsByCategory(activeCategory);
  }, [activeCategory, sortBy, filters]);
  
  useEffect(() => {
    if (searchQuery.trim() !== '') {
      fetchProductsBySearch(searchQuery);
    } else {
      fetchProductsByCategory(activeCategory);
    }
  }, [searchQuery, sortBy]);

  useEffect(() => {
    if (searchQuery.trim() === '') {
      fetchProductsByCategory(activeCategory);
    }
  }, [activeCategory]);
  
  

  return (
    <div className="products-page">
      <Navbar onSearch={(query) => setSearchQuery(query)} />

      <main className="main-content">
        {/* Categories Section */}
        <div className="categories-section">
          <h2>Categories</h2>
          <div className="categories-container">
            {showLeftScroll && (
              <button 
                className="scroll-button left" 
                onClick={() => scroll('left')}
                aria-label="Scroll left"
              >
                <span className="material-icons">chevron_left</span>
              </button>
            )}
            
            <div 
              className="categories-scroll" 
              ref={categoriesRef}
              onScroll={checkScroll}
            >
              {categories.map((category) => (
                <button
                  key={category.id}
                  className={`category-item ${activeCategory === category.id ? 'active' : ''}`}
                  onClick={() => setActiveCategory(category.id)}
                >
                  <span className="material-icons category-icon">{category.icon}</span>
                  {category.name}
                </button>
              ))}
            </div>

            {showRightScroll && (
              <button 
                className="scroll-button right" 
                onClick={() => scroll('right')}
                aria-label="Scroll right"
              >
                <span className="material-icons">chevron_right</span>
              </button>
            )}
          </div>
        </div>
        <div className="filters-section">
        <div className="sort-section">
          <label htmlFor="sort-select">Sort by:</label>
          <select
            id="sort-select"
            className="sort-select"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}

          > <option>Default</option>
            <option value="ratingLowToHigh">Rating: Low to High</option>
            <option value="priceLowHigh">Price: Low to High</option>
            <option value="priceHighLow">Price: High to Low</option>
            <option value="ratingHighToLow">Rating: High to Low</option>
          </select>
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
                isInWishlist={wishlist.includes(product.productid)} // Pass wishlist status
                updateWishlist={(productid: number) => toggleWishlist(productid)} // Pass toggle function
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