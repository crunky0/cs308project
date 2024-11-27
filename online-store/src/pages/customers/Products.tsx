import { useState, useRef, useEffect, useCallback } from 'react';
import Navbar from '../../components/customer/layout/Navbar';
import ProductCard from '../../components/products/ProductCard';
import './Products.css';

// Interface definitions
interface Product {
  id: number;
  name: string;
  price: number;
  discountedPrice?: number;
  image: string;
  description: string;
  rating: number;
  reviews: number;
  categoryId: number;
  color: string;
  material: string;
  date: string;
}

interface Filters {
  priceRange: string;
  rating: number | null;
  color: string[];
  material: string[];
  offer: boolean;
}

interface Category {
  id: number;
  name: string;
  icon: string;
}

// Sample data
const sampleProducts: Product[] = [
  {
    id: 1,
    name: "Wireless Headphones",
    price: 299.99,
    discountedPrice: 249.99,
    image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e", 
    description: "High-quality wireless headphones with noise cancellation",
    rating: 4.5,
    reviews: 128,
    categoryId: 1,
    color: "Black",
    material: "Plastic",
    date: "2024-03-15"
  },
  {
    id: 2,
    name: "Smart Watch",
    price: 399.99,
    discountedPrice: 349.99,
    image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e", 

    description: "Feature-rich smartwatch with health tracking",
    rating: 2.1,
    reviews: 95,
    categoryId: 1,
    color: "Silver",
    material: "Metal",
    date: "2024-03-14"
  },
  {
    id: 3,
    name: "Laptop Pro",
    price: 1299.99,
    discountedPrice: 1199.99,
    image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e", 

    description: "Powerful laptop for professionals",
    rating: 3.1,
    reviews: 156,
    categoryId: 2,
    color: "Space Gray",
    material: "Aluminum",
    date: "2024-03-13"
  },
  {
    id: 4,
    name: "Gaming Mouse",
    price: 79.99,
    discountedPrice: 59.99,
    image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e", 

    description: "High-precision gaming mouse",
    rating: 1.0,
    reviews: 203,
    categoryId: 2,
    color: "RGB",
    material: "Plastic",
    date: "2024-03-12"
  },
  {
    id: 5,
    name: "Gaming Mouse",
    price: 79.99,
    discountedPrice: 59.99,
    image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e", 

    description: "High-precision gaming mouse",
    rating: 1.0,
    reviews: 203,
    categoryId: 2,
    color: "RGB",
    material: "Plastic",
    date: "2024-03-12"
  },
  {
    id: 6,
    name: "Gaming Mouse",
    price: 79.99,
    discountedPrice: 59.99,
    image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e", 

    description: "High-precision gaming mouse",
    rating: 1.0,
    reviews: 203,
    categoryId: 2,
    color: "RGB",
    material: "Plastic",
    date: "2024-03-12"
  }
];

const categories: Category[] = [
  { id: 1, name: "Black Friday Sale", icon: "local_offer" },
  { id: 2, name: "Standing Desks", icon: "table_restaurant" },
  { id: 3, name: "Ergonomic Chairs", icon: "chair" },
  { id: 4, name: "ADUs", icon: "home" },
  { id: 5, name: "Office Accessories", icon: "work" },
  { id: 6, name: "Fitness", icon: "fitness_center" },
  { id: 7, name: "Gift Ideas", icon: "card_giftcard" },
  { id: 8, name: "Home Appliances", icon: "kitchen" },
  { id: 9, name: "Office Furniture", icon: "chair_alt" },
  { id: 10, name: "Gaming", icon: "sports_esports" },
];

interface NavbarProps {
  onSearch: (query: string) => void;
}

const Products = () => {
  // State declarations
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [activeCategory, setActiveCategory] = useState<number>(1);
  const [filteredProducts, setFilteredProducts] = useState<Product[]>(sampleProducts);
  const [showLeftScroll, setShowLeftScroll] = useState(false);
  const [showRightScroll, setShowRightScroll] = useState(true);
  const [sortBy, setSortBy] = useState("popular");
  
  // Refs
  const categoriesRef = useRef<HTMLDivElement>(null);

  // Filter states
  const [filters, setFilters] = useState<Filters>({
    priceRange: "",
    rating: null,
    color: [],
    material: [],
    offer: false
  });

  const [showFilters, setShowFilters] = useState({
    price: false,
    rating: false,
    color: false,
    material: false,
    offer: false
  });

  // Add state for filter dropdowns
  const [showFilterDropdowns, setShowFilterDropdowns] = useState({
    price: false,
    rating: false
  });

  // Price ranges for the filter
  const priceRanges = [
    { label: "Under $300", value: "0-300" },
    { label: "$300 - $600", value: "300-600" },
    { label: "$600 - $1000", value: "600-1000" },
    { label: "$1000+", value: "1000+" }
  ];

  // Rating options
  const ratingOptions = [5, 4, 3, 2, 1];

  // Toggle filter dropdown
  const toggleFilterDropdown = (filter: 'price' | 'rating') => {
    setShowFilterDropdowns(prev => ({
      ...prev,
      [filter]: !prev[filter]
    }));
  };

  // Handler functions
  const toggleFilter = (filterName: keyof typeof showFilters) => {
    setShowFilters(prev => ({
      ...prev,
      [filterName]: !prev[filterName]
    }));
  };

  const handlePriceFilter = (range: string) => {
    setFilters(prev => ({
      ...prev,
      priceRange: prev.priceRange === range ? "" : range
    }));
  };

  const handleRatingFilter = (rating: number) => {
    setFilters(prev => ({
      ...prev,
      rating: prev.rating === rating ? null : rating
    }));
  };

  // Scroll functionality
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

  // Check scroll position
  const checkScroll = useCallback(() => {
    if (categoriesRef.current) {
      const { scrollLeft, scrollWidth, clientWidth } = categoriesRef.current;
      setShowLeftScroll(scrollLeft > 0);
      setShowRightScroll(scrollLeft < scrollWidth - clientWidth - 10);
    }
  }, []);

  // Effects
  useEffect(() => {
    checkScroll();
    window.addEventListener('resize', checkScroll);
    return () => window.removeEventListener('resize', checkScroll);
  }, [checkScroll]);

  useEffect(() => {
    let filtered = sampleProducts;

    // Apply category filter
    if (activeCategory === 1) {
      filtered = filtered.filter(product => product.discountedPrice);
    } else {
      filtered = filtered.filter(product => product.categoryId === activeCategory);
    }

    // Apply search filter
    if (searchQuery.trim()) {
      const searchTerm = searchQuery.toLowerCase().trim();
      filtered = filtered.filter(product => 
        product.name.toLowerCase().includes(searchTerm) || 
        product.description.toLowerCase().includes(searchTerm)
      );
    }

    // Apply price filter
    if (filters.priceRange) {
      filtered = filtered.filter(product => {
        const price = product.discountedPrice || product.price;
        if (filters.priceRange === "1000+") {
          return price >= 1000;
        }
        const [min, max] = filters.priceRange.split("-").map(Number);
        return price >= min && price <= max;
      });
    }

    // Apply rating filter
    if (filters.rating !== null) {
      filtered = filtered.filter(product => 
        Math.floor(product.rating) >= filters.rating!
      );
    }

    // Apply sorting
    filtered = [...filtered].sort((a, b) => {
      switch (sortBy) {
        case "price-low":
          return (a.discountedPrice || a.price) - (b.discountedPrice || b.price);
        case "price-high":
          return (b.discountedPrice || b.price) - (a.discountedPrice || a.price);
        case "newest":
          return new Date(b.date).getTime() - new Date(a.date).getTime();
        default:
          return b.rating - a.rating;
      }
    });

    setFilteredProducts(filtered);
  }, [activeCategory, searchQuery, filters, sortBy]);

  // Add this function
  const handleSearch = (query: string) => {
    setSearchQuery(query);
  };

  return (
    <div className="products-page">
      <Navbar onSearch={handleSearch} />
      
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

        {/* Banner Section */}
        <div className="banner-section">
          <div className="main-banner">
            {activeCategory === 1 ? (
              <>
                <h1>Black Friday Sale</h1>
                <p>Up to 50% off on selected items</p>
                <button className="shop-now-btn">Shop Now</button>
              </>
            ) : (
              <>
                <h1>{categories.find(c => c.id === activeCategory)?.name}</h1>
                <p>Discover our amazing collection</p>
                <button className="shop-now-btn">Explore Now</button>
              </>
            )}
          </div>
        </div>

        {/* Updated Filters Section */}
        <div className="filters-section">
          <div className="filter-buttons">
            {/* Price Filter */}
            <div className="filter-dropdown">
              <button 
                className="filter-btn" 
                onClick={() => toggleFilterDropdown('price')}
              >
                Price
                <span className="dropdown-arrow">
                  {showFilterDropdowns.price ? '▼' : '▶'}
                </span>
              </button>
              {showFilterDropdowns.price && (
                <div className="dropdown-content">
                  {priceRanges.map(range => (
                    <label key={range.value} className="filter-option">
                      <input
                        type="checkbox"
                        checked={filters.priceRange === range.value}
                        onChange={() => handlePriceFilter(range.value)}
                      />
                      {range.label}
                    </label>
                  ))}
                </div>
              )}
            </div>

            {/* Rating Filter */}
            <div className="filter-dropdown">
              <button 
                className="filter-btn" 
                onClick={() => toggleFilterDropdown('rating')}
              >
                Rating
                <span className="dropdown-arrow">
                  {showFilterDropdowns.rating ? '▼' : '▶'}
                </span>
              </button>
              {showFilterDropdowns.rating && (
                <div className="dropdown-content">
                  {ratingOptions.map(rating => (
                    <label key={rating} className="filter-option">
                      <input
                        type="checkbox"
                        checked={filters.rating === rating}
                        onChange={() => handleRatingFilter(rating)}
                      />
                      {rating}+ Stars
                    </label>
                  ))}
                </div>
              )}
            </div>
          </div>

          <div className="sort-section">
            <span>Sort by:</span>
            <select 
              className="sort-select"
              value={sortBy} 
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="popular">Most Popular</option>
              <option value="newest">Newest First</option>
              <option value="price-low">Price: Low to High</option>
              <option value="price-high">Price: High to Low</option>
            </select>
          </div>
        </div>

        {/* Section Title */}
        <h2 className="section-title">
          {activeCategory === 1 
            ? "Black Friday Deals!" 
            : `${categories.find(c => c.id === activeCategory)?.name} For You!`}
        </h2>

        {/* Products Grid */}
        <div className="products-grid">
          {filteredProducts.length > 0 ? (
            filteredProducts.map((product) => (
              <ProductCard 
                key={product.id} 
                {...product} 
              />
            ))
          ) : (
            <div className="no-products">
              <p>No products found matching your criteria.</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Products;