import Markdown from 'react-markdown'

interface ReasoningDisplayProps {
  reasoning: string[]
}

export function ReasoningDisplay({ reasoning }: ReasoningDisplayProps) {
  return (
    <div className="bg-white rounded-2xl shadow-lg border border-purple-100 p-8">
      <h2 className="text-2xl font-bold mb-6 text-purple-900">Analysis Reasoning</h2>
      <div className="space-y-4">
        {reasoning.map((reason, index) => (
          <div key={index} className="bg-gradient-to-r from-purple-50 to-white p-5 rounded-xl border border-purple-100">
            <div className="flex items-start gap-3">
              <span className="flex-shrink-0 w-6 h-6 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                {index + 1}
              </span>
              <div className="prose prose-sm max-w-none text-gray-700 flex-1">
                <Markdown>{reason}</Markdown>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
