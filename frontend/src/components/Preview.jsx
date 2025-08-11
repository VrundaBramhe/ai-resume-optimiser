import React from 'react';

const Preview = ({ resumeText, downloadLinks, backendUrl }) => {
  return (
    <div className="p-8 bg-white rounded-lg border border-slate-200 shadow-sm">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold text-slate-800">Optimized Resume Preview</h2>
        <div className="flex space-x-2">
            <a
              href={`${backendUrl}${downloadLinks.docx}`}
              download
              className="px-4 py-2 text-sm font-semibold text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors"
            >
              Download DOCX
            </a>
            <a
              href={`${backendUrl}${downloadLinks.pdf}`}
              download
              className="px-4 py-2 text-sm font-semibold text-white bg-red-600 rounded-md hover:bg-red-700 transition-colors"
            >
              Download PDF
            </a>
        </div>
      </div>
      <div
        className="p-6 bg-slate-50 border border-slate-200 rounded-md h-[600px] overflow-y-auto"
      >
        <pre className="whitespace-pre-wrap text-sm text-slate-700 font-sans">{resumeText}</pre>
      </div>
    </div>
  );
};

export default Preview;