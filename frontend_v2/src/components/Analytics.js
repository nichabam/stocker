import React, { useState, useEffect } from 'react';
import { FaChartLine, FaExclamationTriangle, FaDollarSign, FaShoppingCart, FaTrash } from 'react-icons/fa';
import apiClient from '../utils/apiClient';

const Analytics = () => {
  const [analyticsData, setAnalyticsData] = useState({
    predictions: [],
    costAnalysis: [],
    salesPerformance: [],
    menuRecommendations: [],
    dashboardSummary: null
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchAnalyticsData();
  }, []);

  const fetchAnalyticsData = async () => {
    try {
      setLoading(true);
      const [
        predictions,
        costAnalysis,
        salesPerformance,
        menuRecommendations,
        dashboardSummary
      ] = await Promise.all([
        apiClient.getRestockPredictions(),
        apiClient.getCostOptimization(),
        apiClient.getSalesPerformance(),
        apiClient.getMenuRecommendations(),
        apiClient.getDashboardSummary()
      ]);

      setAnalyticsData({
        predictions: predictions || [],
        costAnalysis: costAnalysis || [],
        salesPerformance: salesPerformance || [],
        menuRecommendations: menuRecommendations || [],
        dashboardSummary: dashboardSummary
      });
    } catch (err) {
      setError('Failed to load analytics data');
      console.error('Analytics error:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount || 0);
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <div>Loading analytics...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger">
        {error}
      </div>
    );
  }

  return (
    <div>
      <div style={{ marginBottom: '30px' }}>
        <h1 style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
          <FaChartLine style={{ marginRight: '10px', color: '#007bff' }} />
          📊 Analytics & Predictions
        </h1>
      </div>

      {/* Dashboard Summary */}
      {analyticsData.dashboardSummary && (
        <div className="grid grid-4" style={{ marginBottom: '30px' }}>
          <div className="card stats-card">
            <FaExclamationTriangle size={24} style={{ color: '#dc3545', marginBottom: '10px' }} />
            <h3>{analyticsData.dashboardSummary.items_needing_restock}</h3>
            <p>Need Restock (7 days)</p>
          </div>

          <div className="card stats-card">
            <FaDollarSign size={24} style={{ color: '#28a745', marginBottom: '10px' }} />
            <h3>{formatCurrency(analyticsData.dashboardSummary.total_daily_cost)}</h3>
            <p>Daily Cost</p>
          </div>

          <div className="card stats-card">
            <FaShoppingCart size={24} style={{ color: '#ffc107', marginBottom: '10px' }} />
            <h3>{analyticsData.dashboardSummary.high_performance_items}</h3>
            <p>High Performance</p>
          </div>

          <div className="card stats-card">
            <FaTrash size={24} style={{ color: '#6c757d', marginBottom: '10px' }} />
            <h3>{analyticsData.dashboardSummary.items_to_remove}</h3>
            <p>Consider Removing</p>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="tabs">
        <button
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📊 Overview
        </button>
        <button
          className={`tab ${activeTab === 'predictions' ? 'active' : ''}`}
          onClick={() => setActiveTab('predictions')}
        >
          🔮 Predictions
        </button>
        <button
          className={`tab ${activeTab === 'costs' ? 'active' : ''}`}
          onClick={() => setActiveTab('costs')}
        >
          💰 Cost Analysis
        </button>
        <button
          className={`tab ${activeTab === 'sales' ? 'active' : ''}`}
          onClick={() => setActiveTab('sales')}
        >
          📈 Sales Performance
        </button>
        <button
          className={`tab ${activeTab === 'menu' ? 'active' : ''}`}
          onClick={() => setActiveTab('menu')}
        >
          🍽️ Menu Optimization
        </button>
      </div>

      {/* Overview Tab */}
      <div className={`tab-content ${activeTab === 'overview' ? 'active' : ''}`}>
        <div className="card">
          <h3>Restock Predictions</h3>
          {analyticsData.predictions.length > 0 ? (
            <div>
              {analyticsData.predictions
                .filter(p => p.predicted_restock_date)
                .sort((a, b) => new Date(a.predicted_restock_date) - new Date(b.predicted_restock_date))
                .slice(0, 5)
                .map((prediction, index) => (
                  <div key={index} className="expander">
                    <div className="expander-header">
                      <span>{prediction.item_name}</span>
                      <span style={{ 
                        color: prediction.confidence > 0.7 ? '#28a745' : 
                               prediction.confidence > 0.4 ? '#ffc107' : '#dc3545'
                      }}>
                        {Math.round(prediction.confidence * 100)}% confidence
                      </span>
                    </div>
                    <div className="expander-content">
                      <div className="grid grid-3">
                        <div>
                          <strong>Restock Date:</strong> {formatDate(prediction.predicted_restock_date)}
                        </div>
                        <div>
                          <strong>Stock Life:</strong> {Math.round(prediction.stock_life_days)} days
                        </div>
                        <div>
                          <strong>Optimal Quantity:</strong> {prediction.optimal_restock_quantity}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
            </div>
          ) : (
            <div className="alert alert-info">
              No restock predictions available. Add more data to generate predictions.
            </div>
          )}
        </div>
      </div>

      {/* Predictions Tab */}
      <div className={`tab-content ${activeTab === 'predictions' ? 'active' : ''}`}>
        <div className="card">
          <h3>All Restock Predictions</h3>
          {analyticsData.predictions.length > 0 ? (
            analyticsData.predictions.map((prediction, index) => (
              <div key={index} className="expander">
                <div className="expander-header">
                  <span>{prediction.item_name}</span>
                  <span style={{ 
                    color: prediction.current_stock <= prediction.restock_threshold ? '#dc3545' : '#28a745'
                  }}>
                    {prediction.current_stock} {prediction.unit}
                  </span>
                </div>
                <div className="expander-content">
                  <div className="grid grid-4">
                    <div>
                      <strong>Current Stock:</strong> {prediction.current_stock}
                    </div>
                    <div>
                      <strong>Restock Date:</strong> {formatDate(prediction.predicted_restock_date)}
                    </div>
                    <div>
                      <strong>Stock Life:</strong> {Math.round(prediction.stock_life_days)} days
                    </div>
                    <div>
                      <strong>Daily Consumption:</strong> {prediction.daily_consumption?.toFixed(2) || 0}
                    </div>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="alert alert-info">
              No predictions available. Add more stock history data.
            </div>
          )}
        </div>
      </div>

      {/* Cost Analysis Tab */}
      <div className={`tab-content ${activeTab === 'costs' ? 'active' : ''}`}>
        <div className="card">
          <h3>Cost Optimization Analysis</h3>
          {analyticsData.costAnalysis.length > 0 ? (
            analyticsData.costAnalysis.map((item, index) => (
              <div key={index} className="expander">
                <div className="expander-header">
                  <span>{item.item_name}</span>
                  <span style={{ color: '#28a745' }}>
                    {formatCurrency(item.daily_cost)}/day
                  </span>
                </div>
                <div className="expander-content">
                  <div className="grid grid-3">
                    <div>
                      <strong>Daily Cost:</strong> {formatCurrency(item.daily_cost)}
                    </div>
                    <div>
                      <strong>Optimal Restock:</strong> {item.optimal_restock_quantity}
                    </div>
                    <div>
                      <strong>Waste %:</strong> {Math.round(item.waste_percentage * 100)}%
                    </div>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="alert alert-info">
              No cost analysis available. Add cost data to items.
            </div>
          )}
        </div>
      </div>

      {/* Sales Performance Tab */}
      <div className={`tab-content ${activeTab === 'sales' ? 'active' : ''}`}>
        <div className="card">
          <h3>Sales Performance Analysis</h3>
          {analyticsData.salesPerformance.length > 0 ? (
            analyticsData.salesPerformance
              .sort((a, b) => b.sales_velocity - a.sales_velocity)
              .map((item, index) => (
                <div key={index} className="expander">
                  <div className="expander-header">
                    <span>{item.item_name}</span>
                    <span style={{ 
                      color: item.trend === 'increasing' ? '#28a745' : 
                             item.trend === 'decreasing' ? '#dc3545' : '#6c757d'
                    }}>
                      {item.trend} trend
                    </span>
                  </div>
                  <div className="expander-content">
                    <div className="grid grid-3">
                      <div>
                        <strong>Sales Velocity:</strong> {item.sales_velocity?.toFixed(2) || 0}/day
                      </div>
                      <div>
                        <strong>Total Sales:</strong> {item.total_sales}
                      </div>
                      <div>
                        <strong>Trend:</strong> {item.trend}
                      </div>
                    </div>
                  </div>
                </div>
              ))
          ) : (
            <div className="alert alert-info">
              No sales performance data available. Log some sales to see analytics.
            </div>
          )}
        </div>
      </div>

      {/* Menu Optimization Tab */}
      <div className={`tab-content ${activeTab === 'menu' ? 'active' : ''}`}>
        <div className="card">
          <h3>Menu Optimization Recommendations</h3>
          {analyticsData.menuRecommendations.length > 0 ? (
            analyticsData.menuRecommendations
              .filter(item => item.recommendation !== 'keep')
              .sort((a, b) => b.confidence - a.confidence)
              .map((item, index) => (
                <div key={index} className="expander">
                  <div className="expander-header">
                    <span>{item.item_name}</span>
                    <span style={{ 
                      color: item.recommendation === 'remove' ? '#dc3545' :
                             item.recommendation === 'reduce' ? '#ffc107' : '#28a745'
                    }}>
                      {item.recommendation.toUpperCase()}
                    </span>
                  </div>
                  <div className="expander-content">
                    <div className="grid grid-3">
                      <div>
                        <strong>Recommendation:</strong> {item.recommendation}
                      </div>
                      <div>
                        <strong>Confidence:</strong> {Math.round(item.confidence * 100)}%
                      </div>
                      <div>
                        <strong>Reasoning:</strong> {item.reasoning}
                      </div>
                    </div>
                  </div>
                </div>
              ))
          ) : (
            <div className="alert alert-info">
              No menu optimization recommendations available.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Analytics; 