# TSX Artifact Output Examples

Complete examples showing EXACTLY how to output TSX artifacts for blog graphics.

## Critical: Always Use Artifact Format

Every graphic MUST be output as a TSX artifact that the user can see rendered.

## Example 1: Simple Metric Cards

### User Request
"Create 3 metric cards showing 85% accuracy, 120+ customers, 95% retention"

### Claude Response

I'll create a TSX artifact showing your three metric cards:

```tsx
// Blog Graphic: Three Metric Cards
// Placement: Flexible (suggest after intro or before conclusion)
// Dimensions: 800px × 400px

import { Target, Users, Trophy } from 'lucide-react';

export default function MetricCards() {
  return (
    <div style={{
      width: '800px',
      padding: '40px',
      backgroundColor: '#FFFFFF',
      fontFamily: 'Lato, sans-serif'
    }}>
      {/* Title */}
      <h2 style={{
        fontFamily: 'Montserrat, sans-serif',
        fontWeight: 700,
        fontSize: '32px',
        color: '#000FC4',
        textAlign: 'center',
        marginBottom: '48px'
      }}>
        2024 Performance Highlights
      </h2>
      
      {/* Three Cards */}
      <div style={{
        display: 'flex',
        gap: '32px',
        justifyContent: 'center'
      }}>
        {/* Card 1 */}
        <div style={{
          flex: 1,
          backgroundColor: '#F7F7FF',
          padding: '32px',
          borderRadius: '12px',
          textAlign: 'center'
        }}>
          <div style={{
            display: 'flex',
            justifyContent: 'center',
            marginBottom: '20px'
          }}>
            <Target size={80} strokeWidth={2} color="#000FC4" />
          </div>
          <div style={{
            fontFamily: 'Montserrat, sans-serif',
            fontWeight: 700,
            fontSize: '48px',
            color: '#2DE4E6',
            marginBottom: '12px'
          }}>
            85%
          </div>
          <p style={{
            fontFamily: 'Lato, sans-serif',
            fontSize: '16px',
            color: '#434343',
            margin: 0
          }}>
            Accuracy Rate
          </p>
        </div>
        
        {/* Card 2 */}
        <div style={{
          flex: 1,
          backgroundColor: '#F7F7FF',
          padding: '32px',
          borderRadius: '12px',
          textAlign: 'center'
        }}>
          <div style={{
            display: 'flex',
            justifyContent: 'center',
            marginBottom: '20px'
          }}>
            <Users size={80} strokeWidth={2} color="#000FC4" />
          </div>
          <div style={{
            fontFamily: 'Montserrat, sans-serif',
            fontWeight: 700,
            fontSize: '48px',
            color: '#2DE4E6',
            marginBottom: '12px'
          }}>
            120+
          </div>
          <p style={{
            fontFamily: 'Lato, sans-serif',
            fontSize: '16px',
            color: '#434343',
            margin: 0
          }}>
            Active Customers
          </p>
        </div>
        
        {/* Card 3 */}
        <div style={{
          flex: 1,
          backgroundColor: '#F7F7FF',
          padding: '32px',
          borderRadius: '12px',
          textAlign: 'center'
        }}>
          <div style={{
            display: 'flex',
            justifyContent: 'center',
            marginBottom: '20px'
          }}>
            <Trophy size={80} strokeWidth={2} color="#000FC4" />
          </div>
          <div style={{
            fontFamily: 'Montserrat, sans-serif',
            fontWeight: 700,
            fontSize: '48px',
            color: '#2DE4E6',
            marginBottom: '12px'
          }}>
            95%
          </div>
          <p style={{
            fontFamily: 'Lato, sans-serif',
            fontSize: '16px',
            color: '#434343',
            margin: 0
          }}>
            Retention Rate
          </p>
        </div>
      </div>
    </div>
  );
}
```

Does this design work for you? I can adjust colors, sizing, or layout before converting to HubSpot.

---

## Example 2: Three-Column Infographic

### User Request
"Create a three-column infographic about 'Three Forces Reshaping RevOps'"

### Claude Response

I'll create a TSX artifact for your three-column infographic:

```tsx
// Graphic 1: Three Forces Infographic
// Placement: After introduction section
// Dimensions: 800px × 900px

import { Database, RotateCw, Gauge, Zap } from 'lucide-react';

export default function ThreeForcesInfographic() {
  return (
    <div style={{
      width: '800px',
      height: '900px',
      backgroundColor: '#FFFFFF',
      position: 'relative',
      fontFamily: 'Lato, sans-serif'
    }}>
      {/* Header Section */}
      <div style={{ padding: '48px 40px', textAlign: 'center' }}>
        <p style={{
          fontFamily: 'Lato, sans-serif',
          fontWeight: 700,
          fontSize: '13px',
          color: '#000FC4',
          letterSpacing: '1.5px',
          textTransform: 'uppercase',
          marginBottom: '20px'
        }}>
          THE FUTURE OF B2B
        </p>
        
        <h1 style={{
          fontFamily: 'Montserrat, sans-serif',
          fontWeight: 700,
          fontSize: '42px',
          color: '#222222',
          lineHeight: '1.15',
          letterSpacing: '-1.5px',
          margin: 0
        }}>
          3 Forces Reshaping Revenue Operations
        </h1>
      </div>
      
      {/* Three Columns */}
      <div style={{
        display: 'flex',
        gap: '4px',
        padding: '0 32px 24px'
      }}>
        {/* Force 1 */}
        <div style={{
          width: '256px',
          minHeight: '480px',
          backgroundColor: '#ECF1FB',
          padding: '28px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between'
        }}>
          <div>
            {/* Icon */}
            <div style={{
              width: '56px',
              height: '56px',
              backgroundColor: '#000FC4',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '20px',
              position: 'relative'
            }}>
              <Database size={32} strokeWidth={2.5} color="#EEF0FB" />
              <div style={{
                position: 'absolute',
                top: '-4px',
                right: '-4px',
                width: '8px',
                height: '8px',
                borderRadius: '50%',
                backgroundColor: '#2DE4E6'
              }} />
            </div>
            
            <h2 style={{
              fontFamily: 'Montserrat, sans-serif',
              fontWeight: 700,
              fontSize: '22px',
              color: '#222222',
              lineHeight: '1.3',
              marginBottom: '8px'
            }}>
              Data Explosion
            </h2>
            
            <p style={{
              fontFamily: 'Lato, sans-serif',
              fontWeight: 700,
              fontSize: '15px',
              color: '#000FC4',
              marginBottom: '20px'
            }}>
              Demands AI Intelligence
            </p>
            
            <p style={{
              fontFamily: 'Lato, sans-serif',
              fontSize: '15px',
              color: '#222222',
              lineHeight: '1.6'
            }}>
              Teams generate 400M terabytes daily. Yet companies analyze only 12% of available data.
            </p>
          </div>
          
          {/* Stats */}
          <div>
            <div style={{
              width: '70px',
              height: '70px',
              borderRadius: '50%',
              backgroundColor: '#2DE4E6',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 4px 12px rgba(45, 228, 230, 0.25)',
              marginBottom: '8px'
            }}>
              <span style={{
                fontFamily: 'Montserrat, sans-serif',
                fontWeight: 700,
                fontSize: '30px',
                color: '#FFFFFF'
              }}>
                12%
              </span>
            </div>
            <p style={{
              fontFamily: 'Lato, sans-serif',
              fontSize: '13px',
              color: '#434343',
              marginBottom: '12px'
            }}>
              of data analyzed
            </p>
          </div>
        </div>
        
        {/* Force 2 - Similar structure */}
        <div style={{
          width: '256px',
          minHeight: '480px',
          backgroundColor: '#F2F6FC',
          padding: '28px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between'
        }}>
          {/* Content similar to Force 1 */}
        </div>
        
        {/* Force 3 - Similar structure */}
        <div style={{
          width: '256px',
          minHeight: '480px',
          backgroundColor: '#ECF1FB',
          padding: '28px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between'
        }}>
          {/* Content similar to Force 1 */}
        </div>
      </div>
      
      {/* Footer CTA */}
      <div style={{
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        height: '100px',
        background: 'linear-gradient(135deg, #000FC4 0%, #333FD0 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '16px'
      }}>
        <Zap size={36} color="#2DE4E6" fill="#2DE4E6" strokeWidth={2} />
        <p style={{
          fontFamily: 'Montserrat, sans-serif',
          fontWeight: 700,
          fontSize: '26px',
          color: '#FFFFFF',
          lineHeight: '1.2',
          margin: 0
        }}>
          HubSpot's Data Hub + Breeze Agents = Transformation
        </p>
      </div>
    </div>
  );
}
```

This shows your three-column design with icons, stats, and footer CTA. Review and let me know if you'd like any adjustments before I convert to HubSpot.

---

## Example 3: Multiple Graphics Workflow

### User Request
"Create 3 graphics for this blog post about AI adoption"

### Claude Response (Graphic 1)

I'll create 3 graphics for your article. Let's start with Graphic 1:

```tsx
// Graphic 1 of 3: AI Adoption Statistics
// Placement: After introduction, before "The Challenge" section
// Dimensions: 800px × 600px

import { TrendingUp, Users, Target } from 'lucide-react';

export default function AIAdoptionStats() {
  return (
    <div style={{
      width: '800px',
      padding: '48px 40px',
      backgroundColor: '#F7F7FF',
      fontFamily: 'Lato, sans-serif'
    }}>
      <h2 style={{
        fontFamily: 'Montserrat, sans-serif',
        fontWeight: 700,
        fontSize: '36px',
        color: '#000FC4',
        textAlign: 'center',
        marginBottom: '48px'
      }}>
        AI Adoption in 2024
      </h2>
      
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 1fr)',
        gap: '40px'
      }}>
        <div style={{ textAlign: 'center' }}>
          <TrendingUp size={64} strokeWidth={2} color="#2DE4E6" style={{ margin: '0 auto 16px' }} />
          <div style={{
            fontFamily: 'Montserrat, sans-serif',
            fontWeight: 700,
            fontSize: '48px',
            color: '#000FC4',
            marginBottom: '8px'
          }}>
            67%
          </div>
          <p style={{
            fontSize: '16px',
            color: '#434343',
            margin: 0
          }}>
            Increase in AI budgets
          </p>
        </div>
        
        {/* More metric cards... */}
      </div>
    </div>
  );
}
```

**Graphic 1 ready for review.** Does this look good? Reply "next" for Graphic 2, or let me know if you'd like changes.

---

### Claude Response (After User Says "Next")

Creating Graphic 2:

```tsx
// Graphic 2 of 3: Implementation Timeline
// Placement: Section "How to Get Started"
// Dimensions: 800px × 500px

import { Search, Settings, Rocket } from 'lucide-react';

export default function ImplementationTimeline() {
  return (
    <div style={{
      width: '800px',
      padding: '40px',
      backgroundColor: '#FFFFFF',
      fontFamily: 'Lato, sans-serif'
    }}>
      {/* Timeline content */}
    </div>
  );
}
```

**Graphic 2 ready.** Reply "next" for the final graphic.

---

### Claude Response (After User Says "Next")

Creating Graphic 3 (final):

```tsx
// Graphic 3 of 3: ROI Calculator
// Placement: Before conclusion section
// Dimensions: 800px × 400px

import { DollarSign, TrendingUp, CheckCircle } from 'lucide-react';

export default function ROICalculator() {
  return (
    <div style={{
      width: '800px',
      padding: '40px',
      backgroundColor: '#ECF1FB',
      fontFamily: 'Lato, sans-serif'
    }}>
      {/* ROI content */}
    </div>
  );
}
```

**All 3 graphics created!** Review all three and let me know:
- "Convert all to HubSpot" - I'll create all module files
- "Change graphic [number]" - I'll update that one
- Any other adjustments needed

---

## Example 4: Batch Conversion

### User Request (After Reviewing All Graphics)
"Convert all 3 to HubSpot modules"

### Claude Response

## HubSpot Modules (3 Graphics)

### Graphic 1: AI Adoption Statistics

#### ai-adoption-stats.html
```html
<!-- Clean HTML code -->
```

#### ai-adoption-stats.css
```css
/* Organized CSS */
```

---

### Graphic 2: Implementation Timeline

#### implementation-timeline.html
```html
<!-- Clean HTML code -->
```

#### implementation-timeline.css
```css
/* Organized CSS */
```

---

### Graphic 3: ROI Calculator

#### roi-calculator.html
```html
<!-- Clean HTML code -->
```

#### roi-calculator.css
```css
/* Organized CSS */
```

---

**All 3 modules ready!** Copy each set of files into HubSpot Design Manager as separate custom modules.

---

## Key Patterns

### Always Include in TSX Artifacts

1. **Header comment** with graphic number, placement, dimensions
2. **lucide-react imports** for all icons used
3. **export default function** with descriptive name
4. **Inline styles** using style objects
5. **Brand colors** as hex codes (#000FC4, #2DE4E6)
6. **Proper typography** (Montserrat/Lato with weights)

### Always Ask After TSX Artifact

- "Does this look good?"
- "Would you like any changes?"
- "Ready to convert to HubSpot?"

### For Multiple Graphics

- Number clearly: "Graphic 1 of 3"
- Show placement for each
- Create one at a time
- Get approval before next
- Batch convert at end

## Common Mistakes to Avoid

❌ **Don't skip TSX artifact** - Always show preview first
❌ **Don't use className without Tailwind** - Use inline styles
❌ **Don't forget imports** - Include all lucide-react icons
❌ **Don't use wrong colors** - Stick to brand palette
❌ **Don't convert before approval** - Wait for user confirmation
