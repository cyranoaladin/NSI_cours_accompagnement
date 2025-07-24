import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { 
  Trophy, 
  Star, 
  Award, 
  Target, 
  Zap, 
  Crown, 
  Medal, 
  Flame, 
  TrendingUp,
  Calendar,
  BookOpen,
  Brain,
  Users,
  Gift,
  Sparkles,
  ChevronRight,
  Lock,
  CheckCircle,
  Clock,
  BarChart3,
  PieChart,
  Activity,
  Lightbulb,
  Heart,
  Shield,
  Rocket,
  Diamond,
  Gem,
  Coins,
  Plus,
  ArrowUp,
  ArrowDown,
  Minus
} from 'lucide-react'

const Gamification = ({ 
  student, 
  onUpdateProgress, 
  onUnlockBadge, 
  addNotification,
  isVisible,
  onClose 
}) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [selectedBadge, setSelectedBadge] = useState(null);
  const [showBadgeModal, setShowBadgeModal] = useState(false);
  const [dailyStreak, setDailyStreak] = useState(student?.streak || 0);
  const [weeklyXP, setWeeklyXP] = useState(0);
  const [monthlyRank, setMonthlyRank] = useState(0);

  // Système de niveaux et XP
  const levelSystem = {
    1: { min: 0, max: 100, title: 'Débutant', color: 'bg-gray-500', icon: BookOpen },
    2: { min: 100, max: 300, title: 'Apprenti', color: 'bg-green-500', icon: Target },
    3: { min: 300, max: 600, title: 'Étudiant', color: 'bg-blue-500', icon: Brain },
    4: { min: 600, max: 1000, title: 'Expert', color: 'bg-purple-500', icon: Star },
    5: { min: 1000, max: 1500, title: 'Maître', color: 'bg-orange-500', icon: Crown },
    6: { min: 1500, max: 2500, title: 'Champion', color: 'bg-red-500', icon: Trophy },
    7: { min: 2500, max: 4000, title: 'Légende', color: 'bg-yellow-500', icon: Medal },
    8: { min: 4000, max: 6000, title: 'Génie', color: 'bg-pink-500', icon: Diamond },
    9: { min: 6000, max: 10000, title: 'Prodige', color: 'bg-indigo-500', icon: Rocket },
    10: { min: 10000, max: Infinity, title: 'Nexus Master', color: 'bg-gradient-to-r from-purple-500 to-pink-500', icon: Gem }
  };

  // Badges disponibles
  const availableBadges = [
    {
      id: 'first-steps',
      name: 'Premier pas',
      description: 'Complétez votre première session',
      icon: Target,
      rarity: 'common',
      xpReward: 50,
      unlocked: true,
      progress: 100,
      category: 'progression'
    },
    {
      id: 'streak-7',
      name: 'Série de 7 jours',
      description: 'Maintenez une série de 7 jours consécutifs',
      icon: Flame,
      rarity: 'uncommon',
      xpReward: 100,
      unlocked: dailyStreak >= 7,
      progress: Math.min((dailyStreak / 7) * 100, 100),
      category: 'régularité'
    },
    {
      id: 'streak-15',
      name: 'Série de 15 jours',
      description: 'Maintenez une série de 15 jours consécutifs',
      icon: Flame,
      rarity: 'rare',
      xpReward: 250,
      unlocked: dailyStreak >= 15,
      progress: Math.min((dailyStreak / 15) * 100, 100),
      category: 'régularité'
    },
    {
      id: 'math-expert',
      name: 'Expert en fonctions',
      description: 'Maîtrisez parfaitement les fonctions exponentielles',
      icon: Brain,
      rarity: 'rare',
      xpReward: 200,
      unlocked: student?.progress?.mathématiques >= 85,
      progress: student?.progress?.mathématiques || 0,
      category: 'matière'
    },
    {
      id: 'python-master',
      name: 'Maître Python',
      description: 'Complétez 5 projets Python avec succès',
      icon: Award,
      rarity: 'epic',
      xpReward: 300,
      unlocked: false,
      progress: 60,
      category: 'compétence'
    },
    {
      id: 'oral-champion',
      name: 'Orateur confirmé',
      description: 'Excellez dans 3 présentations orales',
      icon: Crown,
      rarity: 'epic',
      xpReward: 350,
      unlocked: student?.name === 'Léa Moreau',
      progress: student?.name === 'Léa Moreau' ? 100 : 33,
      category: 'compétence'
    },
    {
      id: 'data-analyst',
      name: 'Analyste de données',
      description: 'Résolvez 10 problèmes de statistiques',
      icon: BarChart3,
      rarity: 'rare',
      xpReward: 200,
      unlocked: student?.name === 'Sarah Benali',
      progress: student?.name === 'Sarah Benali' ? 100 : 70,
      category: 'compétence'
    },
    {
      id: 'problem-solver',
      name: 'Résolveur de problèmes',
      description: 'Trouvez des solutions créatives à 5 défis complexes',
      icon: Lightbulb,
      rarity: 'legendary',
      xpReward: 500,
      unlocked: student?.level >= 4,
      progress: student?.level >= 4 ? 100 : (student?.level || 1) * 20,
      category: 'excellence'
    },
    {
      id: 'perfectionist',
      name: 'Perfectionniste',
      description: 'Obtenez 5 notes parfaites consécutives',
      icon: Diamond,
      rarity: 'legendary',
      xpReward: 600,
      unlocked: student?.name === 'Léa Moreau',
      progress: student?.name === 'Léa Moreau' ? 100 : 0,
      category: 'excellence'
    },
    {
      id: 'team-player',
      name: 'Esprit d\'équipe',
      description: 'Participez activement à 3 sessions de groupe',
      icon: Users,
      rarity: 'uncommon',
      xpReward: 150,
      unlocked: false,
      progress: 33,
      category: 'social'
    },
    {
      id: 'early-bird',
      name: 'Lève-tôt',
      description: 'Assistez à 5 sessions matinales',
      icon: Clock,
      rarity: 'common',
      xpReward: 75,
      unlocked: false,
      progress: 40,
      category: 'habitude'
    },
    {
      id: 'night-owl',
      name: 'Couche-tard studieux',
      description: 'Complétez 5 sessions d\'étude tardives',
      icon: Shield,
      rarity: 'common',
      xpReward: 75,
      unlocked: false,
      progress: 20,
      category: 'habitude'
    }
  ];

  // Défis quotidiens
  const dailyChallenges = [
    {
      id: 'daily-math',
      title: 'Défi Mathématiques',
      description: 'Résolvez 3 exercices de probabilités',
      xpReward: 50,
      progress: 67,
      completed: false,
      timeLeft: '4h 32min',
      difficulty: 'Moyen'
    },
    {
      id: 'daily-reading',
      title: 'Lecture Active',
      description: 'Lisez et résumez un chapitre de cours',
      xpReward: 30,
      progress: 100,
      completed: true,
      timeLeft: 'Terminé',
      difficulty: 'Facile'
    },
    {
      id: 'daily-code',
      title: 'Code du Jour',
      description: 'Implémentez un algorithme de recherche',
      xpReward: 75,
      progress: 25,
      completed: false,
      timeLeft: '6h 15min',
      difficulty: 'Difficile'
    }
  ];

  // Récompenses hebdomadaires
  const weeklyRewards = [
    {
      id: 'week-xp-bonus',
      title: 'Bonus XP Hebdomadaire',
      description: 'Gagnez 500 XP supplémentaires',
      requirement: '7 jours d\'activité',
      progress: 85,
      unlocked: false,
      reward: '500 XP'
    },
    {
      id: 'week-badge-hunt',
      title: 'Chasseur de Badges',
      description: 'Débloquez 2 nouveaux badges cette semaine',
      requirement: '2 badges débloqués',
      progress: 50,
      unlocked: false,
      reward: 'Badge spécial'
    },
    {
      id: 'week-perfect-score',
      title: 'Semaine Parfaite',
      description: 'Maintenez une moyenne de 90% ou plus',
      requirement: 'Moyenne ≥ 90%',
      progress: student?.progress?.overall || 0,
      unlocked: (student?.progress?.overall || 0) >= 90,
      reward: 'Titre exclusif'
    }
  ];

  // Classement mensuel
  const monthlyLeaderboard = [
    { rank: 1, name: 'Léa Moreau', xp: 4750, badge: 'Légende', avatar: 'LM' },
    { rank: 2, name: 'Sarah Benali', xp: 3250, badge: 'Expert', avatar: 'SB' },
    { rank: 3, name: 'Youssef Khelifi', xp: 2340, badge: 'Étudiant', avatar: 'YK' },
    { rank: 4, name: 'Nour Hamdi', xp: 2100, badge: 'Étudiant', avatar: 'NH' },
    { rank: 5, name: 'Ahmed Trabelsi', xp: 1580, badge: 'Apprenti', avatar: 'AT' }
  ];

  const getCurrentLevel = (xp) => {
    for (let level = 10; level >= 1; level--) {
      if (xp >= levelSystem[level].min) {
        return level;
      }
    }
    return 1;
  };

  const getXPForNextLevel = (currentXP) => {
    const currentLevel = getCurrentLevel(currentXP);
    if (currentLevel === 10) return 0;
    return levelSystem[currentLevel + 1].min - currentXP;
  };

  const getProgressToNextLevel = (currentXP) => {
    const currentLevel = getCurrentLevel(currentXP);
    if (currentLevel === 10) return 100;
    
    const currentLevelMin = levelSystem[currentLevel].min;
    const nextLevelMin = levelSystem[currentLevel + 1].min;
    const progress = ((currentXP - currentLevelMin) / (nextLevelMin - currentLevelMin)) * 100;
    
    return Math.min(progress, 100);
  };

  const getRarityColor = (rarity) => {
    const colors = {
      common: 'text-gray-600 bg-gray-100',
      uncommon: 'text-green-600 bg-green-100',
      rare: 'text-blue-600 bg-blue-100',
      epic: 'text-purple-600 bg-purple-100',
      legendary: 'text-yellow-600 bg-yellow-100'
    };
    return colors[rarity] || colors.common;
  };

  const handleBadgeClick = (badge) => {
    setSelectedBadge(badge);
    setShowBadgeModal(true);
  };

  const claimReward = (challengeId) => {
    const challenge = dailyChallenges.find(c => c.id === challengeId);
    if (challenge && challenge.completed) {
      addNotification({
        type: 'success',
        title: 'Récompense réclamée !',
        message: `Vous avez gagné ${challenge.xpReward} XP`
      });
      
      if (onUpdateProgress) {
        onUpdateProgress({
          xp: student.xp + challenge.xpReward
        });
      }
    }
  };

  const currentLevel = getCurrentLevel(student?.xp || 0);
  const currentLevelInfo = levelSystem[currentLevel];
  const LevelIcon = currentLevelInfo.icon;

  if (!isVisible) return null;

  return (
    <div className="nexus-gamification">
      <div className="nexus-gamification-header">
        <div className="flex items-center space-x-4">
          <div className={`w-12 h-12 ${currentLevelInfo.color} rounded-lg flex items-center justify-center`}>
            <LevelIcon className="w-6 h-6 text-white" />
          </div>
          <div>
            <h2 className="text-xl font-bold">Progression & Récompenses</h2>
            <p className="text-sm text-muted-foreground">
              Niveau {currentLevel} - {currentLevelInfo.title}
            </p>
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <div className="text-right">
            <div className="flex items-center space-x-2">
              <Coins className="w-4 h-4 text-yellow-600" />
              <span className="font-bold text-lg">{student?.xp || 0} XP</span>
            </div>
            <div className="flex items-center space-x-2">
              <Flame className="w-4 h-4 text-orange-600" />
              <span className="text-sm">{dailyStreak} jours</span>
            </div>
          </div>
          
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="w-4 h-4" />
          </Button>
        </div>
      </div>

      <div className="grid lg:grid-cols-4 gap-6">
        {/* Sidebar - Vue d'ensemble */}
        <div className="lg:col-span-1 space-y-6">
          {/* Niveau actuel */}
          <Card className="nexus-card">
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center space-x-2">
                <LevelIcon className="w-5 h-5" />
                <span>Niveau {currentLevel}</span>
              </CardTitle>
              <CardDescription>{currentLevelInfo.title}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex justify-between text-sm">
                  <span>Progression</span>
                  <span>{Math.round(getProgressToNextLevel(student?.xp || 0))}%</span>
                </div>
                <Progress value={getProgressToNextLevel(student?.xp || 0)} className="w-full" />
                
                {currentLevel < 10 && (
                  <p className="text-xs text-muted-foreground">
                    {getXPForNextLevel(student?.xp || 0)} XP pour le niveau suivant
                  </p>
                )}
                
                {currentLevel === 10 && (
                  <p className="text-xs text-yellow-600 font-medium">
                    🎉 Niveau maximum atteint !
                  </p>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Statistiques rapides */}
          <Card className="nexus-card">
            <CardHeader>
              <CardTitle className="text-base">Statistiques</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Trophy className="w-4 h-4 text-yellow-600" />
                  <span className="text-sm">Badges</span>
                </div>
                <span className="font-semibold">
                  {availableBadges.filter(b => b.unlocked).length}/{availableBadges.length}
                </span>
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Flame className="w-4 h-4 text-orange-600" />
                  <span className="text-sm">Série actuelle</span>
                </div>
                <span className="font-semibold">{dailyStreak} jours</span>
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <TrendingUp className="w-4 h-4 text-green-600" />
                  <span className="text-sm">Progression</span>
                </div>
                <span className="font-semibold">{student?.progress?.overall || 0}%</span>
              </div>
              
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Medal className="w-4 h-4 text-purple-600" />
                  <span className="text-sm">Rang mensuel</span>
                </div>
                <span className="font-semibold">
                  #{monthlyLeaderboard.findIndex(p => p.name === student?.name) + 1 || 'N/A'}
                </span>
              </div>
            </CardContent>
          </Card>

          {/* Navigation */}
          <Card className="nexus-card">
            <CardContent className="p-3">
              <nav className="space-y-1">
                <button
                  onClick={() => setActiveTab('overview')}
                  className={`w-full text-left px-3 py-2 rounded-md text-sm transition-colors ${
                    activeTab === 'overview' 
                      ? 'bg-primary text-primary-foreground' 
                      : 'hover:bg-muted'
                  }`}
                >
                  <div className="flex items-center space-x-2">
                    <Activity className="w-4 h-4" />
                    <span>Vue d'ensemble</span>
                  </div>
                </button>
                
                <button
                  onClick={() => setActiveTab('badges')}
                  className={`w-full text-left px-3 py-2 rounded-md text-sm transition-colors ${
                    activeTab === 'badges' 
                      ? 'bg-primary text-primary-foreground' 
                      : 'hover:bg-muted'
                  }`}
                >
                  <div className="flex items-center space-x-2">
                    <Award className="w-4 h-4" />
                    <span>Badges</span>
                  </div>
                </button>
                
                <button
                  onClick={() => setActiveTab('challenges')}
                  className={`w-full text-left px-3 py-2 rounded-md text-sm transition-colors ${
                    activeTab === 'challenges' 
                      ? 'bg-primary text-primary-foreground' 
                      : 'hover:bg-muted'
                  }`}
                >
                  <div className="flex items-center space-x-2">
                    <Target className="w-4 h-4" />
                    <span>Défis</span>
                  </div>
                </button>
                
                <button
                  onClick={() => setActiveTab('leaderboard')}
                  className={`w-full text-left px-3 py-2 rounded-md text-sm transition-colors ${
                    activeTab === 'leaderboard' 
                      ? 'bg-primary text-primary-foreground' 
                      : 'hover:bg-muted'
                  }`}
                >
                  <div className="flex items-center space-x-2">
                    <Trophy className="w-4 h-4" />
                    <span>Classement</span>
                  </div>
                </button>
              </nav>
            </CardContent>
          </Card>
        </div>

        {/* Contenu principal */}
        <div className="lg:col-span-3">
          {/* Vue d'ensemble */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* Défis quotidiens */}
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Target className="w-5 h-5 text-blue-600" />
                    <span>Défis Quotidiens</span>
                  </CardTitle>
                  <CardDescription>
                    Complétez vos défis pour gagner des XP bonus
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-3 gap-4">
                    {dailyChallenges.map((challenge) => (
                      <div key={challenge.id} className="nexus-challenge-card">
                        <div className="flex items-start justify-between mb-3">
                          <div>
                            <h4 className="font-semibold text-sm">{challenge.title}</h4>
                            <p className="text-xs text-muted-foreground">{challenge.description}</p>
                          </div>
                          <Badge 
                            variant="outline" 
                            className={`text-xs ${
                              challenge.difficulty === 'Facile' ? 'text-green-600' :
                              challenge.difficulty === 'Moyen' ? 'text-yellow-600' :
                              'text-red-600'
                            }`}
                          >
                            {challenge.difficulty}
                          </Badge>
                        </div>
                        
                        <div className="space-y-2">
                          <div className="flex justify-between text-xs">
                            <span>Progression</span>
                            <span>{challenge.progress}%</span>
                          </div>
                          <Progress value={challenge.progress} className="w-full h-2" />
                          
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-1">
                              <Coins className="w-3 h-3 text-yellow-600" />
                              <span className="text-xs font-medium">{challenge.xpReward} XP</span>
                            </div>
                            <span className="text-xs text-muted-foreground">
                              {challenge.timeLeft}
                            </span>
                          </div>
                          
                          {challenge.completed ? (
                            <Button 
                              size="sm" 
                              className="w-full"
                              onClick={() => claimReward(challenge.id)}
                            >
                              <Gift className="w-3 h-3 mr-1" />
                              Réclamer
                            </Button>
                          ) : (
                            <Button size="sm" variant="outline" className="w-full">
                              <Play className="w-3 h-3 mr-1" />
                              Continuer
                            </Button>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Récompenses hebdomadaires */}
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Calendar className="w-5 h-5 text-purple-600" />
                    <span>Récompenses Hebdomadaires</span>
                  </CardTitle>
                  <CardDescription>
                    Objectifs à long terme avec des récompenses exclusives
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {weeklyRewards.map((reward) => (
                      <div key={reward.id} className="nexus-reward-card">
                        <div className="flex items-center space-x-4">
                          <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
                            reward.unlocked ? 'bg-green-100' : 'bg-gray-100'
                          }`}>
                            {reward.unlocked ? (
                              <CheckCircle className="w-6 h-6 text-green-600" />
                            ) : (
                              <Lock className="w-6 h-6 text-gray-400" />
                            )}
                          </div>
                          
                          <div className="flex-1">
                            <div className="flex items-center justify-between mb-1">
                              <h4 className="font-semibold">{reward.title}</h4>
                              <Badge className="nexus-badge-info">{reward.reward}</Badge>
                            </div>
                            <p className="text-sm text-muted-foreground mb-2">{reward.description}</p>
                            
                            <div className="flex items-center space-x-4">
                              <div className="flex-1">
                                <div className="flex justify-between text-xs mb-1">
                                  <span>{reward.requirement}</span>
                                  <span>{reward.progress}%</span>
                                </div>
                                <Progress value={reward.progress} className="w-full h-2" />
                              </div>
                              
                              {reward.unlocked && (
                                <Button size="sm">
                                  <Gift className="w-3 h-3 mr-1" />
                                  Réclamer
                                </Button>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Badges récents */}
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Award className="w-5 h-5 text-yellow-600" />
                      <span>Badges Récents</span>
                    </div>
                    <Button 
                      variant="ghost" 
                      size="sm"
                      onClick={() => setActiveTab('badges')}
                    >
                      Voir tout
                      <ChevronRight className="w-4 h-4 ml-1" />
                    </Button>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {availableBadges
                      .filter(badge => badge.unlocked)
                      .slice(0, 4)
                      .map((badge) => {
                        const BadgeIcon = badge.icon;
                        return (
                          <div
                            key={badge.id}
                            className="nexus-badge-mini"
                            onClick={() => handleBadgeClick(badge)}
                          >
                            <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${getRarityColor(badge.rarity)}`}>
                              <BadgeIcon className="w-6 h-6" />
                            </div>
                            <h4 className="font-medium text-sm text-center mt-2">{badge.name}</h4>
                            <Badge variant="outline" className="text-xs mx-auto">
                              {badge.rarity}
                            </Badge>
                          </div>
                        );
                      })}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Badges */}
          {activeTab === 'badges' && (
            <div className="space-y-6">
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Award className="w-5 h-5 text-yellow-600" />
                    <span>Collection de Badges</span>
                  </CardTitle>
                  <CardDescription>
                    {availableBadges.filter(b => b.unlocked).length} sur {availableBadges.length} badges débloqués
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-3 lg:grid-cols-4 gap-4">
                    {availableBadges.map((badge) => {
                      const BadgeIcon = badge.icon;
                      return (
                        <div
                          key={badge.id}
                          className={`nexus-badge-card ${badge.unlocked ? 'unlocked' : 'locked'}`}
                          onClick={() => handleBadgeClick(badge)}
                        >
                          <div className={`w-16 h-16 rounded-lg flex items-center justify-center mb-3 ${
                            badge.unlocked 
                              ? getRarityColor(badge.rarity)
                              : 'bg-gray-100 text-gray-400'
                          }`}>
                            {badge.unlocked ? (
                              <BadgeIcon className="w-8 h-8" />
                            ) : (
                              <Lock className="w-8 h-8" />
                            )}
                          </div>
                          
                          <h4 className={`font-semibold text-center mb-1 ${
                            badge.unlocked ? 'text-foreground' : 'text-muted-foreground'
                          }`}>
                            {badge.name}
                          </h4>
                          
                          <p className="text-xs text-muted-foreground text-center mb-3">
                            {badge.description}
                          </p>
                          
                          <div className="space-y-2">
                            <div className="flex items-center justify-between text-xs">
                              <Badge variant="outline" className="text-xs">
                                {badge.rarity}
                              </Badge>
                              <div className="flex items-center space-x-1">
                                <Coins className="w-3 h-3 text-yellow-600" />
                                <span>{badge.xpReward} XP</span>
                              </div>
                            </div>
                            
                            {!badge.unlocked && (
                              <>
                                <div className="flex justify-between text-xs">
                                  <span>Progression</span>
                                  <span>{Math.round(badge.progress)}%</span>
                                </div>
                                <Progress value={badge.progress} className="w-full h-1" />
                              </>
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Défis */}
          {activeTab === 'challenges' && (
            <div className="space-y-6">
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Target className="w-5 h-5 text-blue-600" />
                    <span>Défis & Objectifs</span>
                  </CardTitle>
                  <CardDescription>
                    Relevez des défis pour progresser plus rapidement
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    {/* Défis quotidiens détaillés */}
                    <div>
                      <h3 className="font-semibold mb-4 flex items-center space-x-2">
                        <Clock className="w-4 h-4" />
                        <span>Défis Quotidiens</span>
                      </h3>
                      <div className="grid md:grid-cols-2 gap-4">
                        {dailyChallenges.map((challenge) => (
                          <div key={challenge.id} className="nexus-challenge-detailed">
                            <div className="flex items-start justify-between mb-4">
                              <div>
                                <h4 className="font-semibold">{challenge.title}</h4>
                                <p className="text-sm text-muted-foreground">{challenge.description}</p>
                              </div>
                              <Badge 
                                variant="outline" 
                                className={`${
                                  challenge.difficulty === 'Facile' ? 'text-green-600' :
                                  challenge.difficulty === 'Moyen' ? 'text-yellow-600' :
                                  'text-red-600'
                                }`}
                              >
                                {challenge.difficulty}
                              </Badge>
                            </div>
                            
                            <div className="space-y-3">
                              <div className="flex justify-between text-sm">
                                <span>Progression</span>
                                <span>{challenge.progress}%</span>
                              </div>
                              <Progress value={challenge.progress} className="w-full" />
                              
                              <div className="flex items-center justify-between">
                                <div className="flex items-center space-x-2">
                                  <Coins className="w-4 h-4 text-yellow-600" />
                                  <span className="font-medium">{challenge.xpReward} XP</span>
                                </div>
                                <span className="text-sm text-muted-foreground">
                                  {challenge.timeLeft}
                                </span>
                              </div>
                              
                              <div className="flex space-x-2">
                                {challenge.completed ? (
                                  <Button 
                                    className="flex-1"
                                    onClick={() => claimReward(challenge.id)}
                                  >
                                    <Gift className="w-4 h-4 mr-2" />
                                    Réclamer la récompense
                                  </Button>
                                ) : (
                                  <>
                                    <Button variant="outline" className="flex-1">
                                      <Play className="w-4 h-4 mr-2" />
                                      Continuer
                                    </Button>
                                    <Button variant="ghost" size="sm">
                                      <Eye className="w-4 h-4" />
                                    </Button>
                                  </>
                                )}
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Défis hebdomadaires */}
                    <div>
                      <h3 className="font-semibold mb-4 flex items-center space-x-2">
                        <Calendar className="w-4 h-4" />
                        <span>Défis Hebdomadaires</span>
                      </h3>
                      <div className="space-y-4">
                        {weeklyRewards.map((reward) => (
                          <div key={reward.id} className="nexus-weekly-challenge">
                            <div className="flex items-center space-x-4">
                              <div className={`w-16 h-16 rounded-lg flex items-center justify-center ${
                                reward.unlocked ? 'bg-green-100' : 'bg-gray-100'
                              }`}>
                                {reward.unlocked ? (
                                  <CheckCircle className="w-8 h-8 text-green-600" />
                                ) : (
                                  <Lock className="w-8 h-8 text-gray-400" />
                                )}
                              </div>
                              
                              <div className="flex-1">
                                <div className="flex items-center justify-between mb-2">
                                  <h4 className="font-semibold">{reward.title}</h4>
                                  <Badge className="nexus-badge-info">{reward.reward}</Badge>
                                </div>
                                <p className="text-sm text-muted-foreground mb-3">{reward.description}</p>
                                
                                <div className="space-y-2">
                                  <div className="flex justify-between text-sm">
                                    <span>{reward.requirement}</span>
                                    <span>{reward.progress}%</span>
                                  </div>
                                  <Progress value={reward.progress} className="w-full" />
                                </div>
                              </div>
                              
                              <div className="flex flex-col space-y-2">
                                {reward.unlocked ? (
                                  <Button>
                                    <Gift className="w-4 h-4 mr-2" />
                                    Réclamer
                                  </Button>
                                ) : (
                                  <Button variant="outline" disabled>
                                    <Lock className="w-4 h-4 mr-2" />
                                    Verrouillé
                                  </Button>
                                )}
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Classement */}
          {activeTab === 'leaderboard' && (
            <div className="space-y-6">
              <Card className="nexus-card">
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Trophy className="w-5 h-5 text-yellow-600" />
                    <span>Classement Mensuel</span>
                  </CardTitle>
                  <CardDescription>
                    Comparez votre progression avec les autres étudiants
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {monthlyLeaderboard.map((player, index) => (
                      <div
                        key={player.rank}
                        className={`nexus-leaderboard-item ${
                          player.name === student?.name ? 'current-user' : ''
                        }`}
                      >
                        <div className="flex items-center space-x-4">
                          <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm ${
                            player.rank === 1 ? 'bg-yellow-100 text-yellow-800' :
                            player.rank === 2 ? 'bg-gray-100 text-gray-800' :
                            player.rank === 3 ? 'bg-orange-100 text-orange-800' :
                            'bg-blue-100 text-blue-800'
                          }`}>
                            {player.rank === 1 ? '🥇' :
                             player.rank === 2 ? '🥈' :
                             player.rank === 3 ? '🥉' :
                             player.rank}
                          </div>
                          
                          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold">
                            {player.avatar}
                          </div>
                          
                          <div className="flex-1">
                            <div className="flex items-center justify-between">
                              <h4 className="font-semibold">{player.name}</h4>
                              <div className="flex items-center space-x-2">
                                <Coins className="w-4 h-4 text-yellow-600" />
                                <span className="font-bold">{player.xp.toLocaleString()} XP</span>
                              </div>
                            </div>
                            <div className="flex items-center space-x-2">
                              <Badge variant="outline" className="text-xs">
                                {player.badge}
                              </Badge>
                              {player.name === student?.name && (
                                <Badge className="nexus-badge-info text-xs">Vous</Badge>
                              )}
                            </div>
                          </div>
                          
                          {index > 0 && (
                            <div className="text-right">
                              <div className="flex items-center space-x-1 text-sm text-muted-foreground">
                                <ArrowDown className="w-3 h-3" />
                                <span>-{monthlyLeaderboard[0].xp - player.xp}</span>
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                  
                  <div className="mt-6 p-4 rounded-lg bg-blue-50 dark:bg-blue-900/20">
                    <div className="flex items-center space-x-3">
                      <Trophy className="w-5 h-5 text-blue-600" />
                      <div>
                        <h4 className="font-medium text-blue-900 dark:text-blue-100">
                          Récompenses de fin de mois
                        </h4>
                        <p className="text-sm text-blue-700 dark:text-blue-300">
                          Top 3 : Badges exclusifs • Top 10 : Bonus XP • Tous : Certificat de participation
                        </p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </div>

      {/* Modal de badge */}
      {showBadgeModal && selectedBadge && (
        <div className="nexus-modal-overlay">
          <div className="nexus-modal max-w-md">
            <div className="text-center p-6">
              <div className={`w-20 h-20 rounded-lg flex items-center justify-center mx-auto mb-4 ${
                selectedBadge.unlocked 
                  ? getRarityColor(selectedBadge.rarity)
                  : 'bg-gray-100 text-gray-400'
              }`}>
                {selectedBadge.unlocked ? (
                  <selectedBadge.icon className="w-10 h-10" />
                ) : (
                  <Lock className="w-10 h-10" />
                )}
              </div>
              
              <h3 className="text-xl font-bold mb-2">{selectedBadge.name}</h3>
              <p className="text-muted-foreground mb-4">{selectedBadge.description}</p>
              
              <div className="flex items-center justify-center space-x-4 mb-4">
                <Badge className={getRarityColor(selectedBadge.rarity)}>
                  {selectedBadge.rarity}
                </Badge>
                <div className="flex items-center space-x-1">
                  <Coins className="w-4 h-4 text-yellow-600" />
                  <span className="font-medium">{selectedBadge.xpReward} XP</span>
                </div>
              </div>
              
              {!selectedBadge.unlocked && (
                <div className="space-y-2 mb-4">
                  <div className="flex justify-between text-sm">
                    <span>Progression</span>
                    <span>{Math.round(selectedBadge.progress)}%</span>
                  </div>
                  <Progress value={selectedBadge.progress} className="w-full" />
                </div>
              )}
              
              <div className="flex space-x-2">
                <Button
                  variant="outline"
                  className="flex-1"
                  onClick={() => setShowBadgeModal(false)}
                >
                  Fermer
                </Button>
                {selectedBadge.unlocked && (
                  <Button className="flex-1">
                    <Share2 className="w-4 h-4 mr-2" />
                    Partager
                  </Button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Gamification;

