import { useState } from "react";
import { FiSearch, FiPaperclip, FiX, FiFileText } from "react-icons/fi";
import { useNavigate } from "react-router-dom";

const SearchBar = () => {
  const navigate = useNavigate();
  const [query, setQuery] = useState("");
  const [pdfFile, setPdfFile] = useState(null); // ← PDF 상태

  const handleSearch = () => {
    if (!query.trim() && !pdfFile) return;
    navigate("/analysis", {
      state: { query, pdfFile }, // ← 둘 다 전달
    });
  };

  return (
    <div className="relative mx-auto mb-8 max-w-2xl">
      <div className="flex flex-col rounded-2xl bg-white shadow-xl ring-1 ring-slate-200 focus-within:ring-2 focus-within:ring-blue-500 transition-all">
        {/* PDF 첨부됐을 때 미리보기 */}
        {pdfFile && (
          <div className="flex items-center gap-2 px-6 pt-4">
            <div className="flex items-center gap-2 bg-blue-50 text-blue-700 rounded-lg px-3 py-1.5 text-xs font-semibold">
              <FiFileText size={14} />
              {pdfFile.name}
              <button
                onClick={() => setPdfFile(null)}
                className="ml-1 hover:text-red-500 transition-colors"
              >
                <FiX size={12} />
              </button>
            </div>
          </div>
        )}

        {/* 입력창 */}
        <div className="flex items-center gap-4 px-6 py-4">
          {/* Paperclip — PDF 첨부 */}
          <div className="relative">
            <input
              type="file"
              accept=".pdf"
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
              onChange={(e) => {
                if (e.target.files?.[0]) setPdfFile(e.target.files[0]);
                e.target.value = "";
              }}
            />
            <button className="text-slate-400 hover:text-blue-600 transition-colors">
              <FiPaperclip size={20} />
            </button>
          </div>

          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            placeholder="무엇이든 물어보세요..."
            className="flex-1 bg-transparent text-lg outline-none placeholder:text-slate-400"
          />

          <button
            onClick={handleSearch}
            className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 text-white shadow-md hover:bg-blue-700 transition-all"
          >
            <FiSearch size={20} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default SearchBar;
