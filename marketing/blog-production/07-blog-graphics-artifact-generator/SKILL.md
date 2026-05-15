---
name: blog-graphics-artifact-generator  
description: "Generate production-quality blog graphics as React/JSX artifacts that render directly in Claude's interface for immediate visual preview. CRITICAL WORKFLOW: (1) Create .jsx artifact file → user sees rendered graphic in interface, (2) Get approval, (3) Convert to HubSpot HTML/CSS modules. NEVER output code in chat unless converting to HubSpot. Always creates actual .jsx React artifacts (NOT markdown code blocks) that render visually. Supports multiple graphics per article. Analyzes blog content to recommend graphic placements, creates brand-compliant MAN Digital designs. Use when creating embeddable graphics for blog posts that need visual preview."
---

# Blog Graphics Artifact Generator

Generate professional blog graphics as **actual React/JSX artifacts** that render directly in Claude's interface. Supports **multiple graphics per article**.

## 🔧 Technical Implementation (Read This First!)

**HOW TO CREATE ARTIFACTS:**

```python
# Use the create_file tool to save .jsx files
create_file(
  description="Creating blog graphic",
  path="/mnt/user-data/outputs/graphic-name.jsx",
  file_text="import { Icon } from 'lucide-react';\n\nexport default function..."
)

# Then provide the artifact link
"Here's your graphic: [View graphic](computer:///mnt/user-data/outputs/graphic-name.jsx)"
```

**WHAT HAPPENS:**
1. ✅ File saves to `/mnt/user-data/outputs/` with .jsx extension
2. ✅ Claude's interface automatically renders it as a visual artifact
3. ✅ User sees RENDERED GRAPHIC (not code)
4. ✅ User can click link to view/interact with artifact

**WHAT NOT TO DO:**
- ❌ Never output JSX code in markdown code blocks in chat
- ❌ Never show code to user (unless converting to HubSpot)
- ❌ Never let user see code when they asked for a graphic

**WORKFLOW:**
1. Create → use `create_file` for .jsx file → user sees rendered graphic
2. Iterate → use `str_replace` to update .jsx → user sees updated graphic  
3. Convert → ONLY NOW output HTML/CSS in markdown code blocks for HubSpot

## ⚠️ CRITICAL: React Artifact Workflow (Technical Implementation)

**THIS IS THE MANDATORY WORKFLOW - NEVER DEVIATE:**

### Technical Steps

1. **Use `create_file` tool** to save a .jsx file to `/mnt/user-data/outputs/`
   - Example: `/mnt/user-data/outputs/blog-graphic.jsx`
   - The .jsx file will automatically render as a visual artifact in Claude's interface
   - User will see the RENDERED graphic, NOT the code

2. **ABSOLUTELY NO CODE IN CHAT** 
   - Do NOT output JSX/TSX code in markdown code blocks
   - Do NOT show code to the user (unless converting to HubSpot)
   - User must see the visual result rendered in the interface

3. **Get user approval on the rendered visual**
   - Wait for feedback on the design shown in the interface
   - Make iterations by updating the .jsx file if needed

4. **Only after approval, convert to HubSpot**
   - NOW output HTML/CSS/JS in markdown code blocks
   - Provide complete HubSpot module code for deployment

### How Artifacts Work

When you use `create_file` to save a .jsx file:
- ✅ File is saved to `/mnt/user-data/outputs/graphic-name.jsx`
- ✅ Claude's interface automatically detects the .jsx extension
- ✅ The React component renders visually in the interface
- ✅ User sees the graphic, NOT the code
- ✅ You provide a link to the rendered artifact

### What NOT to Do

❌ **NEVER output code in markdown blocks like this:**
```jsx
import { Database } from 'lucide-react';
export default function MyGraphic() { ... }
```

❌ **NEVER show JSX/TSX code in the chat thread**
❌ **NEVER let users read code when they asked for graphics**

### What TO Do

✅ **ALWAYS use create_file tool:**
```
create_file(
  path="/mnt/user-data/outputs/blog-graphic.jsx",
  content="import { Database } from 'lucide-react';\n\nexport default function..."
)
```

✅ **ALWAYS provide artifact link after creation**
✅ **ALWAYS let user see rendered visual, not code**

**Example of CORRECT workflow:**
```
User: "Create a three-column infographic"

Claude: [Uses create_file tool]:
        create_file(
          path="/mnt/user-data/outputs/three-column-infographic.jsx",
          content="import { Database, RotateCw, Gauge } from 'lucide-react';\n\nexport default function..."
        )
        
        [Provides link to rendered artifact]
        
        "Here's your three-column infographic: [View graphic](computer:///mnt/user-data/outputs/three-column-infographic.jsx)"
        
        [User sees RENDERED GRAPHIC in interface, NOT code]

User: "Perfect! Convert to HubSpot"

Claude: [NOW outputs HTML/CSS in markdown code blocks]
        
        ### module.html
        ```html
        <div class="three-column-infographic">...</div>
        ```
```

**Example of INCORRECT workflow (NEVER DO THIS):**
```
User: "Create a three-column infographic"

Claude: "Here's the TSX code:"
        ```tsx
        import { Database } from 'lucide-react';
        export default function...
        ```
        
        [❌ WRONG - This is a markdown code block, not a saved file!]
        [❌ User sees CODE text, not a rendered graphic]
        [❌ File is not saved to outputs directory]
        [❌ No artifact link provided]
        [❌ This defeats the entire purpose of artifacts]
```

## Multi-Graphic Support

This skill supports creating **multiple graphics for a single article**.

### Workflow for Multiple Graphics

1. **Analyze content** → Identify 3-5 graphic opportunities
2. **Recommend placements** → Specific section placement for each
3. **Create .jsx files one by one using create_file tool** → Each saves to outputs directory and renders
4. **Batch convert** → After all approved, convert all to HubSpot

**Technical Implementation:**
- Use `create_file` to save each graphic: 
  - `/mnt/user-data/outputs/graphic-1-infographic.jsx`
  - `/mnt/user-data/outputs/graphic-2-timeline.jsx`
  - `/mnt/user-data/outputs/graphic-3-metrics.jsx`
- Each file automatically renders in the interface
- User sees all rendered graphics, NOT code
- NO markdown code blocks until HubSpot conversion phase

### Numbering Convention

When creating multiple graphics for one article:
- Graphic 1: [Type] - [Placement]
- Graphic 2: [Type] - [Placement]
- Graphic 3: [Type] - [Placement]

Example:
- Graphic 1: Three-column infographic - After intro
- Graphic 2: Timeline - Section "Implementation"
- Graphic 3: Metric cards - Before conclusion

## When to Use This Skill

Use when:
- Creating 1-5 graphics for a single blog post
- Need to see rendered graphics (not code) before deploying
- Want clean, maintainable HubSpot module code
- Require brand-compliant MAN Digital designs
- Converting Figma designs or v0.dev components

**Key benefit:** Visual preview via React artifacts, not code blocks

## Quick Start Examples

### Example 1: Single Graphic with React Artifact

```
User: "Create a three-column infographic showing:
       - Data Explosion (12% analyzed, 400M TB daily)  
       - Repeatability Crisis (67% lack docs)
       - Measurement Gaps (40% forecast miss)"

Claude: [Uses create_file tool to save .jsx file]
        [File automatically renders in Claude's interface as artifact]
        
        "Here's your three-column infographic: [View graphic](computer:///mnt/user-data/outputs/data-challenges-infographic.jsx)"
        
        [User sees the VISUAL GRAPHIC rendered, NOT code]
        
        "Does this look good to you?"

User: "Perfect! Give me the HubSpot code"

Claude: [NOW outputs HTML/CSS/JS in markdown code blocks for HubSpot]
        
        ### module.html
        ```html
        <!-- HubSpot module HTML -->
        <div class="data-challenges-infographic">...</div>
        ```
        
        ### module.css
        ```css
        /* HubSpot module CSS */
        .data-challenges-infographic { ... }
        ```
```

### Example 2: Multiple Graphics for One Article

```
User: "Analyze this blog post and create 3 graphics"
      [pastes 2000-word post]

Claude: [Runs analysis]
        "I recommend:
         1. Three-column infographic (after intro)
         2. Timeline (section 3)
         3. Metric cards (before conclusion)
         
         Creating Graphic 1..."
         
        [Uses create_file: graphic-1-infographic.jsx]
        "Graphic 1 ready: [View infographic](computer:///mnt/user-data/outputs/graphic-1-infographic.jsx)"

User: "Good! Next one"

Claude: "Creating Graphic 2..."
        [Uses create_file: graphic-2-timeline.jsx]
        "Graphic 2 ready: [View timeline](computer:///mnt/user-data/outputs/graphic-2-timeline.jsx)"

User: "Great! Last one"

Claude: "Creating Graphic 3..."
        [Uses create_file: graphic-3-metrics.jsx]
        "Graphic 3 ready: [View metrics](computer:///mnt/user-data/outputs/graphic-3-metrics.jsx)"

User: "All approved! Convert all to HubSpot"

Claude: [NOW outputs markdown code blocks with 3 sets of module files]
        
        ## Graphic 1: Three-Column Infographic
        ### graphic-1-infographic.html
        ```html
        ...
        ```
        ### graphic-1-infographic.css
        ```css
        ...
        ```
        
        ## Graphic 2: Timeline
        ### graphic-2-timeline.html
        ```html
        ...
        ```
        ### graphic-2-timeline.css
        ```css
        ...
        ```
        
        ## Graphic 3: Metric Cards
        ### graphic-3-metrics.html
        ```html
        ...
        ```
        ### graphic-3-metrics.css
        ```css
        ...
        ```
```

### Example 3: Preview Then Iterate

```
User: "Create metric cards for Q4 results"

Claude: [Uses create_file: q4-metrics.jsx]
        "Here are your Q4 metric cards: [View metrics](computer:///mnt/user-data/outputs/q4-metrics.jsx)"
        
        [User sees rendered graphic in interface]

User: "Can you make the numbers bigger and add icons?"

Claude: [Updates the .jsx file with str_replace or create_file]
        "Updated! [View updated metrics](computer:///mnt/user-data/outputs/q4-metrics.jsx)"
        
        [User sees updated rendered graphic]

User: "Perfect! HubSpot code please"

Claude: [NOW outputs HTML/CSS in markdown code blocks]
        
        ### q4-metrics.html
        ```html
        <div class="q4-metrics">...</div>
        ```
        
        ### q4-metrics.css
        ```css
        .q4-metrics { ... }
        ```
```

## React Artifact File Format

**⚠️ CRITICAL: Every graphic MUST be created using the `create_file` tool to save a .jsx file to `/mnt/user-data/outputs/`, NOT as a code block in chat.**

### How to Create React Artifacts (The ONLY Correct Method)

**THE CORRECT WAY - Use create_file Tool:**

```python
# Step 1: Use create_file tool
create_file(
  description="Creating blog graphic for data challenges",
  path="/mnt/user-data/outputs/blog-graphic.jsx",
  file_text="""import { Database, RotateCw, Gauge } from 'lucide-react';

export default function BlogGraphic() {
  return (
    <div style={{ 
      width: '800px',
      margin: '0 auto',
      fontFamily: 'Lato, sans-serif'
    }}>
      {/* Your graphic content */}
    </div>
  );
}"""
)

# Step 2: Provide artifact link to user
# "Here's your graphic: [View graphic](computer:///mnt/user-data/outputs/blog-graphic.jsx)"

# Result: 
# ✅ File is saved to outputs directory
# ✅ Claude's interface automatically renders it as a visual artifact
# ✅ User sees the VISUAL GRAPHIC in the interface, NOT code
# ✅ User can click the link to view/interact with the rendered graphic
```

**THE WRONG WAY - DON'T DO THIS:**

```markdown
# ❌ NEVER output code in markdown code blocks like this:

```jsx
import { Database } from 'lucide-react';
export default function MyGraphic() { 
  return <div>...</div>;
}
```

This is WRONG because:
- ❌ Code appears as text in the chat thread
- ❌ File is NOT saved to outputs directory  
- ❌ Does NOT render as a visual artifact
- ❌ User sees CODE text, not a rendered graphic
- ❌ No artifact link is provided
```

### Technical Flow

1. **You call create_file tool** with .jsx extension
2. **File saves to** `/mnt/user-data/outputs/graphic-name.jsx`
3. **Claude's interface detects** the .jsx file extension
4. **React component auto-renders** as a visual artifact
5. **You provide link** to the rendered artifact
6. **User sees** the rendered graphic (NOT code)

### Artifact File Structure

**IMPORTANT: This code structure is what you pass to the `create_file` tool. The user NEVER sees this code - they only see the RENDERED result.**

**What you do:**
```python
create_file(
  path="/mnt/user-data/outputs/blog-graphic.jsx",
  file_text="""
// This code is passed to create_file
// User will see the RENDERED graphic, not this code

import { IconName1, IconName2 } from 'lucide-react';

export default function BlogGraphic() {
  return (
    <div style={{ 
      width: '800px',
      margin: '0 auto',
      fontFamily: 'Lato, sans-serif'
    }}>
      {/* Your graphic content here */}
      <h2 style={{ fontFamily: 'Montserrat, sans-serif', color: '#000FC4' }}>
        Your Headline
      </h2>
    </div>
  );
}
"""
)
```

**What user sees:**
- ✅ A link to the artifact: `[View graphic](computer:///mnt/user-data/outputs/blog-graphic.jsx)`
- ✅ The rendered visual graphic in Claude's interface
- ✅ Interactive, clickable, visual result
- ❌ NOT the code above - they never see the JSX code

### Artifact Requirements

✅ **Must include:**
- Import statements for lucide-react icons
- Export default function
- Inline styles (no external CSS)
- Proper React/JSX syntax
- Brand-compliant colors (hex codes)
- Responsive considerations

✅ **Must use:**
- lucide-react for icons
- Inline style objects
- MAN Digital color palette
- Montserrat for headers, Lato for body

❌ **NEVER DO:**
- Output code in markdown code blocks in chat (unless converting to HubSpot)
- Show TSX/JSX code to the user (they should see rendered graphics)
- Use external CSS files
- Use non-brand colors
- Create code blocks when user asks for graphics

### Correct Implementation Flow

1. **User asks for graphic** → You use `create_file` tool to save .jsx file (NOT markdown code block)
   ```python
   create_file(path="/mnt/user-data/outputs/graphic.jsx", file_text="...")
   ```

2. **Artifact auto-renders** → User sees visual result in Claude's interface
   - Provide artifact link: `[View graphic](computer:///mnt/user-data/outputs/graphic.jsx)`
   - User clicks link or sees inline rendered graphic
   
3. **User gives feedback** → You update the .jsx file if needed (still using create_file or str_replace, never code blocks)
   ```python
   str_replace(path="/mnt/user-data/outputs/graphic.jsx", old_str="...", new_str="...")
   ```

4. **User approves** → ONLY NOW you output HubSpot conversion as markdown code blocks
   ```markdown
   ### module.html
   ```html
   <div class="graphic">...</div>
   ```
   ```

**Key Point:** Steps 1-3 use file tools (create_file, str_replace). Code NEVER appears as markdown blocks in chat until step 4. User only sees rendered graphics via artifact links.

### Example: Complete React Artifact Implementation

**⚠️ CRITICAL: This shows what you pass to `create_file`. The user NEVER sees this code - they see the rendered graphic.**

**What you do (use create_file tool):**

```python
create_file(
  description="Creating three-column infographic for data challenges",
  path="/mnt/user-data/outputs/three-column-infographic.jsx",
  file_text="""// Graphic 1: Three-Column Infographic
// Placement: After introduction section
// Dimensions: 800px × 900px

import { Database, RotateCw, Gauge } from 'lucide-react';

export default function ThreeForceInfographic() {
  return (
    <div style={{
      width: '800px',
      height: '900px',
      backgroundColor: '#FFFFFF',
      padding: '60px 40px',
      display: 'flex',
      flexDirection: 'column',
      gap: '40px',
      fontFamily: 'Lato, sans-serif'
    }}>
      {/* Header */}
      <div style={{ textAlign: 'center' }}>
        <h2 style={{
          fontFamily: 'Montserrat, sans-serif',
          fontSize: '32px',
          fontWeight: 'bold',
          color: '#000FC4',
          margin: 0
        }}>
          Three Forces Reshaping Revenue Operations
        </h2>
      </div>

      {/* Three Columns */}
      <div style={{
        display: 'flex',
        gap: '30px',
        flex: 1
      }}>
        {/* Column 1: Data Explosion */}
        <div style={{
          flex: 1,
          backgroundColor: '#F8F9FA',
          padding: '30px',
          borderRadius: '8px',
          display: 'flex',
          flexDirection: 'column',
          gap: '20px'
        }}>
          <Database size={40} color="#000FC4" />
          <h3 style={{
            fontFamily: 'Montserrat, sans-serif',
            fontSize: '20px',
            fontWeight: 'bold',
            color: '#000FC4',
            margin: 0
          }}>
            Data Explosion
          </h3>
          <div style={{ fontSize: '48px', fontWeight: 'bold', color: '#2DE4E6' }}>
            12%
          </div>
          <p style={{ fontSize: '16px', color: '#333', margin: 0 }}>
            Only 12% of data gets analyzed, while 400M TB are generated daily
          </p>
        </div>

        {/* Column 2: Repeatability Crisis */}
        <div style={{
          flex: 1,
          backgroundColor: '#F8F9FA',
          padding: '30px',
          borderRadius: '8px',
          display: 'flex',
          flexDirection: 'column',
          gap: '20px'
        }}>
          <RotateCw size={40} color="#000FC4" />
          <h3 style={{
            fontFamily: 'Montserrat, sans-serif',
            fontSize: '20px',
            fontWeight: 'bold',
            color: '#000FC4',
            margin: 0
          }}>
            Repeatability Crisis
          </h3>
          <div style={{ fontSize: '48px', fontWeight: 'bold', color: '#2DE4E6' }}>
            67%
          </div>
          <p style={{ fontSize: '16px', color: '#333', margin: 0 }}>
            67% of revenue teams lack documented, repeatable processes
          </p>
        </div>

        {/* Column 3: Measurement Gaps */}
        <div style={{
          flex: 1,
          backgroundColor: '#F8F9FA',
          padding: '30px',
          borderRadius: '8px',
          display: 'flex',
          flexDirection: 'column',
          gap: '20px'
        }}>
          <Gauge size={40} color="#000FC4" />
          <h3 style={{
            fontFamily: 'Montserrat, sans-serif',
            fontSize: '20px',
            fontWeight: 'bold',
            color: '#000FC4',
            margin: 0
          }}>
            Measurement Gaps
          </h3>
          <div style={{ fontSize: '48px', fontWeight: 'bold', color: '#2DE4E6' }}>
            40%
          </div>
          <p style={{ fontSize: '16px', color: '#333', margin: 0 }}>
            40% of forecasts miss by >20% due to measurement inconsistencies
          </p>
        </div>
      </div>
    </div>
  );
}
"""
)
```

**Then you say to user:**
```
"Here's your three-column infographic: [View graphic](computer:///mnt/user-data/outputs/three-column-infographic.jsx)"
```

**What user sees:**
- ✅ A clickable link to the rendered artifact
- ✅ The visual graphic rendered in Claude's interface (3 columns with icons, numbers, text)
- ✅ Interactive, beautifully formatted visual result

**What user does NOT see:**
- ❌ The JSX code above
- ❌ Import statements
- ❌ Function definitions
- ❌ Style objects

**Remember:** When creating graphics, ALWAYS use create_file to save .jsx files. User sees rendered visuals, NOT code.
      position: 'relative',
      fontFamily: 'Lato, sans-serif'
    }}>
      {/* Header */}
      <div style={{ padding: '48px 40px' }}>
        <p style={{
          fontFamily: 'Lato, sans-serif',
          fontWeight: 700,
          fontSize: '13px',
          color: '#000FC4',
          letterSpacing: '1.5px',
          textTransform: 'uppercase',
          textAlign: 'center',
          marginBottom: '20px'
        }}>
          THE CHALLENGE
        </p>
        
        <h1 style={{
          fontFamily: 'Montserrat, sans-serif',
          fontWeight: 700,
          fontSize: '42px',
          color: '#222222',
          lineHeight: '1.15',
          textAlign: 'center',
          letterSpacing: '-1.5px'
        }}>
          3 Forces Reshaping Revenue Operations
        </h1>
      </div>
      
      {/* Three columns */}
      <div style={{ 
        display: 'flex',
        gap: '4px',
        padding: '0 32px'
      }}>
        {/* Column 1 */}
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
            {/* Icon container */}
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
            
            {/* Title */}
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
            
            {/* Subtitle */}
            <p style={{
              fontFamily: 'Lato, sans-serif',
              fontWeight: 700,
              fontSize: '15px',
              color: '#000FC4',
              marginBottom: '20px'
            }}>
              Demands AI Intelligence
            </p>
            
            {/* Description */}
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
          <div style={{ marginTop: '24px' }}>
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
            <p style={{
              fontFamily: 'Lato, sans-serif',
              fontWeight: 700,
              fontSize: '14px',
              color: '#2DE4E6'
            }}>
              400M TB
            </p>
            <p style={{
              fontFamily: 'Lato, sans-serif',
              fontSize: '12px',
              color: '#999999'
            }}>
              created daily
            </p>
          </div>
        </div>
        
        {/* Columns 2 and 3 follow same pattern... */}
        
      </div>
    </div>
  );
}
```

## Multi-Graphic Workflows

### Workflow A: Sequential Creation

**Best for:** Creating 2-5 graphics one at a time

```
Step 1: Analyze content → Identify opportunities
Step 2: Create Graphic 1 TSX artifact → Get approval
Step 3: Create Graphic 2 TSX artifact → Get approval
Step 4: Create Graphic 3 TSX artifact → Get approval
Step 5: Batch convert all to HubSpot modules
```

**Example conversation:**
```
User: "Create 3 graphics for this post"

Claude: "I'll create them one by one.
         
         Graphic 1: Three-column infographic
         Placement: After intro
         
         [TSX ARTIFACT 1]"

User: "Good, next"

Claude: "Graphic 2: Timeline
         Placement: Section 'Implementation'
         
         [TSX ARTIFACT 2]"

User: "Perfect, last one"

Claude: "Graphic 3: Metric cards
         Placement: Before conclusion
         
         [TSX ARTIFACT 3]"

User: "All approved! Convert to HubSpot"

Claude: [Outputs 3 HubSpot module sets]
```

### Workflow B: Batch Preview

**Best for:** Review all graphics before converting any

```
Step 1: Create ALL TSX artifacts first
Step 2: User reviews all previews
Step 3: Make any adjustments
Step 4: Convert all to HubSpot at once
```

**Example conversation:**
```
User: "Create all graphics for this post, let me review all before converting"

Claude: "Creating 3 graphics for review...
         
         === Graphic 1 ===
         Type: Three-column
         Placement: After intro
         [TSX ARTIFACT 1]
         
         === Graphic 2 ===
         Type: Timeline
         Placement: Section 3
         [TSX ARTIFACT 2]
         
         === Graphic 3 ===
         Type: Metric cards
         Placement: Conclusion
         [TSX ARTIFACT 3]
         
         Review all three and let me know if any need changes."

User: "All look great! Convert all to HubSpot"

Claude: [Outputs 3 HubSpot module sets]
```

### Workflow C: Iterative Refinement

**Best for:** Complex graphics needing adjustments

```
Step 1: Create initial TSX artifact
Step 2: User requests changes
Step 3: Update TSX artifact
Step 4: Repeat until approved
Step 5: Convert to HubSpot
```

**Example conversation:**
```
User: "Create a timeline for Q1 roadmap"

Claude: [TSX ARTIFACT - version 1]

User: "Make the icons bigger and add more spacing"

Claude: [TSX ARTIFACT - version 2 with changes]

User: "Perfect! HubSpot code please"

Claude: [Outputs module files]
```

## Graphic Naming Convention

### For Single Graphic

```
// Blog Graphic: [Descriptive Name]
// Article: [Blog post title]
// Placement: [Section name or position]
```

### For Multiple Graphics

```
// Graphic 1 of 3: [Type] - [Brief description]
// Placement: After [section]
// Dimensions: 800px × 900px

// Graphic 2 of 3: [Type] - [Brief description]
// Placement: Section "[name]"
// Dimensions: 800px × 1200px

// Graphic 3 of 3: [Type] - [Brief description]
// Placement: Before conclusion
// Dimensions: 800px × 600px
```

## HubSpot Conversion (Phase 2)

**ONLY after TSX artifact approval, convert to HubSpot:**

1. **module.html**
   - Convert JSX → semantic HTML
   - lucide-react icons → inline SVG
   - Remove all React syntax
   - Add data attributes for JS hooks

2. **module.css**
   - Convert Tailwind → standard CSS
   - Organize by sections
   - Add responsive breakpoints
   - Use brand colors (hex values)

3. **module.js** (only if needed)
   - Convert React hooks → vanilla JS
   - IIFE wrapper for scope
   - Event listeners
   - State management

**Conversion reference files:**
- `references/graphic-patterns.md` - Complete pattern documentation
- `references/brand-guidelines.md` - MAN Digital brand specs

## Graphic Types Supported

### 1. Three-Column Infographic
**Use for:** 3 related concepts, forces, pillars, comparisons  
**Dimensions:** 800px × 900px  
**Example:** `assets/examples/three-column-infographic/`

**Structure:**
```
Eyebrow text
Main title
[Column 1] [Column 2] [Column 3]
Footer CTA
```

Each column: Icon, title, subtitle, description, primary stat, secondary stats

### 2. Horizontal Timeline
**Use for:** Project phases, roadmaps, implementation plans  
**Dimensions:** 800px × 1200-2400px  
**Example:** `assets/examples/timeline-90day/`

**Structure:**
```
Header (title + phase indicators)
Progress bar (gradient with markers)
Phase 1 details
Phase 2 details
Phase 3 details
```

### 3. Vertical Maturity/Level Model
**Use for:** Progression levels, maturity models, growth stages  
**Dimensions:** 1200px × variable height  
**Example:** `assets/examples/maturity-model/`

**Structure:**
```
Header (on colored background)
Level 1 card
Level 2 card
Level 3 card
...
```

### 4. Data Visualization Grid
**Use for:** Multiple metrics, KPIs, statistics  
**Dimensions:** 800-1200px × flexible

**Structure:**
```
Title
[Metric 1] [Metric 2] [Metric 3]
[Metric 4] [Metric 5] [Metric 6]
```

### 5. Process Flow Diagram
**Use for:** Step-by-step processes, workflows  
**Dimensions:** 800-1200px × 400-600px

**Structure:**
```
Title
Step 1 → Step 2 → Step 3 → Step 4
```

## Brand Guidelines (Auto-Applied)

**Colors:**
- Primary: #000FC4 (Blue) - Icons, headers, structure
- Accent: #2DE4E6 (Cyan) - Stats, highlights
- CTA: #F26419 (Orange) - CTAs only
- Neutral: #222222, #434343, #999999, #FFFFFF

**Typography:**
- Headers: Montserrat Bold 700 (42/28/22/18px)
- Body: Lato Regular 400 (18/16/14px)
- Stats: Montserrat Bold 700 (30-56px)

**Icons:**
- Library: lucide-react
- Style: Outline, 2px stroke
- Sizes: 24px (small), 40px (medium), 80px (large)

**Spacing:**
- Major sections: 40-64px
- Internal: 16-32px
- Card padding: 24-32px

**Reference:** `references/brand-guidelines.md` for complete specs

## Reference Files

**Load these when needed:**

### Graphic Patterns (`references/graphic-patterns.md`)
Complete documentation of all 5 graphic patterns:
- Detailed structure breakdowns
- Element specifications
- Color usage
- Responsive behavior
- Accessibility guidelines
- When to use each pattern

**Load when:** Creating any graphic or user asks about patterns

### Brand Guidelines (`references/brand-guidelines.md`)
MAN Digital complete brand specifications:
- Color palette with hex codes
- Typography rules
- Icon usage
- Spacing system
- Logo usage

**Load when:** Questions about brand compliance or colors

## Example Files

Real production graphics in `assets/examples/`:

1. **three-column-infographic.tsx**
   - Three equal columns with stats
   - Icon badges, decorative elements
   - Footer CTA with gradient
   - 18KB complete working example

2. **timeline-90day.tsx**
   - Detailed 90-day execution plan
   - Horizontal progress bar
   - Multiple phase sections
   - 43KB complete working example

3. **maturity-model.tsx**
   - 5-level vertical progression
   - Colored badges per level
   - Blue background with decorations
   - 7KB complete working example

**Usage:** Reference these for structure and patterns when creating similar graphics

## Scripts

### analyze_content.py

Analyzes blog post content to identify graphic opportunities.

**Usage:**
```bash
python scripts/analyze_content.py blog-post.md
```

**Identifies:**
- Statistics (3+ numbers) → Data visualization
- Process steps (3+ steps) → Process flow
- Comparisons (vs, before/after) → Comparison table
- Timelines (3+ dates) → Timeline graphic
- Lists (5+ items) → Icon-based grid

**Output:** Prioritized list of opportunities with placement recommendations

**When to use:**
- Blog posts > 1000 words
- Complex content with multiple sections
- User asks "where should graphics go?"

## Conversion Guidelines

### JSX → HTML

```jsx
// JSX (TSX artifact)
<div className="card">
  <Database size={32} color="#000FC4" />
  {items.map(item => <p>{item}</p>)}
</div>

// HTML (HubSpot)
<div class="card">
  <svg class="icon-database" width="32" height="32" viewBox="0 0 24 24">
    <ellipse cx="12" cy="5" rx="9" ry="3"></ellipse>
    <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path>
    <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>
  </svg>
  <p>Item 1</p>
  <p>Item 2</p>
</div>
```

**Key changes:**
- `className` → `class`
- lucide-react → inline SVG
- `{variable}` → static text
- `.map()` → duplicate HTML

### Tailwind → CSS

```jsx
// TSX
<div className="flex items-center gap-4 p-6 rounded-lg bg-blue-600 text-white">

// CSS
.container {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  border-radius: 0.5rem;
  background-color: #000FC4;
  color: #FFFFFF;
}
```

**Common conversions:**
- `p-6` → `padding: 1.5rem;`
- `flex` → `display: flex;`
- `gap-4` → `gap: 1rem;`
- `text-2xl` → `font-size: 1.5rem; line-height: 2rem;`

### React Hooks → Vanilla JS

```jsx
// React
const [active, setActive] = useState(0);

// Vanilla
let state = { active: 0 };
function setActive(index) {
  state.active = index;
  render();
}
```

## Best Practices

1. **Create artifacts, not code** - ALWAYS use .jsx artifacts, NEVER code blocks for graphics
2. **Visual preview first** - User must see rendered graphic before conversion
3. **Get feedback** - Ask if design looks good before converting
4. **Self-contained** - Keep all styles inline in React artifact
5. **Responsive** - Use mobile-first approach
6. **Brand compliant** - Always use MAN Digital colors/fonts
7. **Clean code** - Well-commented, organized
8. **Accessible** - Semantic HTML, ARIA labels, alt text

## Output Format

### Phase 1: React Artifact (Visual Preview)

**Create a .jsx artifact file** → User sees rendered graphic in interface

Example conversation:
```
Claude: [Creates graphic-1.jsx artifact]
        "Here's your three-column infographic showing the data explosion, 
         repeatability crisis, and measurement gaps. Does it look good?"
```

**NO CODE IN CHAT** - Only the rendered visual appears.

### Phase 2: HubSpot Module (After Approval)

**Output HTML/CSS/JS in markdown code blocks** → User copies to HubSpot

Example conversation:
```
User: "Perfect! Give me the HubSpot code"

Claude: "Here are your HubSpot module files:"
        
        ### module.html
        ```html
        [Clean HTML structure]
        ```
        
        ### module.css
        ```css
        [Organized CSS]
        ```
        
        ### module.js (if needed)
        ```javascript
        [Vanilla JavaScript]
        ```

        ## Implementation Notes
        - Responsive: 320px-1280px
        - Browser support: Modern browsers
        - Dependencies: None (inline SVG)
```

## Troubleshooting

**Artifact not rendering?**
→ Check React syntax, ensure export default
→ Verify all imports (lucide-react)

**Colors don't match brand?**
→ Use exact hex: #000FC4, #2DE4E6, #F26419
→ Reference brand-guidelines.md

**Layout breaks on mobile?**
→ Add responsive breakpoints
→ Test at 320px, 768px, 1024px

**HubSpot module not working?**
→ Verify all SVG is inline
→ Check CSS class prefixes
→ Test in HubSpot preview

## Progressive Disclosure

This skill uses a three-level loading system:

**Level 1: Metadata (always loaded)**
- Skill name and description

**Level 2: SKILL.md (loaded when skill triggers)**
- Core workflow
- Quick reference
- Best practices

**Level 3: References & Examples (loaded as needed)**
- `references/graphic-patterns.md` - Detailed pattern docs
- `references/brand-guidelines.md` - Complete brand specs
- `assets/examples/` - Working TSX examples
- `scripts/analyze_content.py` - Content analysis

**Guidance:** Load references when creating graphics, examples when user needs inspiration or clarification.

## Example Conversations

### Example 1: Simple metric cards

```
User: "Create 3 metric cards: 85% accuracy, 120+ customers, 95% retention"

Claude: [Uses create_file to save metric-cards.jsx]

"Here's your metric cards graphic: [View metrics](computer:///mnt/user-data/outputs/metric-cards.jsx)

The design shows three equal cards with large cyan numbers and icons. Does this look good, or would you like any changes?"

User: "Perfect! Give me the HubSpot code"

Claude: [NOW outputs HTML/CSS in markdown code blocks]

### metric-cards.html
```html
<div class="metric-cards-container">
  <div class="metric-card">
    <div class="metric-number">85%</div>
    <div class="metric-label">Accuracy</div>
  </div>
  ...
</div>
```

### metric-cards.css
```css
.metric-cards-container {
  display: flex;
  gap: 30px;
  ...
}
```

"Here are your HubSpot module files, ready to paste into HubSpot Design Manager."
```

### Example 2: Timeline from scratch

```
User: "I need a timeline showing our Q1 roadmap - January (Planning), 
February (Building), March (Launch)"

Claude: [Reads references/graphic-patterns.md for timeline pattern if needed]
        [Uses create_file to save timeline.jsx]

"I've created a timeline graphic with three phases: [View timeline](computer:///mnt/user-data/outputs/q1-timeline.jsx)

Each phase has its own color and icon. Want to review before I create the HubSpot code?"

User: "Yes, looks great!"

Claude: [NOW outputs HubSpot module files in markdown code blocks]

### q1-timeline.html
```html
<div class="timeline-container">...</div>
```

### q1-timeline.css
```css
.timeline-container { ... }
```
```

### Example 3: With content analysis

```
User: "Analyze this post and suggest graphics"
[pastes 2000-word blog post]

Claude: [Runs analyze_content.py script or analyzes manually]

"I found 4 graphic opportunities:

1. Section 'The Challenge' → Three-column infographic (3 stats found)
2. Section 'Implementation' → Timeline (5 phases detected)
3. Section 'Results' → Data visualization (6 metrics)
4. Section 'Comparison' → Side-by-side table (vs. traditional)

Which would you like me to create first?"

User: "Create the three-column infographic"

Claude: [Uses create_file to save infographic.jsx]

"Here's your three-column infographic: [View graphic](computer:///mnt/user-data/outputs/challenge-infographic.jsx)

This graphic would work well right after your introduction paragraph. Would you like to see the next one?"
```

## Quick Reference

**Brand Colors:**
- #000FC4 (Primary Blue)
- #2DE4E6 (Accent Cyan)
- #F26419 (CTA Orange)

**Fonts:**
- Montserrat Bold (headers)
- Lato Regular (body)

**Icon Sizes:**
- 24px (inline), 40px (section), 80px (hero)

**Graphic Dimensions:**
- Blog graphics: 800px wide
- Wide format: 1200px wide
- Height: Variable by content

---

**Version:** 3.0.0 (React Artifact Update) 
**Last Updated:** November 2024  
**Real Examples:** 3 production graphics included

1. **JSX → HTML**
   - Remove all imports
   - Convert inline styles to CSS classes
   - lucide-react icons → inline SVG
   - Remove export statement

2. **Styles → CSS**
   - Extract inline styles to CSS file
   - Organize by component sections
   - Add responsive breakpoints
   - Use brand color hex codes

3. **JavaScript (if needed)**
   - Convert React hooks → vanilla JS
   - IIFE wrapper
   - Event listeners
   - State management

### File Naming Convention

**Single graphic:**
- `blog-graphic.html`
- `blog-graphic.css`
- `blog-graphic.js` (if needed)

**Multiple graphics:**
- `graphic-1-three-column.html` / `.css`
- `graphic-2-timeline.html` / `.css`
- `graphic-3-metric-cards.html` / `.css`

## Usage Examples

### Example 1: Single Graphic with TSX Artifact

```
User: "Create 3 metric cards showing 85% accuracy, 120+ customers, 95% retention"

Claude: "I'll create a React artifact for you to preview first."

[Uses create_file tool to save metric-cards.jsx]

"Here are your metric cards: [View metrics](computer:///mnt/user-data/outputs/metric-cards.jsx)

Does this look good?"

User: "Looks great! Give me the HubSpot code"

Claude: [NOW outputs module.html and module.css in markdown code blocks]

### metric-cards.html
```html
<div class="metric-cards">...</div>
```

### metric-cards.css
```css
.metric-cards { ... }
```
```

### Example 2: Multiple Graphics Workflow

```
User: "Analyze this post and create 3 graphics"

Claude: "I recommend:
        1. Three-column infographic (after intro)
        2. Timeline (section 3)
        3. Metric cards (before conclusion)
        
        Creating Graphic 1..."
        
        [Uses create_file: graphic-1-infographic.jsx]
        
        "Graphic 1: [View infographic](computer:///mnt/user-data/outputs/graphic-1-infographic.jsx)"

User: "Good! Next"

Claude: "Creating Graphic 2..."
        
        [Uses create_file: graphic-2-timeline.jsx]
        
        "Graphic 2: [View timeline](computer:///mnt/user-data/outputs/graphic-2-timeline.jsx)"

User: "Perfect! Last one"

Claude: "Creating Graphic 3..."
        
        [Uses create_file: graphic-3-metrics.jsx]
        
        "Graphic 3: [View metrics](computer:///mnt/user-data/outputs/graphic-3-metrics.jsx)"

User: "Convert all to HubSpot"

Claude: [NOW outputs 3 sets of module files with clear naming in markdown code blocks]

## Graphic 1: Three-Column Infographic

### graphic-1-infographic.html
```html
...
```

### graphic-1-infographic.css  
```css
...
```

## Graphic 2: Timeline

### graphic-2-timeline.html
```html
...
```

### graphic-2-timeline.css
```css
...
```

## Graphic 3: Metric Cards

### graphic-3-metrics.html
```html
...
```

### graphic-3-metrics.css
```css
...
```
```

## Quick Reference

**Request graphic:**
```
"Create a [type] showing [data/content]"
```

**Multiple graphics:**
```
"Create [number] graphics for this article"
"Analyze and recommend graphics"
```

**Get HubSpot code:**
```
"Convert to HubSpot"
"Give me the module files"
```

**Iterate:**
```
"Make the numbers bigger"
"Add more spacing"
"Change the icon colors"
```

---

**Critical Reminders:**
1. ✅ ALWAYS use `create_file` tool to save .jsx files to `/mnt/user-data/outputs/`
2. ✅ ALWAYS provide artifact links: `[View graphic](computer:///mnt/user-data/outputs/file.jsx)`
3. ✅ User sees rendered graphics in interface (NOT TypeScript/JSX code)
4. ✅ Support multiple graphics per article (separate .jsx files)
5. ✅ Get visual approval before HubSpot conversion
6. ✅ Only output HTML/CSS/JS code in markdown blocks AFTER approval
7. ✅ Use exact brand colors (#000FC4, #2DE4E6, #F26419)
8. ✅ Use `str_replace` to iterate on graphics (not new code blocks)
9. ✅ Number graphics clearly (graphic-1, graphic-2, graphic-3)
10. ✅ Include placement info for each graphic

**Technical Implementation:**
- **Create**: `create_file(path="/mnt/user-data/outputs/name.jsx", file_text="...")`
- **Update**: `str_replace(path="/mnt/user-data/outputs/name.jsx", old_str="...", new_str="...")`
- **Link**: `[View graphic](computer:///mnt/user-data/outputs/name.jsx)`
- **Never**: Output JSX code in markdown code blocks in chat

**Version:** 3.1.0 (Technical Implementation Clarity Update)
**Last Updated:** November 2024
