# MAN Digital Brand Guidelines Reference

**Extracted from Actual Figma Designs**  
Last Updated: November 7, 2025

This document contains real design patterns extracted from MAN Digital's production Figma files, including exact specifications for colors, typography, spacing, and component structures.

---

## Design Philosophy

**Core Principles:**
- **Bold Color Usage**: Primary blue (`#000FC4`) dominates key brand moments
- **Generous White Space**: 32px+ padding creates breathing room
- **Clear Visual Hierarchy**: Size, weight, and color create scannable content
- **Consistent Spacing**: Modular scale (16px, 24px, 32px, 40px, 64px, 96px)
- **Professional + Approachable**: Balance between corporate and modern SaaS

---

## Color System

### Primary Palette

```
PRIMARY BLUE (Brand Identity)
Hex: #000FC4
RGB: 0, 15, 196
Usage: Primary CTAs, headers, icons, brand moments
```

```
ACCENT CYAN (Energy & Innovation)
Hex: #2DE4E6
RGB: 45, 228, 230
Usage: Highlights, badges, secondary elements, data viz
```

```
BLACK (Text & Structure)
Hex: #000000
RGB: 0, 0, 0
Usage: Body text, headings, high-contrast elements
```

```
WHITE (Space & Clarity)
Hex: #FFFFFF
RGB: 255, 255, 255
Usage: Backgrounds, cards, negative space
```

### Secondary Palette

```
LIGHT GRAY/OFF-WHITE (Cards & Sections)
Hex: #F7F7FF
RGB: 247, 247, 255
Usage: Card backgrounds, alternating sections
```

```
DARK GRAY (Secondary Text)
Hex: #222222
RGB: 34, 34, 34
Usage: Body text, descriptions
```

```
MID GRAY (Tertiary Text)
Hex: #434343
RGB: 67, 67, 67
Usage: Supporting text, metadata
```

```
LIGHT BORDER
Hex: #E4E6F9
RGB: 228, 230, 249
Usage: Card borders, dividers
```

### Accent Colors (Badges & Status)

```
ORANGE (Foundation/CTA)
Hex: #FF6B35 or #F26419
RGB: 255, 107, 53 / 242, 100, 25
Usage: "FOUNDATION" badges, primary CTAs
```

```
VIOLET (Automation)
Hex: #8B5CF6 (violet-500)
RGB: 139, 92, 246
Usage: "AUTOMATION" badges
```

```
EMERALD (Prediction)
Hex: #10B981 (emerald-500)
RGB: 16, 185, 129
Usage: "PREDICTION" badges
```

```
PINK (Autonomous)
Hex: #EC4899 (pink-500)
RGB: 236, 72, 153
Usage: "AUTONOMOUS" badges
```

### Background Gradients

```
HERO GRADIENT
From: #000FC4 (primary blue)
To: Darker blue/navy
Opacity: Layered with 40% circular gradients
```

```
DOTTED PATTERN OVERLAY
Color: White dots
Opacity: 40%
Size: 75px × 150px pattern tile
```

### Color Usage Guidelines

**For Headers:**
```
H1 (Main Title): #000FC4 (Primary Blue)
H2 (Subheadlines): #000FC4 or #000000 depending on context
H3 (Subsection): #000FC4
Preheading: #000FC4 or #434343
```

**For Body Text:**
```
Primary text: #000000 (Black) or #222222 (Dark Gray)
Secondary text: #434343 (Mid Gray)
Tertiary text: #999999 (Light Gray)
```

**For Data Visualization:**
```
Primary data: #2DE4E6 (Accent Cyan)
Secondary data: #000FC4 (Primary Blue)
Tertiary data: #5963D9 (Light Blue variation)
Neutral data: #C8CCF2 (Supporting background)
```

**For Backgrounds:**
```
Main background: #FFFFFF (White)
Section background: #F7F7FF (Off-white)
Card/container background: #F7F7FF or #FFFFFF
```

**For Interactive Elements:**
```
Buttons/CTAs: #FF6B35 or #F26419 (Orange)
Hover states: #333FD0 (Blue variation)
Links: #000FC4 (Primary Blue)
```

---

## Typography System

### Font Families

**Primary (Headings & Emphasis):**
- Font: Montserrat
- Weights: Bold (700), Medium (500), Medium Italic (500 italic)
- Usage: All headings, titles, emphasized content

**Secondary (Body & UI):**
- Font: Lato
- Weights: Bold (700), Regular (400)
- Usage: Body text, descriptions, UI elements

### Type Scale

#### Display/Hero Headings
```
H1 - Hero Title
Font: Montserrat Bold
Size: 56px
Line Height: 70px
Color: White on dark backgrounds, #000FC4 on light
Usage: Hero sections, major page titles
```

#### Section Headings
```
H2 - Section Title
Font: Montserrat Bold  
Size: 28px
Line Height: 35px
Color: #000FC4 (primary), #000000 (secondary)
Usage: Card titles, section headings
```

```
H3 - Subsection Title
Font: Montserrat Bold
Size: 24px
Line Height: 29px
Color: #000FC4
Usage: Subsections, card categories
```

#### Body Text
```
Large Body
Font: Lato Regular
Size: 18px
Line Height: 29.25px
Color: #222222
Usage: Primary body content, list items
```

```
Medium Body
Font: Lato Regular
Size: 17px
Line Height: 25.5px
Color: #000FC4 (emphasis), #222222 (standard)
Usage: Targets, metrics, secondary content
```

```
Small Body
Font: Lato Regular
Size: 16px
Line Height: 24px
Color: #222222, #999999 (metadata)
Usage: Captions, metadata, fine print
```

#### Special Elements
```
Badge Text
Font: Lato Bold
Size: 11px
Line Height: 16.5px
Letter Spacing: 0.5px
Transform: UPPERCASE
Color: White
Usage: Status badges, category labels
```

```
Subtitle/Tagline
Font: Montserrat Medium
Size: 24px
Line Height: 36px
Color: rgba(255, 255, 255, 0.9)
Usage: Hero subtitles, taglines
```

#### Typography Usage Rules

1. **ONE H1 Rule:** Each graphic should have exactly ONE H1 element (the main title)
2. **Hierarchy Consistency:** Always follow the hierarchy - don't skip levels
3. **Font Family Mixing:** Never mix Montserrat and Lato within the same text block
4. **Line Height:** Body text should maintain appropriate line height for readability
5. **Letter Spacing:** Apply 0.5px letter spacing to badge text

---

## Spacing & Layout System

### Modular Spacing Scale

```
xs:   8px   - Tight internal spacing
sm:   16px  - Component internal padding
md:   24px  - Icon-to-content gaps, small sections
lg:   32px  - Card padding, section gaps
xl:   40px  - Major section gaps
2xl:  64px  - Large section margins
3xl:  96px  - Hero top margins
4xl:  120px - Maximum safe margins
```

### Container Patterns

#### Full-Width Container (Blog Infographic)
```
Width: 1200px
Side Margins: 64px (content width: 1072px)
Vertical Margins: 96px top, 96px bottom
```

#### Content Container (Website)
```
Width: 1346px - 1350px
Side Margins: 80px - 82px
Responsive: Centers on larger screens
```

#### Card Container
```
Width: 900px (infographic), 372px (services), 446px (testimonials)
Padding: 32px all sides
Gap between cards: 32px vertical
```

### Major Section Spacing
```
Between major sections: 40px minimum
Between content and header: 32px
Top/bottom margins: 60px for blog graphics
```

### Internal Element Spacing
```
Within sections: 20px
Between related items: 16px
Text line spacing: Defined in typography line-height
Icon to text: 12-16px
```

### Container Padding
```
Card/box internal padding: 24-32px
Button padding: 12px vertical, 24px horizontal
```

### Margins for Different Formats
```
Blog graphics: 60px left/right margins
Social posts: 40px margins (square), 60px (vertical)
Presentations: 80-120px safe zones
```

---

## Component Patterns

### Vertical Maturity Model Infographic

**Overall Structure:**
- **Dimensions:** 1200px × 1917.25px (vertical blog format)
- **Background:** `#000FC4` with decorative gradients
- **Container:** 1072px content width (64px side margins)

#### Header Section
```yaml
Layout:
  Height: 192px total (140px title + 36px subtitle + 16px gap)
  Alignment: Center

Title Structure:
  Part 1 (Italic):
    Font: Montserrat Medium Italic 56px
    Text: "AI-Enabled"
    Color: White
  
  Part 2 (Bold):
    Font: Montserrat Bold 56px
    Text: "RevOps"
    Line: Below part 1, centered
  
  Part 3 (Bold):
    Font: Montserrat Bold 56px
    Text: "Maturity Model"
    Line: Below part 2, centered

Subtitle:
  Font: Montserrat Medium 24px
  Color: rgba(255, 255, 255, 0.9)
  Text: "Your Path from Chaos to Predictable Revenue"
  Spacing: 16px gap from title
```

#### Decorative Elements
```yaml
Circular Gradients:
  - Opacity: 40%
  - Positions: Top-left (5.66% from top), Bottom-right (48.79% from bottom)
  - Size: Large, overlapping circles

Dot Patterns:
  - Size: 75px × 150px
  - Color: White
  - Opacity: 40%
  - Positions: Top-left corner (32px, 32px), Bottom-right (1018px, 1810.25px)
```

#### Level Card Pattern (Repeating 5x)

**Card Structure:**
```yaml
Dimensions:
  Width: 900px
  Height: 268.25px
  Background: #F7F7FF
  Padding: 32px
  Gap between cards: 32px

Layout (Horizontal Flex):
  - Icon Container: 72px × 72px (fixed)
  - Gap: 24px
  - Content: Flexible width (772px effective)

Icon Container:
  Background: #000FC4
  Size: 72px × 72px square
  Icon Size: 40px white icon, centered
  Style: Flex, centered alignment
```

**Content Structure:**
```yaml
Header Row:
  Level Heading:
    Font: Montserrat Bold 28px
    Color: #000FC4
    Line Height: 35px
    Examples: "Level 1: Organize & Integrate Data"
  
  Badge (right-aligned):
    Height: 28.5px
    Padding: 16px horizontal
    Border Radius: Very large (pill)
    Font: Lato Bold 11px, UPPERCASE, 0.5px letter-spacing
    Colors:
      - Level 1: #FF6B35 - "FOUNDATION"
      - Level 2: #2DE4E6 - "VISIBILITY"
      - Level 3: #8B5CF6 (violet) - "AUTOMATION"
      - Level 4: #10B981 (emerald) - "PREDICTION"
      - Level 5: #EC4899 (pink) - "AUTONOMOUS"

List Section (16px gap from header):
  Item Structure:
    - Icon: 20px checkmark, 2px from top
    - Text Left Margin: 32px from icon start
    - Vertical Gap: 12px between items
    - Font: Lato Regular 18px, #222222
    - Line Height: 29.25px
    - Count: 3 items standard

Target Metric (16px gap from list):
  Font: Lato Bold 17px
  Color: #000FC4
  Format: "Target: [metric]"
  Line Height: 25.5px
```

---

### Hero Sections

**Primary Hero Pattern:**
```yaml
Container:
  Height: 617px
  Background: #000FC4 with gradient overlay

Layout (Two Columns):
  Left Column (Content):
    Width: 536px
    Padding: 96px from top
    
    Title:
      Font: Montserrat Bold 76px
      Color: White
      Line Height: 91.2px
      Letter Spacing: -2px
      
    Subtitle:
      Font: Montserrat Medium 24px
      Color: rgba(255, 255, 255, 0.9)
      Line Height: 36px
      Margin: 24px from title
      
    CTA Button:
      Width: 260px
      Height: 61px
      Background: #FF6B35 or #F26419
      Border Radius: 4px
      Text: Lato Bold 16px, White
      Margin: 32px from subtitle

  Right Column (Visual):
    Width: 50% (flexible)
    Image or illustration
    Decorative elements (dots, gradients)

Decorative Elements:
  - Circular gradients (40% opacity)
  - Dot patterns (white, 40% opacity)
  - Abstract shapes (#2DE4E6)
```

---

### Service Cards

**Standard Service Card:**
```yaml
Dimensions:
  Width: 372px
  Height: 397px
  Background: White
  Border: 1px solid #E4E6F9
  Border Radius: 12px

Content Structure:
  Padding: 32px all sides
  
  Icon Container:
    Size: 56px × 56px
    Background: #F7F7FF
    Border: 2px solid #000FC4
    Border Radius: 8px
    Icon: 40px centered, #000FC4
  
  Title (32px gap from icon):
    Font: Montserrat Bold 24px
    Color: #000000
    Line Height: 29px
  
  Description (16px gap from title):
    Font: Lato Regular 18px
    Color: #434343
    Line Height: 27px
    Max Height: 90px
  
  CTA Link (at bottom):
    Font: Lato Bold 16px
    Color: #000FC4
    Format: "Get started on [Service] →"
```

**Three-Column Layout:**
```yaml
Grid:
  Columns: 3
  Gap: 32px between cards
  Container: 1200px width
  Card Width: 372px each
```

---

### Testimonial Cards

#### Full-Width Video Testimonial

**Layout:**
```yaml
Container: 1350px width
Left Section (Video):
  Width: 912px
  Height: 609px
  Background: Video thumbnail
  Play Button:
    Size: 162px × 51px
    Background: White/translucent
    Icon: Play triangle (21px)
    Text: "Play Video" - Lato Bold 18px
    Position: Centered

Right Section (Content):
  Width: 438px
  Padding: 40px
  
  Logo: Company logo (153px × 46px)
  Gap: 24px
  Quote: Lato Regular 21px, #000000
    Line Height: 36px
  Gap: Auto
  Avatar: 60px circle
  Name: Lato Bold 18px, #000000
  Title: Lato Regular 14px, #666666
    Max 2 lines
```

#### Text Testimonial Card (2-column grid)

**Card Structure:**
```yaml
Dimensions:
  Width: 550px
  Height: 316px (or 328px for longer content)
  Background: White
  Border: 1px solid #E4E6F9
  Border Radius: 8px

Content Padding: 24px

Logo Section:
  Height: 44px (or 56px)
  Company Logo: Variable width, 20-32px height

Quote Section:
  Margin Top: 60px from top (includes logo + gap)
  Font: Lato Regular 16px
  Color: #000000
  Line Height: 24px
  Max Height: 120px

Reviewer Section:
  Margin Top: 228px from top (or 240px)
  Avatar: 48px circle
  Gap: 12px (60px from card edge)
  Name: Lato Bold 16px, #000000
  Title: Lato Regular 14px, #666666
```

---

### Badge System

#### Pill Badges (Status/Category)

**Foundation Badge:**
```yaml
Background: #FF6B35
Text: "FOUNDATION"
Height: 28.5px
Padding: 16px horizontal
Border Radius: 999px (pill)
Font: Lato Bold 11px
Letter Spacing: 0.5px
Color: White
Transform: UPPERCASE
```

**Visibility Badge:**
```yaml
Background: #2DE4E6
Text: "VISIBILITY"
[Same styling as Foundation]
```

**Automation Badge:**
```yaml
Background: #8B5CF6
Text: "AUTOMATION"
[Same styling as Foundation]
```

**Prediction Badge:**
```yaml
Background: #10B981
Text: "PREDICTION"
[Same styling as Foundation]
```

**Autonomous Badge:**
```yaml
Background: #EC4899
Text: "AUTONOMOUS"
[Same styling as Foundation]
```

---

## Icon System

### Icon Specifications

**Standard Sizes:**
```
Small Icons: 20px
Medium Icons: 32-40px
Large Icons: 56px
Hero Icons: 72px
```

**Icon Style:**
- Style: Outline/Line icons
- Stroke Weight: 2px standard
- Color: Matches context (#000FC4 primary, White on dark)
- Library: Mix of custom and lucide-react compatible

**Icon Containers:**
```yaml
Small Container:
  Size: 20px × 20px
  No background

Medium Container:
  Size: 56px × 56px
  Background: #F7F7FF or #000FC4
  Border: 2px solid (optional)
  Border Radius: 8px
  Icon: 32-40px centered

Large Container:
  Size: 72px × 72px
  Background: #000FC4
  Icon: 40px white, centered
```

---

## Background Patterns

### Gradient Overlays

**Hero Gradient:**
```yaml
Type: Linear gradient
Colors:
  Start: #000FC4
  End: Navy/Dark Blue
Opacity: 100% base
Overlay: Circular gradients at 40% opacity
```

**Circular Accent Gradients:**
```yaml
Type: Radial gradient
Size: 982px diameter (outer), 766px (middle), 533px (inner)
Colors: Lighter blues/whites
Opacity: 10-30%
Blend Mode: Overlay/Soft Light
```

### Dotted Patterns

**Small Dot Pattern:**
```yaml
Tile Size: 75px × 150px
Dot Size: 3-4px
Color: White
Opacity: 40%
Pattern: Regular grid
Usage: Corner accents, subtle texture
```

**Large Dot Pattern:**
```yaml
Tile Size: 222.46px × 108.67px
Dot Size: 5-6px
Color: White or #000FC4
Opacity: 20-40%
Pattern: More spaced grid
Usage: Section backgrounds, large areas
```

### Wave Patterns

**Bottom Wave (Section Divider):**
```yaml
Type: SVG wave vector
Height: 100-200px
Colors: Gradient from section color to next
Usage: Smooth transitions between sections
Position: Bottom of colored sections
```

---

## Usage Guidelines

### When to Use Each Pattern

**Vertical Maturity Model:**
- Multi-level progression content (3-7 levels)
- Step-by-step processes
- Feature comparison ladders
- Skill/certification tiers
- Blog post infographics

**Hero Sections:**
- Homepage
- Landing pages
- Major product launches
- Campaign pages

**Service Cards:**
- Service offerings (3-6 items)
- Product features
- Use cases
- Team capabilities

**Testimonial Cards:**
- Social proof sections
- Case study highlights
- Customer success stories
- Review displays

### Responsive Considerations

**Vertical Infographic:**
- Desktop: 1200px width
- Tablet: Scale to 768px width, maintain aspect ratio
- Mobile: Stack cards vertically, scale to screen width

**Hero Section:**
- Desktop: 1440px+ width
- Tablet: Stack columns vertically
- Mobile: Single column, reduce hero height

**Service Cards:**
- Desktop: 3 columns
- Tablet: 2 columns
- Mobile: 1 column, full width

---

## Layout Principles

### Grid System
- Use 12-column grid for complex layouts
- 8px base grid system for alignment
- Maintain consistent column widths within sections

### Visual Hierarchy
1. **Primary focus:** H1 title + hero element
2. **Secondary focus:** Main content sections (H2 headers + content)
3. **Tertiary focus:** Supporting elements (captions, metadata)

### White Space Usage
- Minimum 60% white space for professional aesthetic
- Generous spacing creates breathing room
- Don't crowd elements together

---

## Brand Voice & Aesthetic

### Visual Style
- **Professional but approachable:** Clean design with personality
- **Data-focused:** Information hierarchy is paramount
- **Modern B2B:** Contemporary without being trendy
- **Trustworthy:** Conservative color use, strong hierarchy

### Design Philosophy
- **Clarity over creativity:** Function before form
- **Consistency:** Repeatable patterns and structures
- **Scalability:** Works at all sizes and contexts
- **Accessibility:** WCAG AA compliance minimum

---

## Accessibility Requirements

### Color Contrast
- Text on white: Minimum 4.5:1 ratio (AA standard)
- Large text: Minimum 3:1 ratio
- Test all color combinations before finalizing

### Readability
- Minimum body text: 16px (prefer 18-20px)
- Minimum line height: 150%
- Maximum line length: 80 characters for body text

### Visual Elements
- Icons should have text labels or alt descriptions
- Charts must have data labels, not just colors
- Important info should not rely on color alone

---

## Common Patterns Reference

### Hero Section Pattern
```
Background: #FFFFFF or #F7F7FF
Title: Montserrat Bold 56-76px, #000FC4
Subtitle: Montserrat Bold 24px, rgba(255,255,255,0.9)
Decorative element: Abstract shape in #E4E6F9
Height: 200-617px
```

### Data Card Pattern
```
Background: #F7F7FF
Border: 2px solid #E4E6F9
Padding: 24-32px
Icon: 40-120px, #000FC4
Number: Montserrat Bold 48-72px, #2DE4E6
Label: Lato Regular 18-20px, #000000
```

### Section Header Pattern
```
Preheading: Lato Bold 20px, #434343
Header: Montserrat Bold 28px, #000FC4
Spacing: 12-16px between preheading and header
Bottom margin: 32px before content
```

### Callout Box Pattern
```
Background: #E4E6F9
Border: 3px solid #000FC4
Border-radius: 12px
Padding: 32px
Title: Montserrat Bold 24px, #000FC4
Content: Lato Regular 18-20px, #000000
```

---

## Export Specifications

### For Web/Blog
- Format: PNG
- Resolution: 2× (retina displays)
- Color space: sRGB
- Optimization: Yes (<500KB preferred)

### For Social Media
- Format: PNG or JPG
- Resolution: Platform-specific (usually 2×)
- Color space: sRGB
- Optimization: Yes (<1MB)

### For Presentations
- Format: PNG at 2× resolution, also SVG for scalability
- Color space: sRGB
- Optimization: Minimal (quality over size)

### For Print
- Format: PDF
- Resolution: 300 DPI
- Color space: CMYK (convert from RGB)
- Include bleed: 3mm

---

## Quick Reference Cheat Sheet

```
PRIMARY BRAND COLOR: #000FC4 (Primary Blue)
ACCENT COLOR: #2DE4E6 (Accent Cyan)
CTA COLOR: #FF6B35 or #F26419 (Orange)
BACKGROUND: #FFFFFF (White)

HEADER FONT: Montserrat Bold
BODY FONT: Lato Regular/Medium

H1: 56-76px, #000FC4 or White
H2: 28px, #000FC4 or #000000
H3: 24px, #000FC4
Body: 18-20px, #222222 or #000000

SPACING: 40px major sections, 20px within sections
MARGINS: 60-96px (blog), 40px (social), 80-120px (presentation)
CARD PADDING: 32px
ICON SIZES: 20px, 40px, 56px, 72px
```

---

## Quick Reference: Common Measurements

```yaml
Card Widths:
  Small: 372px
  Medium: 446px, 550px
  Large: 662px, 900px
  Full: 1072px, 1120px, 1346px

Card Heights:
  Compact: 100px, 181px
  Standard: 268px, 316px, 397px
  Tall: 465px, 609px

Gaps:
  Tight: 12-16px
  Standard: 24-32px
  Loose: 40-64px
  Major: 96-120px

Icons:
  UI: 20-24px
  Card: 32-40px
  Feature: 56px
  Hero: 72px

Text Sizes:
  Display: 56-76px
  Heading: 24-28px
  Body: 16-18px
  Small: 11-14px
```

---

## Design System Checklist

When creating new designs, ensure:

- [ ] Primary blue (`#000FC4`) used for brand elements
- [ ] Accent cyan (`#2DE4E6`) used sparingly for highlights
- [ ] Montserrat Bold for all headings
- [ ] Lato Regular for body text
- [ ] 32px minimum padding on cards
- [ ] 32px gaps between major sections
- [ ] White (`#FFFFFF`) or off-white (`#F7F7FF`) backgrounds
- [ ] Icons sized at 20px, 40px, 56px, or 72px
- [ ] Badge text is UPPERCASE, Lato Bold 11px, 0.5px letter-spacing
- [ ] Consistent border radius (8px cards, 12px containers, 999px pills)

---

## Brand Mistakes to Avoid

❌ **DON'T:**
- Use orange (#FF6B35 or #F26419) for anything except CTAs
- Mix Montserrat and Lato in same text block
- Use more than ONE H1 per graphic
- Use dark mode (light mode only)
- Use colors outside the defined palette
- Set body text below 16px
- Ignore accessibility contrast ratios
- Create designs without 32px minimum padding

✅ **DO:**
- Use #000FC4 for all primary brand elements
- Apply Montserrat Bold only for headers
- Maintain 32-40px spacing between major sections
- Follow the 5-element framework for prompts
- Use exact hex codes in prompts
- Specify exact pixel dimensions
- Test readability at 50% zoom
- Use lucide-react icons with proper specifications

---

## Real Component Examples

### Example 1: Level Card from Infographic
```
Card: Level 1 - Foundation
Background: #F7F7FF
Dimensions: 900px × 268.25px
Icon: Database icon, 40px white in 72px #000FC4 square
Badge: #FF6B35 "FOUNDATION" pill
Title: "Level 1: Organize & Integrate Data" - Montserrat Bold 28px
Items:
  - "Centralize revenue records using Data Hub"
  - "Connect marketing, sales, and customer success datasets"
  - "Establish workflows and naming conventions"
Target: "Target: > 95% data completeness" - Lato Bold 17px, #000FC4
```

### Example 2: Hero CTA Button
```
Primary Button: "Book a Discovery Call"
Background: #FF6B35
Width: 260px
Height: 61px
Padding: 16px 24px
Icon: Avatar circle (61px) on left
Text: 
  Main: "Book a Discovery Call" - Lato Bold 16px, White
  Sub: "Casual chat with an expert" - Lato Regular 14px, rgba(255,255,255,0.8)
Border Radius: 4px
```

### Example 3: Service Card
```
Card: "HubSpot Implementation"
Dimensions: 372px × 397px
Padding: 32px
Icon Container: 56px square, #F7F7FF background, 2px #000FC4 border
Icon: 40px centered
Title: "HubSpot Implementation" - Montserrat Bold 24px, #000000
Description: "Get HubSpot up and running..." - Lato Regular 18px, #434343, 90px height
CTA: "Get started on HubSpot →" - Lato Bold 16px, #000FC4
```

---

**Document End**

This reference guide is based on actual production designs from MAN Digital's Figma files and represents the current design system as of November 2025.
