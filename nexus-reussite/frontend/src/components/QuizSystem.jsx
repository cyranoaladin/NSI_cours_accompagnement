import React, { useState, useEffect } from 'react';
import { 
  Clock, 
  CheckCircle, 
  XCircle, 
  RotateCcw, 
  Play, 
  Pause,
  Trophy,
  Target,
  Brain
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';

export default function QuizSystem({ quizData, onComplete }) {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [isActive, setIsActive] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [score, setScore] = useState(0);

  // Quiz de démonstration
  const defaultQuiz = {
    id: 'demo-math-proba',
    title: 'Probabilités - Terminale',
    subject: 'Mathématiques',
    duration: 900, // 15 minutes
    questions: [
      {
        id: 1,
        question: "Dans une urne contenant 5 boules rouges et 3 boules bleues, quelle est la probabilité de tirer une boule rouge ?",
        type: "multiple_choice",
        options: [
          { id: 'a', text: '3/8', correct: false },
          { id: 'b', text: '5/8', correct: true },
          { id: 'c', text: '1/2', correct: false },
          { id: 'd', text: '5/3', correct: false }
        ],
        explanation: "Il y a 5 boules rouges sur un total de 8 boules (5+3), donc P(rouge) = 5/8."
      },
      {
        id: 2,
        question: "Deux événements A et B sont indépendants si :",
        type: "multiple_choice",
        options: [
          { id: 'a', text: 'P(A ∩ B) = P(A) + P(B)', correct: false },
          { id: 'b', text: 'P(A ∩ B) = P(A) × P(B)', correct: true },
          { id: 'c', text: 'P(A ∪ B) = P(A) × P(B)', correct: false },
          { id: 'd', text: 'P(A|B) = P(B|A)', correct: false }
        ],
        explanation: "Deux événements sont indépendants si P(A ∩ B) = P(A) × P(B)."
      },
      {
        id: 3,
        question: "Dans un jeu de 32 cartes, quelle est la probabilité de tirer un roi ?",
        type: "multiple_choice",
        options: [
          { id: 'a', text: '1/8', correct: true },
          { id: 'b', text: '1/4', correct: false },
          { id: 'c', text: '4/32', correct: false },
          { id: 'd', text: '1/32', correct: false }
        ],
        explanation: "Il y a 4 rois dans un jeu de 32 cartes, donc P(roi) = 4/32 = 1/8."
      },
      {
        id: 4,
        question: "La loi binomiale B(n,p) a pour espérance :",
        type: "multiple_choice",
        options: [
          { id: 'a', text: 'np', correct: true },
          { id: 'b', text: 'np(1-p)', correct: false },
          { id: 'c', text: 'n(1-p)', correct: false },
          { id: 'd', text: 'p(1-p)', correct: false }
        ],
        explanation: "L'espérance d'une loi binomiale B(n,p) est E(X) = np."
      },
      {
        id: 5,
        question: "Si P(A) = 0.6 et P(B) = 0.4, et que A et B sont incompatibles, alors P(A ∪ B) = ?",
        type: "multiple_choice",
        options: [
          { id: 'a', text: '0.24', correct: false },
          { id: 'b', text: '1.0', correct: true },
          { id: 'c', text: '0.76', correct: false },
          { id: 'd', text: '0.2', correct: false }
        ],
        explanation: "Si A et B sont incompatibles, P(A ∩ B) = 0, donc P(A ∪ B) = P(A) + P(B) = 0.6 + 0.4 = 1.0."
      }
    ]
  };

  const quiz = quizData || defaultQuiz;

  useEffect(() => {
    if (isActive && timeRemaining > 0) {
      const timer = setInterval(() => {
        setTimeRemaining(time => {
          if (time <= 1) {
            setIsActive(false);
            handleSubmit();
            return 0;
          }
          return time - 1;
        });
      }, 1000);

      return () => clearInterval(timer);
    }
  }, [isActive, timeRemaining]);

  const startQuiz = () => {
    setTimeRemaining(quiz.duration);
    setIsActive(true);
    setCurrentQuestion(0);
    setSelectedAnswers({});
    setShowResults(false);
    setScore(0);
  };

  const pauseQuiz = () => {
    setIsActive(!isActive);
  };

  const selectAnswer = (questionId, answerId) => {
    setSelectedAnswers(prev => ({
      ...prev,
      [questionId]: answerId
    }));
  };

  const nextQuestion = () => {
    if (currentQuestion < quiz.questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const previousQuestion = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const calculateScore = () => {
    let correctAnswers = 0;
    quiz.questions.forEach(question => {
      const selectedAnswer = selectedAnswers[question.id];
      const correctOption = question.options.find(opt => opt.correct);
      if (selectedAnswer === correctOption.id) {
        correctAnswers++;
      }
    });
    return Math.round((correctAnswers / quiz.questions.length) * 100);
  };

  const handleSubmit = () => {
    const finalScore = calculateScore();
    setScore(finalScore);
    setShowResults(true);
    setIsActive(false);
    
    if (onComplete) {
      onComplete({
        score: finalScore,
        answers: selectedAnswers,
        timeSpent: quiz.duration - timeRemaining
      });
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBadge = (score) => {
    if (score >= 90) return { text: 'Excellent', variant: 'default', color: 'bg-green-500' };
    if (score >= 80) return { text: 'Très bien', variant: 'default', color: 'bg-blue-500' };
    if (score >= 60) return { text: 'Bien', variant: 'secondary', color: 'bg-yellow-500' };
    if (score >= 40) return { text: 'Passable', variant: 'outline', color: 'bg-orange-500' };
    return { text: 'À revoir', variant: 'destructive', color: 'bg-red-500' };
  };

  if (showResults) {
    const badge = getScoreBadge(score);
    
    return (
      <Card className="max-w-4xl mx-auto">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <div className={`h-20 w-20 rounded-full ${badge.color} flex items-center justify-center`}>
              <Trophy className="h-10 w-10 text-white" />
            </div>
          </div>
          <CardTitle className="text-2xl">Quiz terminé !</CardTitle>
          <CardDescription>Voici vos résultats pour "{quiz.title}"</CardDescription>
        </CardHeader>
        
        <CardContent className="space-y-6">
          {/* Score principal */}
          <div className="text-center">
            <div className={`text-6xl font-bold ${getScoreColor(score)} mb-2`}>
              {score}%
            </div>
            <Badge className={badge.color}>{badge.text}</Badge>
          </div>

          {/* Statistiques */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <Target className="h-8 w-8 mx-auto mb-2 text-blue-600" />
              <div className="text-2xl font-bold text-gray-900">
                {Math.round((score / 100) * quiz.questions.length)}/{quiz.questions.length}
              </div>
              <div className="text-sm text-gray-600">Bonnes réponses</div>
            </div>
            
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <Clock className="h-8 w-8 mx-auto mb-2 text-green-600" />
              <div className="text-2xl font-bold text-gray-900">
                {formatTime(quiz.duration - timeRemaining)}
              </div>
              <div className="text-sm text-gray-600">Temps utilisé</div>
            </div>
            
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <Brain className="h-8 w-8 mx-auto mb-2 text-purple-600" />
              <div className="text-2xl font-bold text-gray-900">
                {Math.round((quiz.duration - timeRemaining) / quiz.questions.length)}s
              </div>
              <div className="text-sm text-gray-600">Temps/question</div>
            </div>
          </div>

          {/* Révision des réponses */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Révision des réponses</h3>
            {quiz.questions.map((question, index) => {
              const selectedAnswer = selectedAnswers[question.id];
              const correctOption = question.options.find(opt => opt.correct);
              const selectedOption = question.options.find(opt => opt.id === selectedAnswer);
              const isCorrect = selectedAnswer === correctOption.id;

              return (
                <div key={question.id} className="border rounded-lg p-4">
                  <div className="flex items-start space-x-3">
                    <div className={`h-6 w-6 rounded-full flex items-center justify-center ${
                      isCorrect ? 'bg-green-100' : 'bg-red-100'
                    }`}>
                      {isCorrect ? (
                        <CheckCircle className="h-4 w-4 text-green-600" />
                      ) : (
                        <XCircle className="h-4 w-4 text-red-600" />
                      )}
                    </div>
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900 mb-2">
                        Question {index + 1}: {question.question}
                      </h4>
                      
                      {selectedOption && (
                        <div className={`p-2 rounded mb-2 ${
                          isCorrect ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
                        }`}>
                          <span className="font-medium">Votre réponse: </span>
                          {selectedOption.text}
                        </div>
                      )}
                      
                      {!isCorrect && (
                        <div className="p-2 rounded mb-2 bg-green-50 border border-green-200">
                          <span className="font-medium">Bonne réponse: </span>
                          {correctOption.text}
                        </div>
                      )}
                      
                      <div className="text-sm text-gray-600 bg-blue-50 p-2 rounded">
                        <span className="font-medium">Explication: </span>
                        {question.explanation}
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Actions */}
          <div className="flex justify-center space-x-4">
            <Button onClick={startQuiz} variant="outline">
              <RotateCcw className="h-4 w-4 mr-2" />
              Recommencer
            </Button>
            <Button onClick={() => window.history.back()}>
              Retour aux cours
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!isActive && timeRemaining === 0) {
    return (
      <Card className="max-w-2xl mx-auto">
        <CardHeader className="text-center">
          <CardTitle>{quiz.title}</CardTitle>
          <CardDescription>{quiz.subject}</CardDescription>
        </CardHeader>
        
        <CardContent className="space-y-6">
          <div className="text-center">
            <div className="h-20 w-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Brain className="h-10 w-10 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Prêt à commencer ?</h3>
            <p className="text-gray-600 mb-4">
              Ce quiz contient {quiz.questions.length} questions et dure {Math.round(quiz.duration / 60)} minutes.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
            <div className="p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{quiz.questions.length}</div>
              <div className="text-sm text-gray-600">Questions</div>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">{Math.round(quiz.duration / 60)}</div>
              <div className="text-sm text-gray-600">Minutes</div>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">QCM</div>
              <div className="text-sm text-gray-600">Format</div>
            </div>
          </div>

          <div className="text-center">
            <Button onClick={startQuiz} size="lg">
              <Play className="h-5 w-5 mr-2" />
              Commencer le quiz
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  const currentQ = quiz.questions[currentQuestion];
  const progress = ((currentQuestion + 1) / quiz.questions.length) * 100;

  return (
    <Card className="max-w-4xl mx-auto">
      <CardHeader>
        <div className="flex justify-between items-center">
          <div>
            <CardTitle>{quiz.title}</CardTitle>
            <CardDescription>
              Question {currentQuestion + 1} sur {quiz.questions.length}
            </CardDescription>
          </div>
          <div className="flex items-center space-x-4">
            <Button
              variant="outline"
              size="sm"
              onClick={pauseQuiz}
            >
              {isActive ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
            </Button>
            <div className={`text-lg font-mono ${timeRemaining < 60 ? 'text-red-600' : 'text-gray-900'}`}>
              <Clock className="h-4 w-4 inline mr-1" />
              {formatTime(timeRemaining)}
            </div>
          </div>
        </div>
        
        <Progress value={progress} className="mt-4" />
      </CardHeader>
      
      <CardContent className="space-y-6">
        {/* Question */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            {currentQ.question}
          </h3>
          
          {/* Options */}
          <div className="space-y-3">
            {currentQ.options.map((option) => (
              <button
                key={option.id}
                onClick={() => selectAnswer(currentQ.id, option.id)}
                className={`w-full text-left p-4 rounded-lg border-2 transition-colors ${
                  selectedAnswers[currentQ.id] === option.id
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <div className={`h-4 w-4 rounded-full border-2 ${
                    selectedAnswers[currentQ.id] === option.id
                      ? 'border-blue-500 bg-blue-500'
                      : 'border-gray-300'
                  }`}>
                    {selectedAnswers[currentQ.id] === option.id && (
                      <div className="h-2 w-2 bg-white rounded-full mx-auto mt-0.5" />
                    )}
                  </div>
                  <span className="font-medium text-gray-700">{option.id.toUpperCase()}.</span>
                  <span className="text-gray-900">{option.text}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Navigation */}
        <div className="flex justify-between items-center">
          <Button
            variant="outline"
            onClick={previousQuestion}
            disabled={currentQuestion === 0}
          >
            Précédent
          </Button>
          
          <div className="flex space-x-2">
            {quiz.questions.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentQuestion(index)}
                className={`h-8 w-8 rounded-full text-sm font-medium ${
                  index === currentQuestion
                    ? 'bg-blue-500 text-white'
                    : selectedAnswers[quiz.questions[index].id]
                    ? 'bg-green-100 text-green-700'
                    : 'bg-gray-100 text-gray-600'
                }`}
              >
                {index + 1}
              </button>
            ))}
          </div>
          
          {currentQuestion === quiz.questions.length - 1 ? (
            <Button
              onClick={handleSubmit}
              disabled={Object.keys(selectedAnswers).length !== quiz.questions.length}
            >
              Terminer le quiz
            </Button>
          ) : (
            <Button
              onClick={nextQuestion}
              disabled={!selectedAnswers[currentQ.id]}
            >
              Suivant
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

