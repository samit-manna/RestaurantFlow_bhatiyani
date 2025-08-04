/**
 * Restaurants page component.
 * Displays restaurant list and management functionality.
 */

import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Badge } from '../components/ui/badge'
import { Button } from '../components/ui/button'
import { 
  Store, 
  Phone, 
  Mail, 
  MapPin, 
  Plus,
  Edit,
  Eye
} from 'lucide-react'
import { mockDataAPI } from '../lib/api'
import { Restaurant } from '../types'

/**
 * Restaurants management page component.
 */
export function Restaurants() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadRestaurants()
  }, [])

  /**
   * Load restaurants data from API.
   */
  const loadRestaurants = async () => {
    try {
      setLoading(true)
      const data = await mockDataAPI.getRestaurants()
      setRestaurants(data)
    } catch (error) {
      console.error('Error loading restaurants:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Restaurants</h1>
          <p className="text-gray-600">Manage restaurant locations and information</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Add Restaurant
        </Button>
      </div>

      {/* Restaurants Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {restaurants.map((restaurant) => (
          <Card key={restaurant.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Store className="h-5 w-5 text-blue-600" />
                  <CardTitle className="text-lg">{restaurant.name}</CardTitle>
                </div>
                <Badge variant={restaurant.is_active ? "success" : "destructive"}>
                  {restaurant.is_active ? "Active" : "Inactive"}
                </Badge>
              </div>
              {restaurant.description && (
                <CardDescription>{restaurant.description}</CardDescription>
              )}
            </CardHeader>
            
            <CardContent className="space-y-4">
              {/* Contact Information */}
              <div className="space-y-2">
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <MapPin className="h-4 w-4" />
                  <span>{restaurant.address}</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <Phone className="h-4 w-4" />
                  <span>{restaurant.phone}</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <Mail className="h-4 w-4" />
                  <span>{restaurant.email}</span>
                </div>
              </div>

              {/* Actions */}
              <div className="flex space-x-2">
                <Button variant="outline" size="sm" className="flex-1">
                  <Eye className="h-4 w-4 mr-1" />
                  View
                </Button>
                <Button variant="outline" size="sm" className="flex-1">
                  <Edit className="h-4 w-4 mr-1" />
                  Edit
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Stats Summary */}
      <Card>
        <CardHeader>
          <CardTitle>Restaurant Statistics</CardTitle>
          <CardDescription>Overview of restaurant network</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-3xl font-bold text-blue-600">{restaurants.length}</div>
              <div className="text-sm text-gray-600">Total Restaurants</div>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-3xl font-bold text-green-600">
                {restaurants.filter(r => r.is_active).length}
              </div>
              <div className="text-sm text-gray-600">Active Locations</div>
            </div>
            <div className="text-center p-4 bg-yellow-50 rounded-lg">
              <div className="text-3xl font-bold text-yellow-600">
                {restaurants.filter(r => !r.is_active).length}
              </div>
              <div className="text-sm text-gray-600">Inactive Locations</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Restaurants
