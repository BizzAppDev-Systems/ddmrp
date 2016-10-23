# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# © 2016 Aleph Objects, Inc. (https://www.alephobjects.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models, _
from openerp.exceptions import Warning as UserError

_PERIOD_SELECTION = [
    ('monthly', 'Monthly'),
    ('weekly', 'Weekly')
]


class StockBufferDemandEstimatePeriod(models.Model):
    _name = 'stock.buffer.demand.estimate.period'
    _description = 'Stock Buffer Demand Estimate Period'
    _order = 'date_from'

    name = fields.Char(string="Name", required=True)
    period_type = fields.Selection(string="Type",
                                   selection=_PERIOD_SELECTION,
                                   required=True)
    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)

    estimate_ids = fields.One2many(
        comodel_name="stock.buffer.demand.estimate",
        inverse_name="period_id")

    @api.multi
    @api.constrains('name', 'date_from', 'date_to')
    def _check_period(self):
        for period in self:
            self.env.cr.execute('SELECT id \
                FROM stock_buffer_demand_estimate_period \
                WHERE (date_from <= %s and %s <= date_to) \
                AND period_type=%s \
                AND id <> %s', (period.date_to, period.date_from,
                                period.period_type, period.id))
            if self.env.cr.fetchall():
                raise UserError(_('Two periods of the same type '
                                'cannot overlap.'))
