##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, api


class ResUsers(models.Model):

    _inherit = 'res.users'

    def _has_multiple_groups(self, group_ids):
        user_types_category = self.env.ref(
            'base.module_category_user_type', raise_if_not_found=False)
        # remove internal groups that inherit internal groups
        if user_types_category:
            internal_groups = self.env['res.groups'].search([
                ('category_id', '=', user_types_category.id),
                ('implied_ids.category_id', '=', user_types_category.id)])
            group_ids = list(set(group_ids) - set(internal_groups.ids))
        return super()._has_multiple_groups(group_ids)

    @api.model
    def systray_get_activities(self):
        """ We did this to avoid errors when use portal user when the module "Note" is not a depends of this module.
        Only apply this change if the user is portal.
        """
        if self.env.user.has_group('base.group_portal') and self.env['ir.module.module'].sudo().search(
                [('name', '=', 'note')]).state == 'installed':
            self = self.sudo()
        return super().systray_get_activities()
