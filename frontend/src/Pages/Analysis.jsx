import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import axios from "axios";
import { History, Sliders, Paperclip, Mic, Send } from "lucide-react";
import Navbar from "../components/layout/Navbar";
import AnalysisResultCard from "../components/analysis/AnalysisResultCard";
import CitationButtons from "../components/analysis/CitationButtons";
import LiveAnalysis from "../components/analysis/LiveAnalysis";
import SuggestedTopics from "../components/analysis/SuggestedTopics";

const Analysis = () => {
  const location = useLocation();
  const [inputValue, setInputValue] = useState("");
  const [report, setReport] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: "bot",
      text: "안녕하세요. Antidote 법률 비서입니다. 검토 중인 계약서 조항이나 궁금한 법적 근거에 대해 말씀해 주세요.",
      sources: null,
    },
  ]);

  // PDF 업로드
  const uploadPDF = async (file) => {
    setIsLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await axios.post(
        "http://localhost:8000/api/legal/contract",
        formData,
      );
      setReport(response.data);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now(),
          type: "bot",
          text: "계약서 분석 리포트가 생성되었습니다.",
          sources: null,
        },
      ]);
    } catch (error) {
      console.error("업로드 실패:", error);
      alert("파일 분석 중 오류가 발생했습니다.");
    } finally {
      setIsLoading(false);
    }
  };

  // 텍스트 전송
  const handleSend = async (externalQuery) => {
    const userQuery = externalQuery || inputValue;
    if (!userQuery.trim() || isLoading) return;

    setInputValue("");
    setMessages((prev) => [
      ...prev,
      { id: Date.now(), type: "user", text: userQuery },
    ]);
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userQuery }),
      });
      const data = await response.json();
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          type: "bot",
          text: data.answer || "분석된 법적 근거와 참조 판례입니다.",
          sources: {
            laws: data.related_laws || [],
            precedents: data.related_precedents || [],
          },
        },
      ]);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // Home에서 넘어온 query, pdfFile 처리
  useEffect(() => {
    const { query, pdfFile } = location.state || {};
    if (pdfFile) uploadPDF(pdfFile);
    else if (query) handleSend(query);
    // location.state 초기화 — 뒤로갔다 오면 재실행 방지
    window.history.replaceState({}, document.title);
  }, []);

  return (
    <div className="min-h-screen bg-[#F8FAFC] font-sans">
      <Navbar variant="analysis" />

      {/* 검색바 */}
      <div className="px-8 py-4 max-w-3xl mx-auto w-full">
        <div className="flex items-center gap-4 bg-white rounded-2xl p-4 shadow-xl ring-1 ring-slate-200 focus-within:ring-2 focus-within:ring-blue-600 transition-all">
          <div className="relative">
            <input
              type="file"
              accept=".pdf"
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
              onChange={(e) => {
                if (e.target.files?.[0]) uploadPDF(e.target.files[0]);
                e.target.value = "";
              }}
            />
            <button className="text-slate-400 hover:text-blue-600 transition-colors">
              <Paperclip size={20} />
            </button>
          </div>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="특정 조항, 리스크 지표, 또는 법적 판례에 대해 질문하세요…"
            className="flex-1 bg-transparent text-sm outline-none placeholder:text-slate-400 font-medium"
          />
          <div className="flex items-center gap-2">
            <button className="text-slate-400 hover:text-blue-600 transition-colors">
              <Mic size={20} />
            </button>
            <button
              onClick={() => handleSend()}
              disabled={isLoading}
              className="h-10 w-10 bg-[#1a73e8] text-white rounded-xl flex items-center justify-center shadow-lg hover:bg-[#002244] active:scale-95 transition-all disabled:opacity-50"
            >
              <Send size={20} />
            </button>
          </div>
        </div>

        {isLoading && (
          <p className="text-xs text-blue-600 text-center mt-2 animate-pulse">
            분석 중...
          </p>
        )}
      </div>

      <main className="flex-1 min-h-screen flex flex-col">
        <div className="flex-1 p-8 max-w-5xl mx-auto w-full">
          {/* 채팅 헤더 */}
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-2xl font-bold text-left">
                Legal Intellect AI
              </h2>
              <div className="flex items-center gap-2 text-xs text-blue-600 font-medium">
                <span className="h-1.5 w-1.5 rounded-full bg-blue-600 animate-pulse"></span>
                Analyzing V-24-901 Enterprise Agreement
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

          {/* 메시지 목록 */}
          <div className="space-y-6 mb-12">
            {messages.map((msg, index) => (
              <div
                key={msg.id}
                className={`flex ${msg.type === "user" ? "justify-end" : "gap-4"}`}
              >
                {msg.type === "bot" && (
                  <div className="flex-1 space-y-6">
                    <p className="text-sm font-semibold text-slate-900 leading-relaxed text-left">
                      {msg.text}
                    </p>

                    {report && index === messages.length - 1 && (
                      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        <div className="lg:col-span-2">
                          <AnalysisResultCard report={report} />
                        </div>
                        <div className="lg:col-span-1 space-y-4">
                          <LiveAnalysis report={report} />
                          <SuggestedTopics report={report} />
                        </div>
                      </div>
                    )}

                    {msg.sources && <CitationButtons sources={msg.sources} />}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Analysis;
