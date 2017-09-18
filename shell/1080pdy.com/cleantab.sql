use pdycom_discuz;
delete FROM pre_forum_threadpartake where dateline<(select unix_timestamp()-41536000);
tuncate TABLE pre_ucenter_failedlogins;
tuncate TABLE pre_ucenter_pm_messages;
tuncate TABLE pre_common_connect_guest ;
tuncate TABLE pre_common_member_newprompt ;
delete FROM pre_userlog where logout<(select unix_timestamp()-31536000);
delete from pre_forum_post where first=0 and message regexp '[[:digit:]]{10,}';
SELECT * FROM pre_forum_post WHERE pre_forum_post.`subject` = "" AND authorid NOT in (SELECT pre_common_member.uid FROM pre_common_member where adminid = 1)
delete from pre_forum_post where first=0 and message regexp "%.cc%|%.tk%|%.pw%|%.in%|";
