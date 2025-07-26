import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { HelmetProvider, Helmet } from 'react-helmet-async';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import AuthPage from './components/Auth/AuthPage';
import LandingPage from './components/LandingPage';
import MainDashboard from './components/Dashboard/MainDashboard';
import StudentDashboard from './components/StudentDashboard';
import ParentDashboard from './components/ParentDashboard';
import TeacherDashboard from './components/TeacherDashboard';
import AdminDashboard from './components/AdminDashboard';
import ARIAAgent from './components/ARIAAgent';
import DocumentGenerator from './components/DocumentGenerator';
import ContentLibrary from './components/ContentLibrary';
import VideoConference from './components/VideoConference';
import ScheduleCalendar from './components/Calendar/ScheduleCalendar';
import QuizSystem from './components/QuizSystem';
import LearningPath from './components/LearningPath';
import TeacherProfiles from './components/TeacherProfiles';
import Gamification from './components/Gamification';
import ProgressTracking from './components/ProgressTracking';
import NotificationSystem from './components/NotificationSystem';
import DashboardLayout from './components/Layout/DashboardLayout';
import './App.css';

// Composant pour protéger les routes
function ProtectedRoute({ children, requiredRoles = [] }) {
  const { isAuthenticated, isLoading, user, hasRole } = useAuth();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/auth" replace />;
  }

  if (requiredRoles.length > 0 && !hasRole(requiredRoles)) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Accès non autorisé
          </h2>
          <p className="text-gray-600">
            Vous n'avez pas les permissions nécessaires pour accéder à cette page.
          </p>
        </div>
      </div>
    );
  }

  return children;
}

// Composant pour rediriger selon le rôle
function RoleBasedRedirect() {
  const { user, isStudent, isParent, isTeacher, isAdmin } = useAuth();

  if (isStudent()) {
    return <Navigate to="/dashboard" replace />;
  } else if (isParent()) {
    return <Navigate to="/dashboard" replace />;
  } else if (isTeacher()) {
    return <Navigate to="/dashboard" replace />;
  } else if (isAdmin()) {
    return <Navigate to="/dashboard" replace />;
  }

  return <Navigate to="/dashboard" replace />;
}

// Composant principal de l'application
function AppContent() {
  const { isAuthenticated, isLoading, checkAuthStatus } = useAuth();

  useEffect(() => {
    checkAuthStatus();
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement...</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <Helmet>
        <title>Nexus Réussite - Plateforme Éducative Intelligente</title>
        <meta name="description" content="Plateforme éducative avec IA pour l'accompagnement personnalisé des élèves du système français en Tunisie" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta httpEquiv="X-Content-Type-Options" content="nosniff" />
        <meta httpEquiv="X-Frame-Options" content="DENY" />
        <meta httpEquiv="X-XSS-Protection" content="1; mode=block" />
        <meta httpEquiv="Referrer-Policy" content="strict-origin-when-cross-origin" />
        <meta httpEquiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; style-src-elem 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self'; frame-ancestors 'none';" />
      </Helmet>
      <Router>
        <Routes>
        {/* Route publique - Page d'accueil */}
        <Route 
          path="/" 
          element={isAuthenticated ? <RoleBasedRedirect /> : <LandingPage />} 
        />
        
        {/* Route d'authentification */}
        <Route 
          path="/auth" 
          element={isAuthenticated ? <RoleBasedRedirect /> : <AuthPage />} 
        />

        {/* Routes protégées - Dashboard principal */}
        <Route 
          path="/dashboard" 
          element={
            <ProtectedRoute>
              <MainDashboard />
            </ProtectedRoute>
          } 
        />

        {/* Routes protégées - Dashboards spécifiques */}
        <Route 
          path="/student-dashboard" 
          element={
            <ProtectedRoute requiredRoles={['student']}>
              <DashboardLayout currentPage="dashboard">
                <StudentDashboard />
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/parent-dashboard" 
          element={
            <ProtectedRoute requiredRoles={['parent']}>
              <DashboardLayout currentPage="dashboard">
                <ParentDashboard />
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/teacher-dashboard" 
          element={
            <ProtectedRoute requiredRoles={['teacher']}>
              <DashboardLayout currentPage="dashboard">
                <TeacherDashboard />
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/admin-dashboard" 
          element={
            <ProtectedRoute requiredRoles={['admin']}>
              <DashboardLayout currentPage="dashboard">
                <AdminDashboard />
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        {/* Routes protégées - Fonctionnalités */}
        <Route 
          path="/aria" 
          element={
            <ProtectedRoute>
              <DashboardLayout currentPage="aria">
                <ARIAAgent />
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/documents" 
          element={
            <ProtectedRoute>
              <DashboardLayout currentPage="documents">
                <DocumentGenerator />
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/courses" 
          element={
            <ProtectedRoute>
              <DashboardLayout currentPage="courses">
                <ContentLibrary />
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/video" 
          element={
            <ProtectedRoute>
              <DashboardLayout currentPage="video">
                <VideoConference />
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/calendar" 
          element={
            <ProtectedRoute>
              <DashboardLayout currentPage="calendar">
                <ScheduleCalendar />
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/quiz/:quizId?" 
          element={
            <ProtectedRoute>
              <DashboardLayout currentPage="quiz">
                <QuizSystem />
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/learning-path/:subject?" 
          element={
            <ProtectedRoute>
              <DashboardLayout currentPage="learning">
                <LearningPath />
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/teachers" 
          element={
            <ProtectedRoute>
              <DashboardLayout currentPage="teachers">
                <TeacherProfiles />
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/gamification" 
          element={
            <ProtectedRoute>
              <DashboardLayout currentPage="gamification">
                <Gamification />
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/progress" 
          element={
            <ProtectedRoute>
              <DashboardLayout currentPage="progress">
                <ProgressTracking />
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/notifications" 
          element={
            <ProtectedRoute>
              <DashboardLayout currentPage="notifications">
                <NotificationSystem />
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        {/* Routes spécifiques aux enseignants */}
        <Route 
          path="/students" 
          element={
            <ProtectedRoute requiredRoles={['teacher']}>
              <DashboardLayout currentPage="students">
                <div className="text-center py-12">
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">
                    Gestion des élèves
                  </h2>
                  <p className="text-gray-600">
                    Interface de gestion des élèves en cours de développement.
                  </p>
                </div>
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/create-content" 
          element={
            <ProtectedRoute requiredRoles={['teacher']}>
              <DashboardLayout currentPage="create-content">
                <DocumentGenerator />
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        {/* Routes spécifiques aux parents */}
        <Route 
          path="/children" 
          element={
            <ProtectedRoute requiredRoles={['parent']}>
              <DashboardLayout currentPage="children">
                <div className="text-center py-12">
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">
                    Suivi des enfants
                  </h2>
                  <p className="text-gray-600">
                    Interface de suivi des enfants en cours de développement.
                  </p>
                </div>
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/reports" 
          element={
            <ProtectedRoute requiredRoles={['parent']}>
              <DashboardLayout currentPage="reports">
                <ProgressTracking />
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        {/* Routes spécifiques aux administrateurs */}
        <Route 
          path="/admin" 
          element={
            <ProtectedRoute requiredRoles={['admin']}>
              <DashboardLayout currentPage="admin">
                <AdminDashboard />
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/users" 
          element={
            <ProtectedRoute requiredRoles={['admin']}>
              <DashboardLayout currentPage="users">
                <div className="text-center py-12">
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">
                    Gestion des utilisateurs
                  </h2>
                  <p className="text-gray-600">
                    Interface de gestion des utilisateurs en cours de développement.
                  </p>
                </div>
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        <Route 
          path="/stats" 
          element={
            <ProtectedRoute requiredRoles={['admin']}>
              <DashboardLayout currentPage="stats">
                <div className="text-center py-12">
                  <h2 className="text-2xl font-bold text-gray-900 mb-4">
                    Statistiques
                  </h2>
                  <p className="text-gray-600">
                    Interface de statistiques en cours de développement.
                  </p>
                </div>
              </DashboardLayout>
            </ProtectedRoute>
          } 
        />

        {/* Route par défaut */}
        <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </>
  );
}

// Composant racine avec le provider d'authentification
function App() {
  return (
    <HelmetProvider>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </HelmetProvider>
  );
}

export default App;

