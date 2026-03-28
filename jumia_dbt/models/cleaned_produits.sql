SELECT
    nom,
    marque,
    prix,
    ancien_prix,
    remise,
    rating,
    url,
    date_scraping,
    ROUND(prix * 0.093, 2) as prix_euro,
    CASE
        WHEN remise >= 50 THEN 'Forte remise'
        WHEN remise >= 20 THEN 'Remise moyenne'
        WHEN remise > 0 THEN 'Petite remise'
        ELSE 'Sans remise'
    END as type_remise
FROM
    {{ ref('stg_produits') }}
