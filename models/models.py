# -*- coding: utf-8 -*-

from re import M
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

    nominames_ids = fields.One2many('pagoaprod.nomina.mes',
                                    'entidad_id',
                                    'Nomina mes')                         
    nomina_ids = fields.One2many('pagoaprod.nomina',
                                    'entidad_id',
                                    'Nomina')                         

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

    #_inherit = 'pagoaprod.abstract.state'
    
    name = fields.Char('Mes')

    entidad_id = fields.Many2one('pagoaprod.pagoaprod',
                                 'Entidad',
                                 default=lambda self: self.env['pagoaprod.pagoaprod']
                                 .search([], limit=1))

class Anno(models.Model):
    _name = 'pagoaprod.anno'

    #_inherit = 'pagoaprod.abstract.state'

    name = fields.Char('Año')

    #mes_ids = fields.Many2many('pagoaprod.mes', string='Meses')

    entidad_id = fields.Many2one('pagoaprod.pagoaprod',
                                 'Entidad',
                                 default=lambda self: self.env['pagoaprod.pagoaprod']
                                 .search([], limit=1))
    
    #def iniciar_progressbar(self):
    #    
    #    self.mes_ids = [(0, 0, {'name': mes.name})
    #                     for mes in self.env['pagoaprod.mes'].search([])
    #                      if not len(self.mes_ids)]
    #    
    #    return super().iniciar_progressbar()
        
class Factura(models.Model):
    _name = 'pagoaprod.factura'

    #_inherit = 'pagoaprod.abstract.state.fact'

    entidad_id = fields.Many2one('pagoaprod.pagoaprod',
                                 'Entidad',
                                 default=lambda self: self.env['pagoaprod.pagoaprod']
                                 .search([], limit=1))
    
    parent_id = fields.Integer(related ="entidad_id.name.id" )

    name = fields.Char('No.')

    fecha = fields.Date('Fecha')
      
    socio_id = fields.Many2one('res.partner',
                              'Socio',
                              domain="[('parent_id','=',parent_id)]")
    
    socio = fields.Char( related='socio_id.name')

    observacion = fields.Char('Observación')
    
    importe = fields.Float('Importe',
                           compute='_importe_factura',
                           store=True)

    factura_linea_ids = fields.One2many('pagoaprod.factura.linea',
                                        'factura_id',
                                        'Detalle')

    nomina_linea_ids = fields.Many2many('pagoaprod.nomina.linea',
                                  string='Detalle Nomina')


    conciliacion_ids = fields.Many2many('pagoaprod.conciliacion',
                                        String='Conciliacion')

    conciliada = fields.Boolean(String='Conciliada',
                                compute='_esta_conciliada',
                                store=True)

    liquidada = fields.Boolean(String='Liquidada',
                               compute='_esta_liquidada',
                               store=True)

    pago = fields.Selection([('efectivo', 'Efectivo'),
                             ('credito', 'Crédito'),
                             ('pendiente', 'Liquidacion')],
                             default='pendiente',
                             string='Forma de Pago')

  
    @api.depends('factura_linea_ids.importe')
    def _importe_factura(self):
      for r in self:
           r.importe = sum(factura_linea.importe for factura_linea in r.factura_linea_ids)

    @api.depends('conciliacion_ids')
    def _esta_conciliada(self):
      for r in self:
          r.conciliada = True if len(r.conciliacion_ids) > 0 else False

    @api.depends('nomina_linea_ids')
    def _esta_liquidada(self):
      for r in self:
        r.liquidada = True if len(r.nomina_linea_ids) > 0 else False


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

    parent_id = fields.Integer(related ="entidad_id.name.id" )

    socio_id = fields.Many2one('res.partner',
                               'Socio',
                               domain="[('parent_id','=',parent_id)]")

    observacion= fields.Char('Observación')

    socio = fields.Char(related='socio_id.name')

    factura_ids = fields.Many2many('pagoaprod.factura',
                                   String='Factura',
                                   domain="[('socio_id', '=', socio_id),"
                                          "('conciliada', '=', False)]")


class NominaAnno(models.Model):
    
    _inherit = 'pagoaprod.abstract.state'

    _name = 'pagoaprod.nomina.anno'
    
    entidad_id = fields.Many2one('pagoaprod.pagoaprod',
                                  'Entidad',
                                  default=lambda self: self.env['pagoaprod.pagoaprod']
                                  .search([], limit=1))

    name = fields.Many2one('pagoaprod.anno',
                            'Año')
    
    nominames_ids = fields.One2many('pagoaprod.nomina.mes',
                                    'nominaanno_id',
                                    'Nomina mes')
    
    def iniciar_progressbar(self):
        
        self.nominames_ids = [(0, 0, {'name': mes.id})
                             for mes in self.env['pagoaprod.mes'].search([])
                             if not len(self.nominames_ids)]
        return super().iniciar_progressbar()


class NominaMes(models.Model):
    _name = 'pagoaprod.nomina.mes'

    _inherit = 'pagoaprod.abstract.state'
    
    entidad_id = fields.Many2one('pagoaprod.pagoaprod',
                                 'Entidad',
                                 default=lambda self: self.env['pagoaprod.pagoaprod']
                                 .search([], limit=1))

    name = fields.Many2one('pagoaprod.mes',
                            'Mes')
    
    nominaanno_id = fields.Many2one('pagoaprod.nomina.anno',
                                    'Nomina Anno',
                                    default=lambda self: self.env['pagoaprod.nomina.anno']
                                    .search([], limit=1))

    nomina_ids = fields.One2many('pagoaprod.nomina',
                                 'nominames_id',
                                 'Nomina')


class Nomina(models.Model):
    _name = 'pagoaprod.nomina'
    
    entidad_id = fields.Many2one('pagoaprod.pagoaprod',
                                  'Entidad',
                                  default=lambda self: self.env['pagoaprod.pagoaprod']
                                  .search([], limit=1))

    nominames_id = fields.Many2one('pagoaprod.nomina.mes',
                                   'Nomina',
                                   default=lambda self: self.env['pagoaprod.nomina.mes']
                                   .search([('state','=','edicion')], limit=1))
    
    anno = fields.Char('Anno',
                       related='nominames_id.nominaanno_id.name.name')

    name = fields.Char('Periodo pago')

    fecha = fields.Date('Fecha confección')
    
    conciliacion = fields.Char('Conciliación no.')

    factura = fields.Char('Factura no.')

    moneda = fields.Char('moneda', default="$")

    producto_id = fields.Many2one('product.template',
                                        'Producto')
    
    importe = fields.Float('Importe',
                           (8,2))

    importe_distribuido = fields.Float('Importe distribuido',
                                        (8,2),
                                        compute='_importe_distribuido')

    importe_nodistribuido = fields.Float('Importe no distribuido',
                                        (8,2),
                                        compute='_importe_nodistribuido')

    nominalinea_ids = fields.One2many('pagoaprod.nomina.linea',
                                      'nomina_id',
                                      'Detalle Nomina')
    
    @api.depends('nominalinea_ids.importe_neto')
    def _importe_distribuido(self):
        for r in self:
            r.importe_distribuido =  sum(linea.importe_neto for linea in r.nominalinea_ids)
    
    @api.depends('importe','importe_distribuido','importe_nodistribuido')
    def _importe_nodistribuido(self):
        for r in self:
            r.importe_nodistribuido =  r.importe -r.importe_distribuido

class NominaLinea(models.Model):
    _name = 'pagoaprod.nomina.linea'

    entidad_id = fields.Integer(default = lambda self: self.env['pagoaprod.pagoaprod']
                                .search([], limit=1).name.id)

    nomina_id = fields.Many2one('pagoaprod.nomina',
                                'Nomina')

    producto_tmpl  = fields.Many2one(related = 'nomina_id.producto_id')
    
    um = fields.Many2one(related='producto_tmpl.uom_id', 
                         string ='Unidad de medida') 

    #attribute_id = fields.Many2one(related = 'producto_tmpl.attribute_id')

    name = fields.Many2one('res.partner',
                              'Socio',
                              domain="[('parent_id','=',entidad_id),\
                                       ('producto_ids','like',producto_tmpl)\
                              ]")
    

    #producto_id = fields.Many2one('product.template.attribute.value',
    #                              'Tipo de producto',
    #                              domain="[('attribute_line_id.product_tmpl_id','=', producto_tmpl)]"
    #                              )
    
    producto_id = fields.Many2one('product.product', 
                                   'Producto',
                                   domain="[('product_tmpl_id','=', producto_tmpl)]"
                                   )
    
    precio = fields.Float('Precio',
                          (8,2))

    cantprod = fields.Float('Producción neta',
                            (8,2))

    factura_ids = fields.Many2many('pagoaprod.factura',
                                      string='Factura',
                                      domain="[('socio_id', '=', name),"
                                             "('conciliada', '=', True),"
                                             "('liquidada', '=', False)]")
#                                             ,"
#                                             "('pago', 'in', ['pendiente','credito'])"
#                                             ",('liquidada', '=', False)]")   

    importe_neto = fields.Float('Importe neto',
                                (8,2),
                                compute='_importe_neto')
    
    aporte2 = fields.Float('Aporte 2%',
                              (8,2),
                              compute='_aporte2')                            

    corte = fields.Float('Corte',
                         (8,2))

    otro = fields.Float('Otros',
                        (8,2))

    importe = fields.Float('A tranferir',
                           (8,2),
                           compute='_importe')

    importe_factura = fields.Float('Facturas',
                                  (8,2),
                                   compute='_importe_factura')

    importe_credito = fields.Float('Crédito',
                                   (8,2),
                                   compute='_importe_credito')

    @api.onchange('producto_id')
    def _precio_default(self):
        self.precio = self.producto_id.lst_price                   

    @api.depends('cantprod', 'precio')
    def _importe_neto(self):
        for r in self:
            r.importe_neto = r.precio * r.cantprod    
    
    @api.depends('importe_neto')
    def _aporte2(self):
        for r in self:
            r.aporte2 = r.importe_neto * 0.02

    @api.depends('factura_ids.importe')
    def _importe_factura(self):
        for r in self:
            total = 0
            for mi_factura in r.factura_ids:
                total += mi_factura.importe if mi_factura.pago == 'pendiente' else 0
            r.importe_factura = total

    @api.depends('factura_ids.importe')
    def _importe_credito(self):
        for r in self:
            total = 0
            for mi_factura in r.factura_ids:
                total += mi_factura.importe if mi_factura.pago == 'credito' else 0
            r.importe_credito = total

    @api.depends('importe_neto', 'aporte2', 'corte', 'otro','importe_factura','importe_credito')
    def _importe(self):
        for r in self:
            r.importe = r.importe_neto - r.aporte2 - r.corte - r.otro - r.importe_factura - r.importe_credito        