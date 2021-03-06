-- PrimaryPlaceOfPerformanceCode is a required field for aggregate and non-aggregate records (RecordType = 1 or 2), and
-- must be 00*****, 00FORGN, or start with a valid 2-character state code.
WITH detached_award_financial_assistance_fabs39_1_{0} AS
    (SELECT submission_id,
        row_number,
        record_type,
        place_of_performance_code
    FROM detached_award_financial_assistance
    WHERE submission_id = {0})
SELECT
    dafa.row_number,
    dafa.record_type,
    dafa.place_of_performance_code
FROM detached_award_financial_assistance_fabs39_1_{0} AS dafa
WHERE dafa.record_type IN (1, 2)
    AND (COALESCE(dafa.place_of_performance_code, '') = ''
        OR (dafa.place_of_performance_code <> '00*****'
            AND UPPER(dafa.place_of_performance_code) <> '00FORGN'
            AND dafa.row_number NOT IN (
                SELECT DISTINCT sub_dafa.row_number
                FROM detached_award_financial_assistance_fabs39_1_{0} AS sub_dafa
                JOIN states
                    ON UPPER(SUBSTRING(sub_dafa.place_of_performance_code, 1, 2)) = states.state_code
            )
        )
    );
