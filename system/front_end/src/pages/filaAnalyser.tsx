import { Alert } from "../components/ui/alert";
import AnalysisResults from "../components/ui/analysis_result";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "../components/ui/card";
import { env } from "../config/env";
import { Upload, AlertCircle, Loader2 } from "lucide-react";
import { useState } from "react";

const FileAnalyzer = () => {
  const [file, setFile] = useState<File | null>(null);
  const [results, setResults] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isLoadingVirusTotal, setIsLoadingVirusTotal] = useState(false);

  const analyzeFile = async (uploadedFile: any) => {
    setAnalyzing(true);
    setError(null);
    setResults(null);
    setIsLoadingVirusTotal(false);

    try {
      const formData = new FormData();
      formData.append("file", uploadedFile);

      const response = await fetch(`${env.VITE_API_URL}/analyze_ai`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Analysis failed: ${response.statusText}`);
      }

      const data = await response.json();
      setResults(data);

      if (data.virus_total_analysis) {
        setIsLoadingVirusTotal(false);
      } else if (data.virus_total_analysis_id) {
        console.log("Polling VirusTotal status", data.virus_total_analysis_id);
        setIsLoadingVirusTotal(true);
        pollVirusTotalStatus(data.virus_total_analysis_id);
      }
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unknown error occurred");
      }
    } finally {
      setAnalyzing(false);
    }
  };

  const pollVirusTotalStatus = async (virusTotalId: string) => {
    const interval = setInterval(async () => {
      try {
        const response = await fetch(
          `${env.VITE_API_URL}/virus_total_status/${virusTotalId}`
        );
        const data = await response.json();

        if (data.status === "completed") {
          setResults((prevResults) => ({
            ...prevResults,
            virus_total_analysis: data.virus_total_analysis,
          }));
          setIsLoadingVirusTotal(false);
          clearInterval(interval);
        }
      } catch (error) {
        console.error("Error fetching VirusTotal status:", error);
        setIsLoadingVirusTotal(false);
        clearInterval(interval);
      }
    }, 30000);

    return () => clearInterval(interval);
  };

  const handleFileDrop = async (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile?.name.endsWith(".exe")) {
      setFile(droppedFile);
      await analyzeFile(droppedFile);
    } else {
      setError("Please upload a valid .exe file");
    }
  };

  interface FileSelectEvent extends React.ChangeEvent<HTMLInputElement> {
    target: HTMLInputElement & EventTarget;
  }

  const handleFileSelect = async (e: FileSelectEvent) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile?.name.endsWith(".exe")) {
      setFile(selectedFile);
      await analyzeFile(selectedFile);
    } else {
      setError("Please select a valid .exe file");
    }
  };

  return (
    <div
      className="min-h-screen bg-[rgb(27, 37, 46)] p-8"
      style={{ width: "100%", minWidth: "800px" }}
    >
      <div
        className="max-w-4xl mx-auto space-y-6"
        style={{ width: "100%", minWidth: "800px" }}
      >
        <Card style={{ width: "100%", minWidth: "800px", minHeight: "400px" }}>
          <CardHeader>
            <CardTitle className="text-4xl font-bold text-[#30c48b]">
              EXE File Analyzer
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div
              onDrop={handleFileDrop}
              style={{ cursor: "pointer", height: "250px" }}
              onDragOver={(e) => e.preventDefault()}
              className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-gray-400 transition-colors"
            >
              <input
                type="file"
                accept=".exe"
                onChange={handleFileSelect}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="cursor-pointer flex flex-col items-center"
              >
                <Upload className="h-12 w-12 text-gray-400 mb-4" />
                <span className="text-gray-600 text-3xl">
                  Drag and drop an .exe file here, or click to select
                </span>
                <span className="text-sm text-gray-500 text-2xl mt-2">
                  Only .exe files are supported
                </span>
              </label>
            </div>
          </CardContent>
        </Card>

        {error && (
          <Alert
            severity="error"
            title="An error occurred"
            message={error}
            icon={<AlertCircle className="h-4 w-4" />}
            onClose={() => setError(null)}
            className="custom-alert-class"
          />
        )}

        {analyzing && (
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center space-x-4">
                <Loader2 className="h-6 w-6 animate-spin text-blue-500" />
                <span>Analyzing file...</span>
              </div>
            </CardContent>
          </Card>
        )}

        {results && (
          <AnalysisResults
            results={results}
            isLoadingVirusTotal={isLoadingVirusTotal}
          />
        )}
      </div>
    </div>
  );
};

export default FileAnalyzer;
