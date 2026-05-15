# Blog Graphics Artifact Generator v2.0

Generate production-quality blog graphics with instant preview and HubSpot-ready code.

## What This Skill Does

Creates professional blog graphics through a **two-phase workflow**:

1. **Generate TSX Artifact** → See your graphic immediately as a React component
2. **Export HubSpot Module** → Get clean HTML/CSS/JS files ready to deploy

**The magic:** You see exactly what you're getting before deployment, and the code is production-ready.

## Key Features

✅ **Instant Preview** - TSX artifacts render immediately  
✅ **Real Examples** - 3 production graphics included (68KB of working code)  
✅ **Brand Compliant** - Auto-applies MAN Digital guidelines  
✅ **Zero Dependencies** - Inline SVG, no external files  
✅ **Responsive Design** - Mobile-first, tested 320-1280px  
✅ **Clean Code** - Well-organized, commented, maintainable  
✅ **Content Analysis** - Script identifies where graphics help  

## What's Included

### 📄 Core Skill (SKILL.md)
- Two-phase workflow (TSX → HubSpot)
- 5 graphic type templates
- Conversion guidelines
- Best practices
- Troubleshooting

### 📚 Reference Files
1. **graphic-patterns.md** (14KB) - Complete pattern documentation
   - All 5 graphic types in detail
   - Design specifications
   - When to use each pattern
   - Responsive behavior
   - Accessibility guidelines

2. **brand-guidelines.md** (23KB) - MAN Digital complete specs
   - Color palette with hex codes
   - Typography rules
   - Icon usage guidelines
   - Spacing system

3. **tailwind-conversion.md** (4KB) - Quick CSS reference
   - Common Tailwind → CSS conversions
   - Responsive breakpoints
   - Conversion examples

### 🎨 Production Examples (assets/examples/)
1. **three-column-infographic.tsx** (18KB)
   - Three equal columns with stats
   - Icon badges, decorative elements
   - Footer CTA with gradient
   - Perfect for "3 forces" style content

2. **timeline-90day.tsx** (43KB)
   - Detailed 90-day execution plan
   - Horizontal progress bar with phases
   - Multiple detailed sections
   - Activity cards with icons

3. **maturity-model.tsx** (7KB)
   - 5-level vertical progression
   - Colored badges per level
   - Blue background with decorations
   - Clean, scannable design

### 🔧 Scripts
**analyze_content.py** (7KB) - Content analysis tool
- Finds statistics → suggests data viz
- Detects processes → suggests timelines
- Spots comparisons → suggests tables
- Identifies lists → suggests grids

## Installation

1. Extract the zip file
2. Upload to Claude as a user skill
3. Start using immediately

## Usage Examples

### Example 1: Quick Metric Cards

```
You: "Create 3 metric cards showing:
      - 85% accuracy
      - 120+ customers  
      - 95% retention"

Claude: [Generates TSX artifact - you see it rendered]
        "Does this design work for you?"

You: "Perfect! Give me the HubSpot code"

Claude: [Outputs module.html and module.css]
```

### Example 2: Three-Column Infographic

```
You: "Create a three-column infographic about 
      'Three Forces Reshaping Revenue Operations'"

Claude: [Reads graphic-patterns.md reference]
        [Generates TSX artifact with three columns]
        "Here's your three-column graphic. Each column has
         an icon, title, description, and stats. Review?"

You: "Looks great!"

Claude: [Converts to HubSpot module files]
```

### Example 3: Timeline with Analysis

```
You: "Analyze this blog post and create a timeline"
     [pastes 2000-word post about project phases]

Claude: [Runs analyze_content.py]
        "I identified 4 project phases in the content.
         Creating a horizontal timeline..."
        [Generates TSX artifact]

You: "Perfect. Export to HubSpot"

Claude: [Outputs complete module files]
```

### Example 4: From Existing Design

```
You: "Convert this v0.dev component to HubSpot"
     [pastes React code]

Claude: [Analyzes code structure]
        [Generates TSX artifact for preview]
        "I've recreated this as an artifact. 
         Want me to convert to HubSpot modules?"

You: "Yes"

Claude: [Outputs HubSpot HTML/CSS/JS]
```

## Graphic Types

### 1. Three-Column Infographic (800×900px)
**Best for:** 3 related concepts, forces, pillars  
**Pattern:** Eyebrow → Title → 3 Columns → Footer CTA  
**Example:** `three-column-infographic.tsx`

### 2. Horizontal Timeline (800×1200+px)
**Best for:** Project phases, roadmaps, implementation  
**Pattern:** Header → Progress Bar → Detailed Phases  
**Example:** `timeline-90day.tsx`

### 3. Vertical Maturity Model (1200×variable)
**Best for:** Progression levels, maturity stages  
**Pattern:** Header → Level 1 → Level 2 → Level 3...  
**Example:** `maturity-model.tsx`

### 4. Data Visualization Grid (800-1200×flexible)
**Best for:** Multiple metrics, KPIs, dashboard view  
**Pattern:** Title → Grid of Metric Cards

### 5. Process Flow (800-1200×400-600px)
**Best for:** Step-by-step workflows, sequences  
**Pattern:** Title → Step 1 → Step 2 → Step 3...

## The Two-Phase Workflow

### Phase 1: TSX Artifact Generation

**What happens:**
1. Claude reads your request
2. Loads relevant patterns (if needed)
3. Creates TSX component
4. Outputs as artifact (you see it rendered)
5. Waits for your feedback

**Why TSX first:**
- Instant visual preview
- Easy to iterate and refine
- Uses familiar React patterns
- lucide-react icons (not inline yet)
- Tailwind utilities (not converted yet)

### Phase 2: HubSpot Module Export

**What happens:**
1. Converts TSX → HTML
2. lucide-react → inline SVG
3. Tailwind → standard CSS
4. React hooks → vanilla JS (if needed)
5. Outputs 2-3 files ready for HubSpot

**Why separate phase:**
- Cleaner workflow
- User approves design first
- HubSpot code is optimized
- No unnecessary iterations

## Brand Guidelines (Auto-Applied)

**Colors:**
- Primary: #000FC4 (Blue)
- Accent: #2DE4E6 (Cyan)
- CTA: #F26419 (Orange)
- Neutrals: #222222, #434343, #999999, #FFFFFF

**Typography:**
- Headers: Montserrat Bold
- Body: Lato Regular
- Stats: Montserrat Bold (large)

**Icons:**
- Library: lucide-react → inline SVG
- Style: Outline, 2px stroke
- Colors: Brand palette

## File Structure

```
blog-graphics-artifact-generator/
├── SKILL.md                           # Main skill instructions
├── README.md                          # This file
├── references/
│   ├── graphic-patterns.md            # Complete pattern docs (14KB)
│   ├── brand-guidelines.md            # MAN Digital specs (23KB)
│   └── tailwind-conversion.md         # CSS reference (4KB)
├── scripts/
│   └── analyze_content.py             # Content analyzer (7KB)
└── assets/
    └── examples/
        ├── three-column-infographic/
        │   └── three-column-infographic.tsx (18KB)
        ├── timeline-90day/
        │   └── timeline-90day.tsx (43KB)
        └── maturity-model/
            └── maturity-model.tsx (7KB)
```

## Quick Commands

### Analyze Blog Content
```bash
python scripts/analyze_content.py blog-post.md
```

### Request Specific Graphic
```
"Create a [type] showing [data/concept]"
```

### Get HubSpot Code
```
"Convert this to HubSpot module"
or
"Give me the HubSpot files"
```

## Tips for Best Results

1. **Be specific** - Include actual numbers, labels, content
2. **Review TSX first** - Give feedback before HubSpot conversion
3. **Use examples** - Reference production examples for inspiration
4. **Test responsive** - Ask about mobile behavior if unsure
5. **Iterate quickly** - TSX makes changes fast and visual

## Common Workflows

### Workflow A: From Scratch
```
Request → TSX Artifact → Review → Approve → HubSpot Module
```

### Workflow B: With Analysis
```
Blog Post → Analyze → Recommendations → Pick One → TSX → HubSpot
```

### Workflow C: From Design
```
Figma/v0 Design → TSX Preview → Adjust → HubSpot Module
```

## Troubleshooting

**TSX artifact not showing?**
→ Check React syntax errors
→ Verify lucide-react imports

**Colors look wrong?**
→ Verify hex codes: #000FC4, #2DE4E6, #F26419
→ Check brand-guidelines.md reference

**Layout breaks on mobile?**
→ Add responsive breakpoints
→ Test at 320px width

**HubSpot module not working?**
→ Ensure all SVG is inline
→ Check CSS class names (no conflicts)
→ Test in HubSpot preview mode

## What Makes This Special

### Combines Best of Both Worlds
- **Figma graphics generator**: Content analysis + design patterns
- **v0-to-HubSpot converter**: Clean code conversion
- **Plus TSX artifacts**: Visual preview before deployment

### Real Production Examples
Not just templates - actual graphics used in production:
- 68KB of working code
- Battle-tested patterns
- Real-world complexity

### Complete Workflow
Everything you need from idea → preview → deployment:
- Content analysis
- TSX generation
- Visual preview
- HubSpot conversion
- Brand compliance

## Technical Specifications

**TSX Artifacts:**
- React 18+
- lucide-react icons
- Tailwind CSS utilities
- TypeScript syntax
- Self-contained components

**HubSpot Output:**
- Semantic HTML5
- Standard CSS3
- Vanilla JavaScript ES6+
- Inline SVG (no dependencies)
- Responsive (320-1280px)

**Browser Support:**
- Chrome/Edge (latest 2)
- Firefox (latest 2)
- Safari (latest 2)
- Mobile browsers

## Version History

**v2.0.0 (Current)**
- Added real production examples (68KB)
- Enhanced pattern documentation
- Two-phase workflow (TSX first)
- Complete reference files
- Content analysis script

**v1.0.0**
- Initial release
- Basic workflow
- Brand guidelines

## Support

**Need help?**
1. Check SKILL.md for workflow guidance
2. Review graphic-patterns.md for design specs
3. Study examples in assets/examples/
4. Run analyze_content.py for content analysis
5. Reference brand-guidelines.md for brand questions

**Common Questions:**
- "How do I...?" → Check SKILL.md workflow section
- "What colors...?" → See brand-guidelines.md
- "Which graphic type...?" → Review graphic-patterns.md
- "Where in my post...?" → Run analyze_content.py

## Next Steps

1. **Install the skill** - Upload zip to Claude
2. **Try a simple request** - "Create 3 metric cards with made-up stats"
3. **Review the artifact** - See instant preview
4. **Get HubSpot code** - "Export to HubSpot"
5. **Deploy to blog** - Paste code into HubSpot Design Manager

---

**Ready to create amazing blog graphics?** Just tell Claude what you need!

**Example starter prompts:**
- "Create a three-column infographic about [topic]"
- "Analyze this blog post for graphic opportunities"
- "Show me examples of timeline graphics"
- "Create metric cards showing [your stats]"

**License:** Internal use (MAN Digital)  
**Version:** 2.0.0  
**Last Updated:** November 2024
