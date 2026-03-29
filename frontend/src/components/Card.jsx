export default function Card({ children, className = '', hover = false }) {
  const hoverClass = hover ? 'hover:shadow-lg transition-shadow duration-200' : ''
  
  return (
    <div className={`bg-white rounded-lg shadow-md p-6 ${hoverClass} ${className}`}>
      {children}
    </div>
  )
}
