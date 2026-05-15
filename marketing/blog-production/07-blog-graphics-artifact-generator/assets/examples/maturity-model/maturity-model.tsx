import { Database, BarChart3, Bot, TrendingUp, Rocket, CheckCircle2 } from 'lucide-react';
import svgPaths from "./imports/svg-yora7d2x3t";

function DotsPattern({ className }: { className?: string }) {
  return (
    <div className={className}>
      <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 223 109">
        <g>
          <path d={svgPaths.p18dc0380} fill="#E4E6F9" />
          <path d={svgPaths.p3a984b80} fill="#E4E6F9" />
        </g>
      </svg>
    </div>
  );
}

function CircularGradients() {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      <svg className="block w-full h-full" fill="none" preserveAspectRatio="none" viewBox="0 0 1949 2400">
        <g>
          <path d={svgPaths.p33884200} fill="url(#paint0_linear)" opacity="0.13" />
          <path d={svgPaths.p64312c0} fill="url(#paint1_linear)" opacity="0.1" />
        </g>
        <defs>
          <linearGradient gradientUnits="userSpaceOnUse" id="paint0_linear" x1="155.925" x2="793.246" y1="540.496" y2="399.835">
            <stop stopColor="white" stopOpacity="0" />
            <stop offset="1" stopColor="white" />
          </linearGradient>
          <linearGradient gradientUnits="userSpaceOnUse" id="paint1_linear" x1="1456.48" x2="1868.53" y1="1800" y2="1700">
            <stop stopColor="white" />
            <stop offset="1" stopColor="white" stopOpacity="0" />
          </linearGradient>
        </defs>
      </svg>
    </div>
  );
}

export default function App() {
  const levels = [
    {
      icon: Database,
      level: 1,
      title: "Organize & Integrate Data",
      badge: "FOUNDATION",
      badgeColor: "#FF6B35",
      items: [
        "Centralize revenue records using Data Hub",
        "Connect marketing, sales, and customer success datasets",
        "Establish workflows and naming conventions"
      ],
      target: "Target: > 95% data completeness"
    },
    {
      icon: BarChart3,
      level: 2,
      title: "Establish KPIs & Measure",
      badge: "VISIBILITY",
      badgeColor: "#2DE4E6",
      items: [
        "Define CAC, LTV, and conversion rates",
        "Build dashboards using Data Studio",
        "Replace ad-hoc reporting with automated insights"
      ],
      target: "Target: 40% faster decisions"
    },
    {
      icon: Bot,
      level: 3,
      title: "Deploy AI Agents",
      badge: "AUTOMATION",
      badgeColor: "#8B5CF6",
      items: [
        "Activate AI-powered Segments and Marketing Studio",
        "Launch Prospecting Agents for automated outreach",
        "Implement Customer Agents for instant support"
      ],
      target: "Target: 75% AI adoption"
    },
    {
      icon: TrendingUp,
      level: 4,
      title: "Predictive Excellence",
      badge: "PREDICTION",
      badgeColor: "#10B981",
      items: [
        "Use predictive analytics for pipeline management",
        "Enable AI CPQ for automated quoting",
        "Achieve 85%+ forecast accuracy"
      ],
      target: "Target: 85% forecast accuracy"
    },
    {
      icon: Rocket,
      level: 5,
      title: "Self-Improving Engine",
      badge: "AUTONOMOUS",
      badgeColor: "#EC4899",
      items: [
        "Implement predictive churn prevention",
        "Deploy Loop marketing for continuous improvement",
        "Create autonomous revenue operations"
      ],
      target: "Target: 110% net retention"
    }
  ];

  return (
    <div className="min-h-screen bg-white flex items-center justify-center py-16">
      <div className="w-[1200px] relative">
        {/* Blue Background Container */}
        <div className="relative bg-[#000fc4] py-24 px-16 overflow-hidden">
          {/* Circular Gradients */}
          <CircularGradients />
          
          {/* Dot Patterns */}
          <DotsPattern className="absolute top-8 left-8 w-[150px] h-[75px] opacity-40" />
          <DotsPattern className="absolute bottom-8 right-8 w-[150px] h-[75px] opacity-40 rotate-180" />
          
          {/* Content */}
          <div className="relative z-10">
            {/* Header */}
            <div className="text-center mb-16">
              <h1 className="text-[56px] leading-tight mb-4" style={{ fontFamily: 'Montserrat', fontWeight: 700, color: 'white' }}>
                <span style={{ fontFamily: 'Montserrat', fontWeight: 500, fontStyle: 'italic' }}>AI-Enabled</span> RevOps<br/>
                Maturity Model
              </h1>
              <p className="text-[24px]" style={{ fontFamily: 'Montserrat', fontWeight: 500, color: 'rgba(255,255,255,0.9)' }}>
                Your Path from Chaos to Predictable Revenue
              </p>
            </div>

            {/* Level Cards */}
            <div className="flex flex-col items-center gap-8 max-w-[900px] mx-auto">
              {levels.map((levelData, index) => {
                const Icon = levelData.icon;
                return (
                  <div key={index} className="w-full">
                    <div className="bg-[#f7f7ff] p-8 flex gap-6 items-start">
                      {/* Icon Box */}
                      <div className="bg-[#000fc4] flex items-center justify-center flex-shrink-0 w-[72px] h-[72px]">
                        <Icon size={40} strokeWidth={2} color="white" />
                      </div>
                      
                      {/* Content */}
                      <div className="flex-1">
                        <div className="flex items-start gap-4 mb-4">
                          <h2 className="text-[28px] leading-tight flex-1" style={{ fontFamily: 'Montserrat', fontWeight: 700, color: '#000fc4' }}>
                            Level {levelData.level}: {levelData.title}
                          </h2>
                          <span 
                            className="px-4 py-1.5 text-white rounded-full text-[11px] flex-shrink-0 self-start mt-1" 
                            style={{ fontFamily: 'Lato', fontWeight: 700, letterSpacing: '0.5px', backgroundColor: levelData.badgeColor }}
                          >
                            {levelData.badge}
                          </span>
                        </div>
                        
                        <ul className="space-y-3 mb-4">
                          {levelData.items.map((item, idx) => (
                            <li key={idx} className="flex gap-3 items-start">
                              <CheckCircle2 size={20} className="flex-shrink-0 mt-0.5" color="#000fc4" />
                              <span className="text-[18px] leading-relaxed" style={{ fontFamily: 'Lato', fontWeight: 400, color: '#222222' }}>
                                {item}
                              </span>
                            </li>
                          ))}
                        </ul>
                        
                        <p className="text-[17px]" style={{ fontFamily: 'Lato', fontWeight: 700, color: '#000fc4' }}>
                          {levelData.target}
                        </p>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
