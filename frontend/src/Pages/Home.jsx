import { FiImage } from "react-icons/fi";
import { HiShieldCheck } from "react-icons/hi";
import Navbar from "../components/layout/Navbar";
import SearchBar from "../components/search/SearchBar";
import QuickActions from "../components/search/QuickActions";

const Home = () => {
  return (
    <>
      <style>{`
        .feature-card {
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .feature-card:hover {
          transform: translateY(-4px);
          box-shadow: 0 20px 25px -5px rgba(0,0,0,0.05);
        }
        @keyframes barGrow {
          from { height: 0; }
        }
        .analytics-bar {
          animation: barGrow 1s ease-out forwards;
        }
      `}</style>

      <Navbar variant="home" />

      <div className="flex">
        <main className="flex-1 p-8">
          <div className="mx-auto max-w-5xl pt-12 text-center">
            <h1 className="mb-4 text-6xl font-black tracking-tight text-slate-900">
              계약서의 독소조항을 <br /> 찾아드립니다.
            </h1>
            <p className="mb-12 text-lg text-slate-500">
              계약서 PDF를 첨부하거나 조항을 입력하면 AI가 즉시 분석해드립니다.
            </p>
            <SearchBar />
            <QuickActions />

            {/* User Guide */}
            <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
              {/* 시작하기 */}
              <div className="feature-card col-span-1 md:col-span-2 rounded-3xl bg-white p-8 shadow-lg ring-1 ring-slate-100">
                <span className="inline-block rounded-full bg-blue-100 px-3 py-1 text-[10px] font-bold uppercase tracking-widest text-blue-700">
                  Quick Start
                </span>
                <h3 className="mt-4 text-2xl font-bold text-slate-900">
                  이렇게 시작하세요
                </h3>
                <div className="mt-4 space-y-3">
                  {[
                    {
                      step: "01",
                      text: "검색창에 계약서 조항을 붙여넣거나 질문을 입력하세요.",
                    },
                    {
                      step: "02",
                      text: "또는 📎 아이콘을 눌러 계약서 PDF를 첨부하세요.",
                    },
                    {
                      step: "03",
                      text: "AI가 독소조항과 리스크를 자동으로 분석합니다.",
                    },
                  ].map((item) => (
                    <div key={item.step} className="flex items-start gap-3">
                      <span className="text-xs font-black text-blue-600 mt-0.5 w-6 shrink-0">
                        {item.step}
                      </span>
                      <p className="text-sm text-slate-500 leading-relaxed">
                        {item.text}
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              {/* PDF 분석 */}
              <div className="feature-card rounded-3xl bg-blue-600 p-8 text-white shadow-lg shadow-blue-600/20">
                <div className="h-10 w-10 rounded-xl bg-white/20 flex items-center justify-center text-2xl">
                  📄
                </div>
                <h3 className="mt-6 text-2xl font-bold">PDF 분석</h3>
                <p className="mt-2 text-sm text-blue-50/80 leading-relaxed">
                  계약서 PDF를 첨부하면 전체 조항을 자동으로 읽고 위험 조항을
                  찾아드립니다.
                </p>
              </div>

              {/* 텍스트 질문 */}
              <div className="feature-card rounded-3xl bg-white p-8 shadow-lg ring-1 ring-slate-100">
                <div className="h-10 w-10 rounded-xl bg-slate-100 flex items-center justify-center text-2xl">
                  💬
                </div>
                <h3 className="mt-4 text-lg font-bold text-slate-900">
                  텍스트로 질문
                </h3>
                <p className="mt-2 text-sm text-slate-500 leading-relaxed">
                  특정 조항을 복사해서 붙여넣거나 궁금한 법적 내용을 자유롭게
                  질문하세요.
                </p>
                <div className="mt-4 rounded-xl bg-slate-50 p-3 text-xs text-slate-400 font-mono">
                  "제14조 해지 조항에서 불리한 부분이 있나요?"
                </div>
              </div>

              {/* 독소조항이란 */}
              <div className="feature-card col-span-1 md:col-span-2 rounded-3xl bg-white p-8 shadow-lg ring-1 ring-slate-100">
                <div className="flex items-start gap-6">
                  <div className="flex-1">
                    <h3 className="text-2xl font-bold text-slate-900">
                      독소조항이란?
                    </h3>
                    <p className="mt-2 text-sm text-slate-500 leading-relaxed">
                      계약서에 숨어있는 불리한 조항으로, 일방적인 해지권·과도한
                      위약금· 책임 면제 등이 대표적입니다. Antidote가 자동으로
                      찾아 설명해드립니다.
                    </p>
                    <div className="mt-4 flex flex-wrap gap-2">
                      {[
                        "일방적 해지권",
                        "과도한 위약금",
                        "책임 면제",
                        "자동 갱신",
                      ].map((tag) => (
                        <span
                          key={tag}
                          className="rounded-full bg-red-50 px-3 py-1 text-xs font-semibold text-red-500"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="h-24 w-24 rounded-2xl bg-red-50 flex items-center justify-center text-4xl shrink-0">
                    ⚠️
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </>
  );
};

export default Home;
