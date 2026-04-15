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
} from "lucide-react"; // lucide-react 아이콘들

const LegalAIAssistant = () => {
  // 1. 분석 결과를 저장할 상태(State)
  const [report, setReport] = useState(null);

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
        "http://localhost:8000/api/legal/contract", // 또는 설정하신 경로
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

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userQuery = inputValue;
    setInputValue("");
    const newUserMsg = { id: Date.now(), type: "user", text: userQuery };
    setMessages((prev) => [...prev, newUserMsg]);
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userQuery }),
      });
      const data = await response.json();

      const botMsg = {
        id: Date.now() + 1,
        type: "bot",
        text: data.answer || "분석된 법적 근거와 참조 판례입니다.",
        sources: {
          laws: data.related_laws || [],
          precedents: data.related_precedents || [],
        },
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F8FAFC] font-sans text-[#0F172A] flex">
      {/* 1. 사이드바 (기존 유지) */}
      <aside className="fixed left-0 top-0 h-screen w-64 flex flex-col border-r border-slate-200/50 bg-white p-6 z-40 text-left">
        <div className="mb-10">
          <p className="text-[10px] font-bold uppercase tracking-widest text-slate-400 mb-1">
            Case Dossier
          </p>
          <p className="text-xs font-medium text-slate-500">
            V-24-901 Enterprise Agreement
          </p>
        </div>
        <nav className="flex-1 space-y-1">
          {navItems.map((item) => (
            <button
              key={item.label}
              className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-all ${item.active ? "bg-slate-100 text-[#1E40AF] shadow-sm" : "text-slate-500 hover:bg-slate-50"}`}
            >
              {item.icon} {item.label}
            </button>
          ))}
        </nav>

        <div className="mt-auto pt-6 border-t border-slate-100 space-y-2">
          <div className="relative w-full">
            {/* 1. 실제 클릭을 가로챌 투명한 파일 인풋 (버튼 위에 덧씌워짐) */}
            <input
              type="file"
              accept=".pdf"
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
              onChange={(e) => {
                if (e.target.files?.[0]) {
                  uploadPDF(e.target.files[0]); // 기존에 만드신 함수 호출
                }
                e.target.value = ""; // 같은 파일 재업로드 가능하도록 리셋
              }}
            />
            <button className="w-full flex items-center justify-center gap-2 rounded-lg bg-[#1E40AF] py-3 text-sm font-semibold text-white shadow-lg shadow-blue-600/20 hover:bg-blue-800 transition-all active:scale-95 mb-4">
              Upload New Contract
            </button>
          </div>
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

      {/* 2. 메인 영역 */}
      <main className="flex-1 ml-64 min-h-screen flex flex-col relative">
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

        {/* 3. 분석 결과 리포트 화면 (우측 섹션 예시) */}
        {report && (
          <div className="w-96 border-l bg-white p-6 overflow-y-auto animate-fade-in">
            <h2 className="text-xl font-bold text-gray-800 mb-4">
              {report.title}
            </h2>

            {/* 위험 점수 표시 */}
            <div className="mb-6 p-4 rounded-xl bg-red-50 border border-red-100">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-red-800">
                  위험도 점수
                </span>
                <span className="text-2xl font-bold text-red-600">
                  {report.risk_score}점
                </span>
              </div>
              <div className="w-full bg-red-200 h-2 rounded-full">
                <div
                  className="bg-red-600 h-2 rounded-full transition-all duration-1000"
                  style={{ width: `${report.risk_score}%` }}
                ></div>
              </div>
            </div>

            {/* 감지된 리스크 리스트 */}
            <div className="mb-6">
              <h3 className="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-3">
                <AlertTriangle size={16} className="text-red-500" />
                감지된 주요 리스크
              </h3>
              <ul className="space-y-2">
                {report.detected_risks.map((risk, index) => (
                  <li
                    key={index}
                    className="text-sm p-3 bg-gray-50 rounded-lg border-l-4 border-red-400 text-gray-600"
                  >
                    {risk}
                  </li>
                ))}
              </ul>
            </div>

            {/* 개선 제안 */}
            <div>
              <h3 className="flex items-center gap-2 text-sm font-semibold text-gray-700 mb-3">
                <CheckCircle size={16} className="text-green-500" />
                수정 및 개선 제안
              </h3>
              <ul className="space-y-2">
                {report.improvement_suggestions.map((sugg, index) => (
                  <li
                    key={index}
                    className="text-sm p-3 bg-green-50 rounded-lg text-green-700"
                  >
                    {sugg}
                  </li>
                ))}
              </ul>
            </div>

            <div className="mt-8 text-xs text-gray-400 text-right">
              분석 일시: {report.analyzed_at}
            </div>
          </div>
        )}

        {/* 4. 하단 입력바 (기존 위치 고정) */}
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
                onKeyDown={(e) => e.key === "Enter" && handleSend()}
                placeholder="특정 조항, 리스크 지표, 또는 법적 판례에 대해 질문하세요…"
                className="flex-1 bg-transparent text-sm outline-none placeholder:text-slate-400 font-medium"
              />
              <button
                onClick={handleSend}
                className="h-10 w-10 bg-[#1a73e8] text-white rounded-xl flex items-center justify-center shadow-lg hover:bg-[#002244] transition-all"
              >
                <Send size={20} />
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default LegalAIAssistant;
