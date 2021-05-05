-- PackagePath Variable
SELECT SUBSTRING(t1.package_url, 5, LENGTH(t1.package_url)-4) as package_url
from
(SELECT distinct p.id, package_url FROM package p) as t1
left join
(SELECT p.id, m.value FROM package p left join metric m on p.id = m.package_id WHERE m.key like 'openssf.criticality.raw.stars') as t2
on t1.id = t2.id
order by case when t2.value is null then 1 else 0 end, CAST (t2.value as INT) desc

-- PackageURL Variable
SELECT package_url as package_url from package where package_url like '%${PackagePath}'
