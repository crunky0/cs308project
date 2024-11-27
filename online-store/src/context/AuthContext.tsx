import React, { createContext, useContext, useState } from 'react';

interface User {
  email: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Mock kullanıcı listesi
const mockUsers: { email: string; password: string }[] = [];

export const AuthProvider: React.FC<React.PropsWithChildren<{}>> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  const login = async (email: string, password: string) => {
    return new Promise<void>((resolve, reject) => {
      const existingUser = mockUsers.find(
        (user) => user.email === email && user.password === password
      );
      if (existingUser) {
        setUser({ email });
        resolve();
      } else {
        reject(new Error('Invalid email or password'));
      }
    });
  };

  const signup = async (email: string, password: string) => {
    return new Promise<void>((resolve, reject) => {
      const existingUser = mockUsers.find((user) => user.email === email);
      if (existingUser) {
        reject(new Error('User already exists'));
      } else {
        mockUsers.push({ email, password });
        setUser({ email });
        resolve();
      }
    });
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user, // Kullanıcı varsa true, yoksa false
        login,
        signup,
        logout,
      }}
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
