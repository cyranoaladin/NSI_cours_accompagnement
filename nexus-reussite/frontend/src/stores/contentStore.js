import { create } from 'zustand';
import { contentService, progressService } from '../services/api';

const useContentStore = create((set, get) => ({
  // État des cours
  courses: [],
  currentCourse: null,
  lessons: [],
  currentLesson: null,

  // État de chargement
  isLoading: false,
  error: null,

  // Filtres et pagination
  filters: {
    level: 'all', // 'premiere', 'terminale', 'all'
    category: 'all',
    difficulty: 'all',
    search: '',
  },
  pagination: {
    page: 1,
    limit: 12,
    total: 0,
    totalPages: 0,
  },

  // Progression
  progress: {},
  stats: null,

  // Actions - Courses
  fetchCourses: async (params = {}) => {
    set({ isLoading: true, error: null });

    try {
      const { filters, pagination } = get();
      const queryParams = {
        ...filters,
        page: pagination.page,
        limit: pagination.limit,
        ...params,
      };

      const data = await contentService.getCourses(queryParams);

      set({
        courses: data.courses || [],
        pagination: {
          ...pagination,
          total: data.total || 0,
          totalPages: data.totalPages || 0,
        },
        isLoading: false,
      });

      return data;
    } catch (error) {
      set({
        error: error.response?.data?.message || 'Erreur lors du chargement des cours',
        isLoading: false,
      });
      throw error;
    }
  },

  fetchCourse: async (courseId) => {
    set({ isLoading: true, error: null });

    try {
      const course = await contentService.getCourse(courseId);
      set({
        currentCourse: course,
        isLoading: false,
      });

      return course;
    } catch (error) {
      set({
        error: error.response?.data?.message || 'Erreur lors du chargement du cours',
        isLoading: false,
      });
      throw error;
    }
  },

  // Actions - Lessons
  fetchLessons: async (courseId) => {
    set({ isLoading: true, error: null });

    try {
      const lessons = await contentService.getLessons(courseId);
      set({
        lessons,
        isLoading: false,
      });

      return lessons;
    } catch (error) {
      set({
        error: error.response?.data?.message || 'Erreur lors du chargement des leçons',
        isLoading: false,
      });
      throw error;
    }
  },

  fetchLesson: async (lessonId) => {
    set({ isLoading: true, error: null });

    try {
      const lesson = await contentService.getLesson(lessonId);
      set({
        currentLesson: lesson,
        isLoading: false,
      });

      return lesson;
    } catch (error) {
      set({
        error: error.response?.data?.message || 'Erreur lors du chargement de la leçon',
        isLoading: false,
      });
      throw error;
    }
  },

  // Actions - Filtres
  setFilters: (newFilters) => {
    set((state) => ({
      filters: { ...state.filters, ...newFilters },
      pagination: { ...state.pagination, page: 1 }, // Reset page
    }));

    // Recharger les cours avec les nouveaux filtres
    get().fetchCourses();
  },

  setSearch: (search) => {
    get().setFilters({ search });
  },

  clearFilters: () => {
    set({
      filters: {
        level: 'all',
        category: 'all',
        difficulty: 'all',
        search: '',
      },
      pagination: { ...get().pagination, page: 1 },
    });

    get().fetchCourses();
  },

  // Actions - Pagination
  setPage: (page) => {
    set((state) => ({
      pagination: { ...state.pagination, page },
    }));

    get().fetchCourses();
  },

  nextPage: () => {
    const { pagination } = get();
    if (pagination.page < pagination.totalPages) {
      get().setPage(pagination.page + 1);
    }
  },

  prevPage: () => {
    const { pagination } = get();
    if (pagination.page > 1) {
      get().setPage(pagination.page - 1);
    }
  },

  // Actions - Progression
  fetchProgress: async (studentId) => {
    try {
      const progress = await progressService.getStudentProgress(studentId);
      set({ progress });
      return progress;
    } catch (error) {
      console.error('Erreur lors du chargement de la progression:', error);
      throw error;
    }
  },

  markLessonComplete: async (lessonId) => {
    try {
      const result = await progressService.markLessonComplete(lessonId);

      // Mettre à jour la progression locale
      set((state) => ({
        progress: {
          ...state.progress,
          [lessonId]: {
            ...state.progress[lessonId],
            completed: true,
            completedAt: new Date().toISOString(),
          },
        },
      }));

      return result;
    } catch (error) {
      console.error('Erreur lors de la mise à jour de la progression:', error);
      throw error;
    }
  },

  fetchStats: async () => {
    try {
      const stats = await progressService.getProgressStats();
      set({ stats });
      return stats;
    } catch (error) {
      console.error('Erreur lors du chargement des statistiques:', error);
      throw error;
    }
  },

  // Actions - Gestion
  createCourse: async (courseData) => {
    set({ isLoading: true, error: null });

    try {
      const course = await contentService.createCourse(courseData);
      set((state) => ({
        courses: [course, ...state.courses],
        isLoading: false,
      }));

      return course;
    } catch (error) {
      set({
        error: error.response?.data?.message || 'Erreur lors de la création du cours',
        isLoading: false,
      });
      throw error;
    }
  },

  updateCourse: async (courseId, courseData) => {
    set({ isLoading: true, error: null });

    try {
      const course = await contentService.updateCourse(courseId, courseData);
      set((state) => ({
        courses: state.courses.map((c) => (c.id === courseId ? course : c)),
        currentCourse: state.currentCourse?.id === courseId ? course : state.currentCourse,
        isLoading: false,
      }));

      return course;
    } catch (error) {
      set({
        error: error.response?.data?.message || 'Erreur lors de la mise à jour du cours',
        isLoading: false,
      });
      throw error;
    }
  },

  deleteCourse: async (courseId) => {
    set({ isLoading: true, error: null });

    try {
      await contentService.deleteCourse(courseId);
      set((state) => ({
        courses: state.courses.filter((c) => c.id !== courseId),
        currentCourse: state.currentCourse?.id === courseId ? null : state.currentCourse,
        isLoading: false,
      }));
    } catch (error) {
      set({
        error: error.response?.data?.message || 'Erreur lors de la suppression du cours',
        isLoading: false,
      });
      throw error;
    }
  },

  // Utilitaires
  getCourseProgress: (courseId) => {
    const { progress } = get();
    return progress[`course_${courseId}`] || { completed: 0, total: 0, percentage: 0 };
  },

  getLessonProgress: (lessonId) => {
    const { progress } = get();
    return progress[lessonId] || { completed: false, score: null };
  },

  // Nettoyage
  clearError: () => set({ error: null }),

  reset: () => set({
    currentCourse: null,
    currentLesson: null,
    lessons: [],
    error: null,
  }),

  clearAll: () => set({
    courses: [],
    currentCourse: null,
    lessons: [],
    currentLesson: null,
    isLoading: false,
    error: null,
    progress: {},
    stats: null,
  }),
}));

export default useContentStore;
