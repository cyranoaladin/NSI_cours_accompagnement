'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import useAuthStore from '../../../stores/authStore';

export default function TeacherDashboardPage() {
  const router = useRouter();
  const { isAuthenticated, user, isLoading } = useAuthStore();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/auth/login');
      return;
    }

    // Vérifier que l'utilisateur a le bon rôle
    if (user && user.role !== 'teacher') {
      router.push('/dashboard');
      return;
    }
  }, [isAuthenticated, user, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated || user?.role !== 'teacher') {
    return null; // Redirection en cours
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">Dashboard Enseignant</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">
                Bienvenue, {user?.firstName} {user?.lastName}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Mes Classes */}
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
                    <span className="text-white font-semibold">📚</span>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Mes Classes</dt>
                    <dd className="text-lg font-medium text-gray-900">3 classes actives</dd>
                  </dl>
                </div>
              </div>
            </div>
            <div className="bg-gray-50 px-5 py-3">
              <div className="text-sm">
                <button className="font-medium text-blue-600 hover:text-blue-500">
                  Gérer les classes →
                </button>
              </div>
            </div>
          </div>

          {/* Étudiants */}
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center">
                    <span className="text-white font-semibold">👥</span>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Étudiants</dt>
                    <dd className="text-lg font-medium text-gray-900">47 étudiants</dd>
                  </dl>
                </div>
              </div>
            </div>
            <div className="bg-gray-50 px-5 py-3">
              <div className="text-sm">
                <button className="font-medium text-green-600 hover:text-green-500">
                  Voir les étudiants →
                </button>
              </div>
            </div>
          </div>

          {/* Devoirs à Corriger */}
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-orange-500 rounded-md flex items-center justify-center">
                    <span className="text-white font-semibold">📝</span>
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">À Corriger</dt>
                    <dd className="text-lg font-medium text-gray-900">12 devoirs</dd>
                  </dl>
                </div>
              </div>
            </div>
            <div className="bg-gray-50 px-5 py-3">
              <div className="text-sm">
                <button className="font-medium text-orange-600 hover:text-orange-500">
                  Commencer les corrections →
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Actions Rapides */}
        <div className="mt-8">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Actions Rapides</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <button className="bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow">
              <div className="text-center">
                <div className="text-2xl mb-2">📋</div>
                <div className="text-sm font-medium text-gray-900">Créer un Quiz</div>
              </div>
            </button>
            <button className="bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow">
              <div className="text-center">
                <div className="text-2xl mb-2">📊</div>
                <div className="text-sm font-medium text-gray-900">Voir les Statistiques</div>
              </div>
            </button>
            <button className="bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow">
              <div className="text-center">
                <div className="text-2xl mb-2">💬</div>
                <div className="text-sm font-medium text-gray-900">Messages</div>
              </div>
            </button>
            <button className="bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow">
              <div className="text-center">
                <div className="text-2xl mb-2">📚</div>
                <div className="text-sm font-medium text-gray-900">Bibliothèque</div>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
