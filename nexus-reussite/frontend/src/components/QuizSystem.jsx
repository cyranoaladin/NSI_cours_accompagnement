'use client';

import { Clock, HelpCircle, Play, RotateCcw } from 'lucide-react';
import { useEffect, useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Progress } from './ui/progress';

const QuizSystem = () => {
  const [currentQuiz, setCurrentQuiz] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [quizStarted, setQuizStarted] = useState(false);

  const quizzes = [
    {
      id: 1,
      title: "Algorithmique - Niveau 1",
      description: "Test sur les concepts de base d'algorithmique",
      duration: 15,
      difficulty: "Débutant",
      questions: [
        {
          id: 1,
          question: "Quelle est la complexité temporelle de l'algorithme de tri par insertion dans le pire cas ?",
          options: ["O(n)", "O(n log n)", "O(n²)", "O(2^n)"],
          correct: 2,
          explanation: "Le tri par insertion a une complexité O(n²) dans le pire cas."
        },
        {
          id: 2,
          question: "Qu'est-ce qu'une pile (stack) en informatique ?",
          options: [
            "Une structure FIFO (First In, First Out)",
            "Une structure LIFO (Last In, First Out)",
            "Une structure de données non ordonnée",
            "Un type de boucle"
          ],
          correct: 1,
          explanation: "Une pile est une structure de données LIFO."
        }
      ]
    }
  ];

  useEffect(() => {
    let interval;
    if (quizStarted && timeRemaining > 0) {
      interval = setInterval(() => {
        setTimeRemaining(prev => {
          if (prev <= 1) {
            handleQuizEnd();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [quizStarted, timeRemaining]);

  const startQuiz = (quiz) => {
    setCurrentQuiz(quiz);
    setCurrentQuestion(0);
    setSelectedAnswers({});
    setShowResults(false);
    setTimeRemaining(quiz.duration * 60);
    setQuizStarted(true);
  };

  const selectAnswer = (questionId, answerIndex) => {
    setSelectedAnswers(prev => ({
      ...prev,
      [questionId]: answerIndex
    }));
  };

  const nextQuestion = () => {
    if (currentQuestion < currentQuiz.questions.length - 1) {
      setCurrentQuestion(prev => prev + 1);
    } else {
      handleQuizEnd();
    }
  };

  const handleQuizEnd = () => {
    setQuizStarted(false);
    setShowResults(true);
  };

  const resetQuiz = () => {
    setCurrentQuiz(null);
    setCurrentQuestion(0);
    setSelectedAnswers({});
    setShowResults(false);
    setQuizStarted(false);
    setTimeRemaining(0);
  };

  const calculateScore = () => {
    if (!currentQuiz) return 0;

    let correct = 0;
    currentQuiz.questions.forEach(question => {
      if (selectedAnswers[question.id] === question.correct) {
        correct++;
      }
    });

    return Math.round((correct / currentQuiz.questions.length) * 100);
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (!currentQuiz) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Système de Quiz</h1>
            <p className="text-gray-600">Testez vos connaissances avec nos quiz interactifs</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {quizzes.map((quiz) => (
              <Card key={quiz.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <HelpCircle className="h-5 w-5 text-blue-600" />
                    {quiz.title}
                  </CardTitle>
                  <CardDescription>{quiz.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex justify-between text-sm text-gray-600">
                      <span className="flex items-center gap-1">
                        <Clock className="h-4 w-4" />
                        {quiz.duration} minutes
                      </span>
                      <span className="px-2 py-1 rounded-full text-xs bg-green-100 text-green-800">
                        {quiz.difficulty}
                      </span>
                    </div>

                    <div className="text-sm text-gray-600">
                      {quiz.questions.length} questions
                    </div>

                    <Button
                      className="w-full flex items-center gap-2"
                      onClick={() => startQuiz(quiz)}
                    >
                      <Play className="h-4 w-4" />
                      Commencer le Quiz
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (showResults) {
    const score = calculateScore();
    const correctAnswers = currentQuiz.questions.filter(
      question => selectedAnswers[question.id] === question.correct
    ).length;

    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Card>
            <CardHeader className="text-center">
              <CardTitle className="text-2xl">Résultats du Quiz</CardTitle>
              <CardDescription>{currentQuiz.title}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center mb-8">
                <div className="text-6xl font-bold text-green-600 mb-2">
                  {score}%
                </div>
                <p className="text-lg text-gray-600">
                  {correctAnswers} sur {currentQuiz.questions.length} questions correctes
                </p>
              </div>

              <div className="flex gap-4 mt-8">
                <Button onClick={resetQuiz} className="flex-1">
                  <RotateCcw className="h-4 w-4 mr-2" />
                  Choisir un autre quiz
                </Button>
                <Button
                  onClick={() => startQuiz(currentQuiz)}
                  variant="outline"
                  className="flex-1"
                >
                  <Play className="h-4 w-4 mr-2" />
                  Recommencer ce quiz
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  const currentQ = currentQuiz.questions[currentQuestion];
  const progress = ((currentQuestion + 1) / currentQuiz.questions.length) * 100;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Card className="mb-6">
          <CardContent className="pt-6">
            <div className="flex justify-between items-center mb-4">
              <h1 className="text-xl font-bold">{currentQuiz.title}</h1>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2 text-red-600">
                  <Clock className="h-4 w-4" />
                  <span className="font-mono">{formatTime(timeRemaining)}</span>
                </div>
                <span className="text-sm text-gray-600">
                  Question {currentQuestion + 1} sur {currentQuiz.questions.length}
                </span>
              </div>
            </div>
            <Progress value={progress} className="h-2" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Question {currentQuestion + 1}</CardTitle>
            <CardDescription>{currentQ.question}</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3 mb-6">
              {currentQ.options.map((option, index) => (
                <button
                  key={index}
                  className={`w-full p-4 text-left border-2 rounded-lg transition-colors ${selectedAnswers[currentQ.id] === index
                      ? 'border-blue-600 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                    }`}
                  onClick={() => selectAnswer(currentQ.id, index)}
                >
                  <div className="flex items-center gap-3">
                    <div className={`w-4 h-4 rounded-full border-2 ${selectedAnswers[currentQ.id] === index
                        ? 'border-blue-600 bg-blue-600'
                        : 'border-gray-300'
                      }`}>
                      {selectedAnswers[currentQ.id] === index && (
                        <div className="w-2 h-2 bg-white rounded-full mx-auto mt-0.5"></div>
                      )}
                    </div>
                    <span>{option}</span>
                  </div>
                </button>
              ))}
            </div>

            <div className="flex justify-between">
              <Button
                variant="outline"
                onClick={() => setCurrentQuestion(prev => prev - 1)}
                disabled={currentQuestion === 0}
              >
                Précédent
              </Button>

              <Button
                onClick={nextQuestion}
                disabled={selectedAnswers[currentQ.id] === undefined}
              >
                {currentQuestion === currentQuiz.questions.length - 1 ? 'Terminer' : 'Suivant'}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default QuizSystem;
