
DROP PROCEDURE SHOW_LAST_X_HISTORY_RECORD_BY_DAYS;
DROP PROCEDURE DEL_HISTORY_RECORD_BY_DAYS;
delimiter $$
CREATE PROCEDURE SHOW_LAST_X_HISTORY_RECORD_BY_DAYS(IN NEED_DAYS INTEGER,IN LIMITS_RECORDS INTEGER)
BEGIN
    -- NEED_DAYS: DELETE HOW SOON BEFORE, EG: 7 ==> 7 days before
    -- LIMITS_RECORDS: HOW MANY RECORDS WILL BE DISPLAYED
    SELECT detect_record.* FROM detect_record,(SELECT id,LEFT(check_timestamp,10) AS rec_timestamp 
    FROM detect_record) AS detect_record2 
    WHERE detect_record.id=detect_record2.id AND 
    rec_timestamp < UNIX_TIMESTAMP(DATE_ADD(CURRENT_DATE(), Interval -NEED_DAYS DAY)) LIMIT LIMITS_RECORDS;

    SELECT defect_result.* FROM defect_result,(SELECT id,LEFT(check_timestamp,10) AS rec_timestamp 
    FROM defect_result) AS defect_result2 
    WHERE defect_result.id=defect_result2.id AND 
    rec_timestamp < UNIX_TIMESTAMP(DATE_ADD(CURRENT_DATE(), Interval -NEED_DAYS DAY)) LIMIT LIMITS_RECORDS;

    SELECT defect_info.* FROM defect_info,detect_record,(SELECT id,LEFT(check_timestamp,10) AS rec_timestamp 
    FROM detect_record) AS detect_record2 
    WHERE defect_info.record_id=detect_record.id AND detect_record.id=detect_record2.id AND
    rec_timestamp < UNIX_TIMESTAMP(DATE_ADD(CURRENT_DATE(), Interval -NEED_DAYS DAY)) LIMIT LIMITS_RECORDS;
	-- release space
	optimize table detect_record;
	optimize table defect_result;
	optimize table defect_info;
END$$
delimiter ;

delimiter $$
CREATE PROCEDURE DEL_HISTORY_RECORD_BY_DAYS(IN NEED_DAYS INTEGER)
BEGIN
    DELETE FROM detect_record WHERE detect_record.id IN(
    SELECT detect_record.id FROM detect_record,(SELECT id,LEFT(check_timestamp,10) AS rec_timestamp 
    FROM detect_record) AS detect_record2 
    WHERE detect_record.id=detect_record2.id AND 
    rec_timestamp < UNIX_TIMESTAMP(DATE_ADD(CURRENT_DATE(), Interval -NEED_DAYS DAY)));

    DELETE FROM detect_record WHERE defect_result.id IN(
    SELECT defect_result.id FROM defect_result,(SELECT id,LEFT(check_timestamp,10) AS rec_timestamp 
    FROM defect_result) AS defect_result2 
    WHERE defect_result.id=defect_result2.id AND 
    rec_timestamp < UNIX_TIMESTAMP(DATE_ADD(CURRENT_DATE(), Interval -NEED_DAYS DAY)));

    DELETE FROM detect_record WHERE defect_info.id IN(
    SELECT defect_info.id FROM defect_info,detect_record,(SELECT id,LEFT(check_timestamp,10) AS rec_timestamp 
    FROM detect_record) AS detect_record2 
    WHERE defect_info.record_id=detect_record.id AND detect_record.id=detect_record2.id AND
    rec_timestamp < UNIX_TIMESTAMP(DATE_ADD(CURRENT_DATE(), Interval -NEED_DAYS DAY)));
	
	-- release space
	optimize table detect_record;
	optimize table defect_result;
	optimize table defect_info;
END$$
delimiter ;

select * from mysql.proc where db = 'defect_tag_v2' and `type` = 'PROCEDURE';

