import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import StudentDashboard from '../StudentDashboard';
import ParentDashboard from '../ParentDashboard';
import TeacherDashboard from '../TeacherDashboard';
import AdminDashboard from '../AdminDashboard';
import DashboardLayout from '../Layout/DashboardLayout';

export default function MainDashboard() {
  const { user, isStudent, isParent, isTeacher, isAdmin } = useAuth();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simuler le chargement des données
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center min-h-96">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Chargement de votre tableau de bord...</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  const renderDashboard = () => {
    if (isStudent()) {
      return <StudentDashboard />;
    } else if (isParent()) {
      return <ParentDashboard />;
    } else if (isTeacher()) {
      return <TeacherDashboard />;
    } else if (isAdmin()) {
      return <AdminDashboard />;
    } else {
      return (
        <div className="text-center py-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Rôle non reconnu
          </h2>
          <p className="text-gray-600">
            Votre rôle utilisateur n'est pas reconnu. Veuillez contacter l'administrateur.
          </p>
        </div>
      );
    }
  };

  return (
    <DashboardLayout currentPage="dashboard">
      {renderDashboard()}
    </DashboardLayout>
  );
}

