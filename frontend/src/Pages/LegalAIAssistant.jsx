import React, { useState } from "react";
import axios from "axios";
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
  CheckCircle,
  ArrowRight,
  ChevronLeft,
  Info,
  Scale,
  X,
  Menu,
} from "lucide-react"; // lucide-react 아이콘들

const LegalAIAssistant = () => {
  // 1. 분석 결과를 저장할 상태(State)
  const [report, setReport] = useState(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [inputValue, setInputValue] = useState("");
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: "bot",
      text: "안녕하세요. Antidote 법률 비서입니다. 검토 중인 계약서 조항이나 궁금한 법적 근거에 대해 말씀해 주세요.",
      sources: null,
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const navItems = [
    { icon: <FolderOpen size={20} />, label: "Active Cases" },
    { icon: <FileText size={20} />, label: "Document Library" },
    { icon: <Layers size={20} />, label: "Clause Bank" },
    { icon: <AlertTriangle size={20} />, label: "Risk Profiles" },
    { icon: <Bot size={20} />, label: "AI Assistant", active: true },
  ];

  const uploadPDF = async (file) => {
    setIsLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://localhost:8000/analysis/contract", // 또는 설정하신 경로
        formData,
      );

      // 2. 백엔드에서 보낸 LegalReport 객체가 response.data에 들어있음
      setReport(response.data);

      // 알림 메시지 추가 (선택사항)
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now(),
          type: "bot",
          text: "계약서 분석 리포트가 생성되었습니다. 오른쪽 리포트 섹션을 확인하세요!",
        },
      ]);
    } catch (error) {
      console.error("업로드 실패:", error);
      alert("파일 분석 중 오류가 발생했습니다.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!inputValue.trim() || isLoading) return;
    setIsLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/analysis/text", {
        content: inputValue,
        doc_name: "직접 입력 분석",
      });
      setReport(response.data);
    } catch (error) {
      alert("분석 중 오류가 발생했습니다.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-[#F1F5F9] font-sans text-[#1E293B] overflow-x-hidden">
      {/* 2. 왼쪽 사이드바: 본문을 밀어내며 열림 */}
      <aside
        className={`bg-white border-r border-slate-200 transition-all duration-300 ease-in-out flex flex-col shrink-0 overflow-hidden ${
          isSidebarOpen ? "w-64" : "w-0"
        }`}
      >
        {/* 사이드바 내부 (너비 고정용 div) */}
        <div className="w-64 flex flex-col h-screen sticky top-0">
          <div className="p-6 flex items-center justify-between">
            <div className="flex items-center gap-2 font-black tracking-tighter text-blue-600">
              <Scale size={20} /> ANTIDOTE
            </div>
            <button
              onClick={() => setIsSidebarOpen(false)}
              className="p-2 hover:bg-slate-100 rounded-lg text-slate-400"
            >
              <X size={20} />
            </button>
          </div>
          <nav className="flex-1 px-4">
            <button className="w-full flex items-center gap-3 px-4 py-3 bg-blue-50 text-blue-600 rounded-xl text-sm font-bold">
              <Bot size={18} /> 분석 어시스턴트
            </button>
          </nav>
        </div>
      </aside>

      {/* 2. 메인 콘텐츠 영역: 사이드바가 열리면 왼쪽 마진(ml-64)이 생기고, 닫히면(ml-0) 꽉 참 */}
      <div
        className={`flex-1 flex flex-col transition-all duration-300 ease-in-out ${
          isSidebarOpen ? "ml-64" : "ml-0"
        }`}
      >
        {/* 상단 헤더: 사이드바가 닫혔을 때만 메뉴 버튼을 보여줌 */}
        <header className="flex h-16 w-full items-center justify-between bg-white px-8 border-b border-slate-200 sticky top-0 z-40">
          <div className="flex items-center gap-4">
            {!isSidebarOpen && (
              <button
                onClick={() => setIsSidebarOpen(true)}
                className="p-2 hover:bg-slate-100 rounded-lg text-slate-600 transition-all"
              >
                <Menu size={24} />
              </button>
            )}
            <span className="text-xl font-black tracking-tighter text-slate-900">
              {!isSidebarOpen && "ANTIDOTE AI"}
            </span>
          </div>
          <div className="flex items-center gap-4">
            <button className="text-slate-400">
              <Bell size={20} />
            </button>
            <div className="h-8 w-8 rounded-full bg-slate-200 uppercase flex items-center justify-center text-[10px] font-bold">
              User
            </div>
          </div>
        </header>

        <main className="max-w-6xl mx-auto px-6 py-12">
          {!report ? (
            /* [Step 1: 검색 메인 화면] */
            <div className="flex flex-col items-center justify-center py-24 animate-in fade-in zoom-in duration-500">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 text-blue-600 text-xs font-bold mb-6">
                <ShieldCheck size={14} /> AI-POWERED LEGAL VERIFICATION
              </div>
              <h1 className="text-6xl font-black mb-6 tracking-tight text-slate-900 text-center leading-[1.1]">
                계약서 조항을 <br />
                <span className="text-blue-600 underline decoration-blue-100 underline-offset-8">
                  실시간으로 검증
                </span>
                하세요
              </h1>
              <p className="text-slate-500 mb-12 text-xl font-medium text-center max-w-2xl leading-relaxed">
                의심되는 조항을 복사하여 붙여넣으세요. <br />
                독소 조항 유무를 즉시 판별합니다.
              </p>

              {/* 메인 검색창 컨테이너 */}
              <div className="w-full max-w-4xl relative group">
                <div className="flex flex-col bg-white rounded-[32px] p-4 shadow-2xl shadow-blue-900/10 ring-1 ring-slate-200 focus-within:ring-4 focus-within:ring-blue-100 transition-all">
                  <textarea
                    rows="4"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="분석할 조항 내용을 입력하세요 (예: 손해배상 청구, 비밀유지 의무 등...)"
                    className="w-full p-4 bg-transparent text-lg outline-none placeholder:text-slate-300 font-medium resize-none"
                  />
                  <div className="flex items-center justify-between border-t border-slate-50 pt-4 px-2">
                    <div className="flex items-center gap-2">
                      <div className="relative">
                        <input
                          type="file"
                          accept=".pdf"
                          className="absolute inset-0 opacity-0 cursor-pointer z-10"
                          onChange={(e) =>
                            e.target.files?.[0] && uploadPDF(e.target.files[0])
                          }
                        />
                        <button className="flex items-center gap-2 px-4 py-2 text-slate-500 hover:bg-slate-100 rounded-xl transition-colors font-bold text-sm">
                          <Paperclip size={18} /> PDF 파일 첨부
                        </button>
                      </div>
                    </div>
                    <button
                      onClick={handleSearch}
                      disabled={isLoading}
                      className="flex items-center gap-2 h-12 px-8 bg-blue-600 text-white rounded-2xl font-bold shadow-lg hover:bg-blue-700 transition-all active:scale-95 disabled:opacity-50"
                    >
                      {isLoading ? "분석 중..." : "분석 시작"}{" "}
                      <ArrowRight size={18} />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            /* [Step 2: 대형 결과 리포트 화면] */
            <div className="animate-in slide-in-from-bottom-10 duration-700">
              <button
                onClick={() => {
                  setReport(null);
                  setInputValue("");
                }}
                className="flex items-center gap-2 text-slate-500 hover:text-blue-600 font-bold mb-8 transition-colors group"
              >
                <ChevronLeft
                  size={20}
                  className="group-hover:-translate-x-1 transition-transform"
                />
                다른 조항 분석하기
              </button>

              <div className="bg-white rounded-[48px] shadow-2xl shadow-blue-900/10 border border-white overflow-hidden">
                {/* 리포트 상단 요약 바 */}
                <div className="bg-slate-900 px-12 py-16 text-white flex justify-between items-center">
                  <div>
                    <h2 className="text-4xl font-black mb-4 tracking-tight">
                      계약 조항 분석 리포트
                    </h2>
                    <div className="flex gap-3">
                      <span className="px-3 py-1 bg-red-500/20 text-red-400 rounded-md text-[10px] font-black uppercase tracking-widest border border-red-500/30">
                        Priority High
                      </span>
                      <span className="text-slate-400 text-xs font-bold uppercase flex items-center gap-1">
                        <Info size={14} /> Analyzed at {report.analyzed_at}
                      </span>
                    </div>
                  </div>
                  <div className="flex gap-8 items-center">
                    <div className="text-right">
                      <p className="text-slate-400 text-[10px] font-black uppercase mb-1 tracking-tighter">
                        Total Clauses
                      </p>
                      <p className="text-3xl font-black">
                        {report.risks?.length || 0}
                      </p>
                    </div>
                    <div className="h-12 w-[1px] bg-white/10"></div>
                    <div className="text-right">
                      <p className="text-slate-400 text-[10px] font-black uppercase mb-1 tracking-tighter">
                        Danger Score
                      </p>
                      <p
                        className={`text-6xl font-black ${report.total_risk_score >= 70 ? "text-red-500" : "text-orange-500"}`}
                      >
                        {report.total_risk_score}
                      </p>
                    </div>
                  </div>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                  {/* SAFE (추가됨) */}
                  <div className="bg-green-50/50 border border-green-100 p-6 rounded-[24px] flex flex-col items-center justify-center text-center">
                    <span className="text-green-600 font-black text-sm mb-1 uppercase tracking-wider">
                      Safe
                    </span>
                    <p className="text-3xl font-black text-green-700">80-100</p>
                    <p className="text-[11px] text-green-600/70 mt-2 font-medium">
                      법적으로 안전하며
                      <br />
                      표준적인 조항입니다.
                    </p>
                  </div>

                  {/* WARNING */}
                  <div className="bg-orange-50/50 border border-orange-100 p-6 rounded-[24px] flex flex-col items-center justify-center text-center">
                    <span className="text-orange-600 font-black text-sm mb-1 uppercase tracking-wider">
                      Warning
                    </span>
                    <p className="text-3xl font-black text-orange-700">40-69</p>
                    <p className="text-[11px] text-orange-600/70 mt-2 font-medium">
                      주의가 필요한 조항입니다.
                      <br />
                      문구 수정을 권고합니다.
                    </p>
                  </div>

                  {/* DANGER */}
                  <div className="bg-red-50/50 border border-red-100 p-6 rounded-[24px] flex flex-col items-center justify-center text-center">
                    <span className="text-red-600 font-black text-sm mb-1 uppercase tracking-wider">
                      Danger
                    </span>
                    <p className="text-3xl font-black text-red-700">0-39</p>
                    <p className="text-[11px] text-red-600/70 mt-2 font-medium">
                      독소 조항일 가능성이 높습니다.
                      <br />
                      반드시 전문가와 상의하세요.
                    </p>
                  </div>
                </div>
                {/* 리포트 본문 콘텐츠 */}
                <div className="max-w-4xl mx-auto px-4 py-10">
                  {/* 우측: 핵심 분석 결과 리스트 */}
                  <div className="col-span-8 space-y-8">
                    <h3 className="text-2xl font-black text-slate-900 flex items-center justify-center gap-3 w-full">
                      <AlertTriangle className="text-red-500" size={28} />
                      발견된 위험 조항 상세
                    </h3>

                    {report.risks && report.risks.length > 0 ? (
                      report.risks.map((risk, idx) => (
                        <div
                          key={idx}
                          className="group p-10 rounded-[32px] border border-slate-100 bg-white shadow-sm hover:shadow-xl transition-all duration-300 relative overflow-hidden"
                        >
                          <div
                            className={`absolute top-0 left-0 w-2 h-full ${risk.level === "DANGER" ? "bg-red-500" : "bg-orange-500"}`}
                          ></div>
                          <div className="flex items-center justify-between mb-6">
                            <div className="flex items-center gap-2">
                              <span
                                className={`px-3 py-1 rounded-md text-[10px] font-black ${
                                  risk.level === "DANGER"
                                    ? "bg-red-100 text-red-600"
                                    : "bg-orange-100 text-orange-600"
                                }`}
                              >
                                {risk.level}
                              </span>
                              <span className="text-xs text-slate-400 font-bold uppercase tracking-tighter">
                                Confidence {risk.score}%
                              </span>
                            </div>
                          </div>
                          {/* 1. 분석된 조항 본문 */}
                          <p className="text-2xl text-slate-800 leading-relaxed font-medium mb-4">
                            "{risk.clause}"
                          </p>

                          {/* 2. [추가] AI 상세 설명 (description) */}
                          <div className="bg-slate-50 border-l-4 border-slate-300 p-4 mb-6">
                            <p className="text-sm text-slate-600 leading-relaxed">
                              <span className="font-bold text-slate-800">
                                💡 AI 분석:{" "}
                              </span>
                              {risk.description}
                            </p>
                          </div>

                          {/* 3. [추가] 근거 법령 및 판례 섹션 */}
                          <div className="space-y-4 mb-6">
                            {/* 법령 정보 */}
                            {risk.legal_basis &&
                              risk.legal_basis.length > 0 && (
                                <div>
                                  <h4 className="text-xs font-black text-blue-600 uppercase mb-2">
                                    근거 법령
                                  </h4>
                                  {risk.legal_basis.map((law, lIdx) => (
                                    <div
                                      key={lIdx}
                                      className="text-sm bg-blue-50/50 p-3 rounded-xl border border-blue-100 mb-2"
                                    >
                                      <span className="font-bold text-blue-800">
                                        [{law.title}]
                                      </span>{" "}
                                      {law.summary}
                                    </div>
                                  ))}
                                </div>
                              )}

                            {/* 판례 정보 */}
                            {risk.precedents && risk.precedents.length > 0 && (
                              <div>
                                <h4 className="text-xs font-black text-indigo-600 uppercase mb-2">
                                  관련 판례
                                </h4>
                                {risk.precedents.map((pre, pIdx) => (
                                  <div
                                    key={pIdx}
                                    className="text-sm bg-indigo-50/50 p-3 rounded-xl border border-indigo-100"
                                  >
                                    <span className="font-bold text-indigo-800">
                                      [{pre.title}]
                                    </span>
                                    <p className="text-slate-600 whitespace-pre-wrap break-all leading-relaxed">
                                      {pre.content}
                                    </p>
                                  </div>
                                ))}
                              </div>
                            )}
                          </div>
                          <div className="flex gap-2">
                            <div className="px-4 py-2 bg-slate-50 rounded-xl text-[11px] font-bold text-slate-500">
                              #부당계약
                            </div>
                            <div className="px-4 py-2 bg-slate-50 rounded-xl text-[11px] font-bold text-slate-500">
                              #검토필요
                            </div>
                          </div>
                        </div>
                      ))
                    ) : (
                      <div className="py-24 text-center bg-green-50 rounded-[48px] border border-green-100 border-dashed">
                        <CheckCircle2
                          size={80}
                          className="mx-auto text-green-500 mb-6"
                        />
                        <p className="text-2xl font-black text-green-800">
                          모든 조항이 안전합니다
                        </p>
                        <p className="text-green-600/70 font-medium">
                          입력하신 내용에서 위험 요소가 발견되지 않았습니다.
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default LegalAIAssistant;
