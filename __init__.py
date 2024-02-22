
SEP9_FIELDS = [
    "family_name", "last_name", "given_name", "first_name", "additional_name",
    "address_country_code", "state_or_province", "city", "postal_code", "address",
    "mobile_number", "email_address", "birth_date", "birth_place", "birth_country_code",
    "tax_id", "tax_id_name", "occupation", "employer_name", "employer_address",
    "language_code", "id_type", "id_country_code", "id_issue_date", "id_expiration_date",
    "id_number", "photo_id_front", "photo_id_back", "notary_approval_of_photo_id",
    "ip_address", "photo_proof_residence", "sex", "proof_of_income", "proof_of_liveness",
    "referral_id", "bank_account_type", "bank_account_number", "bank_number", "bank_phone_number",
    "bank_branch_number", "clabe_number", "cbu_number", "cbu_alias", "crypto_address",
    "crypto_memo", "organization.name", "organization.VAT_number", "organization.registration_number",
    "organization.registration_date", "organization.registered_address", "organization.number_of_shareholders",
    "organization.shareholder_name", "organization.photo_incorporation_doc", "organization.photo_proof_address",
    "organization.address_country_code", "organization.state_or_province", "organization.city",
    "organization.postal_code", "organization.director_name", "organization.website", "organization.email",
    "organization.phone"
]

ALLOWED_BUT_NOT_SEP9 = [
    "account", 
    "memo",
    "client_domain",
    "type",
    "id"
]

SEP9_VERIFICATION_FIELDS = [
    "mobile_number_verification",
    "email_address_verification"
]

SEP9_ALL_FIELDS = SEP9_FIELDS + SEP9_VERIFICATION_FIELDS