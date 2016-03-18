/*
SELECT P.name, L.licence_no, P.addr, P.birthday, L.class, DC.description, 
        L.expiring_date
FROM People P, drive_Licence L, driving_condition DC, restriction R
WHERE P.sin = L.sin AND L.licence_no = R.licence_no AND R.r_id = DC.c_id;

SELECT P.name, L.licence_no, P.addr, P.birthday, L.class, L.expiring_date
FROM People P, drive_Licence L
WHERE P.sin = L.sin;
*/

SELECT P.name, L.licence_no, P.addr, P.birthday, L.class, L.expiring_date, 
       (SELECT DC.description
        FROM driving_condition DC, restriction R
        WHERE R.r_id = DC.c_id AND L.licence_no = R.licence_no ) AS condtions
FROM People P, drive_Licence L
WHERE P.sin = L.sin;

SELECT DC.description
 FROM driving_condition DC, restriction R, drive_Licence L
 WHERE R.r_id = DC.c_id AND L.licence_no = R.licence_no;
