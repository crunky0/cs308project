import React, { createContext, useContext, useState } from 'react';

// Define User and AuthContext types
interface User {
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

// Create context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  // Login function
  const login = async (email: string, password: string) => {
    try {
      const response = await fetch('http://localhost:8000/users/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to login');
      }

      const data = await response.json();
      setUser({ email: data.user });
    } catch (error: any) {
      throw new Error(error.message);
    }
  };

  // Signup function
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
        headers: {
          'Content-Type': 'application/json',
        },
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

      setUser({ email });
    } catch (error: any) {
      throw new Error(error.message);
    }
  };

  // Logout function
  const logout = () => {
    setUser(null);
  };

  // Provide the context
  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        login,
        signup,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// Hook to use AuthContext
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
