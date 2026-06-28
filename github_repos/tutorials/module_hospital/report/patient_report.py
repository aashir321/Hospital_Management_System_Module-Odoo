from datetime import datetime

from odoo import api, models  # pyright: ignore[reportMissingImports]


class ReportPatientMedicalReport(models.AbstractModel):
    _name = 'report.module_hospital.patient_medical_report'
    _description = 'Patient Medical Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['hospital.patients'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'hospital.patients',
            'docs': docs,
            'report_generated_date': datetime.now().strftime('%Y-%m-%d'),
            'report_generated_time': datetime.now().strftime('%H:%M:%S'),
        }