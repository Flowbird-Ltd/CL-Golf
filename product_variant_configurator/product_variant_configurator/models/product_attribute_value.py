# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    bom_component_prod_id = fields.Many2one('product.product', string="BOM Component Product")
    parent_attval_id = fields.Many2one('product.attribute.value', string="Parent Attribute Value")
    child_attval_ids = fields.One2many('product.attribute.value', 'parent_attval_id', string="Child Attribute Value")

    @api.constrains('parent_attval_id')
    def _check_category_recursion(self):
        if not self._check_recursion(parent='parent_attval_id'):
            raise ValidationError(_('You cannot create recursive Parent Attribute Value.'))

    @api.model
    def create(self, vals):
        """Link created attribute value to the associated template if proceed.

        This happens when quick-creating values from the product configurator.
        """
        attr_value = super(ProductAttributeValue, self).create(vals)
        if "template_for_attribute_value" in self.env.context:
            template = self.env["product.template"].browse(
                self.env.context["template_for_attribute_value"]
            )
            line = template.attribute_line_ids.filtered(
                lambda x: x.attribute_id == attr_value.attribute_id
            )
            line.value_ids = [(4, attr_value.id)]
        return attr_value
