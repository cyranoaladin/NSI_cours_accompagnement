import React, { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  User, 
  Bell, 
  Settings, 
  LogOut, 
  Moon, 
  Sun, 
  Menu, 
  X,
  Home,
  BookOpen,
  FileText,
  Trophy,
  MessageCircle,
  BarChart3,
  Users,
  Brain
} from 'lucide-react'

const Header = ({ 
  currentUser, 
  userType, 
  setUserType, 
  setCurrentUser, 
  darkMode, 
  toggleDarkMode,
  onShowARIA 
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);

  const navigationItems = {
    guest: [
      { label: 'Accueil', href: '/', icon: Home },
      { label: 'Nos Offres', href: '#offres', icon: BookOpen },
      { label: 'Enseignants', href: '#enseignants', icon: Users },
      { label: 'Contact', href: '#contact', icon: MessageCircle }
    ],
    student: [
      { label: 'Tableau de Bord', href: '/dashboard', icon: Home },
      { label: 'Mes Documents', href: '/documents', icon: FileText },
      { label: 'Mes Badges', href: '/gamification', icon: Trophy },
      { label: 'ARIA', href: '#', icon: Brain, onClick: onShowARIA }
    ],
    parent: [
      { label: 'Dashboard Parent', href: '/dashboard', icon: BarChart3 },
      { label: 'Documents', href: '/documents', icon: FileText },
      { label: 'Communication', href: '#messages', icon: MessageCircle },
      { label: 'Rapports', href: '#reports', icon: BarChart3 }
    ],
    teacher: [
      { label: 'Dashboard Prof', href: '/dashboard', icon: Home },
      { label: 'Mes Élèves', href: '#students', icon: Users },
      { label: 'Générateur', href: '/documents', icon: FileText },
      { label: 'Statistiques', href: '#stats', icon: BarChart3 }
    ]
  };

  const handleLogin = (type) => {
    setUserType(type);
    if (type === 'student') {
      setCurrentUser({
        id: 'demo_student',
        name: 'Sarah Benali',
        avatar: 'SB',
        grade: 'Terminale S'
      });
    } else if (type === 'parent') {
      setCurrentUser({
        id: 'demo_parent',
        name: 'M. Benali',
        avatar: 'MB'
      });
    } else if (type === 'teacher') {
      setCurrentUser({
        id: 'demo_teacher',
        name: 'M. Dubois',
        avatar: 'MD'
      });
    }
    setMobileMenuOpen(false);
  };

  const handleLogout = () => {
    setUserType('guest');
    setCurrentUser(null);
    setUserMenuOpen(false);
  };

  const currentNavItems = navigationItems[userType] || navigationItems.guest;

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-background/95 backdrop-blur-sm border-b border-border">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 nexus-gradient rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">N</span>
            </div>
            <div>
              <h1 className="text-xl font-bold nexus-gradient-text">Nexus Réussite</h1>
              <p className="text-xs text-muted-foreground">Formation d'Excellence</p>
            </div>
          </div>

          {/* Navigation Desktop */}
          <nav className="hidden md:flex items-center space-x-6">
            {currentNavItems.map((item, index) => (
              <a
                key={index}
                href={item.href}
                onClick={item.onClick}
                className="flex items-center space-x-2 text-foreground hover:text-primary transition-colors duration-200 px-3 py-2 rounded-lg hover:bg-muted"
              >
                <item.icon className="w-4 h-4" />
                <span className="font-medium">{item.label}</span>
              </a>
            ))}
          </nav>

          {/* Actions Desktop */}
          <div className="hidden md:flex items-center space-x-4">
            {/* Bouton ARIA pour les utilisateurs connectés */}
            {userType !== 'guest' && (
              <Button
                variant="outline"
                size="sm"
                onClick={onShowARIA}
                className="flex items-center space-x-2"
              >
                <Brain className="w-4 h-4" />
                <span>ARIA</span>
              </Button>
            )}

            {/* Toggle Dark Mode */}
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleDarkMode}
              className="w-9 h-9 p-0"
            >
              {darkMode ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </Button>

            {/* Notifications */}
            {userType !== 'guest' && (
              <Button variant="ghost" size="sm" className="w-9 h-9 p-0 relative">
                <Bell className="w-4 h-4" />
                <Badge className="absolute -top-1 -right-1 w-5 h-5 p-0 flex items-center justify-center text-xs bg-red-500">
                  3
                </Badge>
              </Button>
            )}

            {/* User Menu ou Login */}
            {currentUser ? (
              <div className="relative">
                <Button
                  variant="ghost"
                  onClick={() => setUserMenuOpen(!userMenuOpen)}
                  className="flex items-center space-x-2 px-3"
                >
                  <div className="w-8 h-8 nexus-avatar bg-primary text-primary-foreground text-sm">
                    {currentUser.avatar}
                  </div>
                  <div className="text-left">
                    <p className="text-sm font-medium">{currentUser.name}</p>
                    <p className="text-xs text-muted-foreground capitalize">{userType}</p>
                  </div>
                </Button>

                {userMenuOpen && (
                  <div className="absolute right-0 top-full mt-2 w-48 bg-card border border-border rounded-lg shadow-lg py-2">
                    <a href="#profile" className="flex items-center space-x-2 px-4 py-2 hover:bg-muted">
                      <User className="w-4 h-4" />
                      <span>Mon Profil</span>
                    </a>
                    <a href="#settings" className="flex items-center space-x-2 px-4 py-2 hover:bg-muted">
                      <Settings className="w-4 h-4" />
                      <span>Paramètres</span>
                    </a>
                    <hr className="my-2 border-border" />
                    <button
                      onClick={handleLogout}
                      className="flex items-center space-x-2 px-4 py-2 hover:bg-muted w-full text-left text-red-600"
                    >
                      <LogOut className="w-4 h-4" />
                      <span>Déconnexion</span>
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleLogin('student')}
                >
                  Élève
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleLogin('parent')}
                >
                  Parent
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleLogin('teacher')}
                >
                  Professeur
                </Button>
              </div>
            )}
          </div>

          {/* Menu Mobile */}
          <div className="md:hidden">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="w-9 h-9 p-0"
            >
              {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </Button>
          </div>
        </div>

        {/* Menu Mobile Ouvert */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-border bg-background">
            <div className="py-4 space-y-2">
              {/* Navigation Mobile */}
              {currentNavItems.map((item, index) => (
                <a
                  key={index}
                  href={item.href}
                  onClick={item.onClick}
                  className="flex items-center space-x-3 px-4 py-3 hover:bg-muted rounded-lg mx-2"
                >
                  <item.icon className="w-5 h-5" />
                  <span className="font-medium">{item.label}</span>
                </a>
              ))}

              {/* Actions Mobile */}
              <div className="px-4 pt-4 border-t border-border mt-4">
                {currentUser ? (
                  <div className="space-y-3">
                    <div className="flex items-center space-x-3 px-2">
                      <div className="w-10 h-10 nexus-avatar bg-primary text-primary-foreground">
                        {currentUser.avatar}
                      </div>
                      <div>
                        <p className="font-medium">{currentUser.name}</p>
                        <p className="text-sm text-muted-foreground capitalize">{userType}</p>
                      </div>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={toggleDarkMode}
                        className="flex items-center space-x-2"
                      >
                        {darkMode ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
                        <span>{darkMode ? 'Mode Clair' : 'Mode Sombre'}</span>
                      </Button>
                      
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={onShowARIA}
                        className="flex items-center space-x-2"
                      >
                        <Brain className="w-4 h-4" />
                        <span>ARIA</span>
                      </Button>
                    </div>
                    
                    <Button
                      variant="outline"
                      onClick={handleLogout}
                      className="w-full flex items-center space-x-2 text-red-600"
                    >
                      <LogOut className="w-4 h-4" />
                      <span>Déconnexion</span>
                    </Button>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <p className="text-sm font-medium mb-3">Se connecter en tant que :</p>
                    <Button
                      variant="outline"
                      onClick={() => handleLogin('student')}
                      className="w-full justify-start"
                    >
                      <User className="w-4 h-4 mr-2" />
                      Élève
                    </Button>
                    <Button
                      variant="outline"
                      onClick={() => handleLogin('parent')}
                      className="w-full justify-start"
                    >
                      <Users className="w-4 h-4 mr-2" />
                      Parent
                    </Button>
                    <Button
                      variant="outline"
                      onClick={() => handleLogin('teacher')}
                      className="w-full justify-start"
                    >
                      <BookOpen className="w-4 h-4 mr-2" />
                      Professeur
                    </Button>
                    
                    <div className="pt-3 border-t border-border">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={toggleDarkMode}
                        className="w-full flex items-center space-x-2"
                      >
                        {darkMode ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
                        <span>{darkMode ? 'Mode Clair' : 'Mode Sombre'}</span>
                      </Button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;

