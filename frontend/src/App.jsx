import React, { useState, useEffect } from 'react';
import UploadForm from './components/UploadForm';
import Preview from './components/Preview';
import ChangesList from './components/ChangesList';
// Hook to use localStorage for state persistence
const useStickyState = (defaultValue, key) => {
  const [value, setValue] = useState(() => {
    const stickyValue = window.localStorage.getItem(key);
    return stickyValue !== null ? JSON.parse(stickyValue) : defaultValue;
  });
  useEffect(() => {
    window.localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);
  return [value, setValue];
};

function App() {
  const [jobDescription, setJobDescription] = useStickyState('', 'jobDescription');
  const [optimizationResult, setOptimizationResult] = useStickyState(null, 'optimizationResult');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000';

  const handleOptimization = async (resumeFile, jd) => {
    if (!resumeFile || !jd) {
      setError('Please upload a resume and provide a job description.');
      return;
    }

    setIsLoading(true);
    setError('');
    setOptimizationResult(null);

    const formData = new FormData();
    formData.append('resume_file', resumeFile);
    formData.append('job_description', jd);

    try {
      const response = await fetch(`${BACKEND_URL}/api/optimize-resume/`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'An unknown error occurred.');
      }

      const data = await response.json();
      setOptimizationResult(data);
    } catch (err) {
      setError(err.message);
      console.error('Optimization failed:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen font-sans text-slate-800">
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h1 className="text-2xl font-bold text-slate-900">📄 AI Resume Optimiser</h1>
          <p className="text-slate-500 mt-1">Tailor your resume to any job description in seconds.</p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">

          {/* Left Column: Form */}
          <div>
            <UploadForm
              jobDescription={jobDescription}
              setJobDescription={setJobDescription}
              onOptimize={handleOptimization}
              isLoading={isLoading}
              error={error}
            />
          </div>

          {/* Right Column: Results */}
          <div>
            {isLoading && (
              <div className="flex flex-col items-center justify-center h-full p-8 bg-white rounded-lg border border-slate-200">
                <div className="loader ease-linear rounded-full border-4 border-t-4 border-gray-200 h-12 w-12 mb-4"></div>
                <style>{`.loader { border-top-color: #3498db; animation: spinner 1.5s linear infinite; } @keyframes spinner { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }`}</style>
                <p className="text-lg font-semibold text-slate-700">Optimizing your resume...</p>
                <p className="text-slate-500">This might take a moment. The AI is hard at work! 🪄</p>
              </div>
            )}

            {optimizationResult && !isLoading && (
              <div className="space-y-8">
                <ChangesList changes={optimizationResult.changes_summary} />
                <Preview
                  resumeText={optimizationResult.optimized_resume_text}
                  downloadLinks={optimizationResult.download_links}
                  backendUrl={BACKEND_URL}
                />
              </div>
            )}

            {!optimizationResult && !isLoading && (
               <div className="flex flex-col items-center justify-center h-full p-8 bg-white rounded-lg border-2 border-dashed border-slate-300">
                  <p className="text-lg font-semibold text-slate-500">Your optimized resume will appear here.</p>
                  <p className="text-slate-400 text-center mt-2">Simply upload your resume, paste the job description, and click "Optimize" to get started.</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;