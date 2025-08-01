'use client';

import Image from 'next/image';

const Logo = ({ size = 'md', className = '' }) => {
  const sizes = {
    sm: { width: 120, height: 40, className: 'h-10' },
    md: { width: 200, height: 66, className: 'h-16' },
    lg: { width: 300, height: 99, className: 'h-24' },
    xl: { width: 500, height: 165, className: 'h-32' }
  };

  const logoSize = sizes[size] || sizes.md;

  return (
    <div className={`flex items-center ${className}`}>
      <Image
        src="/logo_nexus-reussite.webp"
        alt="Nexus Réussite - Formation NSI"
        width={logoSize.width}
        height={logoSize.height}
        className={`w-auto object-contain ${logoSize.className}`}
        priority
        quality={100}
      />
    </div>
  );
};

export default Logo;
