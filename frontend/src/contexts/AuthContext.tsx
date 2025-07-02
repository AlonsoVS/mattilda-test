import { createContext, useContext, type ReactNode } from 'react';
import { useAuth as useAuthHook } from '../hooks';
import type { LoginRequest } from '../types';

interface AuthContextType {
  user: any | null;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => Promise<void>;
  loading: boolean;
  error: string | null;
  isAuthenticated: boolean;
  register: (userData: any) => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  // Use the custom hook that manages all auth state
  const authHook = useAuthHook();

  // Wrapper function to adapt the login interface
  const login = async (username: string, password: string): Promise<boolean> => {
    const credentials: LoginRequest = { username, password };
    return authHook.login(credentials);
  };

  const contextValue: AuthContextType = {
    user: authHook.user,
    login,
    logout: authHook.logout,
    loading: authHook.loading,
    error: authHook.error,
    isAuthenticated: authHook.isAuthenticated,
    register: authHook.register,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};
