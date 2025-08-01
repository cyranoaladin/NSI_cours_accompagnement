'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import StudentDashboard from '../../../components/StudentDashboard';
import useAuthStore from '../../../stores/authStore';

export default function StudentDashboardPage() {
  const router = useRouter();
  const { isAuthenticated, user, isLoading } = useAuthStore();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/auth/login');
      return;
    }

    // Vérifier que l'utilisateur a le bon rôle
    if (user && user.role !== 'student') {
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

  if (!isAuthenticated || user?.role !== 'student') {
    return null; // Redirection en cours
  }

  return <StudentDashboard />;
}
