from odoo import fields, models
import json
import base64

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def _compute_json_qr(self):
        for rec in self:
            dict_invoice = ''
            if rec.type in ['out_invoice','out_refund'] and rec.state in ['open','paid'] and rec.afip_auth_code != '':
                try:
                    dict_invoice = {
                        'ver': '1',
                        'fecha': str(rec.date_invoice),
                        'cuit': int(rec.company_id.partner_id.main_id_number),
                        'ptoVta': rec.journal_id.point_of_sale_number,
                        'tipoCmp': int(rec.document_type_id.code),
                        'nroCmp': int(rec.display_name.split('-')[2]),
                        'importe': rec.amount_total,
                        'moneda': rec.currency_id.afip_code,
                        'ctz': rec.currency_rate,
                        'tipoDocRec': int(rec.partner_id.main_id_category_id.afip_code),
                        'nroDocRec': int(rec.partner_id.main_id_number),
                        'tipoCodAut': 'E',
                        'codAut': rec.afip_auth_code,
                            }
                except:
                    dict_invoice = 'ERROR'
                    pass
                res = str(dict_invoice)
            else:
                res = 'N/A'
            rec.json_qr = res
            if type(dict_invoice) == dict:
                enc = res.encode()
                b64 = base64.encodestring(enc)
                rec.texto_modificado_qr = 'https://www.afip.gob.ar/fe/qr/?p=' + str(b64)
            else:
                rec.texto_modificado_qr = 'https://www.afip.gob.ar/fe/qr/?ERROR'

    json_qr = fields.Char("JSON QR AFIP",compute=_compute_json_qr)
    texto_modificado_qr = fields.Char('Texto Modificado QR',compute=_compute_json_qr)
