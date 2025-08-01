'use client';

import Image from 'next/image';
import { useRouter } from 'next/navigation';
import useAuthStore from '../stores/authStore';
import { Button } from './ui/button';

const Header = ({ onGetStarted }) => {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();

  return (
    <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50 h-20">
      <div className="container mx-auto px-4 h-full flex items-center justify-between">
        {/* Logo Section */}
        <div className="flex items-center space-x-2 h-full">
          <div className="w-auto" style={{ height: '60px' }}>
            <Image
              src="/logo_nexus-reussite.webp"
              alt="Nexus Réussite"
              width={500}
              height={165}
              className="w-auto object-contain transition-all duration-200 hover:scale-105"
              priority
              quality={100}
              style={{ height: '60px' }}
            />
          </div>
          <span className="text-xl font-bold text-gray-900">Nexus Réussite</span>
        </div>

        {/* Navigation Section */}
        <div className="flex items-center space-x-4">
          {isAuthenticated ? (
            <Button
              onClick={() => router.push('/dashboard')}
              className="bg-blue-600 hover:bg-blue-700"
            >
              Tableau de bord
            </Button>
          ) : (
            <>
              <Button
                variant="ghost"
                onClick={() => router.push('/auth/login')}
              >
                Connexion
              </Button>
              <Button
                onClick={onGetStarted}
                className="bg-blue-600 hover:bg-blue-700"
              >
                Commencer
              </Button>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
