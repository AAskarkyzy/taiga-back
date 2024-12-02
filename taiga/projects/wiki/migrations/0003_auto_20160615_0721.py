# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos INC

# Generated by Django 1.9.2 on 2016-06-15 07:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0002_remove_wikipage_watchers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wikilink',
            options={'ordering': ['project', 'order', 'id'], 'verbose_name': 'wiki link', 'verbose_name_plural': 'wiki links'},
        ),
        migrations.AlterField(
            model_name='wikilink',
            name='order',
            field=models.PositiveSmallIntegerField(default='10000', verbose_name='order'),
        ),
    ]
