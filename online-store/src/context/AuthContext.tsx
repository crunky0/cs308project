import React, {
  createContext,
  useContext,
  useState,
  useCallback,
  useMemo,
  useEffect
} from 'react';

// Define User and AuthContext types
interface User {
  userid: number;
  email: string;
  role: 'Customer' | 'Product Manager' | 'Sales Manager';
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

  useEffect(() => {
    const storedUser = sessionStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const login = useCallback(async (email: string, password: string) => {
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
      const user = {
        userid: data.user.userid,
        email: data.user.email,
        role: data.user.role,
      };
      setUser(user);
      sessionStorage.setItem('user', JSON.stringify(user));
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }, []); // Dependencies can be added if needed

  const signup = useCallback(async (
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

      const user = {
        userid: data.user.userid,
        email: data.user.email,
        role: data.user.role,
      };
      setUser(user);
      sessionStorage.setItem('user', JSON.stringify(user));
    } catch (error: any) {
      console.error("Signup error:", error.message);
      throw error;
    }
  }, []); // Dependencies can be added if needed

  const logout = useCallback(() => {
    setUser(null);
    sessionStorage.removeItem('user');
  }, []);

  const authValue = useMemo(() => ({
    user,
    isAuthenticated: !!user,
    login,
    signup,
    logout,
  }), [user, login, signup, logout]);

  return (
    <AuthContext.Provider value={authValue}>
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
