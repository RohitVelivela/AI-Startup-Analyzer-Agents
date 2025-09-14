import React, { useState } from 'react';
import {
  ChevronDownIcon,
  ChevronRightIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
  StarIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline';

const AnalysisReport = ({ results }) => {
  const [expandedReports, setExpandedReports] = useState(new Set());

  const toggleReportExpansion = (index) => {
    const newExpanded = new Set(expandedReports);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedReports(newExpanded);
  };

  const getMarketPositionColor = (position) => {
    switch (position?.toLowerCase()) {
      case 'leader':
        return 'text-green-600 bg-green-100';
      case 'challenger':
        return 'text-blue-600 bg-blue-100';
      case 'follower':
        return 'text-yellow-600 bg-yellow-100';
      case 'niche':
        return 'text-purple-600 bg-purple-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="space-y-6">
      {/* Summary Section */}
      <div className="card p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center">
          <ChartBarIcon className="w-6 h-6 mr-2" />
          Analysis Summary
        </h2>
        <div className="bg-gray-50 rounded-lg p-4">
          <p className="text-gray-700 leading-relaxed">{results.summary}</p>
        </div>
      </div>

      {/* Individual Competitor Reports */}
      <div className="space-y-4">
        <h3 className="text-xl font-semibold text-gray-900">
          Individual Competitor Analysis ({results.reports?.length || 0})
        </h3>

        {results.reports?.map((report, index) => {
          const isExpanded = expandedReports.has(index);
          const competitor = report.competitor;

          return (
            <div key={index} className="card">
              {/* Report Header */}
              <div
                className="p-6 cursor-pointer hover:bg-gray-50 transition-colors duration-200"
                onClick={() => toggleReportExpansion(index)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="flex items-center">
                      {isExpanded ? (
                        <ChevronDownIcon className="w-5 h-5 text-gray-400" />
                      ) : (
                        <ChevronRightIcon className="w-5 h-5 text-gray-400" />
                      )}
                    </div>
                    <div>
                      <h4 className="text-lg font-semibold text-gray-900">
                        {competitor.name}
                      </h4>
                      <p className="text-sm text-gray-600">{competitor.industry}</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-medium ${getMarketPositionColor(
                        report.market_position
                      )}`}
                    >
                      {report.market_position || 'Unknown Position'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Expanded Content */}
              {isExpanded && (
                <div className="px-6 pb-6 border-t border-gray-200">
                  <div className="grid md:grid-cols-2 gap-6 mt-6">
                    {/* Strengths */}
                    <div>
                      <h5 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
                        <ArrowTrendingUpIcon className="w-4 h-4 mr-2 text-green-600" />
                        Strengths
                      </h5>
                      <ul className="space-y-2">
                        {report.strengths?.map((strength, idx) => (
                          <li key={idx} className="text-sm text-gray-700 flex items-start">
                            <span className="text-green-600 mr-2">•</span>
                            {strength}
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* Weaknesses */}
                    <div>
                      <h5 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
                        <ArrowTrendingDownIcon className="w-4 h-4 mr-2 text-red-600" />
                        Weaknesses
                      </h5>
                      <ul className="space-y-2">
                        {report.weaknesses?.map((weakness, idx) => (
                          <li key={idx} className="text-sm text-gray-700 flex items-start">
                            <span className="text-red-600 mr-2">•</span>
                            {weakness}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-6 mt-6">
                    {/* Key Differentiators */}
                    <div>
                      <h5 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
                        <StarIcon className="w-4 h-4 mr-2 text-yellow-600" />
                        Key Differentiators
                      </h5>
                      <ul className="space-y-2">
                        {report.key_differentiators?.map((diff, idx) => (
                          <li key={idx} className="text-sm text-gray-700 flex items-start">
                            <span className="text-yellow-600 mr-2">•</span>
                            {diff}
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* Growth Opportunities */}
                    <div>
                      <h5 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
                        <ChartBarIcon className="w-4 h-4 mr-2 text-blue-600" />
                        Growth Opportunities
                      </h5>
                      <ul className="space-y-2">
                        {report.growth_opportunities?.map((opportunity, idx) => (
                          <li key={idx} className="text-sm text-gray-700 flex items-start">
                            <span className="text-blue-600 mr-2">•</span>
                            {opportunity}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>

                  {/* Pricing Strategy */}
                  {report.pricing_strategy && (
                    <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                      <h5 className="text-sm font-semibold text-gray-900 mb-2">
                        Pricing Strategy
                      </h5>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                        <div>
                          <span className="font-medium text-gray-600">Model:</span>
                          <span className="ml-2 text-gray-900">
                            {report.pricing_strategy.model || 'Unknown'}
                          </span>
                        </div>
                        <div>
                          <span className="font-medium text-gray-600">Positioning:</span>
                          <span className="ml-2 text-gray-900">
                            {report.pricing_strategy.positioning || 'Unknown'}
                          </span>
                        </div>
                        <div>
                          <span className="font-medium text-gray-600">Transparency:</span>
                          <span className="ml-2 text-gray-900">
                            {report.pricing_strategy.transparency || 'Unknown'}
                          </span>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Market Gaps */}
                  {report.market_gaps?.length > 0 && (
                    <div className="mt-6">
                      <h5 className="text-sm font-semibold text-gray-900 mb-3">
                        Market Gaps
                      </h5>
                      <ul className="space-y-2">
                        {report.market_gaps.map((gap, idx) => (
                          <li key={idx} className="text-sm text-gray-700 flex items-start">
                            <span className="text-purple-600 mr-2">•</span>
                            {gap}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default AnalysisReport;