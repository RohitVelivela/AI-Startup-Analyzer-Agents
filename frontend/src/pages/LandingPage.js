import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { MagnifyingGlassIcon, ChartBarIcon, DocumentArrowDownIcon, RocketLaunchIcon } from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';
import { competitorAPI } from '../services/api';
import LoadingSpinner from '../components/LoadingSpinner';

const LandingPage = () => {
  const [inputType, setInputType] = useState('url');
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!inputValue.trim()) {
      toast.error('Please enter a URL or business description');
      return;
    }

    setIsLoading(true);
    try {
      const result = await competitorAPI.discoverCompetitors(inputType, inputValue);

      if (result.total_found === 0) {
        toast.error('No competitors found. Try a different input.');
        return;
      }

      toast.success(`Found ${result.total_found} competitors!`);

      // Navigate to dashboard with results
      navigate('/dashboard', {
        state: {
          discoveryResults: result,
          originalInput: { type: inputType, value: inputValue }
        }
      });
    } catch (error) {
      console.error('Discovery failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const features = [
    {
      name: 'AI-Powered Discovery',
      description: 'Automatically discover competitors using advanced AI algorithms and web intelligence.',
      icon: MagnifyingGlassIcon,
    },
    {
      name: 'Deep Analysis',
      description: 'Get comprehensive business intelligence reports with strengths, weaknesses, and opportunities.',
      icon: ChartBarIcon,
    },
    {
      name: 'Side-by-Side Comparison',
      description: 'Compare competitors feature by feature with actionable insights and recommendations.',
      icon: RocketLaunchIcon,
    },
    {
      name: 'Export & Share',
      description: 'Export detailed reports as PDF or CSV for presentations and further analysis.',
      icon: DocumentArrowDownIcon,
    },
  ];

  return (
    <div className="bg-white">
      {/* Hero section */}
      <div className="relative isolate px-6 pt-14 lg:px-8">
        <div className="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80">
          <div className="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-primary-500 to-secondary-500 opacity-30 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]" />
        </div>

        <div className="mx-auto max-w-4xl py-32 sm:py-48 lg:py-56">
          <div className="text-center">
            <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
              AI-Powered Competitor Intelligence Platform
            </h1>
            <p className="mt-6 text-lg leading-8 text-gray-600">
              Discover, analyze, and compare your competitors with advanced AI agents.
              Get actionable insights to stay ahead in your market.
            </p>
          </div>

          {/* Search form */}
          <div className="mt-16 max-w-2xl mx-auto">
            <form onSubmit={handleSubmit} className="card p-8">
              <div className="space-y-6">
                <div>
                  <label className="text-base font-medium text-gray-900">
                    How would you like to discover competitors?
                  </label>
                  <fieldset className="mt-4">
                    <div className="space-y-4">
                      <div className="flex items-center">
                        <input
                          id="url"
                          name="input-type"
                          type="radio"
                          value="url"
                          checked={inputType === 'url'}
                          onChange={(e) => setInputType(e.target.value)}
                          className="h-4 w-4 border-gray-300 text-primary-600 focus:ring-primary-500"
                        />
                        <label htmlFor="url" className="ml-3 block text-sm font-medium text-gray-700">
                          Company URL
                        </label>
                      </div>
                      <div className="flex items-center">
                        <input
                          id="description"
                          name="input-type"
                          type="radio"
                          value="description"
                          checked={inputType === 'description'}
                          onChange={(e) => setInputType(e.target.value)}
                          className="h-4 w-4 border-gray-300 text-primary-600 focus:ring-primary-500"
                        />
                        <label htmlFor="description" className="ml-3 block text-sm font-medium text-gray-700">
                          Business Description
                        </label>
                      </div>
                    </div>
                  </fieldset>
                </div>

                <div>
                  <label htmlFor="input-value" className="block text-sm font-medium text-gray-700">
                    {inputType === 'url' ? 'Company URL' : 'Business Description'}
                  </label>
                  <div className="mt-1">
                    <input
                      type="text"
                      name="input-value"
                      id="input-value"
                      value={inputValue}
                      onChange={(e) => setInputValue(e.target.value)}
                      className="input-field"
                      placeholder={
                        inputType === 'url'
                          ? 'https://example.com'
                          : 'SaaS platform for project management...'
                      }
                      disabled={isLoading}
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={isLoading}
                  className="w-full btn-primary py-3 text-lg flex items-center justify-center"
                >
                  {isLoading ? (
                    <>
                      <LoadingSpinner className="w-5 h-5 mr-3" />
                      Discovering Competitors...
                    </>
                  ) : (
                    <>
                      <MagnifyingGlassIcon className="w-5 h-5 mr-3" />
                      Discover Competitors
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      {/* Feature section */}
      <div className="py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl lg:text-center">
            <h2 className="text-base font-semibold leading-7 text-primary-600">
              Powerful AI Agents
            </h2>
            <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              Everything you need to analyze your competition
            </p>
            <p className="mt-6 text-lg leading-8 text-gray-600">
              Our multi-agent AI system automatically crawls, analyzes, and compares your competitors
              to provide you with actionable business intelligence.
            </p>
          </div>

          <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-4xl">
            <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-10 lg:max-w-none lg:grid-cols-2 lg:gap-y-16">
              {features.map((feature) => (
                <div key={feature.name} className="relative pl-16">
                  <dt className="text-base font-semibold leading-7 text-gray-900">
                    <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-lg bg-primary-600">
                      <feature.icon className="h-6 w-6 text-white" aria-hidden="true" />
                    </div>
                    {feature.name}
                  </dt>
                  <dd className="mt-2 text-base leading-7 text-gray-600">
                    {feature.description}
                  </dd>
                </div>
              ))}
            </dl>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;