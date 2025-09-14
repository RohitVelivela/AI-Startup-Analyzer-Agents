import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  ChartBarIcon,
  DocumentArrowDownIcon,
  EyeIcon,
  ScaleIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';
import { competitorAPI } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';
import CompetitorCard from '../components/CompetitorCard';
import AnalysisReport from '../components/AnalysisReport';

const Dashboard = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [competitors, setCompetitors] = useState([]);
  const [selectedCompetitors, setSelectedCompetitors] = useState([]);
  const [analysisResults, setAnalysisResults] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showAnalysis, setShowAnalysis] = useState(false);

  useEffect(() => {
    if (location.state?.discoveryResults) {
      setCompetitors(location.state.discoveryResults.competitors);
    } else {
      // If no discovery results, redirect to landing page
      navigate('/');
    }
  }, [location.state, navigate]);

  const handleCompetitorSelection = (competitorUrl, isSelected) => {
    if (isSelected) {
      setSelectedCompetitors([...selectedCompetitors, competitorUrl]);
    } else {
      setSelectedCompetitors(selectedCompetitors.filter(url => url !== competitorUrl));
    }
  };

  const handleAnalyzeSelected = async () => {
    if (selectedCompetitors.length === 0) {
      toast.error('Please select at least one competitor to analyze');
      return;
    }

    setIsAnalyzing(true);
    try {
      const results = await competitorAPI.analyzeCompetitors(selectedCompetitors);
      setAnalysisResults(results);
      setShowAnalysis(true);
      toast.success('Analysis completed successfully!');
    } catch (error) {
      console.error('Analysis failed:', error);
      toast.error('Analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleCompareSelected = () => {
    if (selectedCompetitors.length !== 2) {
      toast.error('Please select exactly 2 competitors to compare');
      return;
    }

    navigate('/compare', {
      state: {
        companyA: selectedCompetitors[0],
        companyB: selectedCompetitors[1]
      }
    });
  };

  const handleExportResults = async (format) => {
    if (!analysisResults) {
      toast.error('No analysis results to export');
      return;
    }

    try {
      const blob = await competitorAPI.exportReport(format, 'analysis', analysisResults);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = `competitor_analysis.${format}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      toast.success(`Report exported as ${format.toUpperCase()}`);
    } catch (error) {
      toast.error('Export failed. Please try again.');
    }
  };

  if (competitors.length === 0) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center">
          <ExclamationTriangleIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No competitors found</h3>
          <p className="mt-1 text-sm text-gray-500">
            We couldn't find any competitors. Try a different search.
          </p>
          <div className="mt-6">
            <button
              onClick={() => navigate('/')}
              className="btn-primary"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Competitor Dashboard</h1>
        <p className="mt-2 text-gray-600">
          Found {competitors.length} competitors. Select them to analyze or compare.
        </p>
      </div>

      {/* Action Buttons */}
      <div className="mb-8 flex flex-wrap gap-4">
        <button
          onClick={handleAnalyzeSelected}
          disabled={selectedCompetitors.length === 0 || isAnalyzing}
          className="btn-primary flex items-center"
        >
          {isAnalyzing ? (
            <>
              <LoadingSpinner className="w-4 h-4 mr-2" />
              Analyzing...
            </>
          ) : (
            <>
              <ChartBarIcon className="w-4 h-4 mr-2" />
              Analyze Selected ({selectedCompetitors.length})
            </>
          )}
        </button>

        <button
          onClick={handleCompareSelected}
          disabled={selectedCompetitors.length !== 2}
          className="btn-secondary flex items-center"
        >
          <ScaleIcon className="w-4 h-4 mr-2" />
          Compare Selected (2)
        </button>

        {analysisResults && (
          <div className="flex gap-2">
            <button
              onClick={() => handleExportResults('pdf')}
              className="btn-secondary flex items-center"
            >
              <DocumentArrowDownIcon className="w-4 h-4 mr-2" />
              Export PDF
            </button>
            <button
              onClick={() => handleExportResults('csv')}
              className="btn-secondary flex items-center"
            >
              <DocumentArrowDownIcon className="w-4 h-4 mr-2" />
              Export CSV
            </button>
          </div>
        )}

        {analysisResults && (
          <button
            onClick={() => setShowAnalysis(!showAnalysis)}
            className="btn-secondary flex items-center"
          >
            <EyeIcon className="w-4 h-4 mr-2" />
            {showAnalysis ? 'Hide' : 'Show'} Analysis
          </button>
        )}
      </div>

      {/* Competitors Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {competitors.map((competitor, index) => (
          <CompetitorCard
            key={index}
            competitor={competitor}
            isSelected={selectedCompetitors.includes(competitor.url)}
            onSelectionChange={(isSelected) =>
              handleCompetitorSelection(competitor.url, isSelected)
            }
          />
        ))}
      </div>

      {/* Analysis Results */}
      {showAnalysis && analysisResults && (
        <AnalysisReport results={analysisResults} />
      )}
    </div>
  );
};

export default Dashboard;