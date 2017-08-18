-- +----------------------------------------------------------------------------+
-- |                          Jeffrey M. Hunter                                 |
-- |                      jhunter@idevelopment.info                             |
-- |                         www.idevelopment.info                              |
-- |----------------------------------------------------------------------------|
-- |      Copyright (c) 1998-2011 Jeffrey M. Hunter. All rights reserved.       |
-- |----------------------------------------------------------------------------|
-- | DATABASE : SQL Server                                                      |
-- | FILE     : create_database.sql                                             |
-- | CLASS    : DDL Examples                                                    |
-- | PURPOSE  : Create a new SQL Server database.                               |
-- | USAGE    :                                                                 |
-- |            osql -Usa                                                       |
-- |            USE master                                                      |
-- |            go                                                              |
-- |            :r create_database.sql                                          |
-- |                                                                            |
-- | NOTE     : As with any code, ensure to test this script in a development   |
-- |            environment before attempting to run it in production.          |
-- +----------------------------------------------------------------------------+


CREATE DATABASE Testdb ON PRIMARY (
    NAME = TestdbSystem
  , FILENAME = 'C:\Program Files\Microsoft SQL Server\MSSQL\Data\TestdbSystem01.mdf'
  , SIZE = 5MB
  , MAXSIZE = 10MB
  , FILEGROWTH = 1MB
)
LOG ON (
    NAME = TestdbLog
  , FILENAME = 'C:\Program Files\Microsoft SQL Server\MSSQL\Data\TestdbSystem01.ldf'
  , SIZE = 1MB
  , MAXSIZE = 5MB
  , FILEGROWTH = 1MB
)

