import { describe, it, expect } from 'vitest';

// Utilitaires de date pour tester
const formatDate = (dateString) => {
  if (!dateString) return 'Date invalide';
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR');
  } catch {
    return 'Date invalide';
  }
};

const calculateAge = (birthdate) => {
  const today = new Date();
  const birth = new Date(birthdate);
  let age = today.getFullYear() - birth.getFullYear();
  const monthDiff = today.getMonth() - birth.getMonth();
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--;
  }
  
  return age;
};

const isValidDate = (dateString) => {
  const date = new Date(dateString);
  return date instanceof Date && !isNaN(date);
};

const getRelativeTime = (dateString) => {
  const date = new Date(dateString);
  const now = new Date();
  const diffInHours = Math.abs(now - date) / (1000 * 60 * 60);
  
  if (diffInHours < 1) return 'Il y a moins d\'une heure';
  if (diffInHours < 24) return `Il y a ${Math.floor(diffInHours)} heure(s)`;
  if (diffInHours < 168) return `Il y a ${Math.floor(diffInHours / 24)} jour(s)`;
  return formatDate(dateString);
};

describe('dateUtils', () => {
  describe('formatDate', () => {
    it('should format ISO date to French format', () => {
      expect(formatDate('2025-07-23T10:30:00Z')).toBe('23/07/2025');
    });
    
    it('should format simple date string', () => {
      expect(formatDate('2025-07-23')).toBe('23/07/2025');
    });
    
    it('should handle null input gracefully', () => {
      expect(formatDate(null)).toBe('Date invalide');
    });
    
    it('should handle undefined input gracefully', () => {
      expect(formatDate(undefined)).toBe('Date invalide');
    });
    
    it('should handle invalid date string', () => {
      expect(formatDate('not-a-date')).toBe('Date invalide');
    });
  });
  
  describe('calculateAge', () => {
    it('should calculate correct age from birthdate', () => {
      // Test avec une date de naissance connue
      const birthdate = '2008-01-01';
      const age = calculateAge(birthdate);
      expect(age).toBeGreaterThanOrEqual(16);
      expect(age).toBeLessThanOrEqual(17);
    });
    
    it('should handle leap year correctly', () => {
      const birthdate = '2000-02-29'; // Année bissextile
      const age = calculateAge(birthdate);
      expect(age).toBeGreaterThanOrEqual(24);
    });
    
    it('should handle future birthdate', () => {
      const futureDate = '2030-01-01';
      const age = calculateAge(futureDate);
      expect(age).toBeLessThan(0);
    });
  });

  describe('isValidDate', () => {
    it('should return true for valid ISO date', () => {
      expect(isValidDate('2025-07-23T10:30:00Z')).toBe(true);
    });
    
    it('should return true for valid simple date', () => {
      expect(isValidDate('2025-07-23')).toBe(true);
    });
    
    it('should return false for invalid date', () => {
      expect(isValidDate('not-a-date')).toBe(false);
    });
    
    it('should return false for null', () => {
      expect(isValidDate(null)).toBe(false);
    });
    
    it('should return false for undefined', () => {
      expect(isValidDate(undefined)).toBe(false);
    });
  });

  describe('getRelativeTime', () => {
    it('should return "moins d\'une heure" for recent date', () => {
      const recentDate = new Date(Date.now() - 30 * 60 * 1000); // 30 min ago
      expect(getRelativeTime(recentDate.toISOString())).toBe('Il y a moins d\'une heure');
    });
    
    it('should return hours for same day', () => {
      const hoursAgo = new Date(Date.now() - 3 * 60 * 60 * 1000); // 3 hours ago
      const result = getRelativeTime(hoursAgo.toISOString());
      expect(result).toContain('Il y a 3 heure');
    });
    
    it('should return days for recent past', () => {
      const daysAgo = new Date(Date.now() - 2 * 24 * 60 * 60 * 1000); // 2 days ago
      const result = getRelativeTime(daysAgo.toISOString());
      expect(result).toContain('Il y a 2 jour');
    });
    
    it('should return formatted date for old dates', () => {
      const oldDate = '2025-01-01';
      const result = getRelativeTime(oldDate);
      expect(result).toBe('01/01/2025');
    });
  });
});
