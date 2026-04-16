// import
import {} from "lucide-react"; // 아이콘 없음

const LiveAnalysis = () => {
  return (
    // 들어가는 코드
    <>
      <style>{`
        @keyframes slideInRight {
          from { transform: translateX(100%); opacity: 0; }
          to   { transform: translateX(0); opacity: 1; }
        }
        @keyframes growBar {
          from { width: 0%; }
        }
        .live-card {
          animation: slideInRight 0.5s cubic-bezier(0.16, 1, 0.3, 1);
          transition: all 0.3s ease;
          position: relative;
        }
        .live-card:hover {
          transform: translateY(-6px) scale(1.02);
          box-shadow: 0 20px 25px -5px rgba(0,0,0,0.08);
        }
        .live-card::after {
          content: "";
          position: absolute;
          inset: 0;
          border-radius: 12px;
          background: linear-gradient(120deg, transparent, rgba(30,64,175,0.1), transparent);
          opacity: 0;
          transition: opacity 0.3s;
        }
        .live-card:hover::after {
          opacity: 1;
        }
        .bar-animate {
          animation: growBar 1s ease-out forwards;
        }
      `}</style>
      <div className="w-48 bg-white rounded-xl shadow-xl p-4 ring-1 ring-slate-100 live-card">
        <p className="text-[10px] font-black text-slate-400 uppercase tracking-tighter mb-4 text-left">
          Live Analysis
        </p>
        <div className="space-y-4">
          <div>
            <div className="flex justify-between text-[10px] font-bold mb-1">
              <span>RISK SCORE</span>
              {/* 5. 하드코딩된 수치 */}
              <span className="text-red-500">Elevated</span>
            </div>
            <div className="h-1 w-full bg-slate-100 rounded-full overflow-hidden">
              {/* 하드코딩됨 */}
              <div className="h-full bg-red-500 w-[85%] bar-animate"></div>
            </div>
          </div>
          <div>
            <div className="flex justify-between text-[10px] font-bold mb-1">
              <span>CLAUSE CLARITY</span>
              {/* 하드코딩됨 */}
              <span className="text-blue-500">Optimal</span>
            </div>
            <div className="h-1 w-full bg-slate-100 rounded-full overflow-hidden">
              {/* 하드코딩됨 AI 리스크 점수로 교체*/}
              <div className="h-full bg-blue-500 w-[95%]"></div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default LiveAnalysis;
