query = """
SELECT * FROM recurring_subscription
WHERE (id IN %s OR %s IS NULL) AND
      (%s IS NULL OR due_date = %s) AND
      (%s IS NULL OR EXTRACT(WEEK from due_date) = EXTRACT(WEEK from CURRENT_DATE)) AND
      (%s IS NULL OR EXTRACT(MONTH from due_date) = EXTRACT(MONTH from CURRENT_DATE)) AND
      (%s IS NULL OR EXTRACT(YEAR from due_date) = EXTRACT(YEAR from CURRENT_DATE)) AND
      ((%s IS NULL AND %s IS NULL) OR (%s >= due_date AND %s IS NULL) OR (%s IS NULL AND due_date <= %s) OR (due_date BETWEEN %s AND %s))
"""

params = []
if self.subscription_ids:
    params.append(tuple(self.subscription_ids.ids))
else:
    params.append(None) * 8

if self.frequency == 'daily':
    params.append(date.today())
else:
    params.append(None)
    params.extend([None] * 4)

if self.frequency in ('date', None):
    if self.start_date and not self.end_date:
        params.append(self.start_date)
        params.extend([None] * 3)
    elif self.end_date and not self.start_date:
        params.append(None)  # Add None for start_date
        params.append(self.end_date)
        params.extend([None] * 2)
    elif self.start_date and self.end_date:
        params.extend([self.start_date, self.end_date])
    else:
        params.extend([None] * 4)

self.env.cr.execute(query, tuple(params))
result = self.env.cr.dictfetchall()