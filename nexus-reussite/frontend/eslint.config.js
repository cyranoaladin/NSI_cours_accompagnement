import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'

export default [
  { ignores: ['dist'] },
  {
    files: ['**/*.{js,jsx}'],
    languageOptions: {
      ecmaVersion: 2020,
      globals: {
        ...globals.browser,
        ...globals.node,
        process: 'readonly',
        __dirname: 'readonly',
        require: 'readonly',
        clients: 'readonly',
        generateContent: 'readonly',
        analyzeProgress: 'readonly',
        analyzeLearningStyle: 'readonly',
        analyzeWeaknesses: 'readonly',
        getRecommendations: 'readonly',
        generateCatchupPlan: 'readonly',
        prepareNextSession: 'readonly',
        analyzeCode: 'readonly',
        startGuidedProject: 'readonly',
        generateDiagram: 'readonly',
        startVirtualLab: 'readonly',
        startOralSimulation: 'readonly',
        generateEssayPlan: 'readonly'
      },
      parserOptions: {
        ecmaVersion: 'latest',
        ecmaFeatures: { jsx: true },
        sourceType: 'module',
      },
    },
    plugins: {
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
    },
    rules: {
      ...js.configs.recommended.rules,
      ...reactHooks.configs.recommended.rules,
      'no-unused-vars': 'off',
      'no-useless-escape': 'off',
      'no-undef': 'off',
      'react-hooks/exhaustive-deps': 'off',
      'react-refresh/only-export-components': 'off',
    },
  },
]
