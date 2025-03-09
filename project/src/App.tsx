import React, { useState, useEffect } from 'react';
import { PlusCircle, Wallet, PieChart, Calendar } from 'lucide-react';
import type { Budget, Category } from './types/budget';

function App() {
  const [budgets, setBudgets] = useState<Budget[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulated data for demonstration
    // Replace with actual API calls to your Django backend
    setBudgets([
      {
        id: 1,
        name: "Monthly Budget",
        amount: 5000,
        start_date: "2024-03-01",
        end_date: "2024-03-31",
        allocations: [
          { id: 1, category: 1, category_name: "Food", allocated_amount: 1000 },
          { id: 2, category: 2, category_name: "Rent", allocated_amount: 2000 }
        ]
      }
    ]);
    setCategories([
      { id: 1, name: "Food", usages: [] },
      { id: 2, name: "Rent", usages: [] }
    ]);
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Wallet className="h-8 w-8 text-blue-500" />
              <h1 className="ml-3 text-2xl font-bold text-gray-900">Budget Tracker</h1>
            </div>
            <button className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700">
              <PlusCircle className="h-5 w-5 mr-2" />
              New Budget
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Overview Cards */}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 mb-8">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <Wallet className="h-6 w-6 text-gray-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Total Budget</dt>
                    <dd className="text-lg font-semibold text-gray-900">$5,000.00</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <PieChart className="h-6 w-6 text-gray-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Spent</dt>
                    <dd className="text-lg font-semibold text-gray-900">$2,450.00</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <Calendar className="h-6 w-6 text-gray-400" />
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">Remaining Days</dt>
                    <dd className="text-lg font-semibold text-gray-900">15</dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Budget Categories */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Budget Categories</h3>
          </div>
          <div className="divide-y divide-gray-200">
            {categories.map((category) => (
              <div key={category.id} className="px-4 py-4 sm:px-6">
                <div className="flex items-center justify-between">
                  <div className="text-sm font-medium text-gray-900">{category.name}</div>
                  <div className="flex items-center">
                    <div className="text-sm text-gray-500 mr-4">
                      {budgets[0]?.allocations.find(a => a.category === category.id)?.allocated_amount.toLocaleString('en-US', {
                        style: 'currency',
                        currency: 'USD'
                      })}
                    </div>
                    <div className="relative w-48 h-2 bg-gray-200 rounded">
                      <div 
                        className="absolute left-0 top-0 h-2 bg-blue-500 rounded"
                        style={{ width: '45%' }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;