import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface InputFormProps {
  form: {
    s0: number;
    k: number;
    t: number;
    r: number;
    sigma: number;
    steps: number;
  };
  setForm: (form: any) => void;
  onCalculate: () => void;
  loading: boolean;
}

export default function InputForm({
  form,
  setForm,
  onCalculate,
  loading,
}: InputFormProps) {
  const handleChange = (field: string, value: string) => {
    setForm({ ...form, [field]: parseFloat(value) || 0 });
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
      <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-100">
        Input Parameters
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div>
          <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
            Spot Price (S₀)
          </label>
          <Input
            type="number"
            value={form.s0}
            onChange={(e) => handleChange("s0", e.target.value)}
            className="w-full"
            step="0.01"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
            Strike Price (K)
          </label>
          <Input
            type="number"
            value={form.k}
            onChange={(e) => handleChange("k", e.target.value)}
            className="w-full"
            step="0.01"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
            Time to Maturity (T) years
          </label>
          <Input
            type="number"
            value={form.t}
            onChange={(e) => handleChange("t", e.target.value)}
            className="w-full"
            step="0.01"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
            Risk-free Rate (r)
          </label>
          <Input
            type="number"
            value={form.r}
            onChange={(e) => handleChange("r", e.target.value)}
            className="w-full"
            step="0.001"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
            Volatility (σ)
          </label>
          <Input
            type="number"
            value={form.sigma}
            onChange={(e) => handleChange("sigma", e.target.value)}
            className="w-full"
            step="0.01"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
            Tree Steps
          </label>
          <Input
            type="number"
            value={form.steps}
            onChange={(e) => handleChange("steps", e.target.value)}
            className="w-full"
            step="10"
          />
        </div>
      </div>

      <div className="mt-6">
        <Button
          onClick={onCalculate}
          disabled={loading}
          className="w-full md:w-auto px-8 py-3 text-lg text-white font-semibold bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-700 hover:to-indigo-700"
        >
          {loading ? "Calculating..." : "Calculate Prices"}
        </Button>
      </div>
    </div>
  );
}
