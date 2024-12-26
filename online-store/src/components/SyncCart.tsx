import { useEffect } from 'react';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';

const SyncCart = () => {
  const { mergeGuestCart, fetchCart } = useCart();
  const { user } = useAuth();

  useEffect(() => {
    const syncCart = async () => {
      if (user?.userid) {
        try {
          await mergeGuestCart(user.userid);
          await fetchCart(user.userid);
        } catch (error) {
          console.error('Error syncing cart:', error);
        }
      }
    };

    syncCart();
  }, [user, mergeGuestCart, fetchCart]);

  return null;
};

export default SyncCart;