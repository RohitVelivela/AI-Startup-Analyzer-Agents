import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  ScaleIcon,
  DocumentArrowDownIcon,
  ArrowTopRightOnSquareIcon,
  CheckIcon,
  XMarkIcon,
  MinusIcon
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';
import { competitorAPI } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

const ComparisonPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [companyAUrl, setCompanyAUrl] = useState('');
  const [companyBUrl, setCompanyBUrl] = useState('');
  const [comparisonResults, setComparisonResults] = useState(null);
  const [isComparing, setIsComparing] = useState(false);

  useEffect(() => {
    if (location.state?.companyA && location.state?.companyB) {
      setCompanyAUrl(location.state.companyA);
      setCompanyBUrl(location.state.companyB);
      // Auto-start comparison if URLs are provided
      handleCompare(location.state.companyA, location.state.companyB);
    }
  }, [location.state]);

  const handleCompare = async (urlA = companyAUrl, urlB = companyBUrl) => {
    if (!urlA.trim() || !urlB.trim()) {
      toast.error('Please enter both company URLs');
      return;
    }

    if (urlA === urlB) {
      toast.error('Please enter different URLs for comparison');
      return;
    }

    setIsComparing(true);
    try {
      const results = await competitorAPI.compareCompetitors(urlA, urlB);
      setComparisonResults(results);
      toast.success('Comparison completed successfully!');
    } catch (error) {
      console.error('Comparison failed:', error);
      toast.error('Comparison failed. Please try again.');
    } finally {
      setIsComparing(false);
    }
  };

  const handleExportComparison = async (format) => {
    if (!comparisonResults) {
      toast.error('No comparison results to export');
      return;
    }

    try {
      const blob = await competitorAPI.exportReport(format, 'comparison', comparisonResults);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = `competitor_comparison.${format}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      toast.success(`Comparison exported as ${format.toUpperCase()}`);
    } catch (error) {
      toast.error('Export failed. Please try again.');
    }
  };

  const getAdvantageIcon = (advantage) => {
    switch (advantage) {
      case 'company_a':
        return <CheckIcon className="w-4 h-4 text-green-600" />;
      case 'company_b':
        return <CheckIcon className="w-4 h-4 text-green-600" />;
      case 'tie':
        return <MinusIcon className="w-4 h-4 text-gray-600" />;
      default:
        return <MinusIcon className="w-4 h-4 text-gray-600" />;
    }
  };

  const getAdvantageStyle = (advantage, isCompanyA) => {
    if (advantage === 'tie') return 'bg-gray-50';
    if ((advantage === 'company_a' && isCompanyA) || (advantage === 'company_b' && !isCompanyA)) {
      return 'bg-green-50 border-green-200';
    }
    return 'bg-red-50 border-red-200';
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 flex items-center">
          <ScaleIcon className="w-8 h-8 mr-3" />
          Competitor Comparison
        </h1>
        <p className="mt-2 text-gray-600">
          Compare two competitors side by side to understand their strengths, weaknesses, and market positioning.
        </p>
      </div>

      {/* Input Form */}
      <div className="card p-6 mb-8">
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <label htmlFor="company-a" className="block text-sm font-medium text-gray-700 mb-2">
              Company A URL
            </label>
            <input
              type="url"
              id="company-a"
              value={companyAUrl}
              onChange={(e) => setCompanyAUrl(e.target.value)}
              className="input-field"
              placeholder="https://company-a.com"
              disabled={isComparing}
            />
          </div>
          <div>
            <label htmlFor="company-b" className="block text-sm font-medium text-gray-700 mb-2">
              Company B URL
            </label>
            <input
              type="url"
              id="company-b"
              value={companyBUrl}
              onChange={(e) => setCompanyBUrl(e.target.value)}
              className="input-field"
              placeholder="https://company-b.com"
              disabled={isComparing}
            />
          </div>
        </div>

        <div className="mt-6 flex justify-center">
          <button
            onClick={() => handleCompare()}
            disabled={isComparing}
            className="btn-primary flex items-center px-8 py-3"
          >
            {isComparing ? (
              <>
                <LoadingSpinner className="w-4 h-4 mr-2" />
                Comparing Companies...
              </>
            ) : (
              <>
                <ScaleIcon className="w-4 h-4 mr-2" />
                Compare Companies
              </>
            )}
          </button>
        </div>
      </div>

      {/* Comparison Results */}
      {comparisonResults && (
        <div className="space-y-8">
          {/* Export Controls */}
          <div className="flex justify-end gap-2">
            <button
              onClick={() => handleExportComparison('pdf')}
              className="btn-secondary flex items-center"
            >
              <DocumentArrowDownIcon className="w-4 h-4 mr-2" />
              Export PDF
            </button>
            <button
              onClick={() => handleExportComparison('csv')}
              className="btn-secondary flex items-center"
            >
              <DocumentArrowDownIcon className="w-4 h-4 mr-2" />
              Export CSV
            </button>
          </div>

          {/* Company Headers */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="card p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-gray-900">
                  {comparisonResults.company_a.name}
                </h2>
                <a
                  href={comparisonResults.company_a.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-gray-600"
                >
                  <ArrowTopRightOnSquareIcon className="w-5 h-5" />
                </a>
              </div>
              <p className="text-gray-600 mb-2">{comparisonResults.company_a.industry}</p>
              <p className="text-sm text-gray-700">{comparisonResults.company_a.description}</p>
            </div>

            <div className="card p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-gray-900">
                  {comparisonResults.company_b.name}
                </h2>
                <a
                  href={comparisonResults.company_b.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-gray-400 hover:text-gray-600"
                >
                  <ArrowTopRightOnSquareIcon className="w-5 h-5" />
                </a>
              </div>
              <p className="text-gray-600 mb-2">{comparisonResults.company_b.industry}</p>
              <p className="text-sm text-gray-700">{comparisonResults.company_b.description}</p>
            </div>
          </div>

          {/* Feature Comparison Table */}
          {comparisonResults.feature_comparison && comparisonResults.feature_comparison.length > 0 && (
            <div className="card p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Feature Comparison</h3>
              <div className="overflow-x-auto">
                <table className="min-w-full">
                  <thead>
                    <tr className="border-b border-gray-200">
                      <th className="text-left py-3 px-4 font-medium text-gray-900">Feature</th>
                      <th className="text-left py-3 px-4 font-medium text-gray-900">
                        {comparisonResults.company_a.name}
                      </th>
                      <th className="text-left py-3 px-4 font-medium text-gray-900">
                        {comparisonResults.company_b.name}
                      </th>
                      <th className="text-center py-3 px-4 font-medium text-gray-900">Advantage</th>
                    </tr>
                  </thead>
                  <tbody>
                    {comparisonResults.feature_comparison.map((feature, index) => (
                      <tr key={index} className="border-b border-gray-100">
                        <td className="py-3 px-4 font-medium text-gray-900">
                          {feature.feature}
                        </td>
                        <td
                          className={`py-3 px-4 text-sm text-gray-700 ${getAdvantageStyle(
                            feature.advantage,
                            true
                          )}`}
                        >
                          {feature.company_a}
                        </td>
                        <td
                          className={`py-3 px-4 text-sm text-gray-700 ${getAdvantageStyle(
                            feature.advantage,
                            false
                          )}`}
                        >
                          {feature.company_b}
                        </td>
                        <td className="py-3 px-4 text-center">
                          {getAdvantageIcon(feature.advantage)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Overall Assessment */}
          <div className="card p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Overall Assessment</h3>
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-gray-700 leading-relaxed whitespace-pre-line">
                {comparisonResults.overall_assessment}
              </p>
            </div>
          </div>

          {/* Recommendations */}
          {comparisonResults.recommendations && comparisonResults.recommendations.length > 0 && (
            <div className="card p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Recommendations</h3>
              <ul className="space-y-3">
                {comparisonResults.recommendations.map((recommendation, index) => (
                  <li key={index} className="text-gray-700 flex items-start">
                    <span className="text-primary-600 mr-2 mt-1">•</span>
                    {recommendation}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Empty State */}
      {!comparisonResults && !isComparing && (
        <div className="text-center py-12">
          <ScaleIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No comparison yet</h3>
          <p className="mt-1 text-sm text-gray-500">
            Enter two company URLs above to start comparing competitors.
          </p>
        </div>
      )}
    </div>
  );
};

export default ComparisonPage;