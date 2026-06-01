# UI/UX & Frontend Design System Spec (DESIGN.md)

This specification defines the visual identity, styling tokens, responsive spacing, and glassmorphic layouts applied throughout the Streamlit frontend. All future visual modifications and additions must strictly align with this document.

---

## 1. Visual Theme & Color Palette
The application uses a modern **Dark & Eco-Green Glassmorphism** design theme to reinforce the sustainability focus of the AI Garbage Classifier:

| Token | CSS/HEX Value | Semantic Use |
| :--- | :--- | :--- |
| **Primary (Eco Green)** | `#2E7D32` | Standard buttons, badges, highlighted links, and active nav items. |
| **Primary Dark (Forest)** | `#1B5E20` | Titles, key stats, page headers, hover borders, and hero backgrounds. |
| **Light Accent** | `#E8F5E9` | Selected state backgrounds, confidence cards, chips, and notification banners. |
| **Background (Canvas)** | `#f7faf8` | Main sidebar canvas and body backdrop. |
| **Alert/Warning (Amber)**| `#E65100` | Fallbacks, 'Unsure' classification tags, and low confidence notifications. |

---

## 2. Typography
*   **Font Family**: `Outfit` (Google Fonts), fallback to `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `Roboto`, `Arial`.
*   **Hierarchy**:
    *   **Hero Titles (`h1`)**: Font Size `2.8rem`, Weight `700`, line height `1.2`. Used in top page banner.
    *   **Section Headers (`h2`, `h3`)**: Font Size `1.5rem` - `2.0rem`, Weight `600`, color `#1B5E20`.
    *   **Body Text**: Font Size `1.0rem`, Weight `400` / `500`.

---

## 3. UI Component Specifications

### A. Glassmorphic Bento Cards (`.premium-card`)
Containers for content modules (instructions, settings, input panels):
*   **Background**: `rgba(255, 255, 255, 0.95)` (for maximum readability).
*   **Borders**: `1px solid rgba(46, 125, 50, 0.12)`.
*   **Border Radius**: `16px`.
*   **Shadow**: `0 8px 30px rgba(46, 125, 50, 0.04)`.
*   **Hover State**: Translates `-4px` vertically, shadow increases to `0 16px 40px rgba(46, 125, 50, 0.1)`, and border color intensifies to `rgba(46, 125, 50, 0.25)` over a `0.3s` cubic-bezier transition.

### B. High-Fidelity Metric Cards (`.metric-card`)
Instead of plain text values, statistics are centered in defined boxes:
*   **Background**: `linear-gradient(145deg, #ffffff, #fcfdfe)`.
*   **Top Accent Border**: `4px solid #2E7D32`.
*   **Val Value**: Font Size `2.2rem`, Weight `700`, color `#1B5E20`.

### C. Sidebar Navigation Menu (`[data-testid="stSidebarNav"]`)
Custom override of Streamlit's default side menu:
*   **Canvas BG**: `#f7faf8` with a thin right-side border: `1px solid rgba(46, 125, 50, 0.08)`.
*   **Navigation Links**: Elevated hover state with background-color `rgba(46, 125, 50, 0.05)` and forest green text color.
*   **Vector Icons**: URL-encoded custom SVGs representing Home, Evaluate, Predict, and Train to prevent emojis from rendering inconsistently across operating systems.

### D. Badges & Chips
*   **Confidence Badge (`.confidence-badge`)**: Round pill layout. High-confidence classes use `#E8F5E9` (green bg) and low-confidence / unsure fallbacks use `#FFF3E0` (amber bg).
*   **Category Chip (`.category-chip`)**: Inline tags with flex layout, thin eco-green border, and center-aligned text.

---

## 4. Layout Spacing & Structure
*   **Banner**: Every page must begin with a full-width `.header-banner` containing the main page header and subheading.
*   **Rhythm**: Utilize `st.columns()` to place items in bento grids rather than stacking them vertically.
*   **Margins**: Maintain `.section-gap` (`2rem` margin-top/bottom) between distinct layout sections to ensure whitespace breathing room.
