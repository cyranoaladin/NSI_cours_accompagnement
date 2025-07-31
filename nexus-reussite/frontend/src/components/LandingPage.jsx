import { Badge } from '@/components/ui/badge.jsx';
import { Button } from '@/components/ui/button.jsx';
import { Card } from '@/components/ui/card.jsx';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx';
import {
  Atom,
  Award,
  BookOpen,
  Brain,
  Calculator,
  Calendar,
  Car,
  CheckCircle,
  Clock,
  Code2,
  Coffee,
  Eye,
  Facebook,
  Globe,
  GraduationCap,
  Instagram,
  Lightbulb,
  Linkedin,
  Mail,
  MapPin,
  Menu,
  MessageCircle,
  Monitor,
  Navigation,
  PenTool,
  Phone,
  Play,
  Presentation,
  Quote,
  Rocket,
  Shield,
  Sparkles,
  Star,
  Target,
  TrendingUp,
  Trophy,
  Users,
  X,
  Youtube
} from 'lucide-react';
import { useEffect, useState } from 'react';
import Logo from './Logo';

const LandingPage = ({ onLogin }) => {
  const [activeTab, setActiveTab] = useState('individuel');
  const [currentTestimonial, setCurrentTestimonial] = useState(0);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const testimonials = [
    {
      name: 'Sarah M.',
      grade: 'Terminale S - Mention TB',
      avatar: 'S',
      text: 'ARIA m\'a aidée à comprendre mes points faibles en maths. Les cours avec M. Dubois et les exercices personnalisés m\'ont permis de passer de 12 à 18 de moyenne !',
      rating: 5
    },
    {
      name: 'Mme Benali',
      role: 'Mère d\'élève',
      avatar: 'M',
      text: 'L\'interface parent est fantastique ! Je peux suivre les progrès de mon fils en temps réel. Les rapports hebdomadaires sont très détaillés et rassurants.',
      rating: 5
    },
    {
      name: 'Ahmed K.',
      grade: 'Terminale NSI - Admis Polytechnique',
      avatar: 'A',
      text: 'Les cours de NSI avec des profs diplômés DIU font toute la différence. J\'ai pu intégrer Polytechnique grâce à leur préparation d\'excellence !',
      rating: 5
    }
  ];

  const teachers = [
    {
      id: 'dubois',
      name: 'M. Dubois',
      subject: 'Mathématiques',
      credentials: 'Agrégé de Mathématiques',
      experience: '15 ans d\'expérience AEFE',
      specialties: ['Spécialiste Terminale S'],
      rating: 4.9,
      avatar: 'MD',
      badge: 'Expert',
      description: 'Expert en préparation aux concours d\'ingénieurs et spécialiste des mathématiques avancées. Accompagne les élèves vers l\'excellence avec une pédagogie adaptée.'
    },
    {
      id: 'martin',
      name: 'Mme Martin',
      subject: 'NSI',
      credentials: 'Diplômée DIU NSI',
      experience: 'Expert Python & Algorithmique',
      specialties: ['Préparation Grand Oral'],
      rating: 4.8,
      avatar: 'MM',
      badge: 'DIU NSI',
      description: 'Spécialisée en NSI avec une approche pratique et moderne. Accompagne les élèves dans leurs projets et les prépare aux études supérieures en informatique.'
    },
    {
      id: 'rousseau',
      name: 'Dr. Rousseau',
      subject: 'Français & Grand Oral',
      credentials: 'Expert en éloquence',
      experience: 'Spécialiste Parcoursup',
      specialties: ['Coach en développement personnel'],
      rating: 5.0,
      avatar: 'DR',
      badge: 'Grand Oral',
      description: 'Docteur en Sciences de l\'Éducation, spécialisé dans l\'orientation et la préparation au Grand Oral. Accompagne les élèves dans leur projet d\'avenir.'
    }
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTestimonial((prev) => (prev + 1) % testimonials.length);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const scrollToSection = (sectionId) => {
    document.getElementById(sectionId)?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-white/95 header-blur border-b border-gray-200/50 shadow-sm">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center">
              <Logo size="small" className="h-10" />
            </div>

            {/* Navigation */}
            <nav className="hidden md:flex items-center space-x-8">
              <a href="#formations" className="nav-link text-gray-700 hover:text-blue-600 font-medium transition-colors">
                Formations
              </a>
              <a href="#professeurs" className="nav-link text-gray-700 hover:text-blue-600 font-medium transition-colors">
                Professeurs
              </a>
              <a href="#temoignages" className="nav-link text-gray-700 hover:text-blue-600 font-medium transition-colors">
                Témoignages
              </a>
              <a href="#contact" className="nav-link text-gray-700 hover:text-blue-600 font-medium transition-colors">
                Contact
              </a>
            </nav>

            {/* Actions Desktop */}
            <div className="hidden md:flex items-center space-x-4">
              <Button variant="outline" size="sm" onClick={() => window.location.href = '/auth'}>
                Connexion
              </Button>
              <Button size="sm" onClick={() => window.location.href = '/auth'}>
                S'inscrire
              </Button>
            </div>

            {/* Menu Hamburger Mobile */}
            <div className="md:hidden">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              >
                {mobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
              </Button>
            </div>
          </div>
        </div>

        {/* Menu Mobile */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-gray-200 bg-white mobile-menu-enter">
            <div className="px-4 py-4 space-y-4">
              <nav className="flex flex-col space-y-4">
                <a href="#formations" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
                  Formations
                </a>
                <a href="#professeurs" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
                  Professeurs
                </a>
                <a href="#temoignages" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
                  Témoignages
                </a>
                <a href="#contact" className="text-gray-700 hover:text-blue-600 font-medium transition-colors">
                  Contact
                </a>
              </nav>
              <div className="flex flex-col space-y-2 pt-4 border-t border-gray-200">
                <Button variant="outline" onClick={() => window.location.href = '/auth'}>
                  Connexion
                </Button>
                <Button onClick={() => window.location.href = '/auth'}>
                  S'inscrire
                </Button>
              </div>
            </div>
          </div>
        )}
      </header>

      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-blue-900 dark:to-indigo-900 pt-32 pb-20 lg:pt-40 lg:pb-32">
        <div className="absolute inset-0 bg-grid-pattern opacity-5"></div>
        <div className="container mx-auto px-4 relative">
          <div className="max-w-4xl mx-auto text-center">
            {/* Badges */}
            <div className="flex flex-wrap justify-center gap-3 mb-8">
              <Badge className="nexus-badge-info flex items-center space-x-2">
                <Award className="w-4 h-4" />
                <span>Professeurs Certifiés AEFE</span>
              </Badge>
              <Badge className="nexus-badge-success flex items-center space-x-2">
                <Code2 className="w-4 h-4" />
                <span>Experts DIU NSI</span>
              </Badge>
              <Badge className="nexus-badge-warning flex items-center space-x-2">
                <Presentation className="w-4 h-4" />
                <span>Spécialistes Grand Oral</span>
              </Badge>
            </div>

            {/* Titre principal */}
            <h1 className="text-4xl lg:text-6xl font-bold mb-6">
              <span className="nexus-gradient-text">Le meilleur des deux mondes</span>
              <br />
              <span className="text-foreground">pour votre réussite</span>
            </h1>

            {/* Sous-titre */}
            <p className="text-xl lg:text-2xl text-muted-foreground mb-8 max-w-3xl mx-auto">
              Accompagnement présentiel + plateforme intelligente 24/7
            </p>
            <p className="text-lg text-muted-foreground mb-12">
              Coaching, soutien et excellence pour les élèves de Première et Terminale du système français en Tunisie.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
              <Button
                size="lg"
                className="nexus-button-primary text-lg px-8 py-4"
                onClick={() => scrollToSection('offres')}
              >
                <CheckCircle className="w-5 h-5 mr-2" />
                Bilan de Positionnement Gratuit
              </Button>
              <Button
                variant="outline"
                size="lg"
                className="text-lg px-8 py-4"
                onClick={() => onLogin('student')}
              >
                <Play className="w-5 h-5 mr-2" />
                Découvrir ARIA
              </Button>
            </div>

            {/* Métriques */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-2xl mx-auto">
              <div className="text-center">
                <div className="flex items-center justify-center mb-2">
                  <TrendingUp className="w-6 h-6 text-green-500 mr-2" />
                  <span className="text-3xl font-bold text-primary">87%</span>
                </div>
                <p className="text-sm text-muted-foreground">Progression moyenne</p>
              </div>
              <div className="text-center">
                <div className="flex items-center justify-center mb-2">
                  <Target className="w-6 h-6 text-blue-500 mr-2" />
                  <span className="text-3xl font-bold text-primary">94%</span>
                </div>
                <p className="text-sm text-muted-foreground">Confiance ARIA</p>
              </div>
              <div className="text-center">
                <div className="flex items-center justify-center mb-2">
                  <Brain className="w-6 h-6 text-purple-500 mr-2" />
                  <span className="text-3xl font-bold text-primary">24/7</span>
                </div>
                <p className="text-sm text-muted-foreground">IA disponible</p>
              </div>
              <div className="text-center">
                <div className="flex items-center justify-center mb-2">
                  <MessageCircle className="w-6 h-6 text-orange-500 mr-2" />
                  <span className="text-3xl font-bold text-primary">100%</span>
                </div>
                <p className="text-sm text-muted-foreground">Suivi personnalisé</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Notre Approche */}
      <section id="approche" className="py-20 bg-background">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold mb-6">Notre Approche Hybride Révolutionnaire</h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Nexus associe technologie et humain pour un suivi adapté. Chaque élève dispose d'un cockpit personnel, de cours sur mesure, et d'un coach dédié.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 mb-16">
            <Card className="nexus-card text-center p-8">
              <div className="w-16 h-16 nexus-gradient rounded-full flex items-center justify-center mx-auto mb-6">
                <Users className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold mb-4">Accompagnement Présentiel</h3>
              <p className="text-muted-foreground mb-6">
                Cours en face-à-face avec nos professeurs certifiés et agrégés.
                Interaction humaine, motivation et suivi personnalisé.
              </p>
            </Card>

            <Card className="nexus-card text-center p-8">
              <div className="w-16 h-16 nexus-gradient rounded-full flex items-center justify-center mx-auto mb-6">
                <Brain className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold mb-4">Plateforme Intelligente 24/7</h3>
              <p className="text-muted-foreground mb-6">
                IA ARIA disponible en permanence, ressources documentaires,
                exercices adaptatifs et suivi de progression en temps réel.
              </p>
            </Card>

            <Card className="nexus-card text-center p-8">
              <div className="w-16 h-16 nexus-gradient rounded-full flex items-center justify-center mx-auto mb-6">
                <Target className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-xl font-bold mb-4">Personnalisation Maximale</h3>
              <p className="text-muted-foreground mb-6">
                Diagnostic offert au départ, gamification, progression visible et
                bilans réguliers pour un accompagnement sur mesure.
              </p>
            </Card>
          </div>

          {/* Nos Engagements */}
          <div className="bg-muted rounded-2xl p-8">
            <h3 className="text-2xl font-bold text-center mb-8">Nos Engagements</h3>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="flex items-center space-x-3">
                <CheckCircle className="w-6 h-6 text-green-500 flex-shrink-0" />
                <span className="font-medium">Personnalisation totale du parcours</span>
              </div>
              <div className="flex items-center space-x-3">
                <CheckCircle className="w-6 h-6 text-green-500 flex-shrink-0" />
                <span className="font-medium">Excellence pédagogique garantie</span>
              </div>
              <div className="flex items-center space-x-3">
                <CheckCircle className="w-6 h-6 text-green-500 flex-shrink-0" />
                <span className="font-medium">Résultats mesurables et transparents</span>
              </div>
              <div className="flex items-center space-x-3">
                <CheckCircle className="w-6 h-6 text-green-500 flex-shrink-0" />
                <span className="font-medium">Préparation études supérieures</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Nos Matières */}
      <section className="py-20 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold mb-6">Nos Matières d'Excellence</h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Spécialisation dans les matières clés du baccalauréat français avec une approche moderne et efficace.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card className="nexus-card p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-center space-x-4 mb-4">
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center">
                  <Calculator className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <h3 className="text-lg font-bold">Mathématiques Terminale</h3>
                  <p className="text-sm text-muted-foreground">Renforcement et approfondissement</p>
                </div>
              </div>
              <p className="text-muted-foreground mb-4">
                Renforcement et approfondissement, méthodologie BAC. Maîtrise des fonctions, probabilités et géométrie.
              </p>
              <Button variant="outline" size="sm" className="w-full">
                <Calendar className="w-4 h-4 mr-2" />
                Prendre un rendez-vous
              </Button>
            </Card>

            <Card className="nexus-card p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-center space-x-4 mb-4">
                <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/20 rounded-lg flex items-center justify-center">
                  <Code2 className="w-6 h-6 text-purple-600" />
                </div>
                <div>
                  <h3 className="text-lg font-bold">NSI Spécialisée</h3>
                  <p className="text-sm text-muted-foreground">Cours DIU validés</p>
                </div>
              </div>
              <p className="text-muted-foreground mb-4">
                Cours DIU validés, Grand Oral, projets Python. Enseignants diplômés DIU avec expertise approfondie.
              </p>
              <Button variant="outline" size="sm" className="w-full">
                <Play className="w-4 h-4 mr-2" />
                Voir les prochaines sessions
              </Button>
            </Card>

            <Card className="nexus-card p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-center space-x-4 mb-4">
                <div className="w-12 h-12 bg-green-100 dark:bg-green-900/20 rounded-lg flex items-center justify-center">
                  <Atom className="w-6 h-6 text-green-600" />
                </div>
                <div>
                  <h3 className="text-lg font-bold">Physique-Chimie</h3>
                  <p className="text-sm text-muted-foreground">Explication concrète</p>
                </div>
              </div>
              <p className="text-muted-foreground mb-4">
                Explication concrète, annales corrigées. Mécanique, thermodynamique et chimie organique.
              </p>
              <Button variant="outline" size="sm" className="w-full">
                <BookOpen className="w-4 h-4 mr-2" />
                S'inscrire à un atelier
              </Button>
            </Card>

            <Card className="nexus-card p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-center space-x-4 mb-4">
                <div className="w-12 h-12 bg-red-100 dark:bg-red-900/20 rounded-lg flex items-center justify-center">
                  <PenTool className="w-6 h-6 text-red-600" />
                </div>
                <div>
                  <h3 className="text-lg font-bold">Français & Grand Oral</h3>
                  <p className="text-sm text-muted-foreground">Préparation ciblée</p>
                </div>
              </div>
              <p className="text-muted-foreground mb-4">
                Préparation ciblée, argumentation et éloquence. Dissertation, commentaire et expression orale.
              </p>
              <Button variant="outline" size="sm" className="w-full">
                <MessageCircle className="w-4 h-4 mr-2" />
                Prendre un rendez-vous
              </Button>
            </Card>

            <Card className="nexus-card p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-center space-x-4 mb-4">
                <div className="w-12 h-12 bg-orange-100 dark:bg-orange-900/20 rounded-lg flex items-center justify-center">
                  <Lightbulb className="w-6 h-6 text-orange-600" />
                </div>
                <div>
                  <h3 className="text-lg font-bold">Coaching Scolaire</h3>
                  <p className="text-sm text-muted-foreground">Planification et confiance</p>
                </div>
              </div>
              <p className="text-muted-foreground mb-4">
                Planification, confiance, orientation Parcoursup. Méthodologie de travail et gestion du stress.
              </p>
              <Button variant="outline" size="sm" className="w-full">
                <Users className="w-4 h-4 mr-2" />
                Parler à notre coach
              </Button>
            </Card>

            <Card className="nexus-card p-6 hover:shadow-lg transition-shadow bg-primary text-primary-foreground">
              <div className="flex items-center space-x-4 mb-4">
                <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center">
                  <Sparkles className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white">Autres Matières</h3>
                  <p className="text-sm text-white/80">Histoire-Géo, SES, Philosophie...</p>
                </div>
              </div>
              <p className="text-white/90 mb-4">
                Histoire-Géo, SES, Philosophie... Nous adaptons notre offre à vos besoins spécifiques.
              </p>
              <Button variant="secondary" size="sm" className="w-full">
                <Phone className="w-4 h-4 mr-2" />
                Demander un devis
              </Button>
            </Card>
          </div>
        </div>
      </section>

      {/* Nos Formules & Offres */}
      <section id="offres" className="py-20 bg-background">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold mb-6">Nos Formules & Offres</h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Des parcours adaptés à chaque profil : accompagnement individuel, mini-groupes, stages intensifs.
              Choisissez la formule qui correspond à vos ambitions et votre rythme d'apprentissage.
            </p>
          </div>

          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-4 mb-12">
              <TabsTrigger value="individuel" className="flex items-center space-x-2">
                <Users className="w-4 h-4" />
                <span>Individuel</span>
              </TabsTrigger>
              <TabsTrigger value="mini-groupe" className="flex items-center space-x-2">
                <Users className="w-4 h-4" />
                <span>Mini-Groupe</span>
              </TabsTrigger>
              <TabsTrigger value="specialites" className="flex items-center space-x-2">
                <Star className="w-4 h-4" />
                <span>Spécialités</span>
              </TabsTrigger>
              <TabsTrigger value="stages" className="flex items-center space-x-2">
                <Calendar className="w-4 h-4" />
                <span>Stages</span>
              </TabsTrigger>
            </TabsList>

            <TabsContent value="individuel">
              <div className="grid md:grid-cols-3 gap-8">
                <Card className="nexus-card p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center">
                      <Trophy className="w-6 h-6 text-blue-600" />
                    </div>
                    <div>
                      <h3 className="text-lg font-bold">Coaching Premium</h3>
                      <p className="text-sm text-muted-foreground">Suivi individualisé toutes matières</p>
                    </div>
                  </div>
                  <div className="text-center mb-6">
                    <div className="text-3xl font-bold text-primary mb-2">320<span className="text-lg">DT/mois</span></div>
                  </div>
                  <ul className="space-y-3 mb-6">
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">4 heures de cours individuels/mois</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Accès complet à la plateforme ARIA</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Reporting détaillé parents</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Coach dédié toutes matières</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Suivi personnalisé continu</span>
                    </li>
                  </ul>
                  <Button className="w-full nexus-button-primary">
                    Choisir cette formule
                  </Button>
                </Card>

                <Card className="nexus-card p-6 border-2 border-primary relative">
                  <Badge className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-primary text-primary-foreground">
                    Recommandé
                  </Badge>
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/20 rounded-lg flex items-center justify-center">
                      <GraduationCap className="w-6 h-6 text-purple-600" />
                    </div>
                    <div>
                      <h3 className="text-lg font-bold">Excellence Bac</h3>
                      <p className="text-sm text-muted-foreground">Préparation Bac intensifiée</p>
                    </div>
                  </div>
                  <div className="text-center mb-6">
                    <div className="text-3xl font-bold text-primary mb-2">420<span className="text-lg">DT/mois</span></div>
                  </div>
                  <ul className="space-y-3 mb-6">
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">6 heures de cours intensifs/mois</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Fiche objectifs personnalisée</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Simulations d'examens</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Préparation spécifique Bac</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Suivi intensif progression</span>
                    </li>
                  </ul>
                  <Button className="w-full nexus-button-primary">
                    Choisir cette formule
                  </Button>
                </Card>

                <Card className="nexus-card p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="w-12 h-12 bg-green-100 dark:bg-green-900/20 rounded-lg flex items-center justify-center">
                      <Rocket className="w-6 h-6 text-green-600" />
                    </div>
                    <div>
                      <h3 className="text-lg font-bold">Coaching Parcoursup</h3>
                      <p className="text-sm text-muted-foreground">Aide dossier et orientation</p>
                    </div>
                  </div>
                  <div className="text-center mb-6">
                    <div className="text-3xl font-bold text-primary mb-2">390<span className="text-lg">DT/forfait</span></div>
                  </div>
                  <ul className="space-y-3 mb-6">
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">3 séances de coaching</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Relecture projets motivés</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Support documentation</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Préparation entretiens</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Stratégie orientation</span>
                    </li>
                  </ul>
                  <Button variant="outline" className="w-full">
                    Je veux en savoir plus
                  </Button>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="mini-groupe">
              <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
                <Card className="nexus-card p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center">
                      <Users className="w-6 h-6 text-blue-600" />
                    </div>
                    <div>
                      <h3 className="text-lg font-bold">Groupe Réussite</h3>
                      <p className="text-sm text-muted-foreground">Séances hebdo en présentiel</p>
                    </div>
                  </div>
                  <div className="text-center mb-6">
                    <div className="text-3xl font-bold text-primary mb-2">180<span className="text-lg">DT/mois</span></div>
                  </div>
                  <ul className="space-y-3 mb-6">
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">2h/semaine + module en ligne</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Groupes homogènes (3-5 élèves)</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Comptes rendus individuels</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Dynamique de groupe stimulante</span>
                    </li>
                  </ul>
                  <Button className="w-full nexus-button-primary">
                    Choisir cette formule
                  </Button>
                </Card>

                <Card className="nexus-card p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/20 rounded-lg flex items-center justify-center">
                      <BookOpen className="w-6 h-6 text-purple-600" />
                    </div>
                    <div>
                      <h3 className="text-lg font-bold">Combo Révision</h3>
                      <p className="text-sm text-muted-foreground">2 matières / semaine</p>
                    </div>
                  </div>
                  <div className="text-center mb-6">
                    <div className="text-3xl font-bold text-primary mb-2">290<span className="text-lg">DT/mois</span></div>
                  </div>
                  <ul className="space-y-3 mb-6">
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">4h/semaine + plateforme</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">2 matières dans la même plage</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Optimisation du temps</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Suivi croisé des matières</span>
                    </li>
                  </ul>
                  <Button className="w-full nexus-button-primary">
                    Choisir cette formule
                  </Button>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="specialites">
              <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
                <Card className="nexus-card p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
                      <Code2 className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="text-lg font-bold">Duo Sciences</h3>
                      <p className="text-sm text-muted-foreground">Maths & NSI en mode hybride</p>
                    </div>
                  </div>
                  <div className="text-center mb-6">
                    <div className="text-3xl font-bold text-primary mb-2">400<span className="text-lg">DT/mois</span></div>
                  </div>
                  <ul className="space-y-3 mb-6">
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">6h/mois + exercices corrigés</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Focus Bac & CPGE</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Visio bilan mensuel</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Préparation concours</span>
                    </li>
                  </ul>
                  <Button className="w-full nexus-button-primary">
                    Choisir cette formule
                  </Button>
                </Card>

                <Card className="nexus-card p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="w-12 h-12 bg-gradient-to-r from-red-500 to-orange-500 rounded-lg flex items-center justify-center">
                      <Presentation className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="text-lg font-bold">Orateur Nexus</h3>
                      <p className="text-sm text-muted-foreground">Grand Oral complet</p>
                    </div>
                  </div>
                  <div className="text-center mb-6">
                    <div className="text-3xl font-bold text-primary mb-2">390<span className="text-lg">DT/forfait</span></div>
                  </div>
                  <ul className="space-y-3 mb-6">
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">6h : contenu + structuration</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Simulation filmée</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">De la définition à l'entraînement</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Coaching éloquence</span>
                    </li>
                  </ul>
                  <Button className="w-full nexus-button-primary">
                    Je veux en savoir plus
                  </Button>
                </Card>
              </div>
            </TabsContent>

            <TabsContent value="stages">
              <div className="grid md:grid-cols-3 gap-8">
                <Card className="nexus-card p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="w-12 h-12 bg-orange-100 dark:bg-orange-900/20 rounded-lg flex items-center justify-center">
                      <Calendar className="w-6 h-6 text-orange-600" />
                    </div>
                    <div>
                      <h3 className="text-lg font-bold">Stage Août Bac</h3>
                      <p className="text-sm text-muted-foreground">1 semaine avant-rentrée</p>
                    </div>
                  </div>
                  <div className="text-center mb-6">
                    <div className="text-3xl font-bold text-primary mb-2">290<span className="text-lg">DT/stage</span></div>
                  </div>
                  <ul className="space-y-3 mb-6">
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">10h + support papier/PDF</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Par niveau/matière</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Préparation intensive</span>
                    </li>
                  </ul>
                  <Button variant="outline" className="w-full">
                    M'inscrire au prochain stage
                  </Button>
                </Card>

                <Card className="nexus-card p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center">
                      <BookOpen className="w-6 h-6 text-blue-600" />
                    </div>
                    <div>
                      <h3 className="text-lg font-bold">Stage Vacances</h3>
                      <p className="text-sm text-muted-foreground">Toussaint, hiver, printemps</p>
                    </div>
                  </div>
                  <div className="text-center mb-6">
                    <div className="text-3xl font-bold text-primary mb-2">200<span className="text-lg">DT/stage</span></div>
                  </div>
                  <ul className="space-y-3 mb-6">
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">6h / matière</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Quiz fin de stage</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Révisions ciblées</span>
                    </li>
                  </ul>
                  <Button variant="outline" className="w-full">
                    M'inscrire au prochain stage
                  </Button>
                </Card>

                <Card className="nexus-card p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/20 rounded-lg flex items-center justify-center">
                      <Code2 className="w-6 h-6 text-purple-600" />
                    </div>
                    <div>
                      <h3 className="text-lg font-bold">Python Express</h3>
                      <p className="text-sm text-muted-foreground">Programmation NSI en 5 jours</p>
                    </div>
                  </div>
                  <div className="text-center mb-6">
                    <div className="text-3xl font-bold text-primary mb-2">240<span className="text-lg">DT/semaine</span></div>
                  </div>
                  <ul className="space-y-3 mb-6">
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Algorithmes, boucles, fonctions</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">POO (Programmation Orientée Objet)</span>
                    </li>
                    <li className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm">Du débutant à l'autonomie</span>
                    </li>
                  </ul>
                  <Button variant="outline" className="w-full">
                    M'inscrire au prochain stage
                  </Button>
                </Card>
              </div>
            </TabsContent>
          </Tabs>

          <div className="text-center mt-12">
            <Button size="lg" className="nexus-button-primary">
              <Phone className="w-5 h-5 mr-2" />
              Planifier un appel diagnostic gratuit
            </Button>
          </div>
        </div>
      </section>

      {/* Témoignages */}
      <section className="py-20 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold mb-6">Ils Nous Font Confiance</h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Découvrez les témoignages de nos élèves et de leurs parents qui ont choisi Nexus Réussite.
            </p>
          </div>

          <div className="max-w-4xl mx-auto">
            <Card className="nexus-card p-8 text-center">
              <div className="flex justify-center mb-6">
                <div className="w-16 h-16 nexus-avatar bg-primary text-primary-foreground text-xl">
                  {testimonials[currentTestimonial].avatar}
                </div>
              </div>

              <div className="flex justify-center mb-4">
                {[...Array(testimonials[currentTestimonial].rating)].map((_, i) => (
                  <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                ))}
              </div>

              <blockquote className="text-lg text-muted-foreground mb-6 italic">
                <Quote className="w-6 h-6 text-muted-foreground/50 inline mr-2" />
                {testimonials[currentTestimonial].text}
                <Quote className="w-6 h-6 text-muted-foreground/50 inline ml-2 rotate-180" />
              </blockquote>

              <div>
                <p className="font-semibold text-foreground">{testimonials[currentTestimonial].name}</p>
                <p className="text-sm text-muted-foreground">
                  {testimonials[currentTestimonial].grade || testimonials[currentTestimonial].role}
                </p>
              </div>
            </Card>

            <div className="flex justify-center space-x-2 mt-8">
              {testimonials.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentTestimonial(index)}
                  className={`w-3 h-3 rounded-full transition-colors ${index === currentTestimonial ? 'bg-primary' : 'bg-muted-foreground/30'
                    }`}
                />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Nos Enseignants */}
      <section id="enseignants" className="py-20 bg-background">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold mb-6">Nos Enseignants d'Exception</h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Découvrez nos professeurs certifiés et agrégés, experts du système français AEFE et spécialisés dans l'accompagnement vers l'excellence.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {teachers.map((teacher) => (
              <Card key={teacher.id} className="nexus-card p-6 text-center hover:shadow-lg transition-shadow">
                <div className="relative mb-6">
                  <div className={`w-20 h-20 nexus-avatar mx-auto text-xl ${teacher.id === 'dubois' ? 'bg-blue-500 text-white' :
                      teacher.id === 'martin' ? 'bg-green-500 text-white' :
                        'bg-red-500 text-white'
                    }`}>
                    {teacher.avatar}
                  </div>
                  <Badge className={`absolute -top-2 -right-2 ${teacher.badge === 'Expert' ? 'nexus-badge-success' :
                      teacher.badge === 'DIU NSI' ? 'nexus-badge-info' :
                        'nexus-badge-warning'
                    }`}>
                    <Award className="w-3 h-3 mr-1" />
                    {teacher.badge}
                  </Badge>
                </div>

                <h3 className="text-xl font-bold mb-2">{teacher.name}</h3>
                <p className="text-primary font-medium mb-2">{teacher.title}</p>

                <div className="space-y-2 mb-4">
                  <div className="flex items-center justify-center space-x-2 text-sm text-muted-foreground">
                    <GraduationCap className="w-4 h-4" />
                    <span>{teacher.credentials}</span>
                  </div>
                  <div className="flex items-center justify-center space-x-2 text-sm text-muted-foreground">
                    <Clock className="w-4 h-4" />
                    <span>{teacher.experience}</span>
                  </div>
                  {teacher.specialties.map((specialty, index) => (
                    <div key={index} className="flex items-center justify-center space-x-2 text-sm text-muted-foreground">
                      <Star className="w-4 h-4" />
                      <span>{specialty}</span>
                    </div>
                  ))}
                </div>

                <p className="text-sm text-muted-foreground mb-4 text-left">
                  {teacher.description}
                </p>

                <div className="flex items-center justify-center space-x-1 mb-4">
                  {[...Array(5)].map((_, i) => (
                    <Star
                      key={i}
                      className={`w-4 h-4 ${i < Math.floor(teacher.rating)
                          ? 'text-yellow-400 fill-current'
                          : 'text-gray-300'
                        }`}
                    />
                  ))}
                  <span className="text-sm text-muted-foreground ml-2">({teacher.rating}/5)</span>
                </div>

                <Button variant="outline" className="w-full">
                  <Eye className="w-4 h-4 mr-2" />
                  Voir le profil →
                </Button>
              </Card>
            ))}
          </div>

          <div className="text-center mt-12">
            <Button size="lg" className="nexus-button-primary">
              <Users className="w-5 h-5 mr-2" />
              Découvrir tous nos enseignants
            </Button>
          </div>
        </div>
      </section>

      {/* Notre Centre */}
      <section className="py-20 bg-muted/30">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold mb-6">Notre Centre Nexus</h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              Situé au cœur de Tunis, notre centre Nexus est un lieu moderne et équipé pour accueillir vos cours présentiels en toute sérénité.
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h3 className="text-2xl font-bold mb-8">Nos Espaces</h3>

              <div className="space-y-6">
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Monitor className="w-6 h-6 text-blue-600" />
                  </div>
                  <div>
                    <h4 className="font-semibold mb-2">Salles de cours équipées</h4>
                    <p className="text-muted-foreground">Tableaux interactifs, connexion haut débit, climatisation</p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-green-100 dark:bg-green-900/20 rounded-lg flex items-center justify-center flex-shrink-0">
                    <Coffee className="w-6 h-6 text-green-600" />
                  </div>
                  <div>
                    <h4 className="font-semibold mb-2">Espace détente</h4>
                    <p className="text-muted-foreground">Zone de pause pour les élèves et les parents</p>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/20 rounded-lg flex items-center justify-center flex-shrink-0">
                    <BookOpen className="w-6 h-6 text-purple-600" />
                  </div>
                  <div>
                    <h4 className="font-semibold mb-2">Bibliothèque de ressources</h4>
                    <p className="text-muted-foreground">Manuels, annales et supports pédagogiques</p>
                  </div>
                </div>
              </div>

              <div className="mt-8 p-6 bg-card rounded-lg border">
                <h4 className="font-semibold mb-4">Informations Pratiques</h4>
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <MapPin className="w-5 h-5 text-muted-foreground" />
                    <div>
                      <p className="font-medium">Centre Urbain Nord</p>
                      <p className="text-sm text-muted-foreground">Immeuble VENUS, Apt. C13</p>
                      <p className="text-sm text-muted-foreground">1082 – Tunis</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Clock className="w-5 h-5 text-muted-foreground" />
                    <span>Lun-Sam : 8h00-20h00 | Dim : 9h00-17h00</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Car className="w-5 h-5 text-muted-foreground" />
                    <span>Parking disponible | Accès métro ligne 1</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Shield className="w-5 h-5 text-muted-foreground" />
                    <span>Protocole sanitaire strict | Accès sécurisé</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="space-y-6">
              <div className="bg-muted rounded-lg p-8 text-center">
                <MapPin className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
                <p className="text-muted-foreground mb-4">Carte Google Maps</p>
                <p className="text-sm text-muted-foreground">Centre Nexus Réussite</p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <Button className="nexus-button-primary">
                  <Navigation className="w-4 h-4 mr-2" />
                  Obtenir l'itinéraire
                </Button>
                <Button variant="outline">
                  <Calendar className="w-4 h-4 mr-2" />
                  Planifier une visite
                </Button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Final */}
      <section className="py-20 bg-primary text-primary-foreground">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl lg:text-4xl font-bold mb-6">
            Prêt à Transformer Votre Réussite ?
          </h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto opacity-90">
            Rejoignez les centaines d'élèves qui ont choisi Nexus Réussite pour atteindre l'excellence.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
            <Button
              size="lg"
              variant="secondary"
              className="text-lg px-8 py-4"
              onClick={() => onLogin('student')}
            >
              <CheckCircle className="w-5 h-5 mr-2" />
              Demander un bilan gratuit
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="text-lg px-8 py-4 border-white text-white hover:bg-white hover:text-primary"
              onClick={() => onLogin('parent')}
            >
              <MessageCircle className="w-5 h-5 mr-2" />
              Parler à notre assistante pédagogique
            </Button>
          </div>

          <div className="flex justify-center space-x-8 text-sm opacity-75">
            <span>✓ Sans engagement</span>
            <span>✓ Réponse sous 24h</span>
            <span>✓ Bilan personnalisé</span>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer id="contact" className="bg-gray-900 text-white py-16">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            {/* Logo et description */}
            <div className="md:col-span-2">
              <div className="flex items-center space-x-3 mb-6">
                <div className="w-12 h-12 nexus-gradient rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-xl">N</span>
                </div>
                <div>
                  <h3 className="text-xl font-bold">Nexus Réussite</h3>
                  <p className="text-sm text-gray-400">Formation d'Excellence</p>
                </div>
              </div>
              <p className="text-gray-300 mb-6 max-w-md">
                Accompagnement présentiel et plateforme intelligente pour la réussite des élèves du système français en Tunisie.
              </p>
              <div className="flex space-x-4">
                <a href="#" className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-gray-700 transition-colors">
                  <Facebook className="w-5 h-5" />
                </a>
                <a href="#" className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-gray-700 transition-colors">
                  <Instagram className="w-5 h-5" />
                </a>
                <a href="#" className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-gray-700 transition-colors">
                  <Youtube className="w-5 h-5" />
                </a>
                <a href="#" className="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-gray-700 transition-colors">
                  <Linkedin className="w-5 h-5" />
                </a>
              </div>
            </div>

            {/* Liens rapides */}
            <div>
              <h4 className="font-semibold mb-4">Liens Rapides</h4>
              <ul className="space-y-2 text-gray-300">
                <li><a href="#" className="hover:text-white transition-colors">À propos de Nexus</a></li>
                <li><a href="#offres" className="hover:text-white transition-colors">Nos Offres</a></li>
                <li><a href="#enseignants" className="hover:text-white transition-colors">Nos Enseignants</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Notre Pédagogie</a></li>
                <li><a href="#" className="hover:text-white transition-colors">FAQ</a></li>
              </ul>
            </div>

            {/* Contact */}
            <div>
              <h4 className="font-semibold mb-4">Contact</h4>
              <div className="space-y-3 text-gray-300">
                <div className="flex items-center space-x-3">
                  <MapPin className="w-5 h-5 flex-shrink-0" />
                  <div>
                    <p>Centre Urbain Nord</p>
                    <p>Immeuble VENUS, Apt. C13</p>
                    <p>1082 – Tunis</p>
                  </div>
                </div>
                <div className="flex items-center space-x-3">
                  <Phone className="w-5 h-5 flex-shrink-0" />
                  <span>+216 XX XXX XXX</span>
                </div>
                <div className="flex items-center space-x-3">
                  <Mail className="w-5 h-5 flex-shrink-0" />
                  <span>contact@nexus-reussite.tn</span>
                </div>
                <div className="flex items-center space-x-3">
                  <Globe className="w-5 h-5 flex-shrink-0" />
                  <span>www.nexus-reussite.tn</span>
                </div>
              </div>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-12 pt-8 text-center text-gray-400">
            <p>&copy; 2025 Nexus Réussite. Tous droits réservés.</p>
            <div className="flex justify-center space-x-6 mt-4 text-sm">
              <a href="#" className="hover:text-white transition-colors">Mentions légales</a>
              <a href="#" className="hover:text-white transition-colors">Politique de confidentialité</a>
              <a href="#" className="hover:text-white transition-colors">CGV</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
