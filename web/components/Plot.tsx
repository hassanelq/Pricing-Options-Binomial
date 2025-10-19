"use client";
import React from 'react';

type PlotType = any;

export default function PlotClient(props: any) {
  const [Plot, setPlot] = React.useState<PlotType | null>(null);

  React.useEffect(() => {
    let mounted = true;
    (async () => {
      const Plotly = await import('plotly.js-dist-min');
      const factory = await import('react-plotly.js/factory');
      const P = factory.default(Plotly as any);
      if (mounted) setPlot(() => P);
    })();
    return () => { mounted = false };
  }, []);

  if (!Plot) return null;
  return <Plot {...props} />
}