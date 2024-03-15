# Generated by Django 4.2 on 2024-03-14 12:40

from django.db import migrations, models
import django.db.models.deletion
import garpix_page.fields.grapes_js_html
import garpix_page.utils.all_sites
import garpix_utils.file.file_field


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('garpix_page', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GrapesJsHtmlComponent',
            fields=[
                ('basecomponent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='garpix_page.basecomponent')),
                ('html', garpix_page.fields.grapes_js_html.GrapesJsHtmlField()),
            ],
            options={
                'verbose_name': 'GrapesJs компонент',
                'verbose_name_plural': 'GrapesJs компоненты',
            },
            bases=('garpix_page.basecomponent',),
        ),
        migrations.AddField(
            model_name='basecomponent',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Запись удалена'),
        ),
        migrations.AddField(
            model_name='basepage',
            name='url',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Полный URL страницы'),
        ),
        migrations.AlterField(
            model_name='basecomponent',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='basepage',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype'),
        ),
        migrations.CreateModel(
            name='SeoTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Включено')),
                ('rule_field', models.CharField(max_length=255, verbose_name='Поле')),
                ('model_rule_value', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название')),
                ('rule_value', models.CharField(blank=True, max_length=255, null=True, verbose_name='Значение')),
                ('seo_title', models.CharField(blank=True, default='', max_length=250, verbose_name='SEO заголовок страницы (title)')),
                ('seo_title_ru', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SEO заголовок страницы (title)')),
                ('seo_keywords', models.CharField(blank=True, default='', max_length=250, verbose_name='SEO ключевые слова (keywords)')),
                ('seo_keywords_ru', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SEO ключевые слова (keywords)')),
                ('seo_description', models.TextField(blank=True, default='', verbose_name='SEO описание (description)')),
                ('seo_description_ru', models.TextField(blank=True, default='', null=True, verbose_name='SEO описание (description)')),
                ('seo_author', models.CharField(blank=True, default='', max_length=250, verbose_name='SEO автор (author)')),
                ('seo_author_ru', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SEO автор (author)')),
                ('seo_og_type', models.CharField(blank=True, default='website', max_length=250, verbose_name='SEO og:type')),
                ('seo_image', models.FileField(blank=True, null=True, upload_to=garpix_utils.file.file_field.get_file_path, verbose_name='SEO изображение')),
                ('priority_order', models.PositiveIntegerField(default=1, help_text='Чем меньше число, тем выше приоритет', verbose_name='Приоритетность применения')),
                ('sites', models.ManyToManyField(default=garpix_page.utils.all_sites.get_all_sites, to='sites.site', verbose_name='Сайты для применения')),
            ],
            options={
                'verbose_name': 'Шаблон для seo',
                'verbose_name_plural': 'Шаблоны для seo',
                'ordering': ['priority_order', 'id'],
            },
        ),
    ]
