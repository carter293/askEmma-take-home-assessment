import { useState } from 'react'
import Markdown from 'react-markdown'
import type { Email } from '../client'

interface EmailsDisplayProps {
  emails: Email[]
}

export function EmailsDisplay({ emails }: EmailsDisplayProps) {
  const [currentIndex, setCurrentIndex] = useState(0)
  const hasMultiple = emails.length > 1

  const goToPrevious = () => {
    setCurrentIndex((prev) => Math.max(0, prev - 1))
  }

  const goToNext = () => {
    setCurrentIndex((prev) => Math.min(emails.length - 1, prev + 1))
  }

  const currentEmail = emails[currentIndex]

  return (
    <div className="bg-white rounded-2xl shadow-lg border border-purple-100 p-8">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-purple-900">
          Generated Emails {hasMultiple && `(${currentIndex + 1}/${emails.length})`}
        </h2>
        {hasMultiple && (
          <div className="flex gap-2">
            <button
              onClick={goToPrevious}
              disabled={currentIndex === 0}
              className="p-2 rounded-lg border border-gray-300 hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
              aria-label="Previous email"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <button
              onClick={goToNext}
              disabled={currentIndex === emails.length - 1}
              className="p-2 rounded-lg border border-gray-300 hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
              aria-label="Next email"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        )}
      </div>
      <div className="border border-gray-200 rounded-xl p-6 bg-gray-50">
        <div className="mb-4 space-y-2">
          <div className="flex items-start">
            <span className="text-sm font-semibold text-gray-500 w-16">To:</span>
            <span className="text-gray-900">{currentEmail.to}</span>
          </div>
          {currentEmail.cc && (
            <div className="flex items-start">
              <span className="text-sm font-semibold text-gray-500 w-16">CC:</span>
              <span className="text-gray-900">{currentEmail.cc}</span>
            </div>
          )}
          {currentEmail.bcc && (
            <div className="flex items-start">
              <span className="text-sm font-semibold text-gray-500 w-16">BCC:</span>
              <span className="text-gray-900">{currentEmail.bcc}</span>
            </div>
          )}
          <div className="flex items-start">
            <span className="text-sm font-semibold text-gray-500 w-16">Subject:</span>
            <span className="text-gray-900 font-medium">{currentEmail.subject}</span>
          </div>
        </div>
        <div className="prose prose-sm max-w-none text-gray-700 bg-white p-4 rounded-lg">
          <Markdown>{currentEmail.body}</Markdown>
        </div>
      </div>
    </div>
  )
}
