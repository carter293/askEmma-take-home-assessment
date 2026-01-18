import Markdown from 'react-markdown'

interface PoliciesDisplayProps {
  policiesUsed: string[]
}

export function PoliciesDisplay({ policiesUsed }: PoliciesDisplayProps) {
  return (
    <div className="bg-white rounded-2xl shadow-lg border border-purple-100 p-8">
      <h2 className="text-2xl font-bold mb-6 text-purple-900">Policies Referenced</h2>
      <div className="space-y-4">
        {policiesUsed.map((policy, index) => (
          <div key={index} className="border-l-4 border-purple-500 bg-purple-50 p-5 rounded-r-lg">
            <div className="prose prose-sm max-w-none text-gray-700">
              <Markdown>{policy}</Markdown>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
