/**
 * Tooltip Component
 * Shows helpful information on hover
 */

import { useState } from 'react';

export default function Tooltip({ children, content, position = "top" }) {
  const [isVisible, setIsVisible] = useState(false);
  
  const positions = {
    top: "bottom-full left-1/2 -translate-x-1/2 mb-2",
    bottom: "top-full left-1/2 -translate-x-1/2 mt-2",
    left: "right-full top-1/2 -translate-y-1/2 mr-2",
    right: "left-full top-1/2 -translate-y-1/2 ml-2"
  };
  
  return (
    <div 
      className="relative inline-block"
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
    >
      {children}
      {isVisible && content && (
        <div className={`absolute ${positions[position]} z-50 px-3 py-2 text-sm text-white bg-gray-900 rounded-lg shadow-lg whitespace-nowrap animate-fade-in`}>
          {content}
          <div className="absolute w-2 h-2 bg-gray-900 transform rotate-45" 
               style={{
                 [position === 'top' ? 'bottom' : position === 'bottom' ? 'top' : position === 'left' ? 'right' : 'left']: '-4px',
                 left: position === 'top' || position === 'bottom' ? '50%' : undefined,
                 top: position === 'left' || position === 'right' ? '50%' : undefined,
                 transform: position === 'top' || position === 'bottom' ? 'translateX(-50%) rotate(45deg)' : 'translateY(-50%) rotate(45deg)'
               }}
          />
        </div>
      )}
    </div>
  );
}
