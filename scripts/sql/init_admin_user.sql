# USE gather_city;
# INSERT INTO `role` (`id`, `name`, `permission`, `remark`) VALUES (1, 'admin',
#                                                                   '[
#                                                                     {
#                                                                       \"page_code\": \"000\",
#                                                                       \"page_name\": \"管理员设置管理\",
#                                                                       \"permission_code\": \"11\"
#                                                                     }
#                                                                   ]', 'admin');
# 用户名 admin  密码 admin123
INSERT INTO `user_admin` (`username`, `password`, `remark`, `is_supper`)
VALUES ('admin', 'cc0206ff801dab896e7ece169d55d298', 'admin', 1);
