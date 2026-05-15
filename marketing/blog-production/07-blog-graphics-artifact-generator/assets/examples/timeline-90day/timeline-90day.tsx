import {
  Search,
  Settings,
  Rocket,
  Users,
  Eye,
  Presentation,
  Handshake,
  UserCheck,
  Shield,
  Megaphone,
  Mail,
  Target,
  GraduationCap,
  FileText,
  Trophy,
  Star,
  Calendar,
  Zap,
  Database,
  BarChart3,
  RotateCw,
  TrendingUp,
  Bot,
  RefreshCw,
  Clipboard,
  AlertTriangle,
  Award,
  MessageCircle,
  LineChart,
  AlertCircle,
} from "lucide-react"

export default function RevOpsTimeline() {
  return (
    <div
      className="relative bg-white w-full"
      style={{
        maxWidth: "800px",
        fontFamily: "Lato, sans-serif",
        margin: "0 auto", // Added auto margin for centering in blog
      }}
    >
      {/* Decorative Shape */}
      <div
        className="absolute top-0 right-0 hidden md:block"
        style={{
          width: "60px",
          height: "60px",
          background: "#E4E6F9",
          clipPath: "polygon(100% 0, 0 0, 100% 100%)",
        }}
      />

      {/* Header Section */}
      <div className="relative px-6 md:px-8 pt-8 pb-6">
        <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-4 lg:gap-6">
          {/* Left: Title */}
          <div className="flex-1">
            <h1
              className="font-bold leading-tight text-balance"
              style={{
                fontFamily: "Montserrat, sans-serif",
                fontSize: "clamp(20px, 4vw, 28px)",
                color: "#000FC4",
                marginBottom: "6px",
              }}
            >
              90-Day Execution: People, Momentum, Change
            </h1>
            <p
              className="text-sm md:text-base leading-relaxed"
              style={{
                color: "#434343",
                marginBottom: "4px",
              }}
            >
              The tactical 'how' for RevOps transformation success
            </p>
            <p className="italic text-xs md:text-sm" style={{ color: "#999999" }}>
              70% of transformations fail without proper change management - Forrester
            </p>
          </div>

          {/* Right: Phase Progression */}
          <div className="flex items-center justify-center lg:justify-end gap-2 lg:gap-3 lg:pt-2">
            {/* Phase 1 */}
            <div className="flex flex-col items-center">
              <div
                className="flex items-center justify-center rounded-full"
                style={{
                  width: "44px",
                  height: "44px",
                  background: "#C8CCF2",
                }}
              >
                <Search size={18} style={{ color: "#000FC4" }} />
              </div>
              <div className="mt-1.5 text-center">
                <p className="font-bold text-[10px] leading-tight" style={{ fontFamily: "Montserrat, sans-serif" }}>
                  Discover &<br className="hidden sm:inline" /> Align
                </p>
                <p className="text-[9px] mt-0.5" style={{ color: "#434343" }}>
                  Days 1-30
                </p>
              </div>
            </div>

            {/* Connector */}
            <div style={{ width: "20px", height: "2px", background: "#E4E6F9", marginBottom: "32px" }} />

            {/* Phase 2 */}
            <div className="flex flex-col items-center">
              <div
                className="flex items-center justify-center rounded-full"
                style={{
                  width: "44px",
                  height: "44px",
                  background: "#96F2F3",
                }}
              >
                <Settings size={18} style={{ color: "#000FC4" }} />
              </div>
              <div className="mt-1.5 text-center">
                <p className="font-bold text-[10px] leading-tight" style={{ fontFamily: "Montserrat, sans-serif" }}>
                  Build &<br className="hidden sm:inline" /> Enable
                </p>
                <p className="text-[9px] mt-0.5" style={{ color: "#434343" }}>
                  Days 31-60
                </p>
              </div>
            </div>

            {/* Connector */}
            <div style={{ width: "20px", height: "2px", background: "#E4E6F9", marginBottom: "32px" }} />

            {/* Phase 3 */}
            <div className="flex flex-col items-center">
              <div
                className="flex items-center justify-center rounded-full"
                style={{
                  width: "44px",
                  height: "44px",
                  background: "#2DE4E6",
                }}
              >
                <Rocket size={18} style={{ color: "#000000" }} />
              </div>
              <div className="mt-1.5 text-center">
                <p className="font-bold text-[10px] leading-tight" style={{ fontFamily: "Montserrat, sans-serif" }}>
                  Launch &<br className="hidden sm:inline" /> Scale
                </p>
                <p className="text-[9px] mt-0.5" style={{ color: "#434343" }}>
                  Days 61-90
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="relative px-6 md:px-8 pb-4">
        <div
          className="relative sm:ml-[8px]"
          style={{
            height: "32px",
            background: "linear-gradient(90deg, #C8CCF2 0%, #96F2F3 50%, #2DE4E6 100%)",
            borderRadius: "4px",
          }}
        >
          {/* Vertical dividers - BACKGROUND LAYER */}
          <div
            className="absolute top-0 bottom-0"
            style={{ left: "33.33%", width: "2px", borderLeft: "2px dotted rgba(255,255,255,0.6)", zIndex: 0 }}
          />
          <div
            className="absolute top-0 bottom-0"
            style={{ left: "66.66%", width: "2px", borderLeft: "2px dotted rgba(255,255,255,0.6)", zIndex: 0 }}
          />

          {/* Day Markers - FOREGROUND LAYER */}
          <div className="absolute inset-0 flex items-center justify-between px-2" style={{ zIndex: 10 }}>
            <span className="font-bold text-[10px] md:text-xs" style={{ color: "#000000" }}>
              Day 1
            </span>
            <span className="font-bold text-[10px] md:text-xs" style={{ color: "#000000" }}>
              Day 30
            </span>
            <span className="font-bold text-[10px] md:text-xs" style={{ color: "#000000" }}>
              Day 60
            </span>
            <span className="font-bold text-[10px] md:text-xs" style={{ color: "#000000" }}>
              Day 90
            </span>
          </div>

          {/* Phase Labels - FOREGROUND LAYER */}
          <div className="absolute inset-0 hidden sm:flex" style={{ zIndex: 10 }}>
            <div className="flex-1 flex items-center justify-center">
              <span className="font-bold text-[9px]" style={{ color: "rgba(0,0,0,0.4)" }}>
                PHASE 1
              </span>
            </div>
            <div className="flex-1 flex items-center justify-center">
              <span className="font-bold text-[9px]" style={{ color: "rgba(0,0,0,0.4)" }}>
                PHASE 2
              </span>
            </div>
            <div className="flex-1 flex items-center justify-center">
              <span className="font-bold text-[9px]" style={{ color: "rgba(0,0,0,0.4)" }}>
                PHASE 3
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row px-6 md:px-8 pb-4">
        {/* Track Header */}
        <div
          className="flex sm:flex-col items-center sm:justify-center gap-2 sm:gap-1 py-3 sm:py-2 sm:min-w-[48px] sm:w-[48px] sm:-ml-[48px]"
          style={{ background: "#000FC4" }}
        >
          <Users size={18} className="sm:mb-2" style={{ color: "#FFFFFF" }} />
          <p
            className="font-bold text-center leading-tight sm:hidden"
            style={{ fontSize: "13px", color: "#FFFFFF", lineHeight: "1.3" }}
          >
            Stakeholder Engagement
          </p>
          <div
            className="hidden sm:flex sm:flex-col items-center gap-1"
            style={{
              writingMode: "vertical-rl",
              transform: "rotate(180deg)",
            }}
          >
            <p
              className="font-bold whitespace-nowrap"
              style={{ fontSize: "12px", color: "#FFFFFF", letterSpacing: "0.5px" }}
            >
              Stakeholder
            </p>
            <p
              className="font-bold whitespace-nowrap"
              style={{ fontSize: "12px", color: "#FFFFFF", letterSpacing: "0.5px" }}
            >
              Engagement
            </p>
          </div>
        </div>

        {/* Track Content - aligned with timeline by adding sm:ml-[8px] offset */}
        <div className="flex-1 flex flex-col sm:flex-row sm:ml-[8px]" style={{ background: "#F7F7FF" }}>
          {/* Phase 1 */}
          <div className="flex-1 space-y-2 p-3 md:p-4">
            <div className="flex items-start gap-2">
              <Users size={16} style={{ color: "#000FC4", flexShrink: 0, marginTop: "2px" }} />
              <div>
                <p style={{ fontSize: "13px", color: "#000000", lineHeight: "1.4" }}>
                  1:1 interviews with all dept heads
                </p>
                <p className="italic" style={{ fontSize: "10px", color: "#434343" }}>
                  CEO, CMO, CRO, VP CS, CFO
                </p>
              </div>
            </div>
            <div className="flex items-start gap-2">
              <Eye size={16} style={{ color: "#000FC4", flexShrink: 0, marginTop: "2px" }} />
              <p style={{ fontSize: "13px", color: "#000000", lineHeight: "1.4" }}>Shadow sales calls & CS meetings</p>
            </div>
            <div className="flex items-start gap-2">
              <Presentation size={16} style={{ color: "#000FC4", flexShrink: 0, marginTop: "2px" }} />
              <div
                className="flex flex-wrap items-center gap-2 p-2 rounded flex-1"
                style={{ background: "rgba(45,228,230,0.1)", border: "1px solid #2DE4E6" }}
              >
                <p className="font-bold" style={{ fontSize: "13px", color: "#000000" }}>
                  Execution Presentation + Buy-in
                </p>
                <span
                  className="font-bold px-1.5 py-0.5 rounded-full text-white whitespace-nowrap"
                  style={{ fontSize: "9px", background: "#2DE4E6" }}
                >
                  MILESTONE
                </span>
              </div>
            </div>
          </div>

          {/* Phase 2 */}
          <div className="flex-1 space-y-2 p-3 md:p-4 border-t sm:border-t-0 sm:border-l border-white/20">
            <div className="flex items-start gap-2">
              <Handshake size={16} style={{ color: "#000FC4", flexShrink: 0, marginTop: "2px" }} />
              <p style={{ fontSize: "13px", color: "#000000", lineHeight: "1.4" }}>Cross-functional workshop</p>
            </div>
            <div className="flex items-start gap-2">
              <UserCheck size={16} style={{ color: "#000FC4", flexShrink: 0, marginTop: "2px" }} />
              <div>
                <p style={{ fontSize: "13px", color: "#000000", lineHeight: "1.4" }}>Weekly champion check-ins</p>
                <p className="italic" style={{ fontSize: "10px", color: "#434343" }}>
                  5-7 per department
                </p>
              </div>
            </div>
          </div>

          {/* Phase 3 */}
          <div className="flex-1 space-y-2 p-3 md:p-4 border-t sm:border-t-0 sm:border-l border-white/20">
            <div className="flex items-start gap-2">
              <Users size={16} style={{ color: "#000FC4", flexShrink: 0, marginTop: "2px" }} />
              <p style={{ fontSize: "13px", color: "#000000", lineHeight: "1.4" }}>Daily pilot team stand-ups</p>
            </div>
            <div className="flex items-start gap-2">
              <Shield size={16} style={{ color: "#000FC4", flexShrink: 0, marginTop: "2px" }} />
              <p style={{ fontSize: "13px", color: "#000000", lineHeight: "1.4" }}>Exec sponsor weekly sync</p>
            </div>
          </div>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row px-6 md:px-8 pb-4">
        {/* Track Header */}
        <div
          className="flex sm:flex-col items-center sm:justify-center gap-2 sm:gap-1 py-3 sm:py-2 sm:min-w-[48px] sm:w-[48px] sm:-ml-[48px]"
          style={{ background: "#000FC4" }}
        >
          <Megaphone size={18} className="sm:mb-2" style={{ color: "#FFFFFF" }} />
          <p
            className="font-bold text-center leading-tight sm:hidden"
            style={{ fontSize: "13px", color: "#FFFFFF", lineHeight: "1.3" }}
          >
            Communication Strategy
          </p>
          <div
            className="hidden sm:flex sm:flex-col items-center gap-1"
            style={{
              writingMode: "vertical-rl",
              transform: "rotate(180deg)",
            }}
          >
            <p
              className="font-bold whitespace-nowrap"
              style={{ fontSize: "12px", color: "#FFFFFF", letterSpacing: "0.5px" }}
            >
              Communication
            </p>
            <p
              className="font-bold whitespace-nowrap"
              style={{ fontSize: "12px", color: "#FFFFFF", letterSpacing: "0.5px" }}
            >
              Strategy
            </p>
          </div>
        </div>

        {/* Track Content - aligned with timeline by adding sm:ml-[8px] offset */}
        <div className="flex-1 flex flex-col sm:flex-row sm:ml-[8px]" style={{ background: "#FFFFFF" }}>
          {/* Phase 1 */}
          <div className="flex-1 space-y-1.5 p-3 md:p-4">
            <div className="flex items-center gap-2">
              <Megaphone size={14} style={{ color: "#F26419", flexShrink: 0 }} />
              <p className="font-bold" style={{ fontSize: "13px", color: "#000000" }}>
                All-hands kickoff
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Mail size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Week 1 progress email</p>
            </div>
            <div className="flex items-center gap-2">
              <Users size={14} style={{ color: "#2DE4E6", flexShrink: 0 }} />
              <p className="font-bold" style={{ fontSize: "13px", color: "#000000" }}>
                Town Hall #1: Discovery
              </p>
            </div>
            <div
              className="flex items-center gap-2 p-2 rounded"
              style={{ background: "rgba(45,228,230,0.1)", border: "1px solid #2DE4E6" }}
            >
              <Target size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p className="font-bold" style={{ fontSize: "13px", color: "#000000" }}>
                Month 1 executive readout
              </p>
              <span
                className="font-bold px-1.5 py-0.5 rounded-full text-white whitespace-nowrap ml-auto"
                style={{ fontSize: "9px", background: "#2DE4E6" }}
              >
                MILESTONE
              </span>
            </div>
          </div>

          {/* Phase 2 */}
          <div className="flex-1 space-y-1.5 p-3 md:p-4 border-t sm:border-t-0 sm:border-l border-gray-100">
            <div className="flex items-center gap-2">
              <GraduationCap size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Training kickoff</p>
            </div>
            <div className="flex items-center gap-2">
              <FileText size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Weekly newsletter starts</p>
            </div>
            <div
              className="flex items-center gap-2 p-2 rounded"
              style={{ background: "rgba(45,228,230,0.1)", border: "1px solid #2DE4E6" }}
            >
              <Trophy size={14} style={{ color: "#2DE4E6", flexShrink: 0 }} />
              <p className="font-bold" style={{ fontSize: "13px", color: "#000000" }}>
                Town Hall #2: Wins
              </p>
              <span
                className="font-bold px-1.5 py-0.5 rounded-full text-white whitespace-nowrap ml-auto"
                style={{ fontSize: "9px", background: "#2DE4E6" }}
              >
                MILESTONE
              </span>
            </div>
          </div>

          {/* Phase 3 */}
          <div className="flex-1 space-y-1.5 p-3 md:p-4 border-t sm:border-t-0 sm:border-l border-gray-100">
            <div className="flex items-center gap-2">
              <Star size={14} style={{ color: "#2DE4E6", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Success stories shared</p>
            </div>
            <div
              className="flex items-center gap-2 p-2 rounded"
              style={{ background: "rgba(45,228,230,0.1)", border: "1px solid #2DE4E6" }}
            >
              <Calendar size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p className="font-bold" style={{ fontSize: "13px", color: "#000000" }}>
                Q2 planning + retro
              </p>
              <span
                className="font-bold px-1.5 py-0.5 rounded-full text-white whitespace-nowrap ml-auto"
                style={{ fontSize: "9px", background: "#2DE4E6" }}
              >
                MILESTONE
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row px-6 md:px-8 pb-4">
        {/* Track Header */}
        <div
          className="flex sm:flex-col items-center sm:justify-center gap-2 sm:gap-1 py-3 sm:py-2 sm:min-w-[48px] sm:w-[48px] sm:-ml-[48px]"
          style={{ background: "#000FC4" }}
        >
          <Calendar size={18} className="sm:mb-2" style={{ color: "#FFFFFF" }} />
          <p
            className="font-bold text-center leading-tight sm:hidden"
            style={{ fontSize: "13px", color: "#FFFFFF", lineHeight: "1.3" }}
          >
            Meeting Rhythms
          </p>
          <p
            className="hidden sm:block font-bold whitespace-nowrap"
            style={{
              fontSize: "12px",
              color: "#FFFFFF",
              writingMode: "vertical-rl",
              transform: "rotate(180deg)",
              letterSpacing: "0.5px",
            }}
          >
            Meeting Rhythms
          </p>
        </div>

        {/* Track Content - aligned with timeline by adding sm:ml-[8px] offset */}
        <div className="flex-1 p-3 md:p-4 sm:ml-[8px]" style={{ background: "#F7F7FF" }}>
          <div className="space-y-2.5">
            {/* RevOps Council - Weekly */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-2">
              <div className="flex gap-1 flex-1 w-full">
                {Array.from({ length: 12 }).map((_, i) => (
                  <div key={i} className="flex-1 rounded" style={{ height: "14px", background: "#5963D9" }} />
                ))}
              </div>
              <div className="flex items-center gap-2 sm:gap-3 sm:min-w-[180px]">
                <p className="font-bold" style={{ fontSize: "12px", color: "#5963D9" }}>
                  RevOps Council
                </p>
                <p style={{ fontSize: "10px", color: "#434343" }}>Tues 2pm • Weekly</p>
              </div>
            </div>

            {/* Exec Sponsor - Bi-weekly later */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-2">
              <div className="flex gap-1 flex-1 w-full">
                {Array.from({ length: 12 }).map((_, i) => (
                  <div
                    key={i}
                    className="flex-1 rounded"
                    style={{
                      height: "14px",
                      background: i < 8 || i === 9 || i === 11 ? "#000FC4" : "transparent",
                      border: i >= 8 && i !== 9 && i !== 11 ? "1px dashed #E4E6F9" : "none",
                    }}
                  />
                ))}
              </div>
              <div className="flex items-center gap-2 sm:gap-3 sm:min-w-[180px]">
                <p className="font-bold" style={{ fontSize: "12px", color: "#000FC4" }}>
                  Exec Sponsor 1:1
                </p>
                <p style={{ fontSize: "10px", color: "#434343" }}>Weekly → Bi-weekly</p>
              </div>
            </div>

            {/* Team All-Hands - Bi-weekly */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-2">
              <div className="flex gap-1 flex-1 w-full">
                {Array.from({ length: 12 }).map((_, i) => (
                  <div
                    key={i}
                    className="flex-1 rounded"
                    style={{
                      height: "14px",
                      background: i % 2 === 1 ? "#2DE4E6" : "transparent",
                      border: i % 2 === 0 ? "1px dashed #E4E6F9" : "none",
                    }}
                  />
                ))}
              </div>
              <div className="flex items-center gap-2 sm:gap-3 sm:min-w-[180px]">
                <p className="font-bold" style={{ fontSize: "12px", color: "#2DE4E6" }}>
                  Team All-Hands
                </p>
                <p style={{ fontSize: "10px", color: "#434343" }}>Thurs 3pm • Bi-weekly</p>
              </div>
            </div>

            {/* Training Sessions - Weeks 5-8 */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-2">
              <div className="flex gap-1 flex-1 w-full">
                {Array.from({ length: 12 }).map((_, i) => (
                  <div
                    key={i}
                    className="flex-1 rounded"
                    style={{
                      height: "14px",
                      background: i >= 4 && i <= 7 ? "#F26419" : "transparent",
                      border: i < 4 || i > 7 ? "1px dashed #E4E6F9" : "none",
                    }}
                  />
                ))}
              </div>
              <div className="flex items-center gap-2 sm:gap-3 sm:min-w-[180px]">
                <p className="font-bold" style={{ fontSize: "12px", color: "#F26419" }}>
                  Training Sessions
                </p>
                <p style={{ fontSize: "10px", color: "#434343" }}>Wed • Weeks 5-8 only</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row px-6 md:px-8 pb-4">
        {/* Track Header */}
        <div
          className="flex sm:flex-col items-center sm:justify-center gap-2 sm:gap-1 py-3 sm:py-2 sm:min-w-[48px] sm:w-[48px] sm:-ml-[48px]"
          style={{ background: "#000FC4" }}
        >
          <Zap size={18} className="sm:mb-2" style={{ color: "#FFFFFF" }} />
          <p
            className="font-bold text-center leading-tight sm:hidden"
            style={{ fontSize: "13px", color: "#FFFFFF", lineHeight: "1.3" }}
          >
            Quick Wins
          </p>
          <div
            className="hidden sm:flex sm:flex-col items-center gap-1"
            style={{
              writingMode: "vertical-rl",
              transform: "rotate(180deg)",
            }}
          >
            <p
              className="font-bold whitespace-nowrap"
              style={{ fontSize: "12px", color: "#FFFFFF", letterSpacing: "0.5px" }}
            >
              Quick Wins
            </p>
          </div>
        </div>

        <div className="flex-1 flex flex-col sm:flex-row sm:ml-[8px]" style={{ background: "#FFFFFF" }}>
          {/* Phase 1 */}
          <div className="flex-1 flex flex-col gap-1 p-2 md:p-2.5">
            <div
              className="flex items-center gap-1.5 px-2 py-1 rounded"
              style={{ border: "1px solid #E4E6F9", background: "#FAFBFF" }}
            >
              <Zap size={14} style={{ color: "#2DE4E6", flexShrink: 0 }} />
              <p className="font-bold leading-tight" style={{ fontSize: "12px", color: "#000000" }}>
                Fix routing
              </p>
              <p className="font-bold ml-auto" style={{ fontSize: "11px", color: "#2DE4E6" }}>
                ↓80% time
              </p>
            </div>
            <div
              className="flex items-center gap-1.5 px-2 py-1 rounded"
              style={{ border: "1px solid #E4E6F9", background: "#FAFBFF" }}
            >
              <Database size={14} style={{ color: "#2DE4E6", flexShrink: 0 }} />
              <p className="font-bold leading-tight" style={{ fontSize: "12px", color: "#000000" }}>
                Clean dupes
              </p>
              <p className="font-bold ml-auto" style={{ fontSize: "11px", color: "#2DE4E6" }}>
                95% quality
              </p>
            </div>
            <div
              className="flex items-center gap-1.5 px-2 py-1 rounded"
              style={{ border: "1px solid #E4E6F9", background: "#FAFBFF" }}
            >
              <Calendar size={14} style={{ color: "#2DE4E6", flexShrink: 0 }} />
              <p className="font-bold leading-tight" style={{ fontSize: "12px", color: "#000000" }}>
                Add calendars
              </p>
              <p className="font-bold ml-auto" style={{ fontSize: "11px", color: "#2DE4E6" }}>
                3x bookings
              </p>
            </div>
          </div>

          {/* Phase 2 */}
          <div className="flex-1 flex flex-col gap-1 p-2 md:p-2.5 border-t sm:border-t-0 sm:border-l border-gray-100">
            <div
              className="flex items-center gap-1.5 px-2 py-1 rounded"
              style={{ border: "1px solid #E4E6F9", background: "#FAFBFF" }}
            >
              <BarChart3 size={14} style={{ color: "#2DE4E6", flexShrink: 0 }} />
              <p className="font-bold leading-tight" style={{ fontSize: "12px", color: "#000000" }}>
                Dashboard
              </p>
              <p className="font-bold ml-auto" style={{ fontSize: "11px", color: "#2DE4E6" }}>
                100% visibility
              </p>
            </div>
            <div
              className="flex items-center gap-1.5 px-2 py-1 rounded"
              style={{ border: "1px solid #E4E6F9", background: "#FAFBFF" }}
            >
              <RotateCw size={14} style={{ color: "#2DE4E6", flexShrink: 0 }} />
              <p className="font-bold leading-tight" style={{ fontSize: "12px", color: "#000000" }}>
                Automation
              </p>
              <p className="font-bold ml-auto" style={{ fontSize: "11px", color: "#2DE4E6" }}>
                50% time saved
              </p>
            </div>
          </div>

          {/* Phase 3 */}
          <div className="flex-1 flex flex-col gap-1 p-2 md:p-2.5 border-t sm:border-t-0 sm:border-l border-gray-100">
            <div
              className="flex items-center gap-1.5 px-2 py-1 rounded"
              style={{ border: "1px solid #E4E6F9", background: "#FAFBFF" }}
            >
              <TrendingUp size={14} style={{ color: "#2DE4E6", flexShrink: 0 }} />
              <p className="font-bold leading-tight" style={{ fontSize: "12px", color: "#000000" }}>
                Unified report
              </p>
              <p className="font-bold ml-auto" style={{ fontSize: "11px", color: "#2DE4E6" }}>
                1 source truth
              </p>
            </div>
            <div
              className="flex items-center gap-1.5 px-2 py-1 rounded"
              style={{ border: "1px solid #E4E6F9", background: "#FAFBFF" }}
            >
              <Bot size={14} style={{ color: "#2DE4E6", flexShrink: 0 }} />
              <p className="font-bold leading-tight" style={{ fontSize: "12px", color: "#000000" }}>
                AI pilot
              </p>
              <p className="font-bold ml-auto" style={{ fontSize: "11px", color: "#2DE4E6" }}>
                75% qualified
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row px-6 md:px-8 pb-4">
        {/* Track Header */}
        <div
          className="flex sm:flex-col items-center sm:justify-center gap-2 sm:gap-1 py-3 sm:py-2 sm:min-w-[48px] sm:w-[48px] sm:-ml-[48px]"
          style={{ background: "#000FC4" }}
        >
          <RefreshCw size={18} className="sm:mb-2" style={{ color: "#FFFFFF" }} />
          <p
            className="font-bold text-center leading-tight sm:hidden"
            style={{ fontSize: "13px", color: "#FFFFFF", lineHeight: "1.3" }}
          >
            Change Management
          </p>
          <div
            className="hidden sm:flex sm:flex-col items-center gap-1"
            style={{
              writingMode: "vertical-rl",
              transform: "rotate(180deg)",
            }}
          >
            <p
              className="font-bold whitespace-nowrap"
              style={{ fontSize: "12px", color: "#FFFFFF", letterSpacing: "0.5px" }}
            >
              Change
            </p>
            <p
              className="font-bold whitespace-nowrap"
              style={{ fontSize: "12px", color: "#FFFFFF", letterSpacing: "0.5px" }}
            >
              Management
            </p>
          </div>
        </div>

        {/* Track Content - aligned with timeline by adding sm:ml-[8px] offset */}
        <div className="flex-1 flex flex-col sm:flex-row sm:ml-[8px]" style={{ background: "#F7F7FF" }}>
          {/* Phase 1 */}
          <div className="flex-1 space-y-1.5 p-3 md:p-4">
            <div className="flex items-center gap-2">
              <Clipboard size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Assess resistance</p>
            </div>
            <div className="flex items-center gap-2">
              <Star size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>ID champions (3-5/dept)</p>
            </div>
            <div className="flex items-center gap-2">
              <AlertTriangle size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Document pain points</p>
            </div>
          </div>

          {/* Phase 2 */}
          <div className="flex-1 space-y-1.5 p-3 md:p-4 border-t sm:border-t-0 sm:border-l border-white/20">
            <div className="flex items-center gap-2">
              <Award size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Train champions</p>
            </div>
            <div className="flex items-center gap-2">
              <FileText size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Document SOPs</p>
            </div>
            <div className="flex items-center gap-2">
              <MessageCircle size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>User feedback loops</p>
            </div>
          </div>

          {/* Phase 3 */}
          <div className="flex-1 space-y-1.5 p-3 md:p-4 border-t sm:border-t-0 sm:border-l border-white/20">
            <div className="flex items-center gap-2">
              <LineChart size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Track adoption weekly</p>
            </div>
            <div className="flex items-center gap-2">
              <AlertCircle size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Address blockers</p>
            </div>
            <div className="flex items-center gap-2">
              <RefreshCw size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Pilot retrospective</p>
            </div>
          </div>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row px-6 md:px-8 pb-4">
        {/* Track Header */}
        <div
          className="flex sm:flex-col items-center sm:justify-center gap-2 sm:gap-1 py-3 sm:py-2 sm:min-w-[48px] sm:w-[48px] sm:-ml-[48px]"
          style={{ background: "#2DE4E6" }}
        >
          <Users size={18} className="sm:mb-2" style={{ color: "#FFFFFF" }} />
          <p
            className="font-bold text-center leading-tight sm:hidden"
            style={{ fontSize: "13px", color: "#FFFFFF", lineHeight: "1.3" }}
          >
            People & Culture
          </p>
          <div
            className="hidden sm:flex sm:flex-col items-center gap-1"
            style={{
              writingMode: "vertical-rl",
              transform: "rotate(180deg)",
            }}
          >
            <p
              className="font-bold whitespace-nowrap"
              style={{ fontSize: "12px", color: "#FFFFFF", letterSpacing: "0.5px" }}
            >
              People &
            </p>
            <p
              className="font-bold whitespace-nowrap"
              style={{ fontSize: "12px", color: "#FFFFFF", letterSpacing: "0.5px" }}
            >
              Culture
            </p>
          </div>
        </div>

        {/* Track Content */}
        <div className="flex-1 flex flex-col sm:flex-row sm:ml-[8px]" style={{ background: "#F5FEFF" }}>
          {/* Phase 1 */}
          <div className="flex-1 space-y-1.5 p-3 md:p-4">
            <div className="flex items-center gap-2">
              <Eye size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Stakeholder mapping</p>
            </div>
            <div className="flex items-center gap-2">
              <Presentation size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Leadership buy-in</p>
            </div>
            <div className="flex items-center gap-2">
              <Handshake size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Dept alignment</p>
            </div>
          </div>

          {/* Phase 2 */}
          <div className="flex-1 space-y-1.5 p-3 md:p-4 border-t sm:border-t-0 sm:border-l border-white/20">
            <div className="flex items-center gap-2">
              <UserCheck size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Role definitions</p>
            </div>
            <div className="flex items-center gap-2">
              <Shield size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Governance model</p>
            </div>
            <div className="flex items-center gap-2">
              <Megaphone size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Comms plan</p>
            </div>
          </div>

          {/* Phase 3 */}
          <div className="flex-1 space-y-1.5 p-3 md:p-4 border-t sm:border-t-0 sm:border-l border-white/20">
            <div className="flex items-center gap-2">
              <Mail size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Weekly updates</p>
            </div>
            <div className="flex items-center gap-2">
              <Target size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Success metrics</p>
            </div>
            <div className="flex items-center gap-2">
              <GraduationCap size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Team upskilling</p>
            </div>
          </div>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row px-6 md:px-8 pb-4">
        {/* Track Header */}
        <div
          className="flex sm:flex-col items-center sm:justify-center gap-2 sm:gap-1 py-3 sm:py-2 sm:min-w-[48px] sm:w-[48px] sm:-ml-[48px]"
          style={{ background: "#5963D9" }}
        >
          <Database size={18} className="sm:mb-2" style={{ color: "#FFFFFF" }} />
          <p
            className="font-bold text-center leading-tight sm:hidden"
            style={{ fontSize: "13px", color: "#FFFFFF", lineHeight: "1.3" }}
          >
            Technology & Process
          </p>
          <div
            className="hidden sm:flex sm:flex-col items-center gap-1"
            style={{
              writingMode: "vertical-rl",
              transform: "rotate(180deg)",
            }}
          >
            <p
              className="font-bold whitespace-nowrap"
              style={{ fontSize: "12px", color: "#FFFFFF", letterSpacing: "0.5px" }}
            >
              Technology
            </p>
            <p
              className="font-bold whitespace-nowrap"
              style={{ fontSize: "12px", color: "#FFFFFF", letterSpacing: "0.5px" }}
            >
              & Process
            </p>
          </div>
        </div>

        {/* Track Content */}
        <div className="flex-1 flex flex-col sm:flex-row sm:ml-[8px]" style={{ background: "#F5F6FF" }}>
          {/* Phase 1 */}
          <div className="flex-1 space-y-1.5 p-3 md:p-4">
            <div className="flex items-center gap-2">
              <FileText size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Tech stack audit</p>
            </div>
            <div className="flex items-center gap-2">
              <Trophy size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Quick wins</p>
            </div>
            <div className="flex items-center gap-2">
              <Star size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Priority gaps</p>
            </div>
          </div>

          {/* Phase 2 */}
          <div className="flex-1 space-y-1.5 p-3 md:p-4 border-t sm:border-t-0 sm:border-l border-white/20">
            <div className="flex items-center gap-2">
              <Calendar size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>MVP scope</p>
            </div>
            <div className="flex items-center gap-2">
              <Zap size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Integration build</p>
            </div>
            <div className="flex items-center gap-2">
              <Database size={14} style={{ color: "#000FC4", flexShrink: 0 }} />
              <p style={{ fontSize: "13px", color: "#000000" }}>Data cleanup</p>
            </div>
          </div>

          {/* Phase 3 */}
          <div className="flex-1 space-y-1.5 p-3 md:p-4 border-t sm:border-t-0 sm:border-l border-white/20">
            <div
              className="flex items-center gap-1.5 px-2 py-1 rounded"
              style={{ border: "1px solid #E4E6F9", background: "#FAFBFF" }}
            >
              <BarChart3 size={14} style={{ color: "#2DE4E6", flexShrink: 0 }} />
              <p className="font-bold leading-tight" style={{ fontSize: "12px", color: "#000000" }}>
                Pipeline
              </p>
              <p className="font-bold ml-auto" style={{ fontSize: "11px", color: "#2DE4E6" }}>
                100% visibility
              </p>
            </div>
            <div
              className="flex items-center gap-1.5 px-2 py-1 rounded"
              style={{ border: "1px solid #E4E6F9", background: "#FAFBFF" }}
            >
              <RotateCw size={14} style={{ color: "#2DE4E6", flexShrink: 0 }} />
              <p className="font-bold leading-tight" style={{ fontSize: "12px", color: "#000000" }}>
                Automation
              </p>
              <p className="font-bold ml-auto" style={{ fontSize: "11px", color: "#2DE4E6" }}>
                50% time saved
              </p>
            </div>
          </div>
        </div>
      </div>

      <div
        className="flex flex-col sm:flex-row items-stretch sm:items-center justify-around gap-3 sm:gap-4 py-5 mx-6 md:mx-8"
        style={{
          background: "linear-gradient(90deg, #000FC4 0%, #333FD0 100%)",
        }}
      >
        <div className="flex items-center gap-2.5">
          <Users size={18} style={{ color: "#2DE4E6", flexShrink: 0 }} />
          <div>
            <p className="font-bold leading-tight" style={{ fontSize: "13px", color: "#FFFFFF" }}>
              Executive Sponsor Engaged
            </p>
            <p style={{ fontSize: "11px", color: "rgba(255,255,255,0.8)" }}>40% lower failure risk</p>
          </div>
        </div>
        <div className="flex items-center gap-2.5">
          <MessageCircle size={18} style={{ color: "#2DE4E6", flexShrink: 0 }} />
          <div>
            <p className="font-bold leading-tight" style={{ fontSize: "13px", color: "#FFFFFF" }}>
              Proactive Communication
            </p>
            <p style={{ fontSize: "11px", color: "rgba(255,255,255,0.8)" }}>Weekly updates prevent resistance</p>
          </div>
        </div>
        <div className="flex items-center gap-2.5">
          <Zap size={18} style={{ color: "#2DE4E6", flexShrink: 0 }} />
          <div>
            <p className="font-bold leading-tight" style={{ fontSize: "13px", color: "#FFFFFF" }}>
              Quick Wins Build Momentum
            </p>
            <p style={{ fontSize: "11px", color: "rgba(255,255,255,0.8)" }}>Impact within 2 weeks</p>
          </div>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row items-stretch mx-6 md:mx-8 mb-6">
        {/* Left section with research */}
        <div className="flex items-center gap-3 flex-1 py-2.5 px-4" style={{ background: "#E4E6F9" }}>
          <p className="leading-relaxed" style={{ fontSize: "10px", color: "#434343" }}>
            Research: Forrester, Revenue Operations Alliance, 50+ implementations
          </p>
        </div>
        {/* Right section with branding */}
        <div
          className="flex items-center justify-end gap-3 py-2.5 px-4 sm:min-w-[140px]"
          style={{
            background: "#0A0A0A",
          }}
        >
          <p style={{ fontSize: "10px", color: "rgba(255,255,255,0.5)" }}>www.man.digital</p>
        </div>
      </div>
    </div>
  )
}
