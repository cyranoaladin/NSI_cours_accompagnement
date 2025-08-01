'use client';

import { Award, BookOpen, ChevronRight, Users, Zap } from 'lucide-react';
import Image from 'next/image';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import useAuthStore from '../stores/authStore';
import Header from './Header';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';

const LandingPage = () => {
  const router = useRouter();
  const { isAuthenticated, user } = useAuthStore();
  const [currentTestimonial, setCurrentTestimonial] = useState(0);

  const features = [
    {
      icon: BookOpen,
      title: 'Cours NSI Complets',
      description: 'Programme complet de Première et Terminale NSI avec exercices pratiques et projets.',
      color: 'bg-blue-100 text-blue-600',
    },
    {
      icon: Zap,
      title: 'Assistant IA ARIA',
      description: 'Intelligence artificielle personnalisée pour répondre à vos questions et vous accompagner.',
      color: 'bg-purple-100 text-purple-600',
    },
    {
      icon: Users,
      title: 'Suivi Personnalisé',
      description: 'Accompagnement individuel avec enseignants certifiés et suivi des parents.',
      color: 'bg-green-100 text-green-600',
    },
    {
      icon: Award,
      title: 'Préparation Examens',
      description: 'Entraînement spécialisé pour le Bac NSI avec sujets types et corrections détaillées.',
      color: 'bg-orange-100 text-orange-600',
    },
  ];

  const testimonials = [
    {
      name: 'Emma L.',
      grade: 'Terminale NSI',
      content: 'Grâce à Nexus Réussite, j\'ai obtenu 18/20 au Bac NSI ! L\'assistant ARIA m\'a beaucoup aidée.',
      rating: 5,
    },
    {
      name: 'Thomas M.',
      grade: 'Première NSI',
      content: 'Les cours sont très bien structurés et les exercices progressifs. Je recommande !',
      rating: 5,
    },
    {
      name: 'Sophie P.',
      grade: 'Mère d\'élève',
      content: 'Un suivi excellent, ma fille a retrouvé confiance en informatique.',
      rating: 5,
    },
  ];

  const stats = [
    { number: '500+', label: 'Élèves accompagnés' },
    { number: '18/20', label: 'Note moyenne au Bac' },
    { number: '95%', label: 'Taux de réussite' },
    { number: '24/7', label: 'Support disponible' },
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTestimonial((prev) => (prev + 1) % testimonials.length);
    }, 5000);
    return () => clearInterval(timer);
  }, [testimonials.length]);

  const handleGetStarted = () => {
    if (isAuthenticated) {
      if (user?.role === 'student') {
        router.push('/dashboard/student');
      } else if (user?.role === 'parent') {
        router.push('/dashboard/parent');
      } else if (user?.role === 'teacher') {
        router.push('/dashboard/teacher');
      } else {
        router.push('/dashboard');
      }
    } else {
      router.push('/auth/register');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Header onGetStarted={handleGetStarted} />

      <section className="container mx-auto px-4 py-20 text-center">
        <div className="max-w-4xl mx-auto">
          <Badge className="mb-6 bg-blue-100 text-blue-600 hover:bg-blue-200">
            🚀 Plateforme éducative NSI premium
          </Badge>

          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            Excellez en <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">NSI</span>
            <br />avec l'IA
          </h1>

          <p className="text-xl text-gray-600 mb-12 max-w-2xl mx-auto leading-relaxed">
            Plateforme d'accompagnement NSI révolutionnaire avec intelligence artificielle,
            pour réussir brillamment en Première et Terminale.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Button
              onClick={handleGetStarted}
              size="lg"
              className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 px-8 py-6 text-lg"
            >
              Commencer gratuitement
              <ChevronRight className="ml-2 h-5 w-5" />
            </Button>
          </div>
        </div>
      </section>

      <section className="bg-white py-16">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
                  {stat.number}
                </div>
                <div className="text-gray-600">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="features" className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Pourquoi choisir Nexus Réussite ?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Une approche innovante qui combine technologie de pointe et pédagogie experte
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow duration-300">
                <CardHeader>
                  <div className={`w-12 h-12 rounded-lg ${feature.color} flex items-center justify-center mb-4`}>
                    <feature.icon className="h-6 w-6" />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-gray-600 leading-relaxed">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="md:col-span-2">
              <div className="flex items-center space-x-3 mb-6">
                <div className="h-12 sm:h-16 w-auto">
                  <Image
                    src="/logo_nexus-reussite.webp"
                    alt="Nexus Réussite"
                    width={500}
                    height={165}
                    className="h-full w-auto object-contain"
                    priority
                    quality={100}
                  />
                </div>
                <div>
                  <h3 className="text-xl font-bold">Nexus Réussite</h3>
                  <p className="text-gray-400 text-sm">Formation d'Excellence NSI</p>
                </div>
              </div>
              <p className="text-gray-400 mb-4 max-w-md">
                Plateforme d'accompagnement NSI révolutionnaire avec intelligence artificielle
                pour réussir brillamment en Première et Terminale.
              </p>
            </div>

            <div>
              <h4 className="text-lg font-semibold mb-4">Navigation</h4>
              <ul className="space-y-2">
                <li><a href="#features" className="text-gray-400 hover:text-white transition-colors">Fonctionnalités</a></li>
                <li><a href="/auth/login" className="text-gray-400 hover:text-white transition-colors">Connexion</a></li>
                <li><a href="/auth/register" className="text-gray-400 hover:text-white transition-colors">S'inscrire</a></li>
              </ul>
            </div>

            <div>
              <h4 className="text-lg font-semibold mb-4">Contact</h4>
              <ul className="space-y-2">
                <li className="text-gray-400">Support 24/7</li>
                <li className="text-gray-400">contact@nexus-reussite.fr</li>
                <li className="text-gray-400">+33 1 23 45 67 89</li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-700 mt-8 pt-8 text-center">
            <p className="text-gray-400">
              © 2025 Nexus Réussite. Tous droits réservés.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
