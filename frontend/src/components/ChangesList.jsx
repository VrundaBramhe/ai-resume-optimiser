import React from 'react';

const ChangesList = ({ changes }) => {
  return (
    <div className="p-6 bg-green-50 border border-green-200 rounded-lg shadow-sm">
      <h2 className="text-xl font-bold text-green-900 mb-3">💡 Key Changes & Suggestions</h2>
      <ul className="space-y-2 list-disc list-inside">
        {changes.map((change, index) => (
          <li key={index} className="text-green-800">
            {change}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ChangesList;