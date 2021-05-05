SELECT p.package_url
FROM package p left join metric m on p.id = m.package_id
WHERE key like 'openssf.criticality.raw.stars'
order by CAST(value as INT) desc
