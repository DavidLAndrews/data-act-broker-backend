from collections import OrderedDict
from sqlalchemy import func, cast, Date

from dataactcore.models.stagingModels import DetachedAwardProcurement, AwardProcurement

file_model = DetachedAwardProcurement
staging_model = AwardProcurement

mapping = OrderedDict([
    ('piid', 'piid'),
    ('awardmodificationamendmentnumber', 'award_modification_amendme'),
    ('transaction_number', 'transaction_number'),
    ('referenced_idv_agency_identifier', 'referenced_idv_agency_iden'),
    ('referenced_idv_agency_name', 'referenced_idv_agency_desc'),
    ('parentawardid', 'parent_award_id'),
    ('referenced_idv_modification_number', 'referenced_idv_modificatio'),
    ('federalactionobligation', 'federal_action_obligation'),
    ('total_dollars_obligated', 'total_obligated_amount'),
    ('baseandexercisedoptionsvalue', 'base_exercised_options_val'),
    ('currenttotalvalueofaward', 'current_total_value_award'),
    ('baseandalloptionsvalue', 'base_and_all_options_value'),
    ('potentialtotalvalueofaward', 'potential_total_value_awar'),
    ('actiondate', 'action_date'),
    ('periodofperformancestartdate', 'period_of_performance_star'),
    ('periodofperformancecurrentenddate', 'period_of_performance_curr'),
    ('periodofperformancepotentialenddate', 'period_of_perf_potential_e'),
    ('orderingperiodenddate', 'ordering_period_end_date'),
    ('awardingagencycode', 'awarding_agency_code'),
    ('awardingagencyname', 'awarding_agency_name'),
    ('awardingsubtieragencycode', 'awarding_sub_tier_agency_c'),
    ('awardingsubtieragencyname', 'awarding_sub_tier_agency_n'),
    ('awardingofficecode', 'awarding_office_code'),
    ('awardingofficename', 'awarding_office_name'),
    ('fundingagencycode', 'funding_agency_code'),
    ('fundingagencyname', 'funding_agency_name'),
    ('fundingsubtieragencycode', 'funding_sub_tier_agency_co'),
    ('fundingsubtieragencyname', 'funding_sub_tier_agency_na'),
    ('fundingofficecode', 'funding_office_code'),
    ('fundingofficename', 'funding_office_name'),
    ('foreign_funding', 'foreign_funding'),
    ('foreign_funding_description', 'foreign_funding_desc'),
    ('sam_exception', 'sam_exception'),
    ('sam_exception_description', 'sam_exception_description'),
    ('awardeeorrecipientuniqueidentifier', 'awardee_or_recipient_uniqu'),
    ('awardeeorrecipientlegalentityname', 'awardee_or_recipient_legal'),
    ('vendor_doing_as_business_name', 'vendor_doing_as_business_n'),
    ('cage_code', 'cage_code'),
    ('ultimateparentuniqueidentifier', 'ultimate_parent_unique_ide'),
    ('ultimateparentlegalentityname', 'ultimate_parent_legal_enti'),
    ('legalentitycountrycode', 'legal_entity_country_code'),
    ('legalentitycountryname', 'legal_entity_country_name'),
    ('legalentityaddressline1', 'legal_entity_address_line1'),
    ('legalentityaddressline2', 'legal_entity_address_line2'),
    ('legalentitycityname', 'legal_entity_city_name'),
    ('legalentitystatecode', 'legal_entity_state_code'),
    ('legalentitystatedescription', 'legal_entity_state_descrip'),
    ('legalentityzip_4', 'legal_entity_zip4'),
    ('legalentitycongressionaldistrict', 'legal_entity_congressional'),
    ('vendor_phone_number', 'vendor_phone_number'),
    ('vendor_fax_number', 'vendor_fax_number'),
    ('primaryplaceofperformancecityname', 'place_of_perform_city_name'),
    ('primaryplaceofperformancecountyname', 'place_of_perform_county_na'),
    ('primaryplaceofperformancestatecode', 'place_of_performance_state'),
    ('primaryplaceofperformancestatename', 'place_of_perfor_state_desc'),
    ('primaryplaceofperformancezip+4', 'place_of_performance_zip4a'),
    ('primaryplaceofperformancecongressionaldistrict', 'place_of_performance_congr'),
    ('primaryplaceofperformancecountrycode', 'place_of_perform_country_c'),
    ('primaryplaceofperformancecountryname', 'place_of_perf_country_desc'),
    ('award_or_idv_flag', 'pulled_from'),
    ('contractawardtype', 'contract_award_type'),
    ('contractawardtypedescription', 'contract_award_type_desc'),
    ('idv_type', 'idv_type'),
    ('idv_type_description', 'idv_type_description'),
    ('multiple_or_single_award_idv', 'multiple_or_single_award_i'),
    ('multiple_or_single_award_idv_description', 'multiple_or_single_aw_desc'),
    ('type_of_idc', 'type_of_idc'),
    ('type_of_idc_description', 'type_of_idc_description'),
    ('typeofcontractpricing', 'type_of_contract_pricing'),
    ('typeofcontractpricingdescription', 'type_of_contract_pric_desc'),
    ('awarddescription', 'award_description'),
    ('actiontype', 'action_type'),
    ('actiontypedescription', 'action_type_description'),
    ('solicitation_identifier', 'solicitation_identifier'),
    ('number_of_actions', 'number_of_actions'),
    ('inherently_governmental_function', 'inherently_government_func'),
    ('inherently_governmental_function_description', 'inherently_government_desc'),
    ('product_or_service_code', 'product_or_service_code'),
    ('product_or_service_code_description', 'product_or_service_co_desc'),
    ('contract_bundling', 'contract_bundling'),
    ('contract_bundling_description', 'contract_bundling_descrip'),
    ('dod_claimant_program_code', 'dod_claimant_program_code'),
    ('dod_claimant_program_code_description', 'dod_claimant_prog_cod_desc'),
    ('naics', 'naics'),
    ('naics_description', 'naics_description'),
    ('recovered_materials_sustainability', 'recovered_materials_sustai'),
    ('recovered_materials_sustainability_description', 'recovered_materials_s_desc'),
    ('domestic_or_foreign_entity', 'domestic_or_foreign_entity'),
    ('domestic_or_foreign_entity_description', 'domestic_or_foreign_e_desc'),
    ('dod_acquisition_program', 'program_system_or_equipmen'),
    ('dod_acquisition_program_description', 'program_system_or_equ_desc'),
    ('information_technology_commercial_item_category', 'information_technology_com'),
    ('information_technology_commercial_item_category_description', 'information_technolog_desc'),
    ('epa_designated_product', 'epa_designated_product'),
    ('epa_designated_product_description', 'epa_designated_produc_desc'),
    ('country_of_product_or_service_origin', 'country_of_product_or_serv'),
    ('country_of_product_or_service_origin_description', 'country_of_product_or_desc'),
    ('place_of_manufacture', 'place_of_manufacture'),
    ('place_of_manufacture_description', 'place_of_manufacture_desc'),
    ('subcontracting_plan', 'subcontracting_plan'),
    ('subcontracting_plan_description', 'subcontracting_plan_desc'),
    ('extent_competed', 'extent_competed'),
    ('extent_competed_description', 'extent_compete_description'),
    ('solicitation_procedures', 'solicitation_procedures'),
    ('solicitation_procedures_description', 'solicitation_procedur_desc'),
    ('type_set_aside', 'type_set_aside'),
    ('type_set_aside_description', 'type_set_aside_description'),
    ('evaluated_preference', 'evaluated_preference'),
    ('evaluated_preference_description', 'evaluated_preference_desc'),
    ('research', 'research'),
    ('research_description', 'research_description'),
    ('fair_opportunity_limited_sources', 'fair_opportunity_limited_s'),
    ('fair_opportunity_limited_sources_description', 'fair_opportunity_limi_desc'),
    ('other_than_full_and_open_competition', 'other_than_full_and_open_c'),
    ('other_than_full_and_open_competition_description', 'other_than_full_and_o_desc'),
    ('number_of_offers_received', 'number_of_offers_received'),
    ('commercial_item_acquisition_procedures', 'commercial_item_acquisitio'),
    ('commercial_item_acquisition_procedures_description', 'commercial_item_acqui_desc'),
    ('small_business_competitiveness_demonstration_program', 'small_business_competitive'),
    ('commercial_item_test_program', 'commercial_item_test_progr'),
    ('commercial_item_test_program_description', 'commercial_item_test_desc'),
    ('a76_fair_act_action', 'a_76_fair_act_action'),
    ('a76_fair_act_action_description', 'a_76_fair_act_action_desc'),
    ('fedbizopps', 'fed_biz_opps'),
    ('fedbizoppsdescription', 'fed_biz_opps_description'),
    ('local_area_set_aside', 'local_area_set_aside'),
    ('local_area_set_aside_description', 'local_area_set_aside_desc'),
    ('price_evaluation_adjustment_preference_percent_difference', 'price_evaluation_adjustmen'),
    ('clinger_cohen_act_planning_compliance', 'clinger_cohen_act_planning'),
    ('clinger_cohen_act_planning_compliance_description', 'clinger_cohen_act_pla_desc'),
    ('materials_supplies_article', 'materials_supplies_article'),
    ('materials_supplies_article_description', 'materials_supplies_descrip'),
    ('labor_standards', 'labor_standards'),
    ('labor_standards_description', 'labor_standards_descrip'),
    ('construction_wage_rate_req', 'construction_wage_rate_req'),
    ('construction_wage_rate_req_description', 'construction_wage_rat_desc'),
    ('interagency_contracting_authority', 'interagency_contracting_au'),
    ('interagency_contracting_authority_description', 'interagency_contract_desc'),
    ('other_statutory_authority', 'other_statutory_authority'),
    ('program_acronym', 'program_acronym'),
    ('referenced_idv_type', 'referenced_idv_type'),
    ('referenced_idv_type_description', 'referenced_idv_type_desc'),
    ('referenced_idv_multiple_or_single', 'referenced_mult_or_single'),
    ('referenced_idv_multiple_or_single_description', 'referenced_mult_or_si_desc'),
    ('major_program', 'major_program'),
    ('national_interest_action', 'national_interest_action'),
    ('national_interest_action_description', 'national_interest_desc'),
    ('cost_or_pricing_data', 'cost_or_pricing_data'),
    ('cost_or_pricing_data_description', 'cost_or_pricing_data_desc'),
    ('cost_accounting_standards_clause', 'cost_accounting_standards'),
    ('cost_accounting_standards_clause_description', 'cost_accounting_stand_desc'),
    ('gfe_gfp', 'government_furnished_prope'),
    ('gfe_gfp_description', 'government_furnished_desc'),
    ('sea_transportation', 'sea_transportation'),
    ('sea_transportation_description', 'sea_transportation_desc'),
    ('undefinitized_action', 'undefinitized_action'),
    ('undefinitized_action_description', 'undefinitized_action_desc'),
    ('consolidated_contract', 'consolidated_contract'),
    ('consolidated_contract_description', 'consolidated_contract_desc'),
    ('performance_based_service_acquisition', 'performance_based_service'),
    ('performance_based_service_acquisition_description', 'performance_based_se_desc'),
    ('multi_year_contract', 'multi_year_contract'),
    ('multi_year_contract_description', 'multi_year_contract_desc'),
    ('contract_financing', 'contract_financing'),
    ('contract_financing_description', 'contract_financing_descrip'),
    ('purchase_card_as_payment_method', 'purchase_card_as_payment_m'),
    ('purchase_card_as_payment_method_description', 'purchase_card_as_paym_desc'),
    ('contingency_humanitarian_or_peacekeeping_operation', 'contingency_humanitarian_o'),
    ('contingency_humanitarian_or_peacekeeping_operation_description', 'contingency_humanitar_desc'),
    ('alaskan_native_owned_corporation_or_firm', 'alaskan_native_owned_corpo'),
    ('american_indian_owned_business', 'american_indian_owned_busi'),
    ('indian_tribe_federally_recognized', 'indian_tribe_federally_rec'),
    ('native_hawaiian_owned_business', 'native_hawaiian_owned_busi'),
    ('tribally_owned_business', 'tribally_owned_business'),
    ('veteran_owned_business', 'veteran_owned_business'),
    ('service_disabled_veteran_owned_business', 'service_disabled_veteran_o'),
    ('woman_owned_business', 'woman_owned_business'),
    ('women_owned_small_business', 'women_owned_small_business'),
    ('economically_disadvantaged_women_owned_small_business', 'economically_disadvantaged'),
    ('joint_venture_women_owned_small_business', 'joint_venture_women_owned'),
    ('joint_venture_economically_disadvantaged_women_owned_small_business', 'joint_venture_economically'),
    ('minority_owned_business', 'minority_owned_business'),
    ('subcontinent_asian_asian_indian_american_owned_business', 'subcontinent_asian_asian_i'),
    ('asian_pacific_american_owned_business', 'asian_pacific_american_own'),
    ('black_american_owned_business', 'black_american_owned_busin'),
    ('hispanic_american_owned_business', 'hispanic_american_owned_bu'),
    ('native_american_owned_business', 'native_american_owned_busi'),
    ('other_minority_owned_business', 'other_minority_owned_busin'),
    ('contracting_officer_determination_of_business_size', 'contracting_officers_deter'),
    ('contracting_officer_determination_of_business_size_description', 'contracting_officers_desc'),
    ('emerging_small_business', 'emerging_small_business'),
    ('community_developed_corporation_owned_firm', 'community_developed_corpor'),
    ('labor_surplus_area_firm', 'labor_surplus_area_firm'),
    ('us_federal_government', 'us_federal_government'),
    ('federally_funded_research_and_development_corp', 'federally_funded_research'),
    ('federal_agency', 'federal_agency'),
    ('us_state_government', 'us_state_government'),
    ('us_local_government', 'us_local_government'),
    ('city_local_government', 'city_local_government'),
    ('county_local_government', 'county_local_government'),
    ('inter_municipal_local_government', 'inter_municipal_local_gove'),
    ('local_government_owned', 'local_government_owned'),
    ('municipality_local_government', 'municipality_local_governm'),
    ('school_district_local_government', 'school_district_local_gove'),
    ('township_local_government', 'township_local_government'),
    ('us_tribal_government', 'us_tribal_government'),
    ('foreign_government', 'foreign_government'),
    ('organizational_type', 'organizational_type'),
    ('corporate_entity_not_tax_exempt', 'corporate_entity_not_tax_e'),
    ('corporate_entity_tax_exempt', 'corporate_entity_tax_exemp'),
    ('partnership_or_limited_liability_partnership', 'partnership_or_limited_lia'),
    ('sole_proprietorship', 'sole_proprietorship'),
    ('small_agricultural_cooperative', 'small_agricultural_coopera'),
    ('international_organization', 'international_organization'),
    ('us_government_entity', 'us_government_entity'),
    ('community_development_corporation', 'community_development_corp'),
    ('domestic_shelter', 'domestic_shelter'),
    ('educational_institution', 'educational_institution'),
    ('foundation', 'foundation'),
    ('hospital_flag', 'hospital_flag'),
    ('manufacturer_of_goods', 'manufacturer_of_goods'),
    ('veterinary_hospital', 'veterinary_hospital'),
    ('hispanic_servicing_institution', 'hispanic_servicing_institu'),
    ('contracts', 'contracts'),
    ('grants', 'grants'),
    ('receives_contracts_and_grants', 'receives_contracts_and_gra'),
    ('airport_authority', 'airport_authority'),
    ('council_of_governments', 'council_of_governments'),
    ('housing_authorities_public_tribal', 'housing_authorities_public'),
    ('interstate_entity', 'interstate_entity'),
    ('planning_commission', 'planning_commission'),
    ('port_authority', 'port_authority'),
    ('transit_authority', 'transit_authority'),
    ('subchapter_scorporation', 'subchapter_s_corporation'),
    ('limited_liability_corporation', 'limited_liability_corporat'),
    ('foreign_owned_and_located', 'foreign_owned_and_located'),
    ('for_profit_organization', 'for_profit_organization'),
    ('nonprofit_organization', 'nonprofit_organization'),
    ('other_not_for_profit_organization', 'other_not_for_profit_organ'),
    ('the_abilityone_program', 'the_ability_one_program'),
    ('number_of_employees', 'number_of_employees'),
    ('annual_revenue', 'annual_revenue'),
    ('private_university_or_college', 'private_university_or_coll'),
    ('state_controlled_institution_of_higher_learning', 'state_controlled_instituti'),
    ('c1862_land_grant_college', 'c1862_land_grant_college'),
    ('c1890_land_grant_college', 'c1890_land_grant_college'),
    ('c1994_land_grant_college', 'c1994_land_grant_college'),
    ('minority_institution', 'minority_institution'),
    ('historically_black_college_or_university', 'historically_black_college'),
    ('tribal_college', 'tribal_college'),
    ('alaskan_native_servicing_institution', 'alaskan_native_servicing_i'),
    ('native_hawaiian_servicing_institution', 'native_hawaiian_servicing'),
    ('school_of_forestry', 'school_of_forestry'),
    ('veterinary_college', 'veterinary_college'),
    ('dot_certified_disadvantaged_business_enterprise', 'dot_certified_disadvantage'),
    ('self_certified_small_disadvantaged_business', 'self_certified_small_disad'),
    ('small_disadvantaged_business', 'small_disadvantaged_busine'),
    ('c8a_program_participant', 'c8a_program_participant'),
    ('historically_underutilized_business_zone_hubzone_firm', 'historically_underutilized'),
    ('sba_certified_8a_joint_venture', 'sba_certified_8_a_joint_ve'),
    ('lastmodifieddate', 'last_modified')
])
db_columns = [val for key, val in mapping.items()]


def query_data(session, agency_code, start, end, page_start, page_stop):
    """ Request D1 file data

        Args:
            session - DB session
            agency_code - FREC or CGAC code for generation
            start - Beginning of period for D file
            end - End of period for D file
            page_start - Beginning of pagination
            page_stop - End of pagination
    """
    rows = initial_query(session).\
        filter(file_model.awarding_agency_code == agency_code).\
        filter(func.cast_as_date(file_model.action_date) >= start).\
        filter(func.cast_as_date(file_model.action_date) <= end).\
        slice(page_start, page_stop)

    return rows


def initial_query(session):
    return session.query(*[
        file_model.piid,
        file_model.award_modification_amendme,
        file_model.transaction_number,
        file_model.referenced_idv_agency_iden,
        file_model.referenced_idv_agency_desc,
        file_model.parent_award_id,
        file_model.referenced_idv_modificatio,
        file_model.federal_action_obligation,
        file_model.total_obligated_amount,
        file_model.base_exercised_options_val,
        file_model.current_total_value_award,
        file_model.base_and_all_options_value,
        file_model.potential_total_value_awar,
        func.to_char(cast(file_model.action_date, Date), 'YYYYMMDD'),
        func.to_char(cast(file_model.period_of_performance_star, Date), 'YYYYMMDD'),
        func.to_char(cast(file_model.period_of_performance_curr, Date), 'YYYYMMDD'),
        func.to_char(cast(file_model.period_of_perf_potential_e, Date), 'YYYYMMDD'),
        func.to_char(cast(file_model.ordering_period_end_date, Date), 'YYYYMMDD'),
        file_model.awarding_agency_code,
        file_model.awarding_agency_name,
        file_model.awarding_sub_tier_agency_c,
        file_model.awarding_sub_tier_agency_n,
        file_model.awarding_office_code,
        file_model.awarding_office_name,
        file_model.funding_agency_code,
        file_model.funding_agency_name,
        file_model.funding_sub_tier_agency_co,
        file_model.funding_sub_tier_agency_na,
        file_model.funding_office_code,
        file_model.funding_office_name,
        file_model.foreign_funding,
        file_model.foreign_funding_desc,
        file_model.sam_exception,
        file_model.sam_exception_description,
        file_model.awardee_or_recipient_uniqu,
        file_model.awardee_or_recipient_legal,
        file_model.vendor_doing_as_business_n,
        file_model.cage_code,
        file_model.ultimate_parent_unique_ide,
        file_model.ultimate_parent_legal_enti,
        file_model.legal_entity_country_code,
        file_model.legal_entity_country_name,
        file_model.legal_entity_address_line1,
        file_model.legal_entity_address_line2,
        file_model.legal_entity_city_name,
        file_model.legal_entity_state_code,
        file_model.legal_entity_state_descrip,
        file_model.legal_entity_zip4,
        file_model.legal_entity_congressional,
        file_model.vendor_phone_number,
        file_model.vendor_fax_number,
        file_model.place_of_perform_city_name,
        file_model.place_of_perform_county_na,
        file_model.place_of_performance_state,
        file_model.place_of_perfor_state_desc,
        file_model.place_of_performance_zip4a,
        file_model.place_of_performance_congr,
        file_model.place_of_perform_country_c,
        file_model.place_of_perf_country_desc,
        file_model.pulled_from,
        file_model.contract_award_type,
        file_model.contract_award_type_desc,
        file_model.idv_type,
        file_model.idv_type_description,
        file_model.multiple_or_single_award_i,
        file_model.multiple_or_single_aw_desc,
        file_model.type_of_idc,
        file_model.type_of_idc_description,
        file_model.type_of_contract_pricing,
        file_model.type_of_contract_pric_desc,
        file_model.award_description,
        file_model.action_type,
        file_model.action_type_description,
        file_model.solicitation_identifier,
        file_model.number_of_actions,
        file_model.inherently_government_func,
        file_model.inherently_government_desc,
        file_model.product_or_service_code,
        file_model.product_or_service_co_desc,
        file_model.contract_bundling,
        file_model.contract_bundling_descrip,
        file_model.dod_claimant_program_code,
        file_model.dod_claimant_prog_cod_desc,
        file_model.naics,
        file_model.naics_description,
        file_model.recovered_materials_sustai,
        file_model.recovered_materials_s_desc,
        file_model.domestic_or_foreign_entity,
        file_model.domestic_or_foreign_e_desc,
        file_model.program_system_or_equipmen,
        file_model.program_system_or_equ_desc,
        file_model.information_technology_com,
        file_model.information_technolog_desc,
        file_model.epa_designated_product,
        file_model.epa_designated_produc_desc,
        file_model.country_of_product_or_serv,
        file_model.country_of_product_or_desc,
        file_model.place_of_manufacture,
        file_model.place_of_manufacture_desc,
        file_model.subcontracting_plan,
        file_model.subcontracting_plan_desc,
        file_model.extent_competed,
        file_model.extent_compete_description,
        file_model.solicitation_procedures,
        file_model.solicitation_procedur_desc,
        file_model.type_set_aside,
        file_model.type_set_aside_description,
        file_model.evaluated_preference,
        file_model.evaluated_preference_desc,
        file_model.research,
        file_model.research_description,
        file_model.fair_opportunity_limited_s,
        file_model.fair_opportunity_limi_desc,
        file_model.other_than_full_and_open_c,
        file_model.other_than_full_and_o_desc,
        file_model.number_of_offers_received,
        file_model.commercial_item_acquisitio,
        file_model.commercial_item_acqui_desc,
        file_model.small_business_competitive,
        file_model.commercial_item_test_progr,
        file_model.commercial_item_test_desc,
        file_model.a_76_fair_act_action,
        file_model.a_76_fair_act_action_desc,
        file_model.fed_biz_opps,
        file_model.fed_biz_opps_description,
        file_model.local_area_set_aside,
        file_model.local_area_set_aside_desc,
        file_model.price_evaluation_adjustmen,
        file_model.clinger_cohen_act_planning,
        file_model.clinger_cohen_act_pla_desc,
        file_model.materials_supplies_article,
        file_model.materials_supplies_descrip,
        file_model.labor_standards,
        file_model.labor_standards_descrip,
        file_model.construction_wage_rate_req,
        file_model.construction_wage_rat_desc,
        file_model.interagency_contracting_au,
        file_model.interagency_contract_desc,
        file_model.other_statutory_authority,
        file_model.program_acronym,
        file_model.referenced_idv_type,
        file_model.referenced_idv_type_desc,
        file_model.referenced_mult_or_single,
        file_model.referenced_mult_or_si_desc,
        file_model.major_program,
        file_model.national_interest_action,
        file_model.national_interest_desc,
        file_model.cost_or_pricing_data,
        file_model.cost_or_pricing_data_desc,
        file_model.cost_accounting_standards,
        file_model.cost_accounting_stand_desc,
        file_model.government_furnished_prope,
        file_model.government_furnished_desc,
        file_model.sea_transportation,
        file_model.sea_transportation_desc,
        file_model.undefinitized_action,
        file_model.undefinitized_action_desc,
        file_model.consolidated_contract,
        file_model.consolidated_contract_desc,
        file_model.performance_based_service,
        file_model.performance_based_se_desc,
        file_model.multi_year_contract,
        file_model.multi_year_contract_desc,
        file_model.contract_financing,
        file_model.contract_financing_descrip,
        file_model.purchase_card_as_payment_m,
        file_model.purchase_card_as_paym_desc,
        file_model.contingency_humanitarian_o,
        file_model.contingency_humanitar_desc,
        file_model.alaskan_native_owned_corpo,
        file_model.american_indian_owned_busi,
        file_model.indian_tribe_federally_rec,
        file_model.native_hawaiian_owned_busi,
        file_model.tribally_owned_business,
        file_model.veteran_owned_business,
        file_model.service_disabled_veteran_o,
        file_model.woman_owned_business,
        file_model.women_owned_small_business,
        file_model.economically_disadvantaged,
        file_model.joint_venture_women_owned,
        file_model.joint_venture_economically,
        file_model.minority_owned_business,
        file_model.subcontinent_asian_asian_i,
        file_model.asian_pacific_american_own,
        file_model.black_american_owned_busin,
        file_model.hispanic_american_owned_bu,
        file_model.native_american_owned_busi,
        file_model.other_minority_owned_busin,
        file_model.contracting_officers_deter,
        file_model.contracting_officers_desc,
        file_model.emerging_small_business,
        file_model.community_developed_corpor,
        file_model.labor_surplus_area_firm,
        file_model.us_federal_government,
        file_model.federally_funded_research,
        file_model.federal_agency,
        file_model.us_state_government,
        file_model.us_local_government,
        file_model.city_local_government,
        file_model.county_local_government,
        file_model.inter_municipal_local_gove,
        file_model.local_government_owned,
        file_model.municipality_local_governm,
        file_model.school_district_local_gove,
        file_model.township_local_government,
        file_model.us_tribal_government,
        file_model.foreign_government,
        file_model.organizational_type,
        file_model.corporate_entity_not_tax_e,
        file_model.corporate_entity_tax_exemp,
        file_model.partnership_or_limited_lia,
        file_model.sole_proprietorship,
        file_model.small_agricultural_coopera,
        file_model.international_organization,
        file_model.us_government_entity,
        file_model.community_development_corp,
        file_model.domestic_shelter,
        file_model.educational_institution,
        file_model.foundation,
        file_model.hospital_flag,
        file_model.manufacturer_of_goods,
        file_model.veterinary_hospital,
        file_model.hispanic_servicing_institu,
        file_model.contracts,
        file_model.grants,
        file_model.receives_contracts_and_gra,
        file_model.airport_authority,
        file_model.council_of_governments,
        file_model.housing_authorities_public,
        file_model.interstate_entity,
        file_model.planning_commission,
        file_model.port_authority,
        file_model.transit_authority,
        file_model.subchapter_s_corporation,
        file_model.limited_liability_corporat,
        file_model.foreign_owned_and_located,
        file_model.for_profit_organization,
        file_model.nonprofit_organization,
        file_model.other_not_for_profit_organ,
        file_model.the_ability_one_program,
        file_model.number_of_employees,
        file_model.annual_revenue,
        file_model.private_university_or_coll,
        file_model.state_controlled_instituti,
        file_model.c1862_land_grant_college,
        file_model.c1890_land_grant_college,
        file_model.c1994_land_grant_college,
        file_model.minority_institution,
        file_model.historically_black_college,
        file_model.tribal_college,
        file_model.alaskan_native_servicing_i,
        file_model.native_hawaiian_servicing,
        file_model.school_of_forestry,
        file_model.veterinary_college,
        file_model.dot_certified_disadvantage,
        file_model.self_certified_small_disad,
        file_model.small_disadvantaged_busine,
        file_model.c8a_program_participant,
        file_model.historically_underutilized,
        file_model.sba_certified_8_a_joint_ve,
        func.to_char(cast(file_model.last_modified, Date), 'YYYYMMDD')])
