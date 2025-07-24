import React, { useState, useEffect } from 'react';
import { 
  ChevronLeft, 
  ChevronRight, 
  Plus, 
  Calendar as CalendarIcon,
  Clock,
  MapPin,
  Users,
  Video,
  Edit,
  Trash2,
  Eye
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';

export default function ScheduleCalendar({ userId, userRole = 'student' }) {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [events, setEvents] = useState([]);
  const [viewMode, setViewMode] = useState('month'); // month, week, day
  const [loading, setLoading] = useState(true);

  // Événements de démonstration
  const demoEvents = [
    {
      id: 1,
      title: 'Cours de Mathématiques',
      subject: 'Mathématiques',
      type: 'group_lesson',
      start: new Date(2024, 0, 15, 14, 0), // 15 janvier 2024, 14h00
      end: new Date(2024, 0, 15, 15, 30),
      location: 'Salle A1',
      teacher: 'M. Dubois',
      students: ['Sarah', 'Ahmed', 'Léa', 'Youssef'],
      status: 'confirmed',
      isOnline: false
    },
    {
      id: 2,
      title: 'Session NSI - Algorithmes',
      subject: 'NSI',
      type: 'individual_lesson',
      start: new Date(2024, 0, 16, 10, 0),
      end: new Date(2024, 0, 16, 11, 0),
      location: 'Visioconférence',
      teacher: 'Mme Martin',
      students: ['Ahmed'],
      status: 'confirmed',
      isOnline: true
    },
    {
      id: 3,
      title: 'Physique - Optique',
      subject: 'Physique',
      type: 'group_lesson',
      start: new Date(2024, 0, 17, 16, 0),
      end: new Date(2024, 0, 17, 17, 30),
      location: 'Lab Physique',
      teacher: 'Dr. Rousseau',
      students: ['Sarah', 'Léa', 'Nour'],
      status: 'pending',
      isOnline: false
    },
    {
      id: 4,
      title: 'Coaching Parcoursup',
      subject: 'Orientation',
      type: 'coaching',
      start: new Date(2024, 0, 18, 15, 0),
      end: new Date(2024, 0, 18, 16, 0),
      location: 'Bureau conseil',
      teacher: 'Mme Benali',
      students: ['Sarah'],
      status: 'confirmed',
      isOnline: false
    },
    {
      id: 5,
      title: 'Révision Bac Blanc',
      subject: 'Mathématiques',
      type: 'revision',
      start: new Date(2024, 0, 19, 9, 0),
      end: new Date(2024, 0, 19, 12, 0),
      location: 'Salle d\'examen',
      teacher: 'M. Dubois',
      students: ['Sarah', 'Ahmed', 'Léa', 'Youssef', 'Nour'],
      status: 'confirmed',
      isOnline: false
    }
  ];

  useEffect(() => {
    loadEvents();
  }, [currentDate, userId]);

  const loadEvents = async () => {
    try {
      setLoading(true);
      
      // Simuler le chargement des événements
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setEvents(demoEvents);
    } catch (error) {
      console.error('Erreur lors du chargement des événements:', error);
    } finally {
      setLoading(false);
    }
  };

  const getDaysInMonth = (date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDayOfWeek = firstDay.getDay();

    const days = [];
    
    // Jours du mois précédent
    for (let i = startingDayOfWeek - 1; i >= 0; i--) {
      const prevDate = new Date(year, month, -i);
      days.push({ date: prevDate, isCurrentMonth: false });
    }
    
    // Jours du mois actuel
    for (let day = 1; day <= daysInMonth; day++) {
      days.push({ date: new Date(year, month, day), isCurrentMonth: true });
    }
    
    // Jours du mois suivant pour compléter la grille
    const remainingDays = 42 - days.length; // 6 semaines × 7 jours
    for (let day = 1; day <= remainingDays; day++) {
      days.push({ date: new Date(year, month + 1, day), isCurrentMonth: false });
    }
    
    return days;
  };

  const getEventsForDate = (date) => {
    return events.filter(event => {
      const eventDate = new Date(event.start);
      return eventDate.toDateString() === date.toDateString();
    });
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString('fr-FR', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getEventTypeColor = (type) => {
    switch (type) {
      case 'group_lesson':
        return 'bg-blue-500';
      case 'individual_lesson':
        return 'bg-green-500';
      case 'coaching':
        return 'bg-purple-500';
      case 'revision':
        return 'bg-orange-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getEventTypeLabel = (type) => {
    switch (type) {
      case 'group_lesson':
        return 'Cours groupe';
      case 'individual_lesson':
        return 'Cours individuel';
      case 'coaching':
        return 'Coaching';
      case 'revision':
        return 'Révision';
      default:
        return 'Événement';
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'confirmed':
        return <Badge className="bg-green-100 text-green-800">Confirmé</Badge>;
      case 'pending':
        return <Badge className="bg-yellow-100 text-yellow-800">En attente</Badge>;
      case 'cancelled':
        return <Badge className="bg-red-100 text-red-800">Annulé</Badge>;
      default:
        return <Badge variant="outline">Inconnu</Badge>;
    }
  };

  const navigateMonth = (direction) => {
    const newDate = new Date(currentDate);
    newDate.setMonth(currentDate.getMonth() + direction);
    setCurrentDate(newDate);
  };

  const goToToday = () => {
    const today = new Date();
    setCurrentDate(today);
    setSelectedDate(today);
  };

  const monthNames = [
    'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
    'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
  ];

  const dayNames = ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'];

  const days = getDaysInMonth(currentDate);
  const selectedDateEvents = getEventsForDate(selectedDate);

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="h-96 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* En-tête */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Planning</h1>
          <p className="text-gray-600">Gérez vos cours et rendez-vous</p>
        </div>
        
        <div className="flex space-x-3">
          <Button variant="outline" onClick={goToToday}>
            Aujourd'hui
          </Button>
          {userRole === 'teacher' && (
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Nouveau cours
            </Button>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Calendrier principal */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <div className="flex justify-between items-center">
              <CardTitle className="flex items-center">
                <CalendarIcon className="h-5 w-5 mr-2" />
                {monthNames[currentDate.getMonth()]} {currentDate.getFullYear()}
              </CardTitle>
              
              <div className="flex space-x-2">
                <Button variant="outline" size="sm" onClick={() => navigateMonth(-1)}>
                  <ChevronLeft className="h-4 w-4" />
                </Button>
                <Button variant="outline" size="sm" onClick={() => navigateMonth(1)}>
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </CardHeader>
          
          <CardContent>
            {/* Grille du calendrier */}
            <div className="grid grid-cols-7 gap-1 mb-4">
              {dayNames.map(day => (
                <div key={day} className="p-2 text-center text-sm font-medium text-gray-500">
                  {day}
                </div>
              ))}
            </div>
            
            <div className="grid grid-cols-7 gap-1">
              {days.map((day, index) => {
                const dayEvents = getEventsForDate(day.date);
                const isSelected = selectedDate.toDateString() === day.date.toDateString();
                const isToday = new Date().toDateString() === day.date.toDateString();
                
                return (
                  <button
                    key={index}
                    onClick={() => setSelectedDate(day.date)}
                    className={`p-2 min-h-[80px] text-left border rounded-lg transition-colors ${
                      isSelected
                        ? 'bg-blue-100 border-blue-500'
                        : isToday
                        ? 'bg-blue-50 border-blue-200'
                        : day.isCurrentMonth
                        ? 'hover:bg-gray-50 border-gray-200'
                        : 'text-gray-400 border-gray-100'
                    }`}
                  >
                    <div className={`text-sm font-medium ${
                      day.isCurrentMonth ? 'text-gray-900' : 'text-gray-400'
                    }`}>
                      {day.date.getDate()}
                    </div>
                    
                    {/* Événements du jour */}
                    <div className="mt-1 space-y-1">
                      {dayEvents.slice(0, 2).map(event => (
                        <div
                          key={event.id}
                          className={`text-xs p-1 rounded text-white truncate ${getEventTypeColor(event.type)}`}
                        >
                          {formatTime(event.start)} {event.title}
                        </div>
                      ))}
                      {dayEvents.length > 2 && (
                        <div className="text-xs text-gray-500">
                          +{dayEvents.length - 2} autres
                        </div>
                      )}
                    </div>
                  </button>
                );
              })}
            </div>
          </CardContent>
        </Card>

        {/* Détails du jour sélectionné */}
        <Card>
          <CardHeader>
            <CardTitle>
              {selectedDate.toLocaleDateString('fr-FR', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
              })}
            </CardTitle>
            <CardDescription>
              {selectedDateEvents.length} événement{selectedDateEvents.length !== 1 ? 's' : ''} prévu{selectedDateEvents.length !== 1 ? 's' : ''}
            </CardDescription>
          </CardHeader>
          
          <CardContent>
            {selectedDateEvents.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <CalendarIcon className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                <p>Aucun événement prévu</p>
              </div>
            ) : (
              <div className="space-y-4">
                {selectedDateEvents.map(event => (
                  <div key={event.id} className="border rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-medium text-gray-900">{event.title}</h4>
                      {getStatusBadge(event.status)}
                    </div>
                    
                    <div className="space-y-2 text-sm text-gray-600">
                      <div className="flex items-center">
                        <Clock className="h-4 w-4 mr-2" />
                        {formatTime(event.start)} - {formatTime(event.end)}
                      </div>
                      
                      <div className="flex items-center">
                        {event.isOnline ? (
                          <Video className="h-4 w-4 mr-2" />
                        ) : (
                          <MapPin className="h-4 w-4 mr-2" />
                        )}
                        {event.location}
                      </div>
                      
                      <div className="flex items-center">
                        <Users className="h-4 w-4 mr-2" />
                        {event.teacher}
                      </div>
                      
                      <div className="flex items-center">
                        <Badge variant="outline" className="text-xs">
                          {getEventTypeLabel(event.type)}
                        </Badge>
                      </div>
                    </div>
                    
                    {/* Participants */}
                    {event.students.length > 0 && (
                      <div className="mt-3">
                        <div className="text-xs font-medium text-gray-700 mb-1">
                          Participants ({event.students.length}) :
                        </div>
                        <div className="flex flex-wrap gap-1">
                          {event.students.map((student, index) => (
                            <Badge key={index} variant="secondary" className="text-xs">
                              {student}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    {/* Actions */}
                    <div className="flex space-x-2 mt-4">
                      <Button size="sm" variant="outline">
                        <Eye className="h-3 w-3 mr-1" />
                        Voir
                      </Button>
                      
                      {userRole === 'teacher' && (
                        <>
                          <Button size="sm" variant="outline">
                            <Edit className="h-3 w-3 mr-1" />
                            Modifier
                          </Button>
                          <Button size="sm" variant="outline">
                            <Trash2 className="h-3 w-3 mr-1" />
                            Annuler
                          </Button>
                        </>
                      )}
                      
                      {event.isOnline && (
                        <Button size="sm">
                          <Video className="h-3 w-3 mr-1" />
                          Rejoindre
                        </Button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Prochains événements */}
      <Card>
        <CardHeader>
          <CardTitle>Prochains événements</CardTitle>
          <CardDescription>
            Vos cours et rendez-vous à venir
          </CardDescription>
        </CardHeader>
        
        <CardContent>
          <div className="space-y-3">
            {events
              .filter(event => event.start > new Date())
              .sort((a, b) => a.start - b.start)
              .slice(0, 5)
              .map(event => (
                <div key={event.id} className="flex items-center justify-between p-3 border rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className={`h-3 w-3 rounded-full ${getEventTypeColor(event.type)}`} />
                    <div>
                      <div className="font-medium text-gray-900">{event.title}</div>
                      <div className="text-sm text-gray-600">
                        {event.start.toLocaleDateString('fr-FR')} à {formatTime(event.start)}
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    {getStatusBadge(event.status)}
                    <Button size="sm" variant="outline">
                      Voir
                    </Button>
                  </div>
                </div>
              ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

