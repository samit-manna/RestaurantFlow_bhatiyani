/**
 * Main App component for RestaurantFlow application.
 * Sets up routing, layout, and global providers.
 */

import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navigation from './components/Navigation'
import Dashboard from './pages/Dashboard'
import Restaurants from './pages/Restaurants'
import Orders from './pages/Orders'
import Analytics from './pages/Analytics'
import OrderFlow from './pages/OrderFlow'
import Settings from './pages/Settings'
import './App.css'

/**
 * Main application component with routing and layout.
 */
function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/restaurants" element={<Restaurants />} />
            <Route path="/orders" element={<Orders />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/order-flow" element={<OrderFlow />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="bg-white border-t border-gray-200 mt-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="text-center text-gray-600">
              <p>&copy; 2024 RestaurantFlow. Built with React, TypeScript, and modern web technologies.</p>
              <p className="text-sm mt-1">
                This project was built using AI assistance for rapid development and best practices.
              </p>
            </div>
          </div>
        </footer>
      </div>
    </Router>
  )
}

export default App
