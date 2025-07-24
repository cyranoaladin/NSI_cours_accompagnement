import React, { useState } from 'react';
import { 
  Menu, 
  X, 
  Home, 
  User, 
  BookOpen, 
  MessageSquare, 
  Video, 
  FileText, 
  Settings, 
  LogOut,
  Bell,
  Search
} from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import Logo from '../Logo';
import NotificationSystem from '../NotificationSystem';

export default function DashboardLayout({ children, currentPage = 'dashboard' }) {
  const { user, logout, isStudent, isParent, isTeacher, isAdmin } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [notificationsOpen, setNotificationsOpen] = useState(false);

  const navigation = [
    { name: 'Tableau de bord', href: '/dashboard', icon: Home, current: currentPage === 'dashboard' },
    { name: 'Mon profil', href: '/profile', icon: User, current: currentPage === 'profile' },
    { name: 'Cours & Contenus', href: '/courses', icon: BookOpen, current: currentPage === 'courses' },
    { name: 'ARIA Assistant', href: '/aria', icon: MessageSquare, current: currentPage === 'aria' },
    { name: 'Visioconférence', href: '/video', icon: Video, current: currentPage === 'video' },
    { name: 'Documents', href: '/documents', icon: FileText, current: currentPage === 'documents' },
  ];

  // Navigation spécifique selon le rôle
  if (isTeacher()) {
    navigation.push(
      { name: 'Mes élèves', href: '/students', icon: User, current: currentPage === 'students' },
      { name: 'Créer contenu', href: '/create-content', icon: FileText, current: currentPage === 'create-content' }
    );
  }

  if (isParent()) {
    navigation.push(
      { name: 'Suivi enfants', href: '/children', icon: User, current: currentPage === 'children' },
      { name: 'Rapports', href: '/reports', icon: FileText, current: currentPage === 'reports' }
    );
  }

  if (isAdmin()) {
    navigation.push(
      { name: 'Administration', href: '/admin', icon: Settings, current: currentPage === 'admin' },
      { name: 'Utilisateurs', href: '/users', icon: User, current: currentPage === 'users' },
      { name: 'Statistiques', href: '/stats', icon: FileText, current: currentPage === 'stats' }
    );
  }

  const handleLogout = async () => {
    await logout();
    window.location.href = '/';
  };

  const userInitials = user ? `${user.first_name?.[0] || ''}${user.last_name?.[0] || ''}` : 'U';
  const userName = user ? `${user.first_name || ''} ${user.last_name || ''}`.trim() : 'Utilisateur';

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar mobile */}
      <div className={`fixed inset-0 flex z-40 md:hidden ${sidebarOpen ? '' : 'hidden'}`}>
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setSidebarOpen(false)} />
        
        <div className="relative flex-1 flex flex-col max-w-xs w-full bg-white">
          <div className="absolute top-0 right-0 -mr-12 pt-2">
            <button
              type="button"
              className="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
              onClick={() => setSidebarOpen(false)}
            >
              <X className="h-6 w-6 text-white" />
            </button>
          </div>
          
          <div className="flex-1 h-0 pt-5 pb-4 overflow-y-auto">
            <div className="flex-shrink-0 flex items-center px-4">
              <Logo className="h-8 w-auto" />
            </div>
            <nav className="mt-5 px-2 space-y-1">
              {navigation.map((item) => (
                <a
                  key={item.name}
                  href={item.href}
                  className={`${
                    item.current
                      ? 'bg-blue-100 text-blue-900'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  } group flex items-center px-2 py-2 text-base font-medium rounded-md`}
                >
                  <item.icon
                    className={`${
                      item.current ? 'text-blue-500' : 'text-gray-400 group-hover:text-gray-500'
                    } mr-4 flex-shrink-0 h-6 w-6`}
                  />
                  {item.name}
                </a>
              ))}
            </nav>
          </div>
          
          <div className="flex-shrink-0 flex border-t border-gray-200 p-4">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="h-10 w-10 rounded-full bg-blue-500 flex items-center justify-center text-white font-medium">
                  {userInitials}
                </div>
              </div>
              <div className="ml-3">
                <p className="text-base font-medium text-gray-700">{userName}</p>
                <p className="text-sm font-medium text-gray-500 capitalize">{user?.role}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Sidebar desktop */}
      <div className="hidden md:flex md:w-64 md:flex-col md:fixed md:inset-y-0">
        <div className="flex-1 flex flex-col min-h-0 border-r border-gray-200 bg-white">
          <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
            <div className="flex items-center flex-shrink-0 px-4">
              <Logo className="h-8 w-auto" />
            </div>
            <nav className="mt-5 flex-1 px-2 bg-white space-y-1">
              {navigation.map((item) => (
                <a
                  key={item.name}
                  href={item.href}
                  className={`${
                    item.current
                      ? 'bg-blue-100 text-blue-900'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  } group flex items-center px-2 py-2 text-sm font-medium rounded-md`}
                >
                  <item.icon
                    className={`${
                      item.current ? 'text-blue-500' : 'text-gray-400 group-hover:text-gray-500'
                    } mr-3 flex-shrink-0 h-6 w-6`}
                  />
                  {item.name}
                </a>
              ))}
            </nav>
          </div>
          
          <div className="flex-shrink-0 flex border-t border-gray-200 p-4">
            <div className="flex items-center w-full">
              <div className="flex-shrink-0">
                <div className="h-10 w-10 rounded-full bg-blue-500 flex items-center justify-center text-white font-medium">
                  {userInitials}
                </div>
              </div>
              <div className="ml-3 flex-1">
                <p className="text-sm font-medium text-gray-700">{userName}</p>
                <p className="text-xs font-medium text-gray-500 capitalize">{user?.role}</p>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={handleLogout}
                className="ml-2"
              >
                <LogOut className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Contenu principal */}
      <div className="md:pl-64 flex flex-col flex-1">
        {/* Header */}
        <div className="sticky top-0 z-10 md:hidden pl-1 pt-1 sm:pl-3 sm:pt-3 bg-gray-50">
          <button
            type="button"
            className="-ml-0.5 -mt-0.5 h-12 w-12 inline-flex items-center justify-center rounded-md text-gray-500 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu className="h-6 w-6" />
          </button>
        </div>

        {/* Barre de navigation supérieure */}
        <div className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <div className="hidden md:block">
                  <div className="ml-4 flex items-center md:ml-6">
                    <div className="relative">
                      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <Search className="h-5 w-5 text-gray-400" />
                      </div>
                      <Input
                        type="text"
                        placeholder="Rechercher..."
                        className="pl-10 pr-4 py-2 w-64"
                      />
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="flex items-center">
                {/* Notifications */}
                <div className="relative">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setNotificationsOpen(!notificationsOpen)}
                    className="relative"
                  >
                    <Bell className="h-6 w-6" />
                    <span className="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                      3
                    </span>
                  </Button>
                  
                  {notificationsOpen && (
                    <div className="absolute right-0 mt-2 w-80 bg-white rounded-md shadow-lg ring-1 ring-black ring-opacity-5 z-50">
                      <NotificationSystem />
                    </div>
                  )}
                </div>

                {/* Profil utilisateur (mobile) */}
                <div className="ml-3 md:hidden">
                  <div className="flex items-center">
                    <div className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center text-white font-medium text-sm">
                      {userInitials}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Contenu de la page */}
        <main className="flex-1">
          <div className="py-6">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              {children}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

