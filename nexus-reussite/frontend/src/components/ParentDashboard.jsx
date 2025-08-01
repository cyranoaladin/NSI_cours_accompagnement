'use client';

import { Bell, BookOpen, Calendar, Clock, TrendingUp, User } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Progress } from './ui/progress';

const ParentDashboard = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Tableau de bord Parent</h1>
          <p className="text-gray-600 mt-2">Suivez les progrès de votre enfant</p>
        </div>

        {/* Informations sur l'enfant */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Heures de Cours</CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">24h</div>
              <p className="text-xs text-muted-foreground">Ce mois-ci</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Moyenne Générale</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">16.5/20</div>
              <p className="text-xs text-muted-foreground">+1.2 ce mois</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Cours Suivis</CardTitle>
              <BookOpen className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">5</div>
              <p className="text-xs text-muted-foreground">Matières actives</p>
            </CardContent>
          </Card>
        </div>

        {/* Progrès par matière */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <Card>
            <CardHeader>
              <CardTitle>Progrès par Matière</CardTitle>
              <CardDescription>Évolution de votre enfant par matière</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium">Mathématiques</span>
                  <span className="text-sm text-muted-foreground">85%</span>
                </div>
                <Progress value={85} />
              </div>
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium">NSI</span>
                  <span className="text-sm text-muted-foreground">92%</span>
                </div>
                <Progress value={92} />
              </div>
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium">Physique</span>
                  <span className="text-sm text-muted-foreground">78%</span>
                </div>
                <Progress value={78} />
              </div>
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium">Français</span>
                  <span className="text-sm text-muted-foreground">88%</span>
                </div>
                <Progress value={88} />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Prochains Rendez-vous</CardTitle>
              <CardDescription>Planning des cours à venir</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center space-x-4">
                  <Calendar className="h-4 w-4 text-blue-500" />
                  <div>
                    <p className="text-sm font-medium">Mathématiques</p>
                    <p className="text-sm text-muted-foreground">Demain 14h00 - M. Dubois</p>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <Calendar className="h-4 w-4 text-green-500" />
                  <div>
                    <p className="text-sm font-medium">NSI</p>
                    <p className="text-sm text-muted-foreground">Vendredi 10h00 - Mme Martin</p>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  <Calendar className="h-4 w-4 text-purple-500" />
                  <div>
                    <p className="text-sm font-medium">Physique</p>
                    <p className="text-sm text-muted-foreground">Samedi 16h00 - M. Rousseau</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Actions rapides */}
        <Card>
          <CardHeader>
            <CardTitle>Actions Rapides</CardTitle>
            <CardDescription>Gérez le suivi de votre enfant</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <Button className="w-full" variant="outline">
                <Calendar className="mr-2 h-4 w-4" />
                Planifier un Cours
              </Button>
              <Button className="w-full" variant="outline">
                <User className="mr-2 h-4 w-4" />
                Contacter Professeur
              </Button>
              <Button className="w-full" variant="outline">
                <BookOpen className="mr-2 h-4 w-4" />
                Voir les Devoirs
              </Button>
              <Button className="w-full" variant="outline">
                <Bell className="mr-2 h-4 w-4" />
                Notifications
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ParentDashboard;
