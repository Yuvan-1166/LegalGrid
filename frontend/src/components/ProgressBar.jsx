/**
 * Progress Bar Component
 * Displays progress with smooth animations
 */

export default function ProgressBar({ value, max = 100, label, color = "indigo" }) {
  const percentage = Math.min((value / max) * 100, 100);
  
  const colorClasses = {
    indigo: "bg-indigo-600",
    red: "bg-red-600",
    yellow: "bg-yellow-600",
    green: "bg-green-600",
    purple: "bg-purple-600",
    blue: "bg-blue-600"
  };
  
  const bgColorClasses = {
    indigo: "bg-indigo-100",
    red: "bg-red-100",
    yellow: "bg-yellow-100",
    green: "bg-green-100",
    purple: "bg-purple-100",
    blue: "bg-blue-100"
  };
  
  return (
    <div className="w-full">
      {label && (
        <div className="flex justify-between mb-2">
          <span className="text-sm font-medium text-gray-700">{label}</span>
          <span className="text-sm font-medium text-gray-700">{Math.round(percentage)}%</span>
        </div>
      )}
      <div className={`w-full ${bgColorClasses[color]} rounded-full h-3 overflow-hidden`}>
        <div
          className={`${colorClasses[color]} h-full rounded-full transition-all duration-500 ease-out`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
