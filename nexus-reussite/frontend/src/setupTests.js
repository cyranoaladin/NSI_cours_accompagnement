// Configuration globale des tests
import '@testing-library/jest-dom';
import { server } from './src/mocks/server';

// Configuration MSW (Mock Service Worker)
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
