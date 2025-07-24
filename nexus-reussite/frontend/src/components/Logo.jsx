import React from 'react'

const Logo = ({ 
  size = 'default', 
  variant = 'full', 
  className = '',
  showSlogan = true,
  animated = false 
}) => {
  const sizes = {
    small: { width: 150, height: 50, scale: 0.5, fontSize: 16, sloganSize: 8 },
    default: { width: 300, height: 100, scale: 0.7, fontSize: 24, sloganSize: 12 },
    large: { width: 400, height: 133, scale: 0.9, fontSize: 32, sloganSize: 16 },
    icon: { width: 80, height: 80, scale: 0.8, fontSize: 0, sloganSize: 0 }
  };

  const currentSize = sizes[size] || sizes.default;

  if (variant === 'icon') {
    return (
      <svg 
        width={80} 
        height={80} 
        viewBox="0 0 80 80" 
        className={`nexus-logo-icon ${animated ? 'animate-pulse' : ''} ${className}`}
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          <linearGradient id="nexusGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#0F172A" />
            <stop offset="50%" stopColor="#1E293B" />
            <stop offset="100%" stopColor="#334155" />
          </linearGradient>
          <linearGradient id="arrowGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#E63946" />
            <stop offset="50%" stopColor="#DC2626" />
            <stop offset="100%" stopColor="#B91C1C" />
          </linearGradient>
          <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge> 
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>
        
        <g transform="translate(10, 10) scale(0.8)">
          {/* Barre gauche du N */}
          <path 
            d="M 10 10 V 60" 
            stroke="url(#nexusGradient)" 
            strokeWidth="8" 
            strokeLinecap="round"
            filter={animated ? "url(#glow)" : "none"}
          />
          
          {/* Flèche diagonale */}
          <path 
            d="M 10 60 L 50 10" 
            stroke="url(#arrowGradient)" 
            strokeWidth="8" 
            strokeLinecap="round"
            filter={animated ? "url(#glow)" : "none"}
          />
          <path 
            d="M 50 10 L 40 13" 
            stroke="url(#arrowGradient)" 
            strokeWidth="8" 
            strokeLinecap="round"
          />
          <path 
            d="M 50 10 L 47 20" 
            stroke="url(#arrowGradient)" 
            strokeWidth="8" 
            strokeLinecap="round"
          />
          
          {/* Barre droite du N */}
          <path 
            d="M 50 5 V 60" 
            stroke="url(#nexusGradient)" 
            strokeWidth="8" 
            strokeLinecap="round"
            filter={animated ? "url(#glow)" : "none"}
          />
        </g>
      </svg>
    );
  }

  return (
    <svg 
      width={currentSize.width} 
      height={currentSize.height} 
      viewBox={`0 0 ${currentSize.width} ${currentSize.height}`}
      className={`nexus-logo ${animated ? 'animate-pulse' : ''} ${className}`}
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <linearGradient id="nexusGradientFull" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#0F172A" />
          <stop offset="50%" stopColor="#1E293B" />
          <stop offset="100%" stopColor="#334155" />
        </linearGradient>
        <linearGradient id="arrowGradientFull" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#E63946" />
          <stop offset="50%" stopColor="#DC2626" />
          <stop offset="100%" stopColor="#B91C1C" />
        </linearGradient>
        <linearGradient id="textGradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="#0F172A" />
          <stop offset="100%" stopColor="#1E293B" />
        </linearGradient>
        <filter id="glowEffect">
          <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
          <feMerge> 
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
        <filter id="dropShadow">
          <feDropShadow dx="2" dy="2" stdDeviation="3" floodOpacity="0.3"/>
        </filter>
      </defs>

      {/* Fond subtil pour la visibilité */}
      <rect width="100%" height="100%" fill="transparent"/>

      {/* Logo Icône amélioré */}
      <g transform={`translate(20, 15) scale(${currentSize.scale})`}>
        {/* Barre gauche du N avec effet de profondeur */}
        <path 
          d="M 10 10 V 90" 
          stroke="url(#nexusGradientFull)" 
          strokeWidth="12" 
          strokeLinecap="round"
          filter="url(#dropShadow)"
        />
        
        {/* Flèche diagonale avec gradient et effet lumineux */}
        <path 
          d="M 10 90 L 60 10" 
          stroke="url(#arrowGradientFull)" 
          strokeWidth="12" 
          strokeLinecap="round"
          filter={animated ? "url(#glowEffect)" : "url(#dropShadow)"}
        />
        <path 
          d="M 60 10 L 45 15" 
          stroke="url(#arrowGradientFull)" 
          strokeWidth="12" 
          strokeLinecap="round"
        />
        <path 
          d="M 60 10 L 55 25" 
          stroke="url(#arrowGradientFull)" 
          strokeWidth="12" 
          strokeLinecap="round"
        />
        
        {/* Barre droite du N avec effet de profondeur */}
        <path 
          d="M 60 0 V 90" 
          stroke="url(#nexusGradientFull)" 
          strokeWidth="12" 
          strokeLinecap="round"
          filter="url(#dropShadow)"
        />
        
        {/* Points de connexion subtils */}
        <circle cx="10" cy="90" r="6" fill="url(#nexusGradientFull)" opacity="0.8"/>
        <circle cx="60" cy="10" r="6" fill="url(#arrowGradientFull)" opacity="0.8"/>
      </g>

      {/* Texte de la Marque avec typographie améliorée */}
      {variant === 'full' && currentSize.fontSize > 0 && (
        <g transform={`translate(100, ${currentSize.height * 0.4})`}>
          <text 
            fontFamily="Poppins, Inter, system-ui, sans-serif" 
            fontSize={currentSize.fontSize} 
            fill="url(#textGradient)"
            filter="url(#dropShadow)"
          >
            <tspan fontWeight="800" letterSpacing="1px">NEXUS</tspan>
            <tspan fontWeight="400" letterSpacing="0.5px"> Réussite</tspan>
          </text>
        </g>
      )}
      
      {/* Slogan amélioré */}
      {variant === 'full' && showSlogan && currentSize.sloganSize > 0 && (
        <g transform={`translate(100, ${currentSize.height * 0.7})`}>
          <text 
            fontFamily="Inter, system-ui, sans-serif" 
            fontSize={currentSize.sloganSize} 
            fill="#E63946" 
            letterSpacing="2px"
            fontWeight="500"
          >
            VISER. ATTEINDRE. DÉPASSER.
          </text>
        </g>
      )}

      {/* Éléments décoratifs subtils */}
      {variant === 'full' && (
        <g opacity="0.1">
          <circle cx={currentSize.width - 30} cy="20" r="3" fill="#E63946"/>
          <circle cx={currentSize.width - 20} cy="30" r="2" fill="#0F172A"/>
          <circle cx={currentSize.width - 40} cy="35" r="1.5" fill="#E63946"/>
        </g>
      )}
    </svg>
  );
};

// Composant Logo compact pour les headers
export const LogoCompact = ({ className = '', animated = false }) => (
  <div className={`flex items-center space-x-3 ${className}`}>
    <Logo size="small" variant="icon" animated={animated} />
    <div className="flex flex-col">
      <span className="font-bold text-lg text-slate-900 dark:text-white">
        NEXUS
      </span>
      <span className="text-xs text-red-600 font-medium tracking-wider">
        RÉUSSITE
      </span>
    </div>
  </div>
);

// Composant Logo pour les footers
export const LogoFooter = ({ className = '' }) => (
  <div className={`flex flex-col items-start space-y-2 ${className}`}>
    <Logo size="small" variant="full" showSlogan={false} />
    <p className="text-xs text-muted-foreground max-w-xs">
      Plateforme d'excellence pour les élèves du système français en Tunisie
    </p>
  </div>
);

// Composant Logo animé pour les chargements
export const LogoLoader = ({ className = '' }) => (
  <div className={`flex flex-col items-center space-y-4 ${className}`}>
    <Logo size="default" variant="icon" animated={true} />
    <div className="flex space-x-1">
      <div className="w-2 h-2 bg-red-600 rounded-full animate-bounce"></div>
      <div className="w-2 h-2 bg-red-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
      <div className="w-2 h-2 bg-red-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
    </div>
  </div>
);

// Composant Logo pour les emails et documents
export const LogoDocument = ({ className = '' }) => (
  <div className={`flex items-center space-x-4 ${className}`}>
    <Logo size="small" variant="full" showSlogan={false} />
    <div className="h-8 w-px bg-gray-300"></div>
    <div className="text-xs text-gray-600">
      <div className="font-semibold">Centre Urbain Nord</div>
      <div>Immeuble VENUS, Apt. C13</div>
      <div>1082 – Tunis</div>
    </div>
  </div>
);

export default Logo;

