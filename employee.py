from odoo import models
from odoo import fields
from odoo import _
from odoo import api
from openerp import api
import psycopg2



class CompanyEmployee(models.Model):
    _name = 'company.limited_partner'
    _description = 'limited_partner record'

    limited_partner_name = fields.Char(string='name', required=True)
    parent_id = fields.Char(string='Company')
    job_position = fields.Char(string='Job Position')
    contact_manager = fields.Many2one('res.users', string='Contact Manager')
    contact_country = fields.Many2one('res.country', string='Country')
    partner_id = fields.Many2one('res.partner', string='partner')


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        if res.parent_id:
         self._cr.execute('''INSERT INTO company_limited_partner(limited_partner_name, parent_id,job_position,contact_manager,contact_country,partner_id) SELECT name, (select name from res_partner where id =%s),function,user_id,country_id,id FROM res_partner where id=%s'''% (res.parent_id.id, res.id))
        else:
         self._cr.execute('''INSERT INTO company_limited_partner(limited_partner_name,job_position,contact_manager,contact_country,partner_id) SELECT name,function,user_id,country_id,id FROM res_partner where id=%s'''% res.id)
        return res

    @api.multi
    def write(self, vals):
        for partner in self:
            if partner.id:
             contacts = self.env["company.limited_partner"].search([('partner_id','=',partner.id)])
             if contacts: 
              contact = self.env['company.limited_partner'].browse(contacts[0].id)
              partner_vals = vals.copy()
              if 'user_id' in vals:
                contact.write({'contact_manager': vals['user_id']})
              if 'name' in vals:
                contact.write({'limited_partner_name': vals['name']})
              if 'parent_id' in vals:
                contact.write({'parent_id': vals['parent_id']})
              if 'job_position' in vals:
                contact.write({'job_position': vals['job_position']})
              if 'country_id' in vals:
                contact.write({'contact_country': vals['country_id']})
            super(ResPartner, partner).write(vals)
        return True

    @api.multi
    def unlink(self):
        for partner in self:
            if partner.id:
             for child_contact in partner.child_ids:
              contacts = self.env["company.limited_partner"].search([('partner_id','=',child_contact.id)])
              if contacts: 
               contact = self.env['company.limited_partner'].browse(contacts[0].id)
               contact.unlink()
             contacts = self.env["company.limited_partner"].search([('partner_id','=',partner.id)])
             if contacts:
              contact = self.env['company.limited_partner'].browse(contacts[0].id)
              contact.unlink()
            super(ResPartner, partner).unlink()
        return True