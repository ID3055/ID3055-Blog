truncate table vrp_users;
truncate table vrp_logs;
truncate table vrp_updates;
truncate table vrp_actlog;
truncate table vrp_request;
INSERT INTO "public"."vrp_users" ("username", "password", "create_time", "create_ip", "last_login_time", "last_login_ip", "role", "id", "use_time", "updated_at", "accesskey", "secretkey", "ps_password", "ps_salt") VALUES ('admin', '$2y$10$mGWQswoWsZO.HtzjRk5.euNr1E0q96pFBCQE4q2ChXEtTPdUnjb4m', '2018-01-29', '127.0.0.1', '2018-07-05', '218.20.8.116', '1', '1', '2019-03-31', '2018-07-05', '397d7c28-06d4-382d-8854-4af3f143d945', 'a56efd57e0b7fbcd6d1cdcec3ecf3d1a0a8ce78c2c5ebd70854af4befe870959', '291f75984b041124a9b4883451d8e9dc', '62d7da349455e882f5f158c2d2cbaf8cd41890cd4cb4446d33d5dd6075196d10');
truncate table vrp_port;
truncate table vrp_task;
truncate table vrp_host;
delete from vrp_zones where value <> 'default';
truncate table vrp_slaves;
truncate table vrp_scan;
truncate table vrp_scano;
update vrp_vuldb set "source" = 1;
truncate table vrp_license;
INSERT INTO "public"."vrp_license" ("id", "info", "key", "status") VALUES ('1', '{"vtime": 1531648800.0, "port_count": 1000, "slave_count": 4, "ip_count": 100, "plugin_count": 0, "task_count": 10}', 'XLippXqGj8mJ5IgTujBiYPcpfAeCG7051i0QctZul6Yt8aSwJf1OE5apnp61q/w/dLhEQ7uAf4lTn7jSvlNyIDouHFF7uhK+i39YOhZCBEUjBVqAHT3mEzuipHWh552iL6KVZGpGYJh31no0jnTFxbJs6YOo6VqgWYGyTHpzAwB97IaslQh5L8o0nnVrzxg6oaQ5/4ED+iINLm0Key90n3lGtLK4YsnI7D30RSDAl3bBR6O+pQEkLdycQUR1TS/VKBv9McDN3MXmlGlCJtng1+PdDg5EQYO0Jko+60rycc7GlW6cCGZoAinEFyosEHG7V1YlRa+YUQzFwBM+jie/2Q==', '0');


