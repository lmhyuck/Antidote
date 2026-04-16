import { FiBell, FiHelpCircle, FiSettings } from "react-icons/fi";
import { Download } from "lucide-react";

const Navbar = ({ variant = "home" }) => {
  return (
    <>
      <style>
        {`
       .glass-nav {
         background: rgba(255, 255, 255, 0.7);
         backdrop-filter: blur(20px);
         -webkit-backdrop-filter: blur(20px);
         border-bottom: 1px solid rgba(226, 232, 240, 0.5);
      }
    `}
      </style>

      <nav className="sticky top-0 z-50 flex w-full items-center justify-between bg-white/70 px-8 py-4 backdrop-blur-xl shadow-sm">
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center">
              <div className="h-6 w-6 rounded-full flex items-center justify-center">
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

          {variant === "home" && (
            <button className="text-slate-500 hover:text-slate-900">
              <FiHelpCircle size={20} />
            </button>
          )}

          {variant === "analysis" && (
            <>
              <button className="text-slate-400 hover:text-[#1e40af]">
                <FiSettings size={20} />
              </button>
              <button className="rounded-md bg-[#1e40af] px-4 py-2 text-xs font-bold text-white flex items-center gap-2 hover:bg-[#002244]">
                <Download size={14} /> Export Report
              </button>
            </>
          )}
        </div>
      </nav>
    </>
  );
};

export default Navbar;
