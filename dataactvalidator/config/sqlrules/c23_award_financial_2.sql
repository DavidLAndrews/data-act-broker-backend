SELECT
	af.row_number,
	SUM(af.transaction_obligated_amou) AS transaction_obligated_amou_sum,
  SUM(ap.federal_action_obligation) AS federal_action_obligation_sum
FROM award_financial AS af
	JOIN award_procurement AS ap
		ON af.parent_award_id = ap.parent_award_id
WHERE af.submission_id = {0}
GROUP BY af.parent_award_id
HAVING SUM(af.transaction_obligated_amou) <> SUM(ap.federal_action_obligation)