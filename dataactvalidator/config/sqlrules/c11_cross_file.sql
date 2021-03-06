-- Each unique PIID (or combination of PIID/ParentAwardId) from file C (award financial) should exist in
-- file D1 (award procurement). Do not process if allocation transfer agency is not null and does
-- not match agency ID (per C24, a non-SQL rule negation)
WITH award_financial_c11_{0} AS
    (SELECT transaction_obligated_amou,
        piid,
        parent_award_id,
        row_number,
        allocation_transfer_agency,
        agency_identifier
    FROM award_financial
    WHERE submission_id = {0}),
award_procurement_c11_{0} AS
    (SELECT piid,
        parent_award_id
    FROM award_procurement
    WHERE submission_id = {0})
SELECT
    af.row_number,
    af.piid,
    af.parent_award_id
FROM award_financial_c11_{0} AS af
WHERE af.transaction_obligated_amou IS NOT NULL
    AND af.piid IS NOT NULL
    AND (COALESCE(af.allocation_transfer_agency, '') = ''
        OR (COALESCE(af.allocation_transfer_agency, '') <> ''
            AND af.allocation_transfer_agency = af.agency_identifier
        )
    )
    AND ((af.parent_award_id IS NULL
            AND NOT EXISTS (
              SELECT 1
              FROM award_procurement_c11_{0} AS ap
              WHERE ap.piid = af.piid
            )
        )
         OR (af.parent_award_id IS NOT NULL
             AND NOT EXISTS (
                 SELECT 1
                 FROM award_procurement_c11_{0} AS ap
                 WHERE ap.piid = af.piid
                     AND COALESCE(ap.parent_award_id, '') = COALESCE(af.parent_award_id, '')
             )
         )
    );
