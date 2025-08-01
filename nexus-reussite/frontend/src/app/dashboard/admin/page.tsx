'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import AdminDashboard from '../../../components/AdminDashboard';
import useAuthStore from '../../../stores/authStore';

export default function AdminDashboardPage() {
  const router = useRouter();
  const { isAuthenticated, user, isLoading } = useAuthStore();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/auth/login');
      return;
    }

    // Vérifier que l'utilisateur a le bon rôle
    if (user && user.role !== 'admin') {
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

  if (!isAuthenticated || user?.role !== 'admin') {
    return null; // Redirection en cours
  }

  return <AdminDashboard />;
}
