# Blog Graphics Patterns Reference

Detailed patterns and examples for common blog graphic types based on production graphics.

## Pattern 1: Three-Column Infographic

**Use When:** Presenting 3 related concepts, forces, pillars, or comparison points

**Structure:**
```
Header (eyebrow + title)
  ↓
Three equal-width columns
  ↓
Footer CTA
```

**Key Elements:**
1. **Eyebrow text** - Small uppercase label (Lato Bold 700, 13px, #000FC4, 1.5px letter-spacing)
2. **Main title** - Bold statement (Montserrat Bold 700, 42px, #222222, -1.5px letter-spacing)
3. **Column structure** (256px width each, min-height 480px)
   - Icon container (56px × 56px, #000FC4 background)
   - Icon badge (small cyan dot in top-right corner)
   - Title (Montserrat Bold 700, 22px, #222222)
   - Subtitle (Lato Bold 700, 15px, #000FC4)
   - Description text (Lato Regular 400, 15px, #222222)
   - Primary stat circle (70px diameter, #2DE4E6, white text)
   - Secondary stats (small, below circle)

4. **Footer CTA** (100px height, gradient blue background)
   - Icon (Zap, filled cyan)
   - Statement text (Montserrat Bold 700, 26px, white)

5. **Decorative elements**
   - Dot patterns (top-right, bottom-left)
   - Accent lines (gradient vertical bars)
   - Small circles (scattered accent dots)

**Colors:**
- Column backgrounds: Alternating #ECF1FB and #F2F6FC
- Icons/structure: #000FC4 (primary blue)
- Stats/accents: #2DE4E6 (cyan)
- Text: #222222 (dark), #434343 (medium), #999999 (light)

**Dimensions:** 800px width × 900px height

**Example:** See `assets/examples/three-column-infographic/three-column-infographic.tsx`

---

## Pattern 2: Horizontal Timeline (90-Day Execution)

**Use When:** Showing sequential phases, project plans, implementation roadmaps

**Structure:**
```
Header (title + phase bubbles)
  ↓
Progress bar (gradient timeline)
  ↓
Detailed phase sections (vertical scroll)
  ↓
Bottom summary
```

**Key Elements:**
1. **Header section**
   - Main title (Montserrat Bold, clamp(20px, 4vw, 28px), #000FC4)
   - Subtitle/description (regular text, #434343)
   - Stat citation (italic, small, #999999)
   - Phase bubbles (right side) - small circles with icons and labels

2. **Progress bar** (32px height, gradient background)
   - Gradient: C8CCF2 → 96F2F3 → 2DE4E6 (left to right)
   - Day markers: Day 1, 30, 60, 90
   - Vertical dividers (dotted white lines at 33% and 66%)
   - Phase labels overlay

3. **Phase sections** (detailed breakdown)
   Each phase contains:
   - Phase header with number and title
   - Activities list (bullet points)
   - Key focus areas (with icons)
   - Success metrics
   - Common pitfalls (warning boxes)
   - Tools/resources needed

4. **Activity cards** (within each phase)
   - Icon (lucide-react, 20-24px)
   - Activity name (Montserrat Bold, 15-16px)
   - Description (Lato, 13-14px)
   - Timeline indicator (week numbers)
   - Responsible party label

**Colors:**
- Phase 1 gradient: #C8CCF2 (light purple)
- Phase 2 gradient: #96F2F3 (light cyan)
- Phase 3 gradient: #2DE4E6 (bright cyan)
- Accent elements: #000FC4 (primary blue)
- Warnings: #FFA500 or #FF6B35 (orange)
- Success: #10B981 (green)

**Dimensions:** 800px width × variable height (1200-2400px typical)

**Responsive:**
- Mobile: Single column, stacked sections
- Tablet: Adjusted spacing, compressed timeline
- Desktop: Full horizontal layout

**Example:** See `assets/examples/timeline-90day/timeline-90day.tsx`

---

## Pattern 3: Vertical Maturity/Level Model

**Use When:** Showing progression levels, maturity models, growth stages

**Structure:**
```
Header (title + subtitle)
  ↓
Level 1 card
  ↓
Level 2 card
  ↓
Level 3 card
  ↓
...
```

**Key Elements:**
1. **Container background**
   - Solid colored background (#000FC4 primary blue)
   - Decorative gradients (circular, low opacity)
   - Dot patterns (corners, subtle)

2. **Header** (centered, on blue background)
   - Main title (Montserrat Bold 700, 56px, white)
     - Can include italic emphasis (Montserrat Medium Italic)
   - Subtitle (Montserrat Medium 500, 24px, rgba(255,255,255,0.9))
   - Generous spacing (mb-16 / 64px)

3. **Level cards** (stacked vertically)
   Each card contains:
   - Card background: #F7F7FF (off-white)
   - Padding: 32px all sides
   - Flex layout (horizontal: icon + content)
   
   **Icon section:**
   - Square container: 72px × 72px
   - Background: #000FC4
   - Icon: 40px, white, stroke-width 2
   
   **Content section:**
   - Level badge (colored pill, uppercase)
   - Level number + title (Montserrat Bold 700, 28px, #000FC4)
   - Bullet list (3-4 items, Lato Regular, 16px, #222222)
   - Target metric (italic, #434343, bottom)

4. **Badge colors** (by level)
   - Foundation: #FF6B35 (orange)
   - Visibility: #2DE4E6 (cyan)
   - Automation: #8B5CF6 (purple)
   - Prediction: #10B981 (green)
   - Autonomous: #EC4899 (pink)

**Colors:**
- Background: #000FC4 (primary blue)
- Card background: #F7F7FF (off-white)
- Text on blue: white / rgba(255,255,255,0.9)
- Text on white: #000FC4 (headers), #222222 (body), #434343 (light)
- Badges: varied per level (see above)

**Dimensions:** 1200px width × variable height (fits 5 levels comfortably)

**Spacing:**
- Between levels: 32px gap
- Internal card padding: 32px
- Header margin: 64px bottom

**Example:** See `assets/examples/maturity-model/maturity-model.tsx`

---

## Pattern 4: Data Visualization Grid

**Use When:** Showcasing multiple metrics, KPIs, or statistics

**Structure:**
```
Header/Title
  ↓
Grid of metric cards (2×2, 3×3, or flexible)
  ↓
Optional footer
```

**Key Elements:**
1. **Grid container**
   - CSS Grid or Flexbox
   - Responsive: 1 column mobile, 2-3 columns desktop
   - Equal card heights within rows
   - Gap: 24-32px

2. **Metric card** (individual)
   - Background: #F7F7FF or white
   - Border-radius: 12px
   - Padding: 24-32px
   - Center-aligned content
   
   **Card contents:**
   - Icon (top, 80-100px, #000FC4 or #2DE4E6)
   - Large number (Montserrat Bold 700, 48-56px, #2DE4E6)
   - Label (Lato Regular, 16-18px, #434343)
   - Optional sub-stat or trend indicator

3. **Visual hierarchy**
   - Largest: The number/metric
   - Medium: Icon
   - Smallest: Label text

**Colors:**
- Card background: #F7F7FF (light) or white
- Primary metrics: #2DE4E6 (cyan) - most prominent
- Secondary metrics: #000FC4 (blue)
- Labels: #434343 (gray)

**Dimensions:** Flexible, typically 800-1200px container width

---

## Pattern 5: Process Flow Diagram

**Use When:** Explaining step-by-step processes, workflows, or sequences

**Structure:**
```
Title
  ↓
Step 1 → Step 2 → Step 3 → Step 4
  ↓
Optional sub-steps or details
```

**Key Elements:**
1. **Step containers**
   - Box/card format (rounded corners)
   - Equal widths or sizes
   - Connected by arrows
   
2. **Each step includes:**
   - Step number (small badge or label)
   - Icon (24-32px, centered)
   - Step title (Montserrat Bold, 18-22px)
   - Brief description (Lato, 14-16px)
   - Optional duration/timeline

3. **Connector arrows**
   - Style: Simple right-pointing arrow (→)
   - Size: 40-60px length, 2-4px thick
   - Color: #C8CCF2 (light blue/gray)
   - Can be animated (optional)

**Layout Options:**
- Horizontal: Best for 3-5 steps
- Vertical: Best for 6+ steps or mobile
- Hybrid: Horizontal on desktop, vertical on mobile

**Colors:**
- Step backgrounds: #F7F7FF or white
- Step numbers: #2DE4E6 (cyan circles)
- Icons: #000FC4 (primary blue)
- Arrows: #C8CCF2 (neutral)
- Text: #222222 (dark), #434343 (medium)

---

## Common Design Elements

### Icons
**Source:** lucide-react library  
**Sizes:** 24px (small), 32px (medium), 40px (large), 56-80px (hero)  
**Style:** Outline, 2px stroke weight  
**Colors:** #000FC4 (primary), #2DE4E6 (accent), white (on dark backgrounds)

**Commonly used:**
- Database, Server, Cloud (data/infrastructure)
- Users, UserCheck, UserPlus (people/teams)
- TrendingUp, BarChart3, LineChart (metrics/growth)
- Bot, BrainCircuit, Cpu (AI/automation)
- Rocket, Target, Trophy (goals/achievement)
- Settings, RefreshCw, RotateCw (configuration/process)
- CheckCircle, XCircle, AlertTriangle (status)
- Calendar, Clock, Zap (time/speed)

### Typography Scale
**Headers:**
- H1: Montserrat Bold 700, 42-56px, #000FC4 or #222222
- H2: Montserrat Bold 700, 28-32px, #000FC4 or #222222  
- H3: Montserrat Bold 700, 22-24px, #000FC4 or #222222
- H4: Montserrat Bold 700, 18-20px, #000FC4 or #222222

**Body:**
- Large: Lato Regular 400, 18-20px, #222222
- Normal: Lato Regular 400, 15-16px, #222222
- Small: Lato Regular 400, 13-14px, #434343
- Tiny: Lato Regular 400, 11-12px, #999999

**Special:**
- Stat numbers: Montserrat Bold 700, 30-56px, #2DE4E6
- Labels: Lato Bold 700, 13-15px, #000FC4
- Eyebrow text: Lato Bold 700, 11-13px, #000FC4, uppercase, 1.5px letter-spacing

### Spacing System
- Micro: 4px
- Small: 8px
- Medium: 16px
- Large: 24px
- XL: 32px
- XXL: 40-48px
- Section: 64px+

### Border Radius
- Small: 4px
- Medium: 8px
- Large: 12px
- XL: 16px
- Circle: 50% / 9999px

### Box Shadows
- Subtle: `0 1px 3px rgba(0, 0, 0, 0.1)`
- Medium: `0 4px 6px rgba(0, 0, 0, 0.1)`
- Prominent: `0 10px 15px rgba(0, 0, 0, 0.1)`
- Colored (cyan): `0 4px 12px rgba(45, 228, 230, 0.25)`

---

## Responsive Breakpoints

```css
/* Mobile first approach */
@media (min-width: 640px)  { /* sm - Small tablets */ }
@media (min-width: 768px)  { /* md - Tablets */ }
@media (min-width: 1024px) { /* lg - Small desktops */ }
@media (min-width: 1280px) { /* xl - Large desktops */ }
```

**Common adjustments:**
- Mobile (< 640px):
  - Single column layouts
  - Smaller font sizes (75-85% of desktop)
  - Reduced padding (16-20px vs 32px)
  - Hidden decorative elements
  - Stacked instead of side-by-side

- Tablet (640-1024px):
  - 2-column layouts
  - Medium font sizes (90% of desktop)
  - Medium padding (24px)
  - Simplified decorations

- Desktop (1024px+):
  - Full multi-column layouts
  - Full font sizes
  - Full padding (32-40px)
  - All decorative elements

---

## Accessibility Guidelines

1. **Color Contrast:** Maintain minimum 4.5:1 ratio
   - #000FC4 on white: ✅ Pass
   - #2DE4E6 on white: ⚠️ Use for accents only, not body text
   - White on #000FC4: ✅ Pass

2. **Semantic HTML:** Use proper heading hierarchy (h1 → h2 → h3)

3. **Alt Text:** Describe informational icons (decorative icons can use aria-hidden)

4. **Keyboard Navigation:** Ensure tab order makes sense

5. **Screen Readers:** Use ARIA labels for stat numbers and metrics

---

## Performance Tips

1. **Inline SVG icons** - No external requests
2. **CSS Grid/Flexbox** - Modern, performant layouts
3. **Web fonts** - Preload Montserrat and Lato
4. **Optimize images** - Use WebP when possible
5. **Minimize DOM depth** - Keep nesting shallow
6. **Use CSS transforms** - For animations (better performance)

---

## Quick Reference: When to Use Each Pattern

| Content Type | Best Pattern | Dimensions |
|--------------|-------------|------------|
| 3 key points/forces | Three-Column Infographic | 800×900 |
| Project phases/timeline | Horizontal Timeline | 800×1200+ |
| Maturity levels | Vertical Level Model | 1200×variable |
| Multiple metrics | Data Visualization Grid | 800-1200×flexible |
| Step-by-step process | Process Flow Diagram | 800-1200×400-600 |

---

## File Organization Best Practices

When creating graphics:

1. **Keep components self-contained** - All styles inline or in component
2. **Use TypeScript** - Type-safe props and data structures
3. **Responsive by default** - Mobile-first approach
4. **Comment sections clearly** - Especially for complex layouts
5. **Export as default** - Standard pattern for single-graphic files
6. **Include prop types** - Even for simple components
