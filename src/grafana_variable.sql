-- PackagePath Variable
SELECT SUBSTRING(purls.package_url, 5, LENGTH(purls.package_url)-4) as package_url
FROM
(select distinct p.id, package_url FROM package p) as purls
left join
(select p.id, m.value from package p left join metric m on p.id = m.package_id where m.key like 'openssf.criticality.raw.stars') as stars
on purls.id = stars.id
ORDER BY CASE when stars.value is null then 1 else 0 end, CAST (stars.value as INT) desc

-- PackageURL Variable
SELECT package_url as package_url FROM package WHERE package_url like '%${PackagePath}'
