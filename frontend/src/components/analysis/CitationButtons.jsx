// import
import { Link2, ExternalLink, ShieldCheck, History } from "lucide-react";

const CitationButtons = () => {
  return (
    // 들어가는 코드
    <div className="flex flex-wrap gap-2">
      <button className="flex items-center gap-2 px-3 py-1.5 bg-white border border-slate-200 rounded-md text-[10px] font-bold text-slate-600 hover:bg-slate-50 transition-all">
        {/* // 7. 하드코딩된 인용 데이터
                V-24-901 §14.2
                Precedent: Case #772-B
                Statutory Ref: UCC-301
                // ← AI가 찾아온 실제 인용으로 교체 */}
        <Link2 size={12} className="text-blue-600" /> V-24-901 §14.2
        <ExternalLink size={10} />
      </button>
      <button className="flex items-center gap-2 px-3 py-1.5 bg-white border border-slate-200 rounded-md text-[10px] font-bold text-slate-600 hover:bg-slate-50 transition-all">
        <History size={12} className="text-blue-600" /> Precedent: Case #772-B
        <ExternalLink size={10} />
      </button>
      <button className="flex items-center gap-2 px-3 py-1.5 bg-white border border-slate-200 rounded-md text-[10px] font-bold text-slate-600 hover:bg-slate-50 transition-all">
        <ShieldCheck size={12} className="text-blue-600" /> Statutory Ref:
        UCC-301
        <ExternalLink size={10} />
      </button>
    </div>
  );
};

export default CitationButtons;
