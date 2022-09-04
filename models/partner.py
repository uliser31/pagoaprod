# -*- coding: utf-8 -*-

from dataclasses import field
from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError
#from odoo.exceptions import AccessError, UserError, RedirectWarning, Warning

class Cargo(models.Model):
    _name = 'pagoaprod.cargo'

    name = fields.Char('Cargo')
    
    socio_ids = fields.One2many(
        'res.partner',
         'cargo_id', 
         'Socios'
    )
    
    entidad_id = fields.Many2one('pagoaprod.pagoaprod',
                                  default=lambda self: self.env['pagoaprod.pagoaprod']
                                  .search([],limit=1))
    
    
# Validar  que no se pueda definir mas de 1 presidente y económico

class Entidad(models.Model):
    _inherit = 'res.partner'

    cargo_id = fields.Many2one('pagoaprod.cargo')
    cargo = fields.Char('Cargo', related='cargo_id.name')
    productor = fields.Boolean('Productor')
    producto_ids = fields.Many2many('product.template',string='Productos')

    #@api.constrains('cargo_id')
    #def _validate_cargo(self):
    #    if self.cargo=='Presidente': 
    #        if len(self.env['res.partner'].search([('cargo_id.name',
    #                                                '=',
    #                                                'Presidente')])):
    #            raise ValidationError("No puede existir mas de un cargo de presidente")
            
#default = lambda self: self.env['ctsii.division'].search([], limit = 1)
# class ctsii(models.Model):
#     _name = 'ctsii.ctsii'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100