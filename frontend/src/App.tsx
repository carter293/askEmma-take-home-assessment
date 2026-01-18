import { useState, type FormEvent, useCallback, useRef, useEffect } from 'react'
import { processTranscriptApiV1TranscriptPost } from './client'
import type { PolicyProcessingResultsWithFullPolicy } from './client'
import { FileUpload } from './components/FileUpload'
import { IncidentReportDisplay } from './components/IncidentReportDisplay'
import { EmailsDisplay } from './components/EmailsDisplay'
import { PoliciesDisplay } from './components/PoliciesDisplay'
import { ReasoningDisplay } from './components/ReasoningDisplay'



function App() {
  const [transcript, setTranscript] = useState('')
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [processingResult, setProcessingResult] = useState<PolicyProcessingResultsWithFullPolicy | null>()
  const resultsRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (processingResult && !loading && resultsRef.current) {
      resultsRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }, [processingResult, loading])

  const handleFileChange = useCallback((file: File | null) => {
    setUploadedFile(file)
  }, [])

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (!transcript.trim() && !uploadedFile) return

    setLoading(true)
    setProcessingResult(null)

    try {
      const res = await processTranscriptApiV1TranscriptPost({
        body: {
          text: transcript,
          file: uploadedFile
        }
      })
      setProcessingResult(res.data)
    } catch (error) {
      console.error('Error processing transcript:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setTranscript('')
    setUploadedFile(null)
    setProcessingResult(null)
  }


  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-3 bg-linear-to-r from-purple-600 to-purple-900 bg-clip-text text-transparent">
            Incident Response Analysis
          </h1>
          <p className="text-gray-600">AI-powered incident processing and policy analysis</p>
        </div>

        <form onSubmit={handleSubmit} className="mb-12">
          <div className="bg-white rounded-2xl shadow-lg border border-purple-100 p-8 mb-6">
            <label className="block text-sm font-semibold text-gray-700 mb-3">
              Incident Transcript
            </label>
            <textarea
              value={transcript}
              onChange={(e) => setTranscript(e.target.value)}
              placeholder="Paste or type the incident transcript here..."
              rows={8}
              className="w-full p-4 border border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none transition-all resize-none text-gray-700 placeholder-gray-400"
            />
          </div>

          <div className="bg-white rounded-2xl shadow-lg border border-purple-100 p-8 mb-8">
            <label className="block text-sm font-semibold text-gray-700 mb-3">
              Or Upload File
            </label>
            <FileUpload onFileChange={handleFileChange} file={uploadedFile} />
          </div>

          <div className="flex justify-center gap-4">
            <button
              type="submit"
              disabled={loading || (!transcript.trim() && !uploadedFile)}
              className="px-8 py-3 bg-linear-to-r from-purple-600 to-purple-700 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl hover:from-purple-700 hover:to-purple-800 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105 disabled:transform-none"
            >
              {loading ? 'Processing...' : 'Analyze Incident'}
            </button>

            {(transcript.trim() || uploadedFile || processingResult) && (
              <button
                type="button"
                onClick={handleClear}
                disabled={loading}
                className="px-8 py-3 bg-white border-2 border-gray-300 text-gray-700 rounded-xl font-semibold shadow-lg hover:shadow-xl hover:border-gray-400 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105 disabled:transform-none"
              >
                Clear
              </button>
            )}
          </div>
        </form>

        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-purple-200 border-t-purple-600"></div>
            <p className="mt-4 text-gray-600 font-medium">Processing transcript...</p>
          </div>
        )}

        {processingResult && !loading && (
          <div ref={resultsRef} className="space-y-8">
            <IncidentReportDisplay report={processingResult.report} />
            <EmailsDisplay emails={processingResult.emails} />
            <PoliciesDisplay policiesUsed={processingResult.full_policy_texts} />
            <ReasoningDisplay reasoning={processingResult.reasoning} />
          </div>
        )}
      </div>
    </div>
  )
}

export default App
