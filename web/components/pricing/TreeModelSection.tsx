interface TreeModelSectionProps {
  title: string;
  europeanCall: number;
  europeanPut: number;
  americanCall: number;
  americanPut: number;
  bsPrice: number;
}

export default function TreeModelSection({
  title,
  europeanCall,
  europeanPut,
  americanCall,
  americanPut,
  bsPrice,
}: TreeModelSectionProps) {
  return (
    <div className="bg-gradient-to-br from-violet-50 to-purple-50 dark:from-violet-950/20 dark:to-purple-950/20 rounded-lg shadow-lg p-6 border border-violet-200 dark:border-violet-800">
      <h2 className="text-2xl font-bold mb-6 text-violet-900 dark:text-violet-100">
        {title}
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* European Options */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow">
          <h3 className="text-lg font-semibold mb-4 text-violet-600 dark:text-violet-400">
            European Options
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-gray-600 dark:text-gray-400">Call:</span>
              <span className="text-xl font-bold text-green-600 dark:text-green-400">
                ${europeanCall.toFixed(4)}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600 dark:text-gray-400">Put:</span>
              <span className="text-xl font-bold text-red-600 dark:text-red-400">
                ${europeanPut.toFixed(4)}
              </span>
            </div>
          </div>
        </div>

        {/* American Options */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow">
          <h3 className="text-lg font-semibold mb-4 text-purple-600 dark:text-purple-400">
            American Options
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-gray-600 dark:text-gray-400">Call:</span>
              <span className="text-xl font-bold text-green-600 dark:text-green-400">
                ${americanCall.toFixed(4)}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600 dark:text-gray-400">Put:</span>
              <span className="text-xl font-bold text-red-600 dark:text-red-400">
                ${americanPut.toFixed(4)}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
