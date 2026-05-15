# Tailwind CSS to Standard CSS Conversion

Quick reference for converting Tailwind utility classes to standard CSS when creating HubSpot modules.

## Layout

| Tailwind | CSS |
|----------|-----|
| `flex` | `display: flex;` |
| `grid` | `display: grid;` |
| `block` | `display: block;` |
| `inline-block` | `display: inline-block;` |
| `hidden` | `display: none;` |
| `flex-col` | `flex-direction: column;` |
| `flex-row` | `flex-direction: row;` |
| `items-center` | `align-items: center;` |
| `items-start` | `align-items: flex-start;` |
| `items-end` | `align-items: flex-end;` |
| `justify-center` | `justify-content: center;` |
| `justify-between` | `justify-content: space-between;` |
| `gap-4` | `gap: 1rem;` |
| `gap-8` | `gap: 2rem;` |

## Spacing (multiply by 0.25rem)

| Tailwind | CSS | Value |
|----------|-----|-------|
| `p-4` | `padding: 1rem;` | 16px |
| `p-6` | `padding: 1.5rem;` | 24px |
| `p-8` | `padding: 2rem;` | 32px |
| `px-4` | `padding-left: 1rem; padding-right: 1rem;` | 16px |
| `py-6` | `padding-top: 1.5rem; padding-bottom: 1.5rem;` | 24px |
| `m-4` | `margin: 1rem;` | 16px |
| `mx-auto` | `margin-left: auto; margin-right: auto;` | - |
| `mt-4` | `margin-top: 1rem;` | 16px |
| `mb-8` | `margin-bottom: 2rem;` | 32px |

## Typography

| Tailwind | CSS |
|----------|-----|
| `text-sm` | `font-size: 0.875rem; line-height: 1.25rem;` |
| `text-base` | `font-size: 1rem; line-height: 1.5rem;` |
| `text-lg` | `font-size: 1.125rem; line-height: 1.75rem;` |
| `text-xl` | `font-size: 1.25rem; line-height: 1.75rem;` |
| `text-2xl` | `font-size: 1.5rem; line-height: 2rem;` |
| `text-3xl` | `font-size: 1.875rem; line-height: 2.25rem;` |
| `text-4xl` | `font-size: 2.25rem; line-height: 2.5rem;` |
| `font-bold` | `font-weight: 700;` |
| `font-semibold` | `font-weight: 600;` |
| `font-medium` | `font-weight: 500;` |
| `text-center` | `text-align: center;` |
| `uppercase` | `text-transform: uppercase;` |

## Colors (MAN Digital Brand)

| Tailwind Pattern | CSS | Hex |
|-----------------|-----|-----|
| `bg-blue-600` | `background-color: #000FC4;` | Primary |
| `text-cyan-500` | `color: #2DE4E6;` | Accent |
| `bg-orange-600` | `background-color: #F26419;` | CTA |
| `text-gray-600` | `color: #434343;` | Medium gray |
| `bg-white` | `background-color: #FFFFFF;` | White |

## Borders

| Tailwind | CSS |
|----------|-----|
| `border` | `border-width: 1px;` |
| `border-2` | `border-width: 2px;` |
| `rounded` | `border-radius: 0.25rem;` |
| `rounded-md` | `border-radius: 0.375rem;` |
| `rounded-lg` | `border-radius: 0.5rem;` |
| `rounded-full` | `border-radius: 9999px;` |

## Sizing

| Tailwind | CSS |
|----------|-----|
| `w-full` | `width: 100%;` |
| `h-full` | `height: 100%;` |
| `w-64` | `width: 16rem;` (256px) |
| `max-w-2xl` | `max-width: 42rem;` (672px) |
| `max-w-4xl` | `max-width: 56rem;` (896px) |

## Effects

| Tailwind | CSS |
|----------|-----|
| `shadow` | `box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);` |
| `shadow-lg` | `box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);` |
| `opacity-50` | `opacity: 0.5;` |

## Responsive Breakpoints

```css
/* Mobile first */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
```

## Quick Conversion Example

**Tailwind:**
```jsx
<div className="flex items-center gap-4 p-6 bg-blue-600 text-white rounded-lg shadow-lg">
```

**Standard CSS:**
```css
.container {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background-color: #000FC4;
  color: #FFFFFF;
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
```
