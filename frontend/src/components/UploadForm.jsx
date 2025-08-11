import React, { useState, useCallback } from 'react';

const UploadForm = ({ jobDescription, setJobDescription, onOptimize, isLoading, error }) => {
  const [resumeFile, setResumeFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setResumeFile(e.target.files[0]);
    }
  };

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setResumeFile(e.dataTransfer.files[0]);
    }
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    onOptimize(resumeFile, jobDescription);
  };

  return (
    <div className="p-8 bg-white rounded-lg border border-slate-200 shadow-sm space-y-6">
      <div>
        <h2 className="text-lg font-semibold text-slate-800">1. Upload Your Resume</h2>
        <p className="text-sm text-slate-500 mt-1">Accepted formats: PDF, DOCX.</p>
      </div>

      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors duration-200 ${
          isDragging ? 'border-indigo-500 bg-indigo-50' : 'border-slate-300'
        }`}
      >
        <input
          type="file"
          id="resume-upload"
          className="hidden"
          accept=".pdf,.docx"
          onChange={handleFileChange}
        />
        <label htmlFor="resume-upload" className="cursor-pointer">
          <p className="text-slate-500">
            {resumeFile ? `${resumeFile.name}` : 'Drag & drop your file here, or click to select'}
          </p>
        </label>
      </div>

      <div>
        <h2 className="text-lg font-semibold text-slate-800">2. Paste Job Description</h2>
        <p className="text-sm text-slate-500 mt-1">The more detailed, the better the results.</p>
      </div>

      <textarea
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
        placeholder="Paste the full job description here..."
        className="w-full h-48 p-3 border border-slate-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition"
      />

      {error && <p className="text-sm text-red-600 bg-red-100 p-3 rounded-md">{error}</p>}

      <button
        onClick={handleSubmit}
        disabled={isLoading || !resumeFile || !jobDescription}
        className="w-full bg-indigo-600 text-white font-bold py-3 px-4 rounded-md hover:bg-indigo-700 disabled:bg-slate-400 disabled:cursor-not-allowed transition-colors duration-300"
      >
        {isLoading ? 'Optimizing...' : '✨ Optimize My Resume'}
      </button>
    </div>
  );
};

export default UploadForm;