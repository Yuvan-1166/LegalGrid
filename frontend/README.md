# Smart Legal System - Frontend

React frontend for the Smart Legal System.

## Quick Start

### 1. Install Dependencies

```bash
pnpm install
```

### 2. Configure Environment

```bash
# .env file already created with:
VITE_API_URL=http://localhost:8000
```

### 3. Start Development Server

```bash
pnpm dev
```

The app will be available at http://localhost:5173

## Features

- **Contract Analysis**: Upload and analyze contracts for risks and compliance
- **Case Law Search**: Find relevant legal precedents (coming soon)
- **Compliance Monitoring**: Check regulatory compliance (coming soon)
- **Dispute Mediation**: AI-powered dispute resolution (coming soon)

## Tech Stack

- React 19
- Vite 8
- React Router 7
- TailwindCSS 4
- Axios for API calls

## Project Structure

```
frontend/
├── src/
│   ├── pages/           # Page components
│   │   ├── Home.jsx
│   │   ├── ContractAnalysis.jsx
│   │   ├── CaseSearch.jsx
│   │   ├── Compliance.jsx
│   │   └── Disputes.jsx
│   ├── services/        # API client
│   │   └── api.js
│   ├── App.jsx          # Main app component
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── public/              # Static assets
└── package.json
```

## Development

### Adding New Pages

1. Create component in `src/pages/`
2. Add route in `src/App.jsx`
3. Add navigation link in the navbar

### API Integration

All API calls go through `src/services/api.js`. Add new API functions there.

## Build for Production

```bash
pnpm build
```

Output will be in `dist/` directory.

## Deploy

```bash
# Deploy to Vercel
vercel

# Or build and deploy manually
pnpm build
# Upload dist/ to your hosting provider
```
