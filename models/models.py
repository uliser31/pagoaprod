# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AbstractState(models.AbstractModel):
    _name = 'pagoaprod.abstract.state'
    
    state = fields.Selection([('inicio', 'Iniciar'),
                              ('edicion', 'Edición'),
                              ('confirmado', 'Confirmado')],
                              default='inicio',
                              string='Estado')

    def iniciar_progressbar(self):
        
        self.write({'state': 'edicion'})

    #def editar_progressbar(self):
    #    self.ensure_one()    
    #    self.write({'state': 'confirmado'})

    def confirmar_progressbar(self):
        self.write({'state': 'confirmado'})


class AbstractStateFact(models.AbstractModel):
    _name = 'pagoaprod.abstract.state.fact'
    
    state = fields.Selection([('edicion', 'Edición'),
                              ('conciliada', 'Conciliada'),
                              ('pagada', 'Pagada')],
                              default='edicion',
                              string='Estado')

    #def iniciar_progressbar(self):
    #    self.write({'state': 'edicion'})

    def conciliada_progressbar(self):
        self.write({'state': 'conciliada'})

    def pagada_progressbar(self):
        self.write({'state': 'pagada'})

class Pagoaprod(models.Model):
    _name = 'pagoaprod.pagoaprod'
    
    name = fields.Many2one(
        'res.partner', 
        string = "Entidad",
        domain = "[('active', '=' , True),('is_company', '=', True)]")
    
    socio_ids =  fields.One2many('pagoaprod.socio',
        'entidad_id',
        string='Socios')

    producto_ids = fields.One2many('pagoaprod.producto',
                                    'entidad_id',
                                    'Producto')
    
    insumo_ids = fields.One2many('pagoaprod.insumo',
                                 'entidad_id',
                                    'Insumo')

    factura_ids = fields.One2many('pagoaprod.factura',
                                  'entidad_id',
                                    'Factura')                                    

    conciliacion_ids = fields.One2many('pagoaprod.conciliacion',
                                       'entidad_id',
                                       'Conciliacion') 

    mes_ids = fields.One2many('pagoaprod.mes',
                              'entidad_id',
                              'Mes')

    anno_ids = fields.One2many('pagoaprod.anno',
                              'entidad_id',
                              'Anno')                         
    
    cargo_ids = fields.One2many('pagoaprod.cargo',
                              'entidad_id',
                              'Cargo')       

    nominaanno_ids = fields.One2many('pagoaprod.nomina.anno',
                              'entidad_id',
                              'Nomina anno')                         

    presidente = fields.Char('Presidente', compute = '_presidente')
    
    economico = fields.Char('Económico', compute = '_economico')
    
    @api.depends('socio_ids.name.cargo_id')
    def _presidente(self):
        for r in self:
            r.presidente = self.env['res.partner'].search([('cargo_id.name',
                                                                          '=',
                                                                          'Presidente')],
                                                                         limit=1).name
    @api.depends('socio_ids.name.cargo_id')
    def _economico(self):
        for r in self:
            r.economico = self.env['res.partner'].search([('cargo_id.name',
                                                                          '=',
                                                                          'Economico')],
                                                                         limit=1).name

class Cooperativista(models.Model):
    _name = 'pagoaprod.socio'
    
    name = fields.Many2one(
        'res.partner', 
        string="Socio",
        domain="[('parent_id.id', '=', company_id )]")

    entidad_id =  fields.Many2one(
        'pagoaprod.pagoaprod', 
        string="Entidad")
            
    company_id = fields.Integer(
       'Entidad', 
        related = 'entidad_id.name.id'
    )


#class Cargo(models.Model):      DEFINIDO EN -> parner.py
#    _name = 'pagoaprod.cargo'
 

class Producto(models.Model):
    _name = 'pagoaprod.producto'

    #name = fields.Char('Nombre')
    
    name = fields.Many2one(
        'product.product', 
        string = "Nombre",
        domain = "[('active', '=' , True)]") 
    
    entidad_id = fields.Many2one('pagoaprod.pagoaprod',
                                  'Entidad',
                                  default=lambda self: self.env['pagoaprod.pagoaprod']
                                  .search([],limit=1))


class Insumos(models.Model):
    _name = 'pagoaprod.insumo'

    #name = fields.Char('Nombre')
    
    precio = fields.Float('Precio', 
                          related = 'name.lst_price')
    
    unidad_medida_venta = fields.Char('Unidad Medida', 
                                      related = 'name.uom_po_id.name')
    
    name = fields.Many2one(
        'product.product', 
        string = "Nombre",
        domain = "[('active', '=' , True)]") 
    
    entidad_id = fields.Many2one('pagoaprod.pagoaprod',
                                  'Entidad',
                                  default=lambda self: self.env['pagoaprod.pagoaprod']
                                  .search([],limit=1))

class Mes(models.Model):
    _name = 'pagoaprod.mes'

    _inherit = 'pagoaprod.abstract.state'
    
    name = fields.Char('Mes')

    entidad_id = fields.Many2one('pagoaprod.pagoaprod',
                                 'Entidad',
                                 default=lambda self: self.env['pagoaprod.pagoaprod']
                                 .search([], limit=1))

class Anno(models.Model):
    _name = 'pagoaprod.anno'

    _inherit = 'pagoaprod.abstract.state'

    name = fields.Char('Año')

    mes_ids = fields.Many2many('pagoaprod.mes', string='Meses')

    entidad_id = fields.Many2one('pagoaprod.pagoaprod',
                                 'Entidad',
                                 default=lambda self: self.env['pagoaprod.pagoaprod']
                                 .search([], limit=1))
    
    def iniciar_progressbar(self):
        
        self.mes_ids = [(0, 0, {'name': mes.name})
                         for mes in self.env['pagoaprod.mes'].search([])
                          if not len(self.mes_ids)]
        
        return super().iniciar_progressbar()
        
class Factura(models.Model):
    _name = 'pagoaprod.factura'

    _inherit = 'pagoaprod.abstract.state.fact'

    name = fields.Char('No.')

    fecha = fields.Date('Fecha')

    socio_id = fields.Many2one('res.partner',
                                         'Socio')
    
    socio = fields.Char( related='socio_id.name')

    observacion = fields.Char('Observación')
    
    importe = fields.Float('Importe',
                           compute='_importe_factura',
                           store=True)

    factura_linea_ids = fields.One2many('pagoaprod.factura.linea',
                                        'factura_id',
                                        'Detalle')

     #detallenomina_ids = fields.Many2many('pagoaprod.detallenomina',
     #                                     string='Detalle Nomina')

    entidad_id = fields.Many2one('pagoaprod.pagoaprod',
                                 'Entidad',
                                 default=lambda self: self.env['pagoaprod.pagoaprod']
                                 .search([], limit=1))

    conciliacion_ids = fields.Many2many('pagoaprod.conciliacion',
                                        String='Conciliacion')

    conciliada = fields.Boolean(String='Conciliada',
                                compute='_esta_conciliada',
                                store=True)

     #liquidada = fields.Boolean(String='Liquidada',
     #                           compute='_esta_liquidada',
     #                           store=True)

    pago = fields.Selection([('efectivo', 'Efectivo'),
                             ('credito', 'Crédito'),
                             ('pendiente', 'Liquidacion')],
                             default='pendiente',
                             string='Forma de Pago')

    

     #detalle_nomina_ids = fields.Many2many('pagoaprod.detallenomina',
     #                                      'Nomina')

    @api.depends('factura_linea_ids.importe')
    def _importe_factura(self):
      for r in self:
           r.importe = sum(factura_linea.importe for factura_linea in r.factura_linea_ids)

    @api.depends('conciliacion_ids')
    def _esta_conciliada(self):
      for r in self:
          if len(r.conciliacion_ids) :
            r.conciliada_progressbar()
            r.conciliada = True
          else :
            r.conciliada = False

      #r.conciliada = True if len(r.conciliacion_ids) > 0 else False
          


     #@api.depends('detallenomina_ids')
     #def _esta_liquidada(self):
     #  for r in self:
     #      r.liquidada = True if len(r.detallenomina_ids) > 0 else False


class FacturaLinea(models.Model):
    _name = 'pagoaprod.factura.linea'

    #name = fields.Many2one('pagoaprod.insumo',
    #                        'Insumo/Servicio')

    name = fields.Many2one('product.product',
                            'Insumo/Servicio')

    cantidad = fields.Integer('Cantidad')
    
    #precio_default = fields.Float('Precio default', 
    #                              related = 'name.precio')

    precio_default = fields.Float('Precio default', 
                                  related = 'name.lst_price')
    
    #unidad_medida = fields.Char('Unidad Medida', 
    #                              related = 'name.unidad_medida_venta')

    unidad_medida = fields.Char('Unidad Medida', 
                                  related = 'name.uom_po_id.name')

    precio = fields.Float('Precio',default = lambda self: self.precio_default)

    importe = fields.Float('Importe',
                            compute='_importe',
                            store=True)

    factura_id = fields.Many2one('pagoaprod.factura',
                                  'Factura')

    @api.onchange('name')
    def _importe_default(self):
        self.precio = self.precio_default

    @api.depends('cantidad','precio')
    def _importe(self):
         for r in self:
              r.importe = r.precio * r.cantidad


class Conciliacion(models.Model):
         _name = 'pagoaprod.conciliacion'

         name = fields.Date('Fecha')

         entidad_id = fields.Many2one('pagoaprod.pagoaprod',
                                      'Entidad',
                                      default=lambda self: self.env['pagoaprod.pagoaprod']
                                      .search([], limit=1))

         socio_id = fields.Many2one('res.partner',
                                    'Socio')

         observacion= fields.Char('Observación')

         socio = fields.Char(related='socio_id.name')

         factura_ids = fields.Many2many('pagoaprod.factura',
                                        String='Factura',
                                        domain="[('socio_id', '=', socio_id),"
                                               "('conciliada', '=', False)]")


class NominaAnno(models.Model):
    _name = 'pagoaprod.nomina.anno'
    entidad_id = fields.Many2one('pagoaprod.pagoaprod',
                                  'Entidad',
                                  default=lambda self: self.env['pagoaprod.pagoaprod']
                                  .search([], limit=1))

    name = fields.Many2one('pagoaprod.anno',
                            'Año')
