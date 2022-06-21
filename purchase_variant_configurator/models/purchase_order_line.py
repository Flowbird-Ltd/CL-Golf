# Copyright 2016 Oihane Crucelaegui - AvanzOSC
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2016 ACSONE SA/NV
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models


class PurchaseOrderLine(models.Model):
    _inherit = ["purchase.order.line", "product.configurator"]
    _name = "purchase.order.line"


class product_template(models.Model):
    _inherit = 'product.template'

    def create_auto_bom_from_att_value(self, ppid=False):
        if not ppid:
            return
        prod_obj = self.env['product.product']
        bom_obj = self.env['mrp.bom']
        for tmpl in self:
            av_rel_prod_ids = []
            for ptvv_id in ppid.product_template_attribute_value_ids:
                if ptvv_id.product_attribute_value_id.bom_component_prod_id:
                        av_rel_prod_ids.append(ptvv_id.product_attribute_value_id.bom_component_prod_id.id)
            if av_rel_prod_ids:
                bom_id = bom_obj._bom_find(products=ppid, bom_type='phantom')
                if not bom_id:
                    bom_lines = []
                    for bomprodid in list(set(av_rel_prod_ids)):
                        bom_lines.append((0, 0, {'product_id': bomprodid,
                                                 'product_qty': 1}))
                    bom_obj.create({'product_tmpl_id': tmpl.id,
                                    'product_id': ppid.id,
                                    'type': 'phantom',
                                    'bom_line_ids': bom_lines})

#     def _create_variant_ids(self):
#         res = super(product_template, self)._create_variant_ids()
#         self.create_auto_bom_from_att_value()
#         return res


class ProductConfigurator(models.AbstractModel):
    _inherit = "product.configurator"

    def create_variant_if_needed(self):
        product = super(ProductConfigurator, self).create_variant_if_needed()
        if product:
            product.product_tmpl_id.create_auto_bom_from_att_value(ppid=product)
        return product
