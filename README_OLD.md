# RestaurantFlow_bhatiyani

A comprehensive restaurant management system with order tracking, analytics dashboard, and real-time data visualization.

## 🚀 Project Overview

This project demonstrates a full-stack restaurant management solution that includes:
- Order management and tracking
- Real-time analytics dashboard
- Interactive workflow visualization
- Responsive design across all devices
- Complete CRUD operations

## 🛠️ Tech Stack

### Frontend
- **React** with TypeScript
- **shadcn/ui** for modern UI components
- **React Flow** for order workflow visualization
- **Chart.js** for analytics charts
- **JSON Server** for mock data
- **Tailwind CSS** for responsive styling

### Backend
- **FastAPI** (Python) for high-performance API
- **SQLite** database
- **Pydantic** for data validation
- **CORS** enabled for frontend integration

## 📱 Features

### Core Features
- ✅ Restaurant dashboard
- ✅ Order management (Create, Read, Update, Delete)
- ✅ Menu item management
- ✅ Real-time order tracking
- ✅ Analytics and reporting
- ✅ Interactive workflow visualization

### Advanced Features
- 📊 Sales analytics with charts
- 🔄 Order status workflow
- 📱 Responsive design
- 🎯 Real-time updates
- 📈 Performance metrics

## 🏗️ Project Structure

```
RestaurantFlow_bhatiyani/
├── frontend/                 # React TypeScript frontend
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Main application pages
│   │   ├── hooks/          # Custom React hooks
│   │   ├── lib/            # Utility functions
│   │   ├── types/          # TypeScript type definitions
│   │   └── data/           # JSON Server data
│   ├── public/
│   └── package.json
├── backend/                 # FastAPI Python backend
│   ├── app/
│   │   ├── models/         # Database models
│   │   ├── routes/         # API routes
│   │   ├── services/       # Business logic
│   │   └── database/       # Database configuration
│   ├── requirements.txt
│   └── main.py
├── docs/                   # Documentation
│   ├── api-docs.md
│   └── prompts.md
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Node.js (v18+)
- Python (v3.8+)
- Git

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### JSON Server (Mock Data)
```bash
cd frontend
npm run json-server
```

## 🌐 Deployment

- **Frontend**: Deployed on Vercel
- **Backend**: Deployed on Railway/Heroku

## 🤖 AI Usage Documentation

This project extensively used AI tools for development:
- Code generation and optimization
- Component structure planning
- API design patterns
- Testing strategies

See `docs/prompts.md` for detailed AI usage documentation.

## 📝 Development Timeline

**Day 1**: Project setup, backend API, database models
**Day 2**: Frontend components, React Flow integration, Chart.js implementation
**Day 3**: Integration, testing, deployment

## 🎯 Key Learning Outcomes

- Modern React patterns with TypeScript
- FastAPI best practices
- Data visualization techniques
- Responsive design principles
- Full-stack integration
- Deployment strategies

---

Built with ❤️ using AI assistance and modern web technologies.
