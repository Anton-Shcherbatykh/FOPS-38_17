## Домашнее задание к занятию «Работа с roles» FOPS-38 (Щербатых А.Е.)

### Основная часть
---
Ваша цель — разбить ваш playbook на отдельные roles.

Задача — сделать roles для ClickHouse, Vector и LightHouse и написать playbook для использования этих ролей.

Ожидаемый результат — существуют три ваших репозитория: два с roles и один с playbook.

Что нужно сделать

Создайте в старой версии playbook файл ```requirements.yml``` и заполните его содержимым:

```bash
---
  - src: git@github.com:AlexeySetevoi/ansible-clickhouse.git
    scm: git
    version: "1.13"
    name: clickhouse
``` 
