import React, { useState } from 'react';
import { Eye, EyeOff, Mail, Lock, AlertCircle } from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import Logo from '../Logo';

export default function LoginForm({ onSwitchToRegister }) {
  const { login, isLoading, error, clearError } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [formErrors, setFormErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Effacer les erreurs lors de la saisie
    if (formErrors[name]) {
      setFormErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
    
    if (error) {
      clearError();
    }
  };

  const validateForm = () => {
    const errors = {};
    
    if (!formData.email) {
      errors.email = 'L\'email est requis';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'Format d\'email invalide';
    }
    
    if (!formData.password) {
      errors.password = 'Le mot de passe est requis';
    } else if (formData.password.length < 6) {
      errors.password = 'Le mot de passe doit contenir au moins 6 caractères';
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    const result = await login(formData.email, formData.password);
    
    if (result.success) {
      // Redirection gérée par le contexte d'authentification
      console.log('Connexion réussie');
    }
  };

  const handleDemoLogin = async (role) => {
    const demoAccounts = {
      student: { email: 'sarah@demo.nexusreussite.tn', password: 'demo123' },
      parent: { email: 'parent.sarah@demo.nexusreussite.tn', password: 'demo123' },
      teacher: { email: 'prof.dubois@demo.nexusreussite.tn', password: 'demo123' },
      admin: { email: 'admin@demo.nexusreussite.tn', password: 'demo123' }
    };
    
    const account = demoAccounts[role];
    if (account) {
      setFormData(account);
      await login(account.email, account.password);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Logo et titre */}
        <div className="text-center">
          <div className="flex justify-center mb-6">
            <Logo className="h-16 w-auto" />
          </div>
          <h2 className="text-3xl font-bold text-gray-900">
            Connexion à votre espace
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Accédez à votre tableau de bord personnalisé
          </p>
        </div>

        <Card className="shadow-xl">
          <CardHeader className="space-y-1">
            <CardTitle className="text-2xl text-center">Se connecter</CardTitle>
            <CardDescription className="text-center">
              Entrez vos identifiants pour accéder à votre compte
            </CardDescription>
          </CardHeader>
          
          <CardContent className="space-y-4">
            {/* Erreur générale */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-md p-4">
                <div className="flex">
                  <AlertCircle className="h-5 w-5 text-red-400" />
                  <div className="ml-3">
                    <p className="text-sm text-red-800">{error}</p>
                  </div>
                </div>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Email */}
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                  Adresse email
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Mail className="h-5 w-5 text-gray-400" />
                  </div>
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    value={formData.email}
                    onChange={handleChange}
                    className={`pl-10 ${formErrors.email ? 'border-red-300' : ''}`}
                    placeholder="votre@email.com"
                  />
                </div>
                {formErrors.email && (
                  <p className="mt-1 text-sm text-red-600">{formErrors.email}</p>
                )}
              </div>

              {/* Mot de passe */}
              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                  Mot de passe
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Lock className="h-5 w-5 text-gray-400" />
                  </div>
                  <Input
                    id="password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    autoComplete="current-password"
                    value={formData.password}
                    onChange={handleChange}
                    className={`pl-10 pr-10 ${formErrors.password ? 'border-red-300' : ''}`}
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-3 flex items-center"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? (
                      <EyeOff className="h-5 w-5 text-gray-400" />
                    ) : (
                      <Eye className="h-5 w-5 text-gray-400" />
                    )}
                  </button>
                </div>
                {formErrors.password && (
                  <p className="mt-1 text-sm text-red-600">{formErrors.password}</p>
                )}
              </div>

              {/* Options */}
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <input
                    id="remember-me"
                    name="remember-me"
                    type="checkbox"
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-900">
                    Se souvenir de moi
                  </label>
                </div>

                <div className="text-sm">
                  <a href="#" className="font-medium text-blue-600 hover:text-blue-500">
                    Mot de passe oublié ?
                  </a>
                </div>
              </div>

              {/* Bouton de connexion */}
              <Button
                type="submit"
                className="w-full"
                disabled={isLoading}
              >
                {isLoading ? (
                  <div className="flex items-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Connexion en cours...
                  </div>
                ) : (
                  'Se connecter'
                )}
              </Button>
            </form>

            {/* Comptes de démonstration */}
            <div className="mt-6">
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-300" />
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-white text-gray-500">Comptes de démonstration</span>
                </div>
              </div>

              <div className="mt-4 grid grid-cols-2 gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleDemoLogin('student')}
                  disabled={isLoading}
                >
                  Élève
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleDemoLogin('parent')}
                  disabled={isLoading}
                >
                  Parent
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleDemoLogin('teacher')}
                  disabled={isLoading}
                >
                  Enseignant
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleDemoLogin('admin')}
                  disabled={isLoading}
                >
                  Admin
                </Button>
              </div>
            </div>

            {/* Lien vers l'inscription */}
            <div className="text-center">
              <p className="text-sm text-gray-600">
                Pas encore de compte ?{' '}
                <button
                  type="button"
                  onClick={onSwitchToRegister}
                  className="font-medium text-blue-600 hover:text-blue-500"
                >
                  Créer un compte
                </button>
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Informations supplémentaires */}
        <div className="text-center">
          <p className="text-xs text-gray-500">
            En vous connectant, vous acceptez nos{' '}
            <a href="#" className="text-blue-600 hover:text-blue-500">
              Conditions d'utilisation
            </a>{' '}
            et notre{' '}
            <a href="#" className="text-blue-600 hover:text-blue-500">
              Politique de confidentialité
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}

