import { Database, RotateCw, Gauge, Zap } from 'lucide-react';
import svgPaths from './imports/svg-kommqy1cec';

function DotPattern() {
  return (
    <svg className="block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 250 109">
      <g>
        <path d={svgPaths.pafc3d00} fill="#333FD0" opacity="0.15" />
        <path d={svgPaths.pe0ab100} fill="#333FD0" opacity="0.15" />
      </g>
    </svg>
  );
}

export default function App() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100 p-8">
      <div className="relative bg-white" style={{ width: '800px', height: '900px' }}>
        {/* Decorative Dot Pattern - Top Right */}
        <div className="absolute right-0 top-8 w-32 h-14 opacity-30">
          <DotPattern />
        </div>

        {/* Decorative Dot Pattern - Bottom Left */}
        <div className="absolute left-0 bottom-28 w-32 h-14 opacity-30">
          <DotPattern />
        </div>

        {/* Decorative Accent Lines - Top Left */}
        <div className="absolute left-10 top-16">
          <div className="flex gap-1.5">
            <div className="w-1 h-12 bg-gradient-to-b from-cyan-400 to-blue-600 rounded-full" />
            <div className="w-1 h-8 bg-gradient-to-b from-cyan-400 to-blue-600 rounded-full opacity-60" />
          </div>
        </div>

        {/* Decorative Accent Lines - Bottom Right */}
        <div className="absolute right-10 bottom-32">
          <div className="flex gap-1.5">
            <div className="w-1 h-8 bg-gradient-to-b from-cyan-400 to-blue-600 rounded-full opacity-60" />
            <div className="w-1 h-12 bg-gradient-to-b from-cyan-400 to-blue-600 rounded-full" />
          </div>
        </div>

        {/* Decorative Circle - Middle Left */}
        <div className="absolute left-6 top-1/3">
          <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#2DE4E6', opacity: 0.4 }} />
        </div>

        {/* Decorative Circle - Middle Right */}
        <div className="absolute right-6 top-2/3">
          <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#2DE4E6', opacity: 0.4 }} />
        </div>

        {/* Header Section */}
        <div className="relative pt-12 pb-12 px-10">
          {/* Eyebrow */}
          <div className="flex justify-center mb-5">
            <p
              className="uppercase text-center"
              style={{
                fontFamily: 'Lato, sans-serif',
                fontWeight: 700,
                fontSize: '13px',
                color: '#000FC4',
                letterSpacing: '1.5px'
              }}
            >
              THE FUTURE OF B2B
            </p>
          </div>

          {/* Main Title */}
          <h1
            className="text-center px-4"
            style={{
              fontFamily: 'Montserrat, sans-serif',
              fontWeight: 700,
              fontSize: '42px',
              color: '#222222',
              lineHeight: '1.15',
              letterSpacing: '-1.5px'
            }}
          >
            3 Forces Reshaping Revenue Operations
          </h1>
        </div>

        {/* Three Column Section */}
        <div className="relative px-8 pb-6">
          <div className="flex gap-1">
            {/* Force 1 - Data Explosion */}
            <div
              className="flex flex-col p-7 justify-between"
              style={{
                width: '256px',
                minHeight: '480px',
                backgroundColor: '#ECF1FB'
              }}
            >
              <div>
                {/* Icon Container */}
                <div
                  className="flex items-center justify-center mb-5 relative"
                  style={{
                    width: '56px',
                    height: '56px',
                    backgroundColor: '#000FC4'
                  }}
                >
                  <Database size={32} strokeWidth={2.5} color="#EEF0FB" />
                  <div className="absolute -right-1 -top-1 w-2 h-2 rounded-full" style={{ backgroundColor: '#2DE4E6' }} />
                </div>

                {/* Title */}
                <h2
                  className="mb-2"
                  style={{
                    fontFamily: 'Montserrat, sans-serif',
                    fontWeight: 700,
                    fontSize: '22px',
                    color: '#222222',
                    lineHeight: '1.3',
                    letterSpacing: '-0.5px'
                  }}
                >
                  Data Explosion
                </h2>

                {/* Subtitle */}
                <p
                  className="mb-5"
                  style={{
                    fontFamily: 'Lato, sans-serif',
                    fontWeight: 700,
                    fontSize: '15px',
                    color: '#000FC4',
                    lineHeight: '1.3'
                  }}
                >
                  Demands AI Intelligence
                </p>

                {/* Description */}
                <p
                  style={{
                    fontFamily: 'Lato, sans-serif',
                    fontWeight: 400,
                    fontSize: '15px',
                    color: '#222222',
                    lineHeight: '1.6'
                  }}
                >
                  Teams generate 400M terabytes daily. Yet companies analyze only 12% of available data.
                </p>
              </div>

              {/* Statistic */}
              <div className="mt-6">
                <div
                  className="inline-flex flex-col items-center justify-center rounded-full mb-2 relative"
                  style={{
                    width: '70px',
                    height: '70px',
                    backgroundColor: '#2DE4E6',
                    boxShadow: '0 4px 12px rgba(45, 228, 230, 0.25)'
                  }}
                >
                  <span
                    style={{
                      fontFamily: 'Montserrat, sans-serif',
                      fontWeight: 700,
                      fontSize: '30px',
                      color: '#FFFFFF',
                      lineHeight: '1'
                    }}
                  >
                    12%
                  </span>
                </div>
                <p
                  className="mb-3"
                  style={{
                    fontFamily: 'Lato, sans-serif',
                    fontWeight: 400,
                    fontSize: '13px',
                    color: '#434343',
                    lineHeight: '1.4'
                  }}
                >
                  of data analyzed
                </p>
                {/* Secondary Stat */}
                <div className="mt-2">
                  <p
                    style={{
                      fontFamily: 'Lato, sans-serif',
                      fontWeight: 700,
                      fontSize: '14px',
                      color: '#2DE4E6',
                      lineHeight: '1.2'
                    }}
                  >
                    400M TB
                  </p>
                  <p
                    style={{
                      fontFamily: 'Lato, sans-serif',
                      fontWeight: 400,
                      fontSize: '12px',
                      color: '#999999',
                      lineHeight: '1.3'
                    }}
                  >
                    created daily
                  </p>
                </div>
              </div>
            </div>

            {/* Force 2 - Repeatability Crisis */}
            <div
              className="flex flex-col p-7 justify-between"
              style={{
                width: '256px',
                minHeight: '480px',
                backgroundColor: '#F2F6FC'
              }}
            >
              <div>
                {/* Icon Container */}
                <div
                  className="flex items-center justify-center mb-5 relative"
                  style={{
                    width: '56px',
                    height: '56px',
                    backgroundColor: '#000FC4'
                  }}
                >
                  <RotateCw size={32} strokeWidth={2.5} color="#EEF0FB" />
                  <div className="absolute -right-1 -top-1 w-2 h-2 rounded-full" style={{ backgroundColor: '#2DE4E6' }} />
                </div>

                {/* Title */}
                <h2
                  className="mb-2"
                  style={{
                    fontFamily: 'Montserrat, sans-serif',
                    fontWeight: 700,
                    fontSize: '22px',
                    color: '#222222',
                    lineHeight: '1.3',
                    letterSpacing: '-0.5px'
                  }}
                >
                  Repeatability Crisis
                </h2>

                {/* Subtitle */}
                <p
                  className="mb-5"
                  style={{
                    fontFamily: 'Lato, sans-serif',
                    fontWeight: 700,
                    fontSize: '15px',
                    color: '#000FC4',
                    lineHeight: '1.3'
                  }}
                >
                  Heroes Don't Scale
                </p>

                {/* Description */}
                <p
                  style={{
                    fontFamily: 'Lato, sans-serif',
                    fontWeight: 400,
                    fontSize: '15px',
                    color: '#222222',
                    lineHeight: '1.6'
                  }}
                >
                  Sustainable growth needs documented processes. Most rely on tribal knowledge.
                </p>
              </div>

              {/* Statistic */}
              <div className="mt-6">
                <div
                  className="inline-flex flex-col items-center justify-center rounded-full mb-2 relative"
                  style={{
                    width: '70px',
                    height: '70px',
                    backgroundColor: '#2DE4E6',
                    boxShadow: '0 4px 12px rgba(45, 228, 230, 0.25)'
                  }}
                >
                  <span
                    style={{
                      fontFamily: 'Montserrat, sans-serif',
                      fontWeight: 700,
                      fontSize: '30px',
                      color: '#FFFFFF',
                      lineHeight: '1'
                    }}
                  >
                    67%
                  </span>
                </div>
                <p
                  className="mb-3"
                  style={{
                    fontFamily: 'Lato, sans-serif',
                    fontWeight: 400,
                    fontSize: '13px',
                    color: '#434343',
                    lineHeight: '1.4'
                  }}
                >
                  lack documentation
                </p>
                {/* Secondary Stat */}
                <div className="mt-2">
                  <p
                    style={{
                      fontFamily: 'Lato, sans-serif',
                      fontWeight: 700,
                      fontSize: '14px',
                      color: '#2DE4E6',
                      lineHeight: '1.2'
                    }}
                  >
                    31%
                  </p>
                  <p
                    style={{
                      fontFamily: 'Lato, sans-serif',
                      fontWeight: 400,
                      fontSize: '12px',
                      color: '#999999',
                      lineHeight: '1.3'
                    }}
                  >
                    data-driven orgs
                  </p>
                </div>
              </div>
            </div>

            {/* Force 3 - Measurement Gaps */}
            <div
              className="flex flex-col p-7 justify-between"
              style={{
                width: '256px',
                minHeight: '480px',
                backgroundColor: '#ECF1FB'
              }}
            >
              <div>
                {/* Icon Container */}
                <div
                  className="flex items-center justify-center mb-5 relative"
                  style={{
                    width: '56px',
                    height: '56px',
                    backgroundColor: '#000FC4'
                  }}
                >
                  <Gauge size={32} strokeWidth={2.5} color="#EEF0FB" />
                  <div className="absolute -right-1 -top-1 w-2 h-2 rounded-full" style={{ backgroundColor: '#2DE4E6' }} />
                </div>

                {/* Title */}
                <h2
                  className="mb-2"
                  style={{
                    fontFamily: 'Montserrat, sans-serif',
                    fontWeight: 700,
                    fontSize: '22px',
                    color: '#222222',
                    lineHeight: '1.3',
                    letterSpacing: '-0.5px'
                  }}
                >
                  Measurement Gaps
                </h2>

                {/* Subtitle */}
                <p
                  className="mb-5"
                  style={{
                    fontFamily: 'Lato, sans-serif',
                    fontWeight: 700,
                    fontSize: '15px',
                    color: '#000FC4',
                    lineHeight: '1.3'
                  }}
                >
                  Kill Growth
                </p>

                {/* Description */}
                <p
                  style={{
                    fontFamily: 'Lato, sans-serif',
                    fontWeight: 400,
                    fontSize: '15px',
                    color: '#222222',
                    lineHeight: '1.6'
                  }}
                >
                  Poor data quality costs billions. Most forecasts miss targets.
                </p>
              </div>

              {/* Statistic */}
              <div className="mt-6">
                <div
                  className="inline-flex flex-col items-center justify-center rounded-full mb-2 relative"
                  style={{
                    width: '70px',
                    height: '70px',
                    backgroundColor: '#2DE4E6',
                    boxShadow: '0 4px 12px rgba(45, 228, 230, 0.25)'
                  }}
                >
                  <span
                    style={{
                      fontFamily: 'Montserrat, sans-serif',
                      fontWeight: 700,
                      fontSize: '30px',
                      color: '#FFFFFF',
                      lineHeight: '1'
                    }}
                  >
                    40%
                  </span>
                </div>
                <p
                  className="mb-3"
                  style={{
                    fontFamily: 'Lato, sans-serif',
                    fontWeight: 400,
                    fontSize: '13px',
                    color: '#434343',
                    lineHeight: '1.4'
                  }}
                >
                  forecast miss rate
                </p>
                {/* Secondary Stat */}
                <div className="mt-2">
                  <p
                    style={{
                      fontFamily: 'Lato, sans-serif',
                      fontWeight: 700,
                      fontSize: '14px',
                      color: '#2DE4E6',
                      lineHeight: '1.2'
                    }}
                  >
                    $3.1T
                  </p>
                  <p
                    style={{
                      fontFamily: 'Lato, sans-serif',
                      fontWeight: 400,
                      fontSize: '12px',
                      color: '#999999',
                      lineHeight: '1.3'
                    }}
                  >
                    cost of bad data
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom CTA Section */}
        <div
          className="absolute bottom-0 left-0 right-0 flex items-center justify-center px-12 overflow-hidden"
          style={{
            height: '100px',
            background: 'linear-gradient(135deg, #000FC4 0%, #333FD0 100%)'
          }}
        >
          {/* Background Decorative Element */}
          <div className="absolute left-0 top-0 w-40 h-40 opacity-10">
            <div className="w-full h-full rounded-full" style={{ background: 'radial-gradient(circle, #2DE4E6 0%, transparent 70%)' }} />
          </div>
          <div className="absolute right-0 bottom-0 w-32 h-32 opacity-10">
            <div className="w-full h-full rounded-full" style={{ background: 'radial-gradient(circle, #2DE4E6 0%, transparent 70%)' }} />
          </div>

          <div className="flex items-center gap-4 relative z-10">
            <div className="flex items-center justify-center" style={{ width: '48px', height: '48px' }}>
              <Zap size={36} color="#2DE4E6" fill="#2DE4E6" strokeWidth={2} />
            </div>
            <p
              style={{
                fontFamily: 'Montserrat, sans-serif',
                fontWeight: 700,
                fontSize: '26px',
                color: '#FFFFFF',
                lineHeight: '1.2',
                letterSpacing: '-0.5px'
              }}
            >
              HubSpot's Data Hub + Breeze Agents = Transformation
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
