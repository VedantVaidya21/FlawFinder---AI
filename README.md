# 🔍 FlawFinder AI

A stunning, ultra-modern SaaS frontend for analyzing business workflows and detecting operational flaws using AI.

## ✨ Features

### 🎨 **World-Class Design**
- **Dark Theme**: Deep purples, electric blues, and neon accents
- **Glassmorphism & Neumorphism**: Beautiful frosted glass effects
- **Smooth Animations**: Framer Motion powered micro-interactions
- **Responsive Design**: Perfect on all devices

### 🚀 **Pages & Components**
- **Login Page**: Animated wave background with Google OAuth
- **Dashboard**: Brutality score indicator with animated charts
- **Upload Page**: Drag-and-drop file upload with progress bars
- **Fix Plan Page**: Accordion UI with animated fix suggestions
- **CEO Report Page**: Elegant report viewer with export options

### 💫 **UI Elements**
- **Navigation**: Hover glow effects & animated logo
- **Buttons**: Gradient backgrounds with scaling animations
- **Charts**: Chart.js integration with custom themes
- **Toast Notifications**: Floating animated alerts
- **Modal Windows**: Glassmorphic confirmation dialogs

## 🛠️ Tech Stack

- **React** (Vite)
- **Tailwind CSS** (with @tailwindcss/vite plugin)
- **Framer Motion** (Animations)
- **Chart.js** (Data visualization)
- **React Router** (Navigation)
- **React Hot Toast** (Notifications)
- **Lucide React** (Icons)
- **React Dropzone** (File uploads)

## 🚀 Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Start the development server**
   ```bash
   npm run dev
   ```

3. **Open your browser**
   Navigate to `http://localhost:5173`

## 🔐 Demo Credentials

Use these credentials to access the demo:
- **Email**: `admin@flawfinder.ai`
- **Password**: `password123`

## 🎯 Key Features

### 📊 **Dashboard**
- **Brutality Score**: Animated radial progress indicator
- **Real-time Charts**: Line, bar, and doughnut charts
- **Flaw Cards**: Interactive cards with hover effects
- **Statistics**: Key metrics with animated counters

### 📤 **Upload System**
- **Drag & Drop**: Intuitive file upload interface
- **Progress Bars**: Animated upload progress
- **File Validation**: PDF, DOC, DOCX support
- **Visual Feedback**: Hover states and animations

### 🔧 **Fix Plans**
- **Accordion UI**: Expandable fix suggestions
- **Click-to-Copy**: Easy tool recommendation copying
- **Step-by-Step**: Numbered implementation guides
- **Cost Estimates**: Timeline and budget information

### 📈 **CEO Reports**
- **Tabbed Interface**: Department-wise breakdown
- **Export Options**: PDF and print functionality
- **Executive Summary**: Key findings and recommendations
- **Interactive Charts**: Data visualization

## 🎨 Design System

### **Color Palette**
- **Primary**: Deep purples (#a855f7, #7c3aed)
- **Secondary**: Electric blues (#0ea5e9, #06b6d4)
- **Accent**: Neon colors (#ff10f0, #10d9ff)
- **Dark**: Custom dark grays (#18181b → #fafafa)

### **Typography**
- **Primary**: Inter (Google Fonts)
- **Monospace**: JetBrains Mono

### **Animations**
- **Hover Effects**: Scale, glow, and color transitions
- **Loading States**: Spinners and progress bars
- **Page Transitions**: Smooth enter/exit animations
- **Micro-interactions**: Button clicks and form inputs

## 📱 Responsive Design

The application is fully responsive with:
- **Mobile Navigation**: Collapsible menu
- **Tablet Layout**: Optimized grid systems
- **Desktop Experience**: Full-featured interface

## 🔧 Customization

### **Theme Toggle**
Light/dark mode toggle is available in the navigation bar (defaults to dark).

### **Custom Scrollbars**
Beautiful purple-themed scrollbars throughout the application.

### **Glassmorphism Effects**
- `.glass` - Light glassmorphic effect
- `.glass-dark` - Dark glassmorphic effect
- `.neumorphic` - Neumorphic shadows

## 🚀 Build for Production

```bash
npm run build
```

## 📦 Project Structure

```
src/
├── components/         # Reusable UI components
│   └── Navigation.jsx  # Main navigation component
├── contexts/          # React contexts
│   └── ThemeContext.jsx
├── pages/            # Page components
│   ├── Login.jsx
│   ├── Signup.jsx
│   ├── Dashboard.jsx
│   ├── Upload.jsx
│   ├── FixPlan.jsx
│   └── CEOReport.jsx
├── App.jsx           # Main application component
├── main.jsx          # Application entry point
└── index.css         # Global styles and utilities
```

## 🎯 Performance Features

- **Lazy Loading**: Code splitting for optimal performance
- **Optimized Images**: Efficient asset loading
- **Smooth Animations**: 60fps animations with hardware acceleration
- **Responsive Charts**: Efficient data visualization

## 🔒 Security Features

- **Input Validation**: Form validation and sanitization
- **Authentication**: JWT token management
- **Route Protection**: Private route guards
- **XSS Prevention**: Sanitized data rendering

---

**Built with ❤️ using React, Tailwind CSS, and Framer Motion**

*"The UI should feel like a futuristic AI business tool that combines luxury, tech, and brutal honesty. Like something from Apple, Notion, and Vercel had a baby."*

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
