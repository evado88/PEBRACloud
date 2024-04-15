-- SQLite

-- Remove all peer navigators
DELETE FROM app_peer_navigators WHERE username IN ('test1000','test2','peer100',
'test7000','training25','test1008','est1001','test1004','test1003','training10',
'training2','training1','test1','demo','peer1','peer2','peer50','training2501',
'trainingday2');


-- Remove all participants
DELETE FROM app_participants WHERE username IN ('test1000','test2','peer100',
'test7000','training25','test1008','est1001','test1004','test1003','training10',
'training2','training1','test1','demo','peer1','peer2','peer50','training2501',
'trainingday2');

-- Remove all followups
DELETE FROM app_followups WHERE username IN ('test1000','test2','peer100',
'test7000','training25','test1008','est1001','test1004','test1003','training10',
'training2','training1','test1','demo','peer1','peer2','peer50','training2501',
'trainingday2');

--Renmve all phones
DELETE FROM app_phones WHERE phone_number IN ('260977123001','260977123002','260977123003',
'260977123004','260977123005','260977123456','260977123451','260978989259');


