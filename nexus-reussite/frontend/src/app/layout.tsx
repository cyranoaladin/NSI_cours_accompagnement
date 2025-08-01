import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { Providers } from '../components/Providers';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'),
  title: 'Nexus Réussite - Plateforme éducative NSI premium',
  description: 'Plateforme d\'accompagnement NSI révolutionnaire avec intelligence artificielle pour réussir brillamment en Première et Terminale.',
  keywords: 'NSI, informatique, bac, cours, IA, assistant, éducation, programmation',
  authors: [{ name: 'Nexus Réussite' }],
  creator: 'Nexus Réussite',
  publisher: 'Nexus Réussite',
  robots: {
    index: true,
    follow: true,
  },
  openGraph: {
    type: 'website',
    locale: 'fr_FR',
    url: 'https://nexus-reussite.fr',
    title: 'Nexus Réussite - Excellence en NSI avec l\'IA',
    description: 'Plateforme d\'accompagnement NSI révolutionnaire avec intelligence artificielle',
    siteName: 'Nexus Réussite',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'Nexus Réussite - Plateforme éducative NSI',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Nexus Réussite - Excellence en NSI avec l\'IA',
    description: 'Plateforme d\'accompagnement NSI révolutionnaire avec intelligence artificielle',
    images: ['/og-image.png'],
    creator: '@nexusreussite',
  },
  icons: {
    icon: '/favicon.ico',
    shortcut: '/nexus-favicon.svg',
    apple: '/logo_nexus-reussite.png',
  },
  manifest: '/manifest.json',
  verification: {
    google: 'your-google-verification-code',
  },
};

export const viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr" suppressHydrationWarning>
      <head>
        <meta name="theme-color" content="#2563eb" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content="Nexus Réussite" />
        <meta name="format-detection" content="telephone=no" />
        <meta name="mobile-web-app-capable" content="yes" />
        <meta name="msapplication-TileColor" content="#2563eb" />
        <meta name="msapplication-tap-highlight" content="no" />
      </head>
      <body className={`${inter.className} antialiased`}>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}
