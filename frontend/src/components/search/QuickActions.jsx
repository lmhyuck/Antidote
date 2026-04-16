import { FiEdit, FiFileText, FiImage, FiCode } from "react-icons/fi";
{
  /* Quick Actions */
}
const QuickActions = () => {
  return (
    <div className="mt-6 flex flex-wrap justify-center gap-3">
      {[
        { icon: <FiEdit />, label: "Write a poem" },
        { icon: <FiFileText />, label: "Summarize text" },
        { icon: <FiImage />, label: "Generate Image" },
        { icon: <FiCode />, label: "Code help" },
      ].map((action) => (
        <button
          key={action.label}
          className="flex items-center gap-2 rounded-lg bg-slate-100 px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-200 transition-colors"
        >
          <span className="text-blue-600 text-sm">{action.icon}</span>
          {action.label}
        </button>
      ))}
    </div>
  );
};

export default QuickActions;
