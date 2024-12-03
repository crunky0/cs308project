import React, { createContext, useContext, useState } from 'react';
import { useCart } from './CartContext';

// Define User and AuthContext types
interface User {
  userid: number;
  email: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (
    email: string,
    password: string,
    name: string,
    surname: string,
    taxID: string,
    homeAddress: string
  ) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  const login = async (email: string, password: string) => {
    try {
      const response = await fetch('http://localhost:8000/users/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: email, password }),
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to login');
      }
  
      const data = await response.json();
      setUser({ userid: data.user.userid, email: data.user.email });
    } catch (error) {
      console.error('Login error:', error);
      throw new Error();
    }
  };  

  const signup = async (
    email: string,
    password: string,
    name: string,
    surname: string,
    taxID: string,
    homeAddress: string
  ) => {
    try {
      const response = await fetch('http://localhost:8000/users/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: email,
          password,
          name,
          surname,
          email,
          taxID,
          homeAddress,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to sign up');
      }

      const data = await response.json();
      console.log("Signup response data:", data); // Debugging line

      setUser({ userid: data.user.userid, email: data.user.email });
    } catch (error: any) {
      console.error("Signup error:", error.message);
      throw new Error(error.message);
    }
  };

  const logout = () => setUser(null);

  return (
    <AuthContext.Provider
      value={{ user, isAuthenticated: !!user, login, signup, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};