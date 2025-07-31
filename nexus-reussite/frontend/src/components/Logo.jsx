
const Logo = ({
  size = 'default',
  variant = 'full',
  className = '',
  showSlogan = true,
  animated = false
}) => {
  const sizes = {
    small: { height: 32, maxWidth: 120 },
    default: { height: 48, maxWidth: 180 },
    large: { height: 64, maxWidth: 240 },
    icon: { height: 40, maxWidth: 40 }
  };

  const currentSize = sizes[size] || sizes.default;

  return (
    <img
      src="/logo_nexus-reussite.png"
      alt="Nexus Réussite - Plateforme Éducative"
      className={`nexus-logo ${animated ? 'animate-pulse' : ''} ${className}`}
      style={{
        height: `${currentSize.height}px`,
        maxWidth: `${currentSize.maxWidth}px`,
        width: 'auto',
        objectFit: 'contain'
      }}
    />
  );
};

// Composant Logo compact pour les headers
export const LogoCompact = ({ className = '', animated = false }) => (
  <div className={`flex items-center space-x-3 ${className}`}>
    <Logo size="small" animated={animated} />
  </div>
);

// Composant Logo pour les footers
export const LogoFooter = ({ className = '' }) => (
  <div className={`flex flex-col items-start space-y-2 ${className}`}>
    <Logo size="small" />
    <p className="text-xs text-muted-foreground max-w-xs">
      Plateforme d'excellence pour les élèves du système français en Tunisie
    </p>
  </div>
);

// Composant Logo animé pour les chargements
export const LogoLoader = ({ className = '' }) => (
  <div className={`flex flex-col items-center space-y-4 ${className}`}>
    <Logo size="default" animated={true} />
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
    <Logo size="small" />
    <div className="h-8 w-px bg-gray-300"></div>
    <div className="text-xs text-gray-600">
      <div className="font-semibold">Centre Urbain Nord</div>
      <div>Immeuble VENUS, Apt. C13</div>
      <div>1082 – Tunis</div>
    </div>
  </div>
);

export default Logo;
