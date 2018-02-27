"""All expected field names from the Uber API are defined here."""

ESTIMATE_FIELDS = ['localized_display_name', 'distance', 'display_name',
                   'product_id', 'high_estimate', 'low_estimate', 'duration',
                   'estimate', 'currency_code', 'timestamp']

ESTIMATE_CSV_FIELDS = ESTIMATE_FIELDS

ESTIMATE_STDOUT_FIELDS = ['display_name', 'estimate', 'distance', 'duration']
