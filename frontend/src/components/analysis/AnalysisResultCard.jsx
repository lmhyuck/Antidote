import {
  CheckCircle2,
  AlertCircle,
  Edit3,
  Search,
  ShieldCheck,
  ChevronDown,
} from "lucide-react";

const AnalysisResultCard = () => {
  return (
    <>
      <style>{`
        @keyframes slideInRight {
          from { transform: translateX(100%); opacity: 0; }
          to   { transform: translateX(0); opacity: 1; }
        }
        @keyframes fadeIn {
          from { opacity: 0; }
          to   { opacity: 1; }
        }
        .panel-animate-in {
          animation: slideInRight 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        .fade-in {
          animation: fadeIn 0.3s ease-out forwards;
        }
        .findings-card {
          transition: border-color 0.3s ease;
        }
        .findings-card:hover {
          border-color: #1e40af;
        }
      `}</style>
      <div className="bg-slate-50/50 border-l-4 border-blue-600 rounded-r-2xl p-6 relative overflow-visible ring-1 ring-slate-200">
        <div className="space-y-6 relative z-10">
          {/* 항목 1 — CheckCircle */}
          <div className="flex gap-4">
            <div className="h-6 w-6 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 mt-1 shrink-0">
              <CheckCircle2 size={14} />
            </div>
            <div className="text-left">
              <h4 className="text-sm font-bold text-slate-900">
                Qualified Right to Terminate
              </h4>
              {/* 4. 하드코딩된 분석 결과 지워야 함 */}
              <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                제14.2조는 사전 통지 90일을 조건으로...
              </p>
            </div>
          </div>

          {/* 항목 2 — AlertCircle */}
          <div className="flex gap-4">
            <div className="h-6 w-6 rounded-full bg-red-100 flex items-center justify-center text-red-600 mt-1 shrink-0">
              <AlertCircle size={14} />
            </div>
            <div className="text-left">
              <h4 className="text-sm font-bold text-slate-900">
                The 3-Month Trigger Risk
              </h4>
              <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                {/* 전부 삭제, AI 분석 결과로 교체 */}
                해당 조항은 "3개월 연속"이라는 조건이...
              </p>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-3 pt-4 border-t border-slate-100">
          <button className="flex items-center gap-2 px-4 py-2 border border-blue-600 text-blue-600 rounded-lg text-xs font-bold hover:bg-blue-50 transition-all">
            <Edit3 size={14} /> fix clause
          </button>
          <button className="flex items-center gap-2 px-4 py-2 border border-blue-600 text-blue-600 rounded-lg text-xs font-bold hover:bg-blue-50 transition-all">
            <Search size={14} /> Search Precedents
          </button>
          <button className="flex items-center gap-2 px-4 py-2 border border-blue-600 text-blue-600 rounded-lg text-xs font-bold hover:bg-blue-50 transition-all">
            <ShieldCheck size={14} /> Explain Risk
          </button>
          <button className="flex items-center gap-1 text-slate-400 text-xs font-bold ml-2">
            See More <ChevronDown size={14} />
          </button>
        </div>
      </div>
    </>
  );
};

export default AnalysisResultCard;
