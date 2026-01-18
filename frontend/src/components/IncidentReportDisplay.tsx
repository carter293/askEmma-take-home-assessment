import type { IncidentReport } from '../client'

interface IncidentReportDisplayProps {
  report: IncidentReport
}

export function IncidentReportDisplay({ report }: IncidentReportDisplayProps) {
  return (
    <div className="bg-white rounded-2xl shadow-lg border border-purple-100 p-8">
      <h2 className="text-2xl font-bold mb-6 text-purple-900">Incident Report</h2>
      <div className="grid grid-cols-1 gap-5">
        <div className="pb-4 border-b border-gray-100">
          <span className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Date/Time</span>
          <p className="mt-1 text-gray-900">{report.date_time_of_incident || 'Not specified'}</p>
        </div>
        <div className="pb-4 border-b border-gray-100">
          <span className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Service User</span>
          <p className="mt-1 text-gray-900">{report.service_user_name}</p>
        </div>
        <div className="pb-4 border-b border-gray-100">
          <span className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Location</span>
          <p className="mt-1 text-gray-900">{report.location_of_incident || 'Not specified'}</p>
        </div>
        <div className="pb-4 border-b border-gray-100">
          <span className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Type of Incident</span>
          <p className="mt-1 text-gray-900">{report.type_of_incident}</p>
        </div>
        <div className="pb-4 border-b border-gray-100">
          <span className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Description</span>
          <p className="mt-1 text-gray-900">{report.description_of_incident}</p>
        </div>
        <div className="pb-4 border-b border-gray-100">
          <span className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Immediate Actions</span>
          <p className="mt-1 text-gray-900">{report.immediate_actions_taken || 'None'}</p>
        </div>
        <div className="grid grid-cols-2 gap-4 pb-4 border-b border-gray-100">
          <div>
            <span className="text-sm font-semibold text-gray-500 uppercase tracking-wide block">First Aid</span>
            <span className={`inline-block mt-1 px-3 py-1 rounded-full text-sm font-medium ${report.first_aid_administered ? 'bg-purple-100 text-purple-700' : 'bg-gray-100 text-gray-700'}`}>
              {report.first_aid_administered ? 'Yes' : 'No'}
            </span>
          </div>
          <div>
            <span className="text-sm font-semibold text-gray-500 uppercase tracking-wide block">Emergency Services</span>
            <span className={`inline-block mt-1 px-3 py-1 rounded-full text-sm font-medium ${report.emergency_services_contacted ? 'bg-purple-100 text-purple-700' : 'bg-gray-100 text-gray-700'}`}>
              {report.emergency_services_contacted ? 'Yes' : 'No'}
            </span>
          </div>
        </div>
        <div className="pb-4 border-b border-gray-100">
          <span className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Who Was Notified</span>
          <p className="mt-1 text-gray-900">{report.who_was_notified || 'Not specified'}</p>
        </div>
        <div className="pb-4 border-b border-gray-100">
          <span className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Witnesses</span>
          <p className="mt-1 text-gray-900">{report.witnesses || 'None'}</p>
        </div>
        <div className="pb-4 border-b border-gray-100">
          <span className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Agreed Next Steps</span>
          <p className="mt-1 text-gray-900">{report.agreed_next_steps || 'None'}</p>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <span className="text-sm font-semibold text-gray-500 uppercase tracking-wide block">Risk Assessment Needed</span>
            <span className={`inline-block mt-1 px-3 py-1 rounded-full text-sm font-medium ${report.risk_assessment_needed ? 'bg-purple-100 text-purple-700' : 'bg-gray-100 text-gray-700'}`}>
              {report.risk_assessment_needed ? 'Yes' : 'No'}
            </span>
          </div>
          <div>
            <span className="text-sm font-semibold text-gray-500 uppercase tracking-wide block">Type</span>
            <p className="mt-1 text-gray-900">{report.risk_assessment_type || 'N/A'}</p>
          </div>
        </div>
      </div>
    </div>
  )
}
