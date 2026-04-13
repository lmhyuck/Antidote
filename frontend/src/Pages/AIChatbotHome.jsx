import React from "react";
import { useNavigate } from "react-router-dom";
import {
  FiMessageSquare,
  FiBookmark,
  FiRotateCcw,
  FiBarChart2,
  FiSettings,
  FiUser,
  FiSearch,
  FiBell,
  FiHelpCircle,
  FiEdit,
  FiFileText,
  FiImage,
  FiCode,
} from "react-icons/fi";
import profileImg from "../assets/profile.png";
import { HiShieldCheck } from "react-icons/hi";

const AIChatbotHome = () => {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen bg-slate-50 font-manrope text-slate-900">
      <nav className="sticky top-0 z-50 flex w-full items-center justify-between bg-white/70 px-8 py-4 backdrop-blur-xl shadow-sm">
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center">
              <div className="h-6 w-6 rounded-full bg-[#1a73e8] flex items-center justify-center">
                <div className="h-2 w-2 rounded-full bg-white"></div>
              </div>
            </div>
            <span className="text-xl font-bold tracking-tighter text-slate-900">
              Dot AI
            </span>
          </div>
          <div className="flex gap-6 text-sm font-medium text-slate-500">
            <a href="#" className="hover:text-blue-600 transition-colors">
              Discover
            </a>
            <a href="#" className="hover:text-blue-600 transition-colors">
              Plugins
            </a>
            <a href="#" className="hover:text-blue-600 transition-colors">
              Tools
            </a>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <button className="text-slate-500 hover:text-slate-900">
            <FiBell size={20} />
          </button>

          <button className="text-slate-500 hover:text-slate-900">
            <FiHelpCircle size={20} />
          </button>

          <img
            src={profileImg}
            alt="Profile"
            className="h-8 w-8 rounded-full object-cover border border-slate-200"
          />
        </div>
      </nav>

      <div className="flex">
        {/* Side Navigation Bar */}
        <aside className="fixed left-0 top-0 h-screen w-64 flex-col border-r border-slate-100 bg-slate-50 p-6 pt-24 hidden lg:flex">
          <button className="mb-8 flex items-center justify-center gap-2 rounded-full bg-blue-600 py-3 text-sm font-semibold text-white shadow-lg transition-all hover:bg-blue-700 active:scale-95">
            <i className="material-icons text-sm">add</i>
            New Chat
          </button>

          <div className="space-y-1">
            <p className="px-4 text-[10px] font-bold uppercase tracking-wider text-slate-400">
              Main
            </p>
            {[
              { icon: <FiMessageSquare />, label: "Recent Chat", active: true },
              { icon: <FiBookmark />, label: "Saved Prompts" },
              { icon: <FiRotateCcw />, label: "History" },
              { icon: <FiBarChart2 />, label: "Analytics" },
            ].map((item) => (
              <button
                key={item.label}
                className={`flex items-center gap-3 px-4 py-2.5 rounded-full text-sm font-medium transition-colors ${
                  item.active
                    ? "bg-white text-blue-600 shadow-sm"
                    : "text-slate-500 hover:bg-slate-200"
                }`}
              >
                <span className="text-lg">{item.icon}</span>
                {item.label}
              </button>
            ))}
          </div>

          <div className="mt-auto space-y-1">
            <button className="flex items-center gap-3 px-4 py-2.5 rounded-full text-sm font-medium text-slate-500 hover:bg-slate-200 transition-colors">
              <FiSettings size={20} />
              Settings
            </button>

            <button className="flex items-center gap-3 px-4 py-2.5 rounded-full text-sm font-medium text-slate-500 hover:bg-slate-200 transition-colors">
              <FiUser size={20} />
              Account
            </button>
          </div>
        </aside>

        {/* Main Content Area */}
        <main className="flex-1 lg:ml-64 p-8">
          <div className="mx-auto max-w-5xl pt-12 text-center">
            <h1 className="mb-4 text-6xl font-black tracking-tight text-slate-900">
              Hello, how can I help <br /> you today?
            </h1>
            <p className="mb-12 text-lg text-slate-500">
              Experience the next evolution of assistance with The Dot.
            </p>

            {/* Search Section */}
            <div className="relative mx-auto mb-8 max-w-2xl">
              <div className="flex items-center gap-4 rounded-full bg-white px-6 py-4 shadow-xl shadow-blue-900/5 ring-1 ring-slate-200 focus-within:ring-2 focus-within:ring-blue-500 transition-all">
                <input
                  type="text"
                  placeholder="무엇이든 물어보세요..."
                  className="flex-1 bg-transparent text-lg outline-none placeholder:text-slate-400"
                />

                <button
                  onClick={() => navigate("/chat")} // 넘어가라
                  className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 text-white shadow-md hover:bg-blue-700 transition-all"
                  aria-label="검색"
                >
                  <FiSearch size={20} />
                </button>
              </div>

              {/* Quick Actions */}
              <div className="mt-6 flex flex-wrap justify-center gap-3">
                {[
                  { icon: <FiEdit />, label: "Write a poem" },
                  { icon: <FiFileText />, label: "Summarize text" },
                  { icon: <FiImage />, label: "Generate Image" },
                  { icon: <FiCode />, label: "Code help" },
                ].map((action) => (
                  <button
                    key={action.label}
                    className="flex items-center gap-2 rounded-lg bg-slate-100 px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-200 transition-colors"
                  >
                    <span className="text-blue-600 text-sm">{action.icon}</span>
                    {action.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Feature Cards Grid */}
            <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
              {/* Multimodal Reasoning Card */}
              <div className="col-span-1 md:col-span-2 rounded-3xl bg-white p-8 shadow-lg ring-1 ring-slate-100 flex items-center justify-between overflow-hidden group">
                <div className="max-w-xs">
                  <span className="inline-block rounded-full bg-blue-100 px-3 py-1 text-[10px] font-bold uppercase tracking-widest text-blue-700">
                    New Model
                  </span>
                  <h3 className="mt-4 text-2xl font-bold text-slate-900">
                    Multimodal Reasoning
                  </h3>
                  <p className="mt-2 text-sm text-slate-500 leading-relaxed">
                    The Dot now understands images, audio, and complex visual
                    datasets with human-like precision.
                  </p>
                </div>
                <div className="relative h-32 w-32 opacity-20 group-hover:opacity-40 transition-opacity flex items-center justify-center">
                  <FiImage size={80} className="text-blue-600" />
                </div>
              </div>

              {/* Private by Design Card */}
              <div className="rounded-3xl bg-blue-600 p-8 text-white shadow-lg shadow-blue-600/20">
                <div className="h-10 w-10 rounded-xl bg-white/20 flex items-center justify-center">
                  <HiShieldCheck size={24} />
                </div>
                <h3 className="mt-6 text-2xl font-bold">Private by Design</h3>
                <p className="mt-2 text-sm text-blue-50/80 leading-relaxed">
                  Your data is never used to train our base models. Complete
                  anonymity guaranteed.
                </p>
              </div>

              {/* Live Analytics Card */}
              <div className="rounded-3xl bg-white p-8 shadow-lg ring-1 ring-slate-100">
                <div className="flex items-center justify-between">
                  <h4 className="font-bold text-slate-900">Live Analytics</h4>
                  <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
                </div>
                <div className="mt-6 flex h-32 items-end justify-between gap-2">
                  {[40, 60, 100, 70, 30].map((h, i) => (
                    <div
                      key={i}
                      className={`w-full rounded-t-lg transition-all duration-1000 ${i === 2 ? "bg-blue-600" : "bg-blue-200"}`}
                      style={{ height: `${h}%` }}
                    ></div>
                  ))}
                </div>
                <p className="mt-4 text-[10px] text-slate-400">
                  Processing 2.4k requests per second globally.
                </p>
              </div>

              {/* Developer Tools Card */}
              <div className="col-span-1 md:col-span-2 rounded-3xl bg-white p-8 shadow-lg ring-1 ring-slate-100 flex items-center gap-8 group">
                <div className="flex-1">
                  <h3 className="text-2xl font-bold text-slate-900">
                    Developer Tools
                  </h3>
                  <p className="mt-2 text-sm text-slate-500 leading-relaxed">
                    Connect Dot AI directly to your VS Code environment or
                    terminal via our official plugins.
                  </p>
                  <button className="mt-4 flex items-center gap-1 text-sm font-bold text-blue-600 hover:gap-2 transition-all">
                    Get Started{" "}
                    <i className="material-icons text-sm">chevron_right</i>
                  </button>
                </div>
                <div className="h-32 w-48 overflow-hidden rounded-2xl bg-slate-900 shadow-inner">
                  <div className="p-3 text-[8px] font-mono text-emerald-400/80">
                    <p className="text-slate-500">// Initialize Dot AI</p>
                    <p>const Dot = new Dot(&apos;api_key&apos;);</p>
                    <p className="mt-2">await Dot.analyze(image);</p>
                    <p className="text-blue-400">
                      console.log(&quot;Success&quot;);
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default AIChatbotHome;
