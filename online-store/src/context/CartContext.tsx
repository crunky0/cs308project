import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

export interface CartItem {
  productid: number;
  productname: string;
  price: number;
  stock: number;
  quantity: number;
  total_price: number;
}

export interface CartContextType {
  cart: CartItem[];
  total: number;
  addToCart: (productid: number, quantity?: number, userid?: number) => Promise<void>;
  removeFromCart: (productid: number, userid?: number) => Promise<void>;
  updateQuantity: (productid: number, increment: boolean, userid?: number) => Promise<void>;
  fetchCart: (userid?: number) => Promise<void>;
  clearCart: () => void;
  mergeGuestCart: (userid: number) => Promise<void>;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [total, setTotal] = useState<number>(0);

  // Helper to fetch product details
  const fetchProductDetails = useCallback(async (productId: number) => {
    try {
      const response = await fetch(`http://localhost:8000/products/${productId}/`);
      if (!response.ok) throw new Error('Product not found');
      return await response.json();
    } catch (error) {
      console.error('Error fetching product details:', error);
      throw error;
    }
  }, []);

  // Fetch cart (guest or logged-in)
  const fetchCart = useCallback(async (userid?: number) => {
    if (userid) {
      // Fetch logged-in user's cart from server
      try {
        const response = await fetch(`http://localhost:8000/cart?userid=${userid}`);
        if (!response.ok) throw new Error('Failed to fetch cart');
        const data = await response.json();
        setCartItems(prev => {
            if (JSON.stringify(prev) === JSON.stringify(data.cart || [])) {
                return prev; // Eğer veri değişmediyse state güncellenmesin.
            }
            return data.cart || [];
        });
        setTotal(data.total_cart_price || 0);
    } catch (error) {
        console.error('Error fetching cart:', error);
    }
    } else {
      // Fetch guest cart from localStorage
      const storedCart = JSON.parse(localStorage.getItem('guestCart') || '[]');
      try {
        const fullCart = await Promise.all(
          storedCart.map(async (item: { productid: number; quantity: number }) => {
            const productDetails = await fetchProductDetails(item.productid);
            return {
              ...productDetails,
              quantity: item.quantity,
              total_price: productDetails.price * item.quantity,
            };
          })
        );
        setCartItems(fullCart);
        setTotal(fullCart.reduce((acc, item) => acc + item.total_price, 0));
      } catch (error) {
        console.error('Error building full cart:', error);
      }
    }
  }, [fetchProductDetails]); // Include dependencies that could change
  

  // Add to cart
  const addToCart = async (productid: number, quantity = 1, userid?: number) => {
    if (userid) {
      try {
        const response = await fetch('http://localhost:8000/cart/add', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ userid, productid, quantity }),
        });
        if (!response.ok) throw new Error('Failed to add item to cart');
        await fetchCart(userid);
      } catch (error) {
        console.error('Error adding to cart:', error);
      }
    } else {
      const storedCart = JSON.parse(localStorage.getItem('guestCart') || '[]');
      const existingItem = storedCart.find((item: { productid: number }) => item.productid === productid);
      if (existingItem) {
        existingItem.quantity += quantity;
      } else {
        storedCart.push({ productid, quantity });
      }
      localStorage.setItem('guestCart', JSON.stringify(storedCart));
      await fetchCart();
    }
  };

  // Remove from cart
  const removeFromCart = async (productid: number, userid?: number) => {
    if (userid) {
      try {
        const response = await fetch(`http://localhost:8000/cart/remove?userid=${userid}&productid=${productid}`, {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ userid, productid }),
        });
        if (!response.ok) throw new Error('Failed to remove item from cart');
        await fetchCart(userid);
      } catch (error) {
        console.error('Error removing from cart:', error);
      }
    } else {
      const storedCart = JSON.parse(localStorage.getItem('guestCart') || '[]');
      const updatedCart = storedCart.filter((item: { productid: number }) => item.productid !== productid);
      localStorage.setItem('guestCart', JSON.stringify(updatedCart));
      await fetchCart();
    }
  };

  // Update quantity
  const updateQuantity = async (productid: number, increment: boolean, userid?: number) => {
    if (userid) {
      try {
        const endpoint = increment ? 'increase' : 'decrease';
        const response = await fetch(`http://localhost:8000/cart/${endpoint}?userid=${userid}&productid=${productid}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ userid, productid }),
        });
        if (!response.ok) throw new Error(`Failed to ${increment ? 'increase' : 'decrease'} quantity`);
        await fetchCart(userid);
      } catch (error) {
        console.error('Error updating quantity:', error);
      }
    } else {
      const storedCart = JSON.parse(localStorage.getItem('guestCart') || '[]');
      const existingItem = storedCart.find((item: { productid: number }) => item.productid === productid);
      if (existingItem) {
        existingItem.quantity += increment ? 1 : -1;
        if (existingItem.quantity <= 0) {
          await removeFromCart(productid);
        } else {
          localStorage.setItem('guestCart', JSON.stringify(storedCart));
          await fetchCart();
        }
      }
    }
  };

  // Clear cart
  const clearCart = () => {
    setCartItems([]);
    setTotal(0);
    localStorage.removeItem('guestCart');
  };

  // Merge guest cart with logged-in user cart
  const mergeGuestCart = async (userid: number) => {
    const guestCart = JSON.parse(localStorage.getItem('guestCart') || '[]');
    if (guestCart.length > 0) {
      try {
        for (const item of guestCart) {
          await fetch('http://localhost:8000/cart/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ userid, productid: item.productid, quantity: item.quantity }),
          });
        }
        localStorage.removeItem('guestCart'); // Clear guest cart after merging
        await fetchCart(userid);
      } catch (error) {
        console.error('Error merging guest cart:', error);
      }
    }
  };

  return (
    <CartContext.Provider
      value={{
        cart: cartItems,
        total,
        addToCart,
        removeFromCart,
        updateQuantity,
        fetchCart,
        clearCart,
        mergeGuestCart,
      }}
    >
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (context === undefined) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};