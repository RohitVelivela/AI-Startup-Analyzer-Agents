import React from 'react';
import { CheckIcon, ArrowTopRightOnSquareIcon } from '@heroicons/react/24/outline';

const CompetitorCard = ({ competitor, isSelected, onSelectionChange }) => {
  const handleToggleSelection = () => {
    onSelectionChange(!isSelected);
  };

  const handleVisitWebsite = (e) => {
    e.stopPropagation();
    window.open(competitor.url, '_blank', 'noopener,noreferrer');
  };

  return (
    <div
      className={`card p-6 cursor-pointer transition-all duration-200 hover:shadow-xl ${
        isSelected ? 'ring-2 ring-primary-500 bg-primary-50' : 'hover:shadow-lg'
      }`}
      onClick={handleToggleSelection}
    >
      {/* Selection Indicator */}
      <div className="flex justify-between items-start mb-4">
        <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
          isSelected
            ? 'bg-primary-600 border-primary-600'
            : 'border-gray-300 hover:border-primary-400'
        }`}>
          {isSelected && <CheckIcon className="w-4 h-4 text-white" />}
        </div>
        <button
          onClick={handleVisitWebsite}
          className="text-gray-400 hover:text-gray-600 transition-colors duration-200"
          title="Visit website"
        >
          <ArrowTopRightOnSquareIcon className="w-5 h-5" />
        </button>
      </div>

      {/* Company Info */}
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
          {competitor.name}
        </h3>
        <p className="text-sm text-gray-600 line-clamp-3 mb-3">
          {competitor.description || 'No description available'}
        </p>
      </div>

      {/* Company Details */}
      <div className="space-y-2">
        <div className="flex justify-between items-center text-sm">
          <span className="text-gray-500">Industry:</span>
          <span className="text-gray-900 font-medium">
            {competitor.industry || 'Unknown'}
          </span>
        </div>

        {competitor.size && (
          <div className="flex justify-between items-center text-sm">
            <span className="text-gray-500">Size:</span>
            <span className="text-gray-900 font-medium">
              {competitor.size}
            </span>
          </div>
        )}

        {competitor.founded && (
          <div className="flex justify-between items-center text-sm">
            <span className="text-gray-500">Founded:</span>
            <span className="text-gray-900 font-medium">
              {competitor.founded}
            </span>
          </div>
        )}
      </div>

      {/* URL Display */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <p className="text-xs text-gray-500 truncate" title={competitor.url}>
          {competitor.url}
        </p>
      </div>
    </div>
  );
};

export default CompetitorCard;