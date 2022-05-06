# Copyright 2020 ForgeFlow S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductTemplateAttributeValue(models.Model):
    _inherit = "product.template.attribute.value"

    def _get_combination_name(self):
        """Overwritten method to avoid:
        Exclude values from single value lines or from no_variant attributes."""
        return ", ".join([ptav.name for ptav in self._filter_single_value_lines()])

    child_attribute_val_ids = fields.Many2many('product.attribute.value', 'table_ptav_pav_child_rel', 'ptav_id', 'pav_id', string="Parent Attribute Value")
    bom_component_prod_id = fields.Many2one('product.product', string="BOM Component Product")

    @api.constrains('child_attribute_val_ids')
    def check_selected_value_on_template(self):
        for ptav in self:
            ptid = ptav.product_tmpl_id
            if ptav.child_attribute_val_ids and ptid and ptid.attribute_line_ids:
                all_pt_att_val_ids = ptid.attribute_line_ids.mapped('value_ids').ids
                for ptav_child_att_val_id in ptav.child_attribute_val_ids:
                    if ptav_child_att_val_id.id not in all_pt_att_val_ids:
                        raise ValidationError(_("Select Attribute Value '%s' is not selected on the Product.") % (ptav_child_att_val_id.name))
