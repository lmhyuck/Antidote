const SuggestedTopics = () => {
  return (
    <>
      <style>{`
        .live-card {
          animation: slideInRight 0.5s cubic-bezier(0.16, 1, 0.3, 1);
          transition: all 0.3s ease;
        }
        .live-card:hover {
          transform: translateY(-6px) scale(1.02);
        }
        @keyframes slideInRight {
          from { transform: translateX(100%); opacity: 0; }
          to   { transform: translateX(0); opacity: 1; }
        }
      `}</style>
      <div className="w-64 bg-white rounded-2xl shadow-xl p-6 ring-1 ring-slate-100 live-card">
        <h3 className="text-sm font-extrabold text-slate-800 mb-4 tracking-tight">
          SUGGESTED TOPICS
        </h3>
        <ul className="space-y-3 text-sm font-semibold text-blue-600">
          <li className="hover:underline cursor-pointer">
            {/* 6. 하드코딩된 토픽 리스트 아래 세개 */}• Liability Limitations
          </li>
          <li className="hover:underline cursor-pointer">
            • Force Majeure Audit
          </li>
          <li className="hover:underline cursor-pointer">
            • GDPR Compliance Gaps
          </li>
        </ul>
      </div>
    </>
  );
};

export default SuggestedTopics;
