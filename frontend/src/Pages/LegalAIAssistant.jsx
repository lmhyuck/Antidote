import React, { useState } from "react";
import {
  FolderOpen,
  FileText,
  Layers,
  AlertTriangle,
  Bot,
  HelpCircle,
  Archive,
  Bell,
  Settings,
  Download,
  Paperclip,
  Mic,
  Send,
  History,
  Sliders,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  Link2,
  ExternalLink,
  Edit3,
  Search,
  ShieldCheck,
  ChevronDown,
} from "lucide-react";

const LegalAIAssistant = () => {
  const [inputValue, setInputValue] = useState("");

  const navItems = [
    { icon: <FolderOpen size={20} />, label: "Active Cases" },
    { icon: <FileText size={20} />, label: "Document Library" },
    { icon: <Layers size={20} />, label: "Clause Bank" },
    { icon: <AlertTriangle size={20} />, label: "Risk Profiles" },
    { icon: <Bot size={20} />, label: "AI Assistant", active: true },
  ];

  return (
    <div className="min-h-screen bg-[#F8FAFC] font-sans text-[#0F172A] flex">
      {/* Side Navigation Bar */}
      <aside className="fixed left-0 top-0 h-screen w-64 flex flex-col border-r border-slate-200/50 bg-white p-6 z-40">
        <div className="mb-10">
          <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-1 text-left">
            Case Dossier
          </p>
          <p className="text-xs font-medium text-slate-500 text-left">
            V-24-901 Enterprise Agreement
          </p>
        </div>

        <nav className="flex-1 space-y-1">
          {navItems.map((item) => (
            <button
              key={item.label}
              className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-all ${
                item.active
                  ? "bg-slate-100 text-[#1E40AF] shadow-sm"
                  : "text-slate-500 hover:bg-slate-50"
              }`}
            >
              {item.icon}
              {item.label}
            </button>
          ))}
        </nav>

        <div className="mt-auto pt-6 border-t border-slate-100 space-y-2">
          <button className="w-full flex items-center justify-center gap-2 rounded-lg bg-[#1E40AF] py-3 text-sm font-semibold text-white shadow-lg shadow-blue-600/20 hover:bg-blue-800 transition-all active:scale-95 mb-4">
            Upload New Contract
          </button>
          <button className="w-full flex items-center gap-3 px-4 py-2 text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors">
            <HelpCircle size={18} />
            Support
          </button>
          <button className="w-full flex items-center gap-3 px-4 py-2 text-sm font-medium text-slate-500 hover:text-slate-900 transition-colors">
            <Archive size={18} />
            Archive
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 ml-64 min-h-screen flex flex-col">
        {/* Top Nav */}
        <header className="sticky top-0 z-50 flex h-16 w-full items-center justify-between bg-white/60 px-8 backdrop-blur-xl border-b border-slate-200/50">
          <div className="flex items-center gap-8">
            <div className="flex items-center gap-2">
              <div className="h-6 w-6 rounded-full bg-[#1a73e8] flex items-center justify-center">
                <div className="h-2 w-2 rounded-full bg-white"></div>
              </div>
              <span className="text-xl font-black tracking-tighter text-[#000000]">
                Dot AI
              </span>
            </div>
            <nav className="flex gap-6 text-sm font-semibold text-slate-500">
              {["Dashboard", "Contract Hub", "Risk Reports", "Analytics"].map(
                (link) => (
                  <a
                    key={link}
                    href="#"
                    className="hover:text-[#1e40af] transition-colors"
                  >
                    {link}
                  </a>
                ),
              )}
            </nav>
          </div>
          <div className="flex items-center gap-4">
            <button className="text-slate-400 hover:text-[#1e40af] transition-colors">
              <Bell size={20} />
            </button>
            <button className="text-slate-400 hover:text-[#1e40af] transition-colors">
              <Settings size={20} />
            </button>
            <button className="rounded-md bg-[#1e40af] px-4 py-2 text-xs font-bold text-white hover:bg-[#002244] transition-all flex items-center gap-2">
              <Download size={14} /> Export Report
            </button>
          </div>
        </header>

        {/* Chat Section */}
        <div className="flex-1 p-8 max-w-5xl mx-auto w-full pb-32">
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center gap-4">
              <div className="h-12 w-12 rounded-xl bg-[#1a73e8] flex items-center justify-center shadow-lg shadow-blue-900/20 text-white">
                <Bot size={28} />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-[#0F172A] text-left">
                  Legal Intellect AI
                </h2>
                <div className="flex items-center gap-2 text-xs text-blue-600 font-medium">
                  <span className="h-1.5 w-1.5 rounded-full bg-blue-600 animate-pulse"></span>
                  Analyzing V-24-901 Enterprise Agreement
                </div>
              </div>
            </div>
            <div className="flex gap-2">
              <button className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-600 text-xs font-bold rounded-md transition-colors flex items-center gap-2">
                <History size={14} /> History
              </button>
              <button className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-600 text-xs font-bold rounded-md transition-colors flex items-center gap-2">
                <Sliders size={14} /> Parameters
              </button>
            </div>
          </div>

          {/* User Message */}
          <div className="flex justify-end mb-8">
            <div className="max-w-2xl bg-white border border-slate-200 rounded-2xl rounded-tr-none p-6 shadow-sm">
              <p className="text-sm leading-relaxed text-slate-700 text-left">
                제14.2조(편의에 의한 계약 해지)와 서비스 수준 부속서(SLA)와의
                관계를 고려하여 답변하시오.
              </p>
            </div>
          </div>

          {/* AI Response */}
          <div className="flex gap-4 mb-12">
            <div className="h-8 w-8 rounded-lg bg-blue-600 flex items-center justify-center text-white shrink-0 mt-1 shadow-md">
              <Sparkles size={18} />
            </div>
            <div className="flex-1 space-y-6">
              <div className="max-w-3xl">
                <p className="text-sm font-semibold text-slate-900 leading-relaxed mb-4 text-left">
                  제14.2조는 사전 통지 90일을 조건으로 사유 없는 해지를 명시하고
                  있으나, 이에 대한 준수 여부에 따라 제15.4조(중대한 계약 위반에
                  의한 해지)가 적용될 수 있다.
                </p>

                {/* Findings Card */}
                <div className="bg-slate-50/50 border-l-4 border-blue-600 rounded-r-2xl p-6 relative overflow-visible ring-1 ring-slate-200">
                  {/* 기존 내용 */}
                  <div className="space-y-6 relative z-10">
                    <div className="flex gap-4">
                      <div className="h-6 w-6 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 mt-1 shrink-0">
                        <CheckCircle2 size={14} />
                      </div>
                      <div className="text-left">
                        <h4 className="text-sm font-bold text-slate-900">
                          Qualified Right to Terminate - 제한적 해지 권한
                          (조건부)
                        </h4>
                        <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                          제14.2조는 사전 통지 90일을 조건으로 사유 없는 해지를
                          명시하고 있으나, 이에 대한 준수 여부에 따라
                          제15.4조(중대한 계약 위반에 의한 해지)가 적용될 수
                          있다.
                        </p>
                      </div>
                    </div>

                    <div className="flex gap-4">
                      <div className="h-6 w-6 rounded-full bg-red-100 flex items-center justify-center text-red-600 mt-1 shrink-0">
                        <AlertCircle size={14} />
                      </div>
                      <div className="text-left">
                        <h4 className="text-sm font-bold text-slate-900">
                          The 3-Month Trigger Risk - 3개월 조건 트리거 리스크
                        </h4>
                        <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                          해당 조항은 “3개월 연속”이라는 조건이 중대한 계약
                          위반과 직접적으로 연결된다고 명시하고 있지 않다.
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* 오른쪽 패널 (한 덩어리로 묶기) */}
                  <div className="absolute top-0 left-full ml-6 flex flex-col gap-6 z-20">
                    {/* Live Analysis */}
                    <div className="w-48 bg-white rounded-xl shadow-xl p-4 ring-1 ring-slate-100 live-card">
                      <p className="text-[10px] font-black text-slate-400 uppercase tracking-tighter mb-4 text-left">
                        Live Analysis
                      </p>

                      <div className="space-y-4">
                        <div>
                          <div className="flex justify-between text-[10px] font-bold mb-1">
                            <span>RISK SCORE</span>
                            <span className="text-red-500">Elevated</span>
                          </div>
                          <div className="h-1 w-full bg-slate-100 rounded-full overflow-hidden">
                            <div className="h-full bg-red-500 w-[85%] bar-animate"></div>
                          </div>
                        </div>

                        <div>
                          <div className="flex justify-between text-[10px] font-bold mb-1">
                            <span>CLAUSE CLARITY</span>
                            <span className="text-blue-500">Optimal</span>
                          </div>
                          <div className="h-1 w-full bg-slate-100 rounded-full overflow-hidden">
                            <div className="h-full bg-blue-500 w-[95%]"></div>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Suggested Topics */}
                    <div className="w-64 bg-white rounded-2xl shadow-xl p-6 ring-1 ring-slate-100 live-card">
                      <h3 className="text-sm font-extrabold text-slate-800 mb-4 tracking-tight">
                        SUGGESTED TOPICS
                      </h3>

                      <ul className="space-y-3 text-sm font-semibold text-blue-600">
                        <li className="hover:underline cursor-pointer">
                          • Liability Limitations
                        </li>
                        <li className="hover:underline cursor-pointer">
                          • Force Majeure Audit
                        </li>
                        <li className="hover:underline cursor-pointer">
                          • GDPR Compliance Gaps
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

              {/* Citations */}
              <div className="flex flex-wrap gap-2">
                <button className="flex items-center gap-2 px-3 py-1.5 bg-white border border-slate-200 rounded-md text-[10px] font-bold text-slate-600 hover:bg-slate-50 transition-all">
                  <Link2 size={12} className="text-blue-600" /> V-24-901 §14.2{" "}
                  <ExternalLink size={10} />
                </button>
                <button className="flex items-center gap-2 px-3 py-1.5 bg-white border border-slate-200 rounded-md text-[10px] font-bold text-slate-600 hover:bg-slate-50 transition-all">
                  <History size={12} className="text-blue-600" /> Precedent:
                  Case #772-B <ExternalLink size={10} />
                </button>
                <button className="flex items-center gap-2 px-3 py-1.5 bg-white border border-slate-200 rounded-md text-[10px] font-bold text-slate-600 hover:bg-slate-50 transition-all">
                  <ShieldCheck size={12} className="text-blue-600" /> Statutory
                  Ref: UCC-301 <ExternalLink size={10} />
                </button>
              </div>

              {/* Actions */}
              <div className="flex items-center gap-3 pt-4 border-t border-slate-100">
                <button className="flex items-center gap-2 px-4 py-2 border border-blue-600 text-blue-600 rounded-lg text-xs font-bold hover:bg-blue-50 transition-all">
                  <Edit3 size={14} /> Fix this clause
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
          </div>
        </div>

        {/* Floating Input Bar */}
        <div className="fixed bottom-0 left-64 right-0 p-8 bg-gradient-to-t from-[#F8FAFC] via-[#F8FAFC] to-transparent z-40">
          <div className="max-w-4xl mx-auto relative group">
            <div className="flex items-center gap-4 bg-white rounded-2xl p-4 shadow-2xl shadow-blue-900/10 ring-1 ring-slate-200 focus-within:ring-2 focus-within:ring-blue-600 transition-all">
              <button className="text-slate-400 hover:text-blue-600 transition-colors">
                <Paperclip size={20} />
              </button>
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="특정 조항, 리스크 지표, 또는 법적 판례에 대해 질문하세요…"
                className="flex-1 bg-transparent text-sm outline-none placeholder:text-slate-400 font-medium"
              />
              <div className="flex items-center gap-2">
                <button className="text-slate-400 hover:text-blue-600 transition-colors">
                  <Mic size={20} />
                </button>
                <button className="h-10 w-10 bg-[#1a73e8] text-white rounded-xl flex items-center justify-center shadow-lg hover:bg-[#002244] active:scale-95 transition-all">
                  <Send size={20} />
                </button>
              </div>
            </div>
            <div className="mt-4 flex justify-center gap-8 opacity-40 group-hover:opacity-60 transition-opacity">
              <div className="flex items-center gap-1.5 text-[8px] font-bold uppercase tracking-widest">
                <div className="h-1 w-1 rounded-full bg-blue-600"></div> Press{" "}
                <span className="bg-slate-200 px-1 rounded">CMD + K</span> for
                command menu
              </div>
              <div className="flex items-center gap-1.5 text-[8px] font-bold uppercase tracking-widest text-red-500">
                AI may hallucinate legal data. Verify with counsel.
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default LegalAIAssistant;
