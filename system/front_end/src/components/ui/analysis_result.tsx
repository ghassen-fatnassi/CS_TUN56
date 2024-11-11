import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './card';
import { Shield, FileText, Hash, Brain, AlertTriangle, Loader2 } from 'lucide-react';

interface AnalysisResultsProps {
  results: {
    file_info: Record<string, string>;
    hashes: Record<string, string>;
    model_analysis: string;
    virus_total_analysis_id?: string;
    virus_total_analysis?: {
      data?: {
        attributes?: {
          stats: Record<string, number>;
          results: Record<string, { result: string; category: string; engine_version: string }>;
          date: number;
        };
      };
    };
  };
  isLoadingVirusTotal: boolean;
}

interface Stats {
  malicious: number;
  undetected: number;
  [key: string]: number;
}

const getDetectionColor = (stats?: Stats): string => {
  if (!stats) return 'text-white';
  const maliciousRatio = stats.malicious / (stats.malicious + stats.undetected);
  if (maliciousRatio > 0.7) return 'text-red-500';
  if (maliciousRatio > 0.3) return 'text-yellow-500';
  return 'text-green-500';
};

const formatDate = (timestamp: number | undefined): string => {
  if (!timestamp) return '';
  return new Date(timestamp * 1000).toLocaleString();
};

const AnalysisResults: React.FC<AnalysisResultsProps> = ({ results, isLoadingVirusTotal }) => {
  return (
    <div className="space-y-6">
      {/* File Information */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <FileText className="h-5 w-5 text-blue-500" />
            <span className="text-[aliceblue]">File Information</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            {Object.entries(results.file_info).map(([key, value]) => (
              <div key={key} className="space-y-1">
                <p className="text-sm text-white">{key.replace(/_/g, ' ').toUpperCase()}</p>
                <p className="font-medium text-[aliceblue]">{value}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Hashes */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Hash className="h-5 w-5 text-purple-500" />
            <span className="text-[aliceblue]">File Hashes</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {Object.entries(results.hashes).map(([key, value]) => (
              <div key={key} className="space-y-1">
                <p className="text-sm text-white">{key.toUpperCase()}</p>
                <p className="font-mono text-sm bg-gray-50 p-2 rounded">{value}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Model Analysis */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Brain className="h-5 w-5 text-indigo-500" />
            <span className="text-[aliceblue]">Model Analysis</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-lg font-medium text-[aliceblue]">{results.model_analysis}</p>
        </CardContent>
      </Card>

      {/* VirusTotal Analysis */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Shield className={`h-5 w-5 ${getDetectionColor(results.virus_total_analysis?.data?.attributes?.stats as Stats)}`} />
            <span className="text-[aliceblue]">VirusTotal Analysis</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {isLoadingVirusTotal ? (
            <div className="flex justify-center items-center p-8">
              <Loader2 className="h-10 w-10 animate-spin text-blue-500" />
              <span className="ml-4">Fetching VirusTotal analysis...</span>
            </div>
          ) : results.virus_total_analysis?.data?.attributes ? (
            <div className="space-y-6">
              {/* Statistics Summary */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {Object.entries(results.virus_total_analysis.data.attributes.stats).map(([key, value]) => (
                  <div key={key} className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-sm">{key.replace(/-/g, ' ').toUpperCase()}</p>
                    <p className="text-2xl font-bold">{value}</p>
                  </div>
                ))}
              </div>

              {/* Scan Results */}
              <div className="space-y-2">
                <h3 className="font-medium text-lg">Detailed Scan Results</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {Object.entries(results.virus_total_analysis.data.attributes.results)
                    .filter(([_, result]) => result.result)
                    .map(([engine, result]) => (
                      <div key={engine} className="bg-gray-50 p-4 rounded-lg">
                        <div className="flex items-center space-x-2">
                          <AlertTriangle className={`h-4 w-4 ${result.category === 'malicious' ? 'text-red-500' : 'text-yellow-500'}`} />
                          <p className="font-medium">{engine}</p>
                        </div>
                        <p className="text-sm mt-1">{result.result}</p>
                        <p className="text-xs mt-1">Version: {result.engine_version}</p>
                      </div>
                    ))}
                </div>
              </div>

              {/* Scan Info */}
              <div className="text-sm text-white">
                <p>Scan completed: {formatDate(results.virus_total_analysis.data.attributes.date)}</p>
              </div>
            </div>
          ) : (
            <p className="text-white">No VirusTotal analysis available</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default AnalysisResults;