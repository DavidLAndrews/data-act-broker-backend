SELECT
    approp.row_number,
    approp.obligations_incurred_total_cpe,
    sf.amount
FROM appropriation as approp
    INNER JOIN sf_133 as sf ON approp.tas = sf.tas
    INNER JOIN submission as sub ON approp.submission_id = sub.submission_id AND
        sf.period = sub.reporting_fiscal_period AND
        sf.fiscal_year = sub.reporting_fiscal_year
WHERE submission_id = {} AND
    sf.line = 2190 AND
    approp.obligations_incurred_total_cpe <> sf.amount